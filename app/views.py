import base64
import json
import time
import uuid

from flask import request, render_template, Response

from app import app
from app.image_ocr import handle_ocr_async, handle_ocr, handle_ocr_async_test
from app.libs.common import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('ocr.html')


@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    result = request.form.to_dict()
    img_string = result['img_string'].encode().split(b';base64,')[-1]
    img_string = base64.b64decode(img_string)
    job_id = uuid.uuid1().__str__()
    path = '/tmp/{}.png'.format(job_id)
    with open(path, 'wb') as f:
        f.write(img_string)
    start = time.time()
    result = handle_ocr(image_path=path)
    res = map(
        lambda x: {'w': x['w'], 'h': x['h'], 'cx': x['cx'], 'cy': x['cy'], 'degree': x['degree'], 'text': x['text']},
        result)
    res = list(res)
    time_take = time.time() - start
    return json.dumps({'res': res, 'timeTake': round(time_take, 4)})


@app.route('/ocr_t', methods=['POST'])
def ocr_t():
    result = request.get_data(as_text=True)
    result = json.loads(result)
    version = get_result_param_value(result=result, param='version')
    msgid = get_result_param_value(result=result, param='msgid')
    systemtime = get_result_param_value(result=result, param='systemtime')
    localUrl = get_result_param_value(result=result, param='localUrl')
    if not version or not msgid or not systemtime or not localUrl:
        result = {'resultCode': '300', 'resultDesc': 'Params Error'}
        return Response(json.dumps(result), mimetype='application/json')
    handle_ocr_async_test(image_path=localUrl, msgid=msgid)
    result = {'resultCode': '200', 'resultDesc': 'Success'}
    return Response(json.dumps(result), mimetype='application/json')

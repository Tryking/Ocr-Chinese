import base64
import uuid

from flask import request, render_template

from app import app
from app.image_ocr import handle_ocr
from app.libs.common import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('ocr.html')


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    result = request.form.to_dict()
    img_string = result['img_string'].encode().split(b';base64,')[-1]
    img_string = base64.b64decode(img_string)
    job_id = uuid.uuid1().__str__()
    path = '/tmp/{}.jpg'.format(job_id)
    with open(path, 'wb') as f:
        f.write(img_string)
    handle_ocr(image_path=path)
    return 'true'


@app.route('/ocr_t', methods=['GET'])
def ocr_t():
    result = request.form.to_dict()
    version = get_result_param_value(result=result, param='version')
    msgid = get_result_param_value(result=result, param='msgid')
    systemtime = get_result_param_value(result=result, param='systemtime')
    localUrl = get_result_param_value(result=result, param='localUrl')
    handle_ocr(image_path=localUrl)
    return 'true'

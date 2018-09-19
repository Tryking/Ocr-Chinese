from flask import request

from app import app
from app.image_ocr import handle_ocr
from app.libs.common import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'index'


@app.route('/ocr', methods=['GET', 'POST'])
def ocr():
    result = request.form.to_dict()
    version = get_result_param_value(result=result, param='version')
    msgid = get_result_param_value(result=result, param='msgid')
    systemtime = get_result_param_value(result=result, param='systemtime')
    localUrl = get_result_param_value(result=result, param='localUrl')
    handle_ocr(image_path=localUrl)
    return 'true'

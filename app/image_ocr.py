import json
import time
from threading import Thread

import requests
from PIL import Image

from app import model
from app.libs.common import get_now

index = 0


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def handle_ocr_async(image_path):
    """
    后台处理OCR
    """
    img = Image.open(image_path).convert("RGB")
    W, H = img.size
    start = time.time()
    _, result, angle = model.model(img, detect_angle=True, config=dict(MAX_HORIZONTAL_GAP=200,
                                                                       MIN_V_OVERLAPS=0.6,
                                                                       MIN_SIZE_SIM=0.6,
                                                                       TEXT_PROPOSALS_MIN_SCORE=0.2,
                                                                       TEXT_PROPOSALS_NMS_THRESH=0.3,
                                                                       TEXT_LINE_NMS_THRESH=0.99,
                                                                       MIN_RATIO=1.0,
                                                                       LINE_MIN_SCORE=0.2,
                                                                       TEXT_PROPOSALS_WIDTH=5,
                                                                       MIN_NUM_PROPOSALS=0,
                                                                       text_model='opencv_dnn_detect'
                                                                       ),
                                   left_adjust=True, right_adjust=True, alph=0.1)


@async
def handle_ocr_async_test(image_path, msgid):
    """
    后台处理OCR
    """
    # img = Image.open(image_path).convert("RGB")
    time.sleep(1)
    systemtime = get_now()
    check_result = ['test0', 'test1', 'test2']
    data = {'version': '1.0', 'msgid': msgid, 'systemtime': systemtime, 'type': '103', 'checkResult': check_result}
    requests.post(url='http://www.baidu.com', data=json.dumps(data))


def handle_ocr(image_path):
    """
    后台处理OCR
    """
    try:
        img = Image.open(image_path).convert("RGB")
        W, H = img.size
        start = time.time()
        _, result, angle = model.model(img, detect_angle=True, config=dict(MAX_HORIZONTAL_GAP=200,
                                                                           MIN_V_OVERLAPS=0.6,
                                                                           MIN_SIZE_SIM=0.6,
                                                                           TEXT_PROPOSALS_MIN_SCORE=0.2,
                                                                           TEXT_PROPOSALS_NMS_THRESH=0.3,
                                                                           TEXT_LINE_NMS_THRESH=0.99,
                                                                           MIN_RATIO=1.0,
                                                                           LINE_MIN_SCORE=0.2,
                                                                           TEXT_PROPOSALS_WIDTH=5,
                                                                           MIN_NUM_PROPOSALS=0,
                                                                           text_model='darknet_detect'
                                                                           ),
                                       left_adjust=True, right_adjust=True, alph=0.1)
        return result
    except Exception as e:
        print(str(e))

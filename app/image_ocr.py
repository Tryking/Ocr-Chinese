import json
import time
from threading import Thread

import requests
from PIL import Image

from app import model, app
from app.config import CALLBACK_URL
from app.libs.common import get_now

index = 0


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def handle_ocr_async(image_path, msgid):
    """
    后台处理OCR
    """
    try:
        start = time.time()
        result = handle_ocr(image_path=image_path)
        res = []
        for _ in result:
            res.append(_['text'])
        res = '\n'.join(res)
        data = {'version': '1.0', 'msgid': msgid, 'systemtime': get_now(), 'type': '103', 'checkResult': res}
        headers = {'Content-Type': 'application/json'}
        app.logger.debug('send: %s', json.dumps(data))
        response = requests.post(url=CALLBACK_URL, headers=headers, data=json.dumps(data), timeout=5)
        cost = round(time.time() - start, ndigits=2)
        app.logger.debug('status code: %s , cost: %s', str(response.status_code), str(cost))
        app.logger.debug('response: %s', str(response.content, encoding='utf-8'))
    except Exception as e:
        app.logger.error('message info is %s', str(e), exc_info=True)


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
        app.logger.error('message info is %s', str(e), exc_info=True)

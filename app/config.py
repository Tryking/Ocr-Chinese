import os

# yolo 安装目录
DARKNET_ROOT = os.path.join(os.path.curdir, "darknet")
pwd = os.getcwd()
YOLO_CFG = os.path.join(pwd, "models", "text.cfg")
YOLO_WEIGHTS = os.path.join(pwd, "models", "text.weights")
YOLO_DATA = os.path.join(pwd, "models", "text.data")
OCR_MODEL = os.path.join(pwd, "models", "ocr.pth")

GPU = True

CALLBACK_URL = 'http://10.148.94.79:7001/ai_httpproxy/authentication/checkResultReturn'

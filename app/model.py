"""
模型
"""
import numpy as np
from PIL import Image
from numpy import cos, sin, pi
from app import darknet_detect, opencv_dnn_detect
from app.crnn.crnn import crnnOcr
from app.detector.detectors import TextDetector
from app.detector.other import get_boxes


def model(img, detect_angle=False, config=None, if_im=True, left_adjust=False, right_adjust=False, alph=0.1):
    """
    :param img: 
    :param detect_angle: 是否检测文字朝向
    :param config: 
    :param if_im: 
    :param left_adjust: 
    :param right_adjust: 
    :param alph: 
    :return: 
    """
    if config is None:
        config = {}
    angle = 0
    img = letterbox_image(img, (608, 608))
    config['img'] = img
    text_recs, tmp = text_detect(**config)

    new_box = sort_box(text_recs)
    result = crnn_rec(np.array(img), new_box, if_im, left_adjust, right_adjust, alph)
    return img, result, angle


def letterbox_image(image, size):
    """
    resize image with unchanged aspect ratio using padding
    Reference: https://github.com/qqwweee/keras-yolo3/blob/master/yolo3/utils.py
    :param image:
    :param size:
    :return:
    """
    iw, ih = image.size
    w, h = size
    scale = min(w * 1.0 / iw, h / ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)

    resized_image = image.resize((new_w, new_h), Image.BICUBIC)

    boxed_image = Image.new(mode='RGB', size=size, color=(128, 128, 128))
    boxed_image.paste(resized_image, ((w - new_w) // 2, (h - new_h) // 2))
    return boxed_image


def text_detect(img, MAX_HORIZONTAL_GAP=30,
                MIN_V_OVERLAPS=0.6,
                MIN_SIZE_SIM=0.6,
                TEXT_PROPOSALS_MIN_SCORE=0.7,
                TEXT_PROPOSALS_NMS_THRESH=0.3,
                TEXT_LINE_NMS_THRESH=0.3,
                MIN_RATIO=1.0,
                LINE_MIN_SCORE=0.8,
                TEXT_PROPOSALS_WIDTH=5,
                MIN_NUM_PROPOSALS=1,
                text_model='darknet_detect'):
    if text_model == 'darknet_detect':
        boxes, scores = darknet_detect.text_detect(np.array(img))
    else:
        boxes, scores = opencv_dnn_detect.text_detect(np.array(img))

    boxes = np.array(boxes, dtype=np.float32)
    scores = np.array(scores, dtype=np.float32)
    text_detector = TextDetector(MAX_HORIZONTAL_GAP, MIN_V_OVERLAPS, MIN_SIZE_SIM)
    shape = img.size[::-1]
    boxes = text_detector.detect(boxes,
                                 scores[:, np.newaxis],
                                 shape,
                                 TEXT_PROPOSALS_MIN_SCORE,
                                 TEXT_PROPOSALS_NMS_THRESH,
                                 TEXT_LINE_NMS_THRESH,
                                 MIN_RATIO,
                                 LINE_MIN_SCORE,
                                 TEXT_PROPOSALS_WIDTH,
                                 MIN_NUM_PROPOSALS)

    text_recs, tmp = get_boxes(np.array(img), boxes)
    new_box = []
    rx = 1
    ry = 1
    for box in text_recs:
        x1, y1 = (box[0], box[1])
        x2, y2 = (box[2], box[3])
        x3, y3 = (box[6], box[7])
        x4, y4 = (box[4], box[5])
        new_box.append([x1 * rx, y1 * ry, x2 * rx, y2 * ry, x3 * rx, y3 * ry, x4 * rx, y4 * ry])
    return new_box, tmp


def sort_box(box):
    """
        对box排序,及页面进行排版
        box[index, 0] = x1
        box[index, 1] = y1
        box[index, 2] = x2
        box[index, 3] = y2
        box[index, 4] = x3
        box[index, 5] = y3
        box[index, 6] = x4
        box[index, 7] = y4
    """

    box = sorted(box, key=lambda x: sum([x[1], x[3], x[5], x[7]]))
    return list(box)


def crnn_rec(im, boxes, if_im=False, left_adjust=False, right_adjust=False, alph=0.2):
    """
    crnn模型，ocr识别

    :param im:
    :param boxes:
    :param if_im:  是否返回图像
    :param left_adjust:
    :param right_adjust:
    :param alph:
    :return:
    """
    results = []
    im = Image.fromarray(im)
    for index, box in enumerate(boxes):

        degree, w, h, cx, cy = solve(box)
        partImg, newW, newH = rotate_cut_img(im, degree, box, w, h, left_adjust, right_adjust, alph)
        new_box = xy_rotate_box(cx, cy, newW, newH, degree)
        part_img = partImg.convert('L')
        # 识别的文本
        sim_pred = crnnOcr(part_img)
        if sim_pred.strip() != u'':
            results.append({'cx': cx, 'cy': cy, 'text': sim_pred, 'w': newW, 'h': newH, 'degree': degree * 180.0 / np.pi})

    return results


def solve(box):
    """
        绕 cx,cy点 w,h 旋转 angle 的坐标
        x = cx-w/2
        y = cy-h/2
        x1-cx = -w/2*cos(angle) +h/2*sin(angle)
        y1 -cy= -w/2*sin(angle) -h/2*cos(angle)

        h(x1-cx) = -wh/2*cos(angle) +hh/2*sin(angle)
        w(y1 -cy)= -ww/2*sin(angle) -hw/2*cos(angle)
        (hh+ww)/2sin(angle) = h(x1-cx)-w(y1 -cy)
    """
    x1, y1, x2, y2, x3, y3, x4, y4 = box[:8]
    cx = (x1 + x3 + x2 + x4) / 4.0
    cy = (y1 + y3 + y4 + y2) / 4.0
    w = (np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) + np.sqrt((x3 - x4) ** 2 + (y3 - y4) ** 2)) / 2
    h = (np.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2) + np.sqrt((x1 - x4) ** 2 + (y1 - y4) ** 2)) / 2
    # x = cx-w/2
    # y = cy-h/2
    sinA = (h * (x1 - cx) - w * (y1 - cy)) * 1.0 / (h * h + w * w) * 2
    angle = np.arcsin(sinA)
    return angle, w, h, cx, cy


def rotate_cut_img(im, degree, box, w, h, leftAdjust=False, rightAdjust=False, alph=0.2):
    x1, y1, x2, y2, x3, y3, x4, y4 = box[:8]
    x_center, y_center = np.mean([x1, x2, x3, x4]), np.mean([y1, y2, y3, y4])
    degree_ = degree * 180.0 / np.pi
    right = 0
    left = 0
    if rightAdjust:
        right = 1
    if leftAdjust:
        left = 1

    box = (max(1, x_center - w / 2 - left * alph * (w / 2))  ##xmin
           , y_center - h / 2,  ##ymin
           min(x_center + w / 2 + right * alph * (w / 2), im.size[0] - 1)  ##xmax
           , y_center + h / 2)  ##ymax

    newW = box[2] - box[0]
    newH = box[3] - box[1]
    tmpImg = im.rotate(degree_, center=(x_center, y_center)).crop(box)
    return tmpImg, newW, newH


def xy_rotate_box(cx, cy, w, h, angle):
    """
        绕 cx,cy点 w,h 旋转 angle 的坐标
        x_new = (x-cx)*cos(angle) - (y-cy)*sin(angle)+cx
        y_new = (x-cx)*sin(angle) + (y-cy)*sin(angle)+cy
    """

    cx = float(cx)
    cy = float(cy)
    w = float(w)
    h = float(h)
    angle = float(angle)
    x1, y1 = rotate(cx - w / 2, cy - h / 2, angle, cx, cy)
    x2, y2 = rotate(cx + w / 2, cy - h / 2, angle, cx, cy)
    x3, y3 = rotate(cx + w / 2, cy + h / 2, angle, cx, cy)
    x4, y4 = rotate(cx - w / 2, cy + h / 2, angle, cx, cy)
    return x1, y1, x2, y2, x3, y3, x4, y4


def rotate(x, y, angle, cx, cy):
    # *pi/180
    angle = angle
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new, y_new

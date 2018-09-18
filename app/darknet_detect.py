"""

"""


def text_detect(img):
    r = detect_np(net, meta, img, thresh=0.1, hier_thresh=0.5, nms=0.8)
    bboxes = to_box(r)
    return bboxes

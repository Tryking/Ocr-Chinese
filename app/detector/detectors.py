# coding:utf-8
from app.detector.other import normalize
import numpy as np
from app.detector.utils.cython_nms import nms as cython_nms

try:
    from app.detector.utils.gpu_nms import gpu_nms
except:
    gpu_nms = cython_nms


def nms(dets, thresh):
    if dets.shape[0] == 0:
        return []

    try:
        return gpu_nms(dets, thresh, device_id=0)
    except:
        return cython_nms(dets, thresh)


from app.detector.text_proposal_connector import TextProposalConnector


class TextDetector:
    """
        Detect text from an image
    """

    def __init__(self, MAX_HORIZONTAL_GAP=30, MIN_V_OVERLAPS=0.6, MIN_SIZE_SIM=0.6):
        """
        pass
        """
        self.text_proposal_connector = TextProposalConnector(MAX_HORIZONTAL_GAP, MIN_V_OVERLAPS, MIN_SIZE_SIM)

    def detect(self, text_proposals, scores, size,
               TEXT_PROPOSALS_MIN_SCORE=0.7,
               TEXT_PROPOSALS_NMS_THRESH=0.3,
               TEXT_LINE_NMS_THRESH=0.3,
               MIN_RATIO=1.0,
               LINE_MIN_SCORE=0.8,
               TEXT_PROPOSALS_WIDTH=5,
               MIN_NUM_PROPOSALS=1
               ):
        """
        Detecting texts from an image

        :param text_proposals:
        :param scores:
        :param size:
        :param TEXT_PROPOSALS_MIN_SCORE: 过滤字符box阀值
        :param TEXT_PROPOSALS_NMS_THRESH: nms过滤重复字符box
        :param TEXT_LINE_NMS_THRESH: nms过滤行文本重复过滤阀值
        :param MIN_RATIO: widths/heights宽度与高度比例
        :param LINE_MIN_SCORE: 行文本置信度
        :param TEXT_PROPOSALS_WIDTH: 每个字符的默认最小宽度
        :param MIN_NUM_PROPOSALS: 最小字符数
        :return: the bounding boxes of the detected texts
        """
        # text_proposals, scores=self.text_proposal_detector.detect(im, cfg.MEAN)
        keep_inds = np.where(scores > TEXT_PROPOSALS_MIN_SCORE)[0]  ###

        text_proposals, scores = text_proposals[keep_inds], scores[keep_inds]

        sorted_indices = np.argsort(scores.ravel())[::-1]
        text_proposals, scores = text_proposals[sorted_indices], scores[sorted_indices]

        # nms for text proposals

        # nms 过滤重复的box
        keep_inds = nms(np.hstack((text_proposals, scores)), TEXT_PROPOSALS_NMS_THRESH)
        text_proposals, scores = text_proposals[keep_inds], scores[keep_inds]

        scores = normalize(scores)

        # 合并文本行
        text_lines = self.text_proposal_connector.get_text_lines(text_proposals, scores, size)
        return text_lines

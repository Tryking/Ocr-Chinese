import tensorflow as tf

from .cfg import Config
from .other import resize_im
from ..lib.networks.factory import get_network
from ..lib.fast_rcnn.config import cfg
from ..lib.fast_rcnn.test import test_ctpn


def load_tf_model():
    # Use RPN for proposals
    cfg.TEST.HAS_RPN = True
    # init session
    # allow_soft_placement：如果你指定的设备不存在，允许TF自动分配设备
    config = tf.ConfigProto(allow_soft_placement=True)
    _sess = tf.Session(config=config)
    # load network
    _net = get_network("VGGnet_test")
    # load model
    saver = tf.train.Saver()
    ckpt = tf.train.get_checkpoint_state('ctpn/models/')
    saver.restore(_sess, ckpt.model_checkpoint_path)
    return _sess, saver, _net


# init model
sess, saver, net = load_tf_model()


def ctpn(img):
    """
    text box detect
    """
    scale, max_scale = Config.SCALE, Config.MAX_SCALE
    img, f = resize_im(img, scale=scale, max_scale=max_scale)
    scores, boxes = test_ctpn(sess, net, img)
    return scores, boxes, img

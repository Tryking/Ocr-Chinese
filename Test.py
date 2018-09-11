from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2

from PIL import Image


def conv_image():
    paths = glob('./test/*.*')

    fig = plt.gcf()
    fig.set_size_inches(w=(12, 14))

    for i in range(0, len(paths)):
        ax = plt.subplot(5, 5, 1 + i)

        im = Image.open(paths[i])
        im_convert = im.convert('RGB')
        test_im = np.array(im)
        ax.imshow(im)
        ax.set_title(label=paths[i], fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax_conv = plt.subplot(5, 5, 1 + i + len(paths))
        ax_conv.imshow(im_convert)
        ax_conv.set_title(label=paths[i], fontsize=10)
        ax_conv.set_xticks([])
        ax_conv.set_yticks([])
    plt.show()


paths = glob('./test/*.*')
im = Image.open(paths[1])
img = np.array(im.convert('RGB'))
im_orig = img.astype(np.float32, copy=True)
print('_______________')

if __name__ == '__main__':
    # conv_image()
    pass

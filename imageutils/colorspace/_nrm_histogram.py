
# from ._clr_base import COLORSPACE
import numpy as np
from skimage import exposure

_name = "HISTOGRAM"
_desc = {_name : " "}


def HISTOGRAM(img):
    """
    """
    img_out    = np.copy(img)
    channels   = img_out[:,:,0], img_out[:,:,1], img_out[:,:,2]
    # self.p_val = []
    for i,c in enumerate(channels):
        img_out[:,:,i] = exposure.equalize_hist(c)
    return img_out

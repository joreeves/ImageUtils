
# from ._clr_base import COLORSPACE
import numpy as np

_name = "CONTRAST"
_desc = {_name : " "}

def CONTRAST(img, low=10, high=99):
    """
    Contrast Stretching
    - low
    - high
    """
    # img_rescale = np.copy(img)
    img_out    = np.copy(img)
    channels   = img_out[:,:,0], img_out[:,:,1], img_out[:,:,2]
    # self.p_val = []
    for i,c in enumerate(channels):
        p_low, p_high = np.percentile(c, (low,high))
        # self.p_val.append([p_low,p_high])
        img_out[:,:,i] = np.interp(c, (p_low,p_high), (0,1))
    return img_out


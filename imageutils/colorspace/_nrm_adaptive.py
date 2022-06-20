
import numpy as np
from skimage import exposure

_name = "ADAPTIVE"
_desc = {_name : " "}

def ADAPTIVE(img, kernel_size=None, clip_limit=0.03):
    """
    Adaptive Equialization
    - kernel_size
    - clip_limit
    """
    img_out    = np.copy(img).astype(np.float64)
    channels   = img_out[:,:,0], img_out[:,:,1], img_out[:,:,2]
    for i,c in enumerate(channels):
        img_out[:,:,i] = exposure.equalize_adapthist(c,
                                    kernel_size=kernel_size,
                                    clip_limit=clip_limit)
    return img_out


from ._clr_base import COLORSPACE
import numpy as np

_name = "STANDARD"
_desc = {_name : "Normalize from 0-255 to 0-1"}

class STANDARD(COLORSPACE):
    """
    Normalize from 0-255 to 0-1
    """
    def __forward__(self, img):
        return img * (1 / 255.0)

    def __backward__(self, img):
        return img * 255.0

from ._clr_base import COLORSPACE
import numpy as np

_name = "LINLOG"
_desc = {_name : "Converts from Linear to Log"}

class LINLOG(COLORSPACE):
    """
    linear | log

    - linear to log
    - log to linear
    """

    def __color__(self, l_offset=0.1e-3, l_base=10, l_center=0.5):
        self.l_offset = l_offset
        self.l_base   = l_base
        self.l_center = l_center

    def __forward__(self, img):
        """
        linear to log
        """
        # CLIP TO 0 JUST INCASE
        img = np.clip(img,0,None)
        img = np.log10(img + self.l_offset)
        return (img / self.l_base) + self.l_center

    def __backward__(self, img):
        """
        log to linear
        """
        img = (img - self.l_center) * self.l_base
        img = self.l_base ** img
        return img - self.l_offset

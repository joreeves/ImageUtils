from ._clr_base import COLORSPACE
from decimal import Decimal
import numpy as np

_name = "LINLOGX"
_desc = {_name : "Converts from Linear to LogX"}

class LINLOGX(COLORSPACE):
    """
    linear | logx

    - linear to logx
    - logx to linear
    """
    def __color__(self, p=2.4, m=500000, base=10, offset=5):
        self.p      = p # EXPONENT
        self.m      = m # MAX VALUE
        self.base   = base
        self.offset = offset #abs(offset.as_tuple().exponent)
        self.lift   = float(Decimal("1e-{}".format(offset)))
        self.den    = ( np.log10( np.power(self.m, self.p) + self.lift ) + self.offset )

    def npLog(self, img, base):
        return np.log(img) / np.log(base)

    def __forward__(self, img):
        """
        linear to logx
        """
        img = np.clip(img,0,None)
        img = np.power(img,self.p)
        img = self.npLog(img+self.lift,self.base) # np.log10(img + lift)
        img = (img+self.offset)/self.den
        return img

    def __backward__(self, img):
        """
        logx to linear
        """
        img = np.clip(img,0,None)
        img = (img*self.den)-self.offset
        img = (self.base**img)-self.lift
        img = np.power(img,1/self.p)
        return img

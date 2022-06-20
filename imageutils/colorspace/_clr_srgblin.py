from ._clr_base import COLORSPACE
import numpy as np

_name = "SRGBLIN"
_desc = {_name : "Converts from sRGB to Linear"}

class SRGBLIN(COLORSPACE):
    """
    srgb | linear

    - srgb to linear
    - linear to srgb
    """

    def __forward__(self, img):
        """
        srgb to linear
        """
        x = np.power(np.clip( ((img + 0.055) / 1.055), 0, None), 2.4)
        y = img / 12.92
        return np.where(img<=0.0404482362771082, y, x)

    def __backward__(self, img):
        """
        linear to srgb
        """
        x = 1.055 * (np.power(np.clip(img, 0, None), (1.0 / 2.4))) - 0.055
        y = 12.92 * img
        return np.where(img<=0.0031308, y, x)

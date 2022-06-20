from lib.utils.lazy_loader import LazyLoader
tf = LazyLoader("tf", globals(), "tensorflow")

from ._clr_base import COLORSPACE
from decimal import Decimal
import numpy as np

_name = "STDDEV"
_desc = {_name : "Uses standard deviation and mean"}

class STDDEV(COLORSPACE):
    """
    linear | logx

    - linear to logx
    - logx to linear
    """
    # def __color__(self):
    #     pass

    def __forward__(self, img):
        """
        normalize
        """
        # ToDo: only works on 3 channel images currently?? Make more abstracted.
        orig_dtype = img.dtype

        _pixels = tf.math.reduce_prod(img.shape[-3:])
        self._mean = tf.math.reduce_mean(img, axis=[-1, -2, -3], keepdims=True)

        stddev = tf.math.reduce_std(img, axis=[-1, -2, -3], keepdims=True)
        min_stddev = tf.math.rsqrt(tf.cast(_pixels, orig_dtype))
        self._adjusted_stddev = tf.math.maximum(stddev, min_stddev)

        img -= self._mean
        img = tf.math.divide(img, self._adjusted_stddev)
        return img

    def __backward__(self, img):
        """
        reverse normalization
        """
        if (not hasattr(self, "_mean")) and (not hasattr(self, "_adjusted_stddev")):
            raise ValueError("Run the forward pass to set values")
        
        img = tf.math.multiply(img, self._adjusted_stddev)
        img += self._mean
        
        return img

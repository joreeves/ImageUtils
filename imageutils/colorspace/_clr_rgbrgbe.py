from ._clr_base import COLORSPACE
import numpy as np

# ToDo: Add optional alpha input
_name = "RGBRGBE"
_desc = {_name : "Converts from Linear to RGBE (Radiance format)"}

class RGBRGBE(COLORSPACE):
    # https://gist.github.com/edouardp/3089602
    # https://gist.github.com/edouardp/3089602
    # See FreeImage3180\FreeImage\Source\FreeImage\PluginHDR.cpp for more

    # RADIANCE FORMAT : RGB E(xponent)
    
    def __color__(self, scale=True):
        self.scale = scale

    def __forward__(self, img):
        """
        v = (float)(frexp(v, &e) * 256.0 / v);
        rgbe[0] = (BYTE) (rgbf->red * v);
        rgbe[1] = (BYTE) (rgbf->green * v);
        rgbe[2] = (BYTE) (rgbf->blue * v);
        rgbe[3] = (BYTE) (e + 128);
        """
        """
        scale
        Return the numbers from 0-1 instead of 0-255
        """
        brightest = np.maximum(np.maximum(img[...,0], img[...,1]), img[...,2])
        mantissa = np.zeros_like(brightest)
        exponent = np.zeros_like(brightest)
        np.frexp(brightest, mantissa, exponent)
        scaled_mantissa = mantissa * 256.0 / brightest
        rgbe = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
        rgbe[...,0:3] = np.around(img[...,0:3] * scaled_mantissa[...,None])
        rgbe[...,3] = np.around(exponent + 128)

        # ToDo: Causese some pixel artifacts. Guessing this is from pixel values that equal 0?

        if self.scale: return rgbe/255
        else: return rgbe

    def __backward__(self, img):
        """
        const float f = (float)(ldexp(1.0, rgbe[3] - (int)(128+8)));
        rgbf->red   = rgbe[0] * f;
        rgbf->green = rgbe[1] * f;
        rgbf->blue  = rgbe[2] * f;
        """
        if self.scale: img *= 255
        exp = img[...,3].astype(np.uint8)
        exp = exp - np.full(exp.shape, (128))
        exp_invr = np.ldexp(1.0, exp )
        rgb = np.around(img[...,0:3] * exp_invr[...,None])

        if self.scale: return rgb/255
        else: return rgb

from ._clr_rgbgray   import rgb2gray

__color_desc__ = {"None" : " "}
__color__      = {}

from ._clr_base import COLORSPACE

from ._clr_rgbrgbe import RGBRGBE, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: RGBRGBE})

from ._clr_linlog import LINLOG, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: LINLOG})

from ._clr_linlogx import LINLOGX, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: LINLOGX})

from ._clr_srgblin import SRGBLIN, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: SRGBLIN})

from ._clr_standard import STANDARD, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: STANDARD})

from ._clr_stddev import STDDEV, _desc, _name
__color_desc__.update(_desc)
__color__.update({_name: STDDEV})


def get_color(color, reverse=False, **kwargs):
    """
    Returns a color conversion class from an input string.
    - STANDARD
    - SRGBLIN
    - LINLOGX
    - RGBRGBE
    - LINLOG
    - STDDEV
    - RESCALE
    """

    if color is None:
        return COLORSPACE(reverse, **kwargs)

    _clr = __color__.get(color.upper(), COLORSPACE)

    return _clr(reverse, **kwargs)


__normalization_desc__ = {"None" : " "}
__normalizations__     = {}


from ._nrm_contrast   import CONTRAST, _desc, _name
__normalization_desc__.update(_desc)
__normalizations__.update({_name: CONTRAST})

from ._nrm_histogram   import HISTOGRAM, _desc, _name
__normalization_desc__.update(_desc)
__normalizations__.update({_name: HISTOGRAM})

from ._nrm_adaptive   import ADAPTIVE, _desc, _name
__normalization_desc__.update(_desc)
__normalizations__.update({_name: ADAPTIVE})

def get_normalization(norm:str):
    """
    Returns a normalization class from an input string.
    - CONTRAST
        Contrast stretching
    - HISTOGRAM
        Histogram Equalization
    - ADAPTIVE
        Adaptive Equalization
    """

    if norm is None:
        return None

    _nrm = __normalizations__.get(norm.upper(), None) #default should be none

    return _nrm

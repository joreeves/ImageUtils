import numpy as np

def PhotographicExposure(img,
        iso=800,
        fStop=10,
        shutterRatio=180,
        whitepoint=[1.73395, 1.8, 1.4182],
        saturation=1
        ):
    """
    Tone mapper based on the Redshift Photographic Exposure filter
    See nuke implementation here:
    https://www.patreon.com/posts/26516541
    Photographic settings:
        ISO
        fStop
        Shutter Ratio
        Whitepoint
        Saturation
    """

    white = np.array(whitepoint)
    shape = img.shape

    # Candela / Meter Squared
    cdm2 = 10000

    wp = 1 / np.resize(white, shape)
    adjustment = np.array([0.2126, 0.7152, 0.0722])

    factor = cdm2 * (18.0 / 106.0) * (iso * (1.0 / shutterRatio)) / (15.4 * fStop * fStop)

    adjustedImg = (img * factor * wp) / np.sum( white * adjustment )
    adjustedImg = np.maximum(adjustedImg * saturation + np.expand_dims( np.sum(adjustedImg * np.resize(adjustment,shape), axis=2), axis=2 ) * (1-saturation), np.full(shape, 0))
    
    return adjustedImg
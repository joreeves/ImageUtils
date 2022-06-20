''' Lazily load tensorflow '''
from lazyloader import LazyLoader
tf = LazyLoader('tf', globals(), 'tensorflow')

# from lib.utils.image import logger

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# import warnings
# import cv2
from skimage.transform import resize

from .colorspace import get_color

def viewImg(imgs,
            size        = (10,10),
            actual_size = False,
            srgb        = True,
            color       = "None",
            path        = None,
            title       = [],
            interp      = 'nearest',
            aa          = True,
            dim_reduce  = {'batch':'max',
                           'width':'min',
                           'height':'min',
                           'channel':'max'},
            rtrn        = False
            ):
    '''
    bilinear: Bilinear interpolation. If antialias is true, becomes a hat/tent filter function with radius 1 when downsampling.
    lanczos3: Lanczos kernel with radius 3. High-quality practical filter but may have some ringing, especially on synthetic images.
    lanczos5: Lanczos kernel with radius 5. Very-high-quality filter but may have stronger ringing.
    bicubic: Cubic interpolant of Keys. Equivalent to Catmull-Rom kernel. Reasonably good quality and faster than Lanczos3Kernel, particularly when upsampling.
    gaussian: Gaussian kernel with radius 3, sigma = 1.5 / 3.0.
    nearest: Nearest neighbor interpolation. antialias has no effect when used with nearest neighbor interpolation.
    area: Anti-aliased resampling with area interpolation. antialias has no effect when used with area interpolation; it always anti-aliases.
    mitchellcubic:
    '''

    dpi = mpl.rcParams['figure.dpi']
    res = size

    def _recursive_flatten(inpt, sublist=None):
        ''' Recursive list/tuple search '''
        if sublist is None:
            sublist = []

        if isinstance(inpt, list) or isinstance(inpt, tuple):
            for i in inpt:
                _recursive_flatten(i, sublist)
        else:
            sublist.append(inpt)

        return sublist

    def _to_numpy(inpt):
        if isinstance(inpt, np.ndarray):
            return inpt
        elif tf.is_tensor(inpt):
            return inpt.numpy()
        else:
            logger.warning("Unkown type encountered: {}".format( type(x) ))

    def _chk_dims(inpt):
        shp = inpt.shape
        if len(shp)==3:
            return np.expand_dims(inpt,axis=0), [1,*shp]
        elif len(shp)==4:
            return inpt, list(shp)
        else:
            logger.warning("Bad shape: {}".format(shp))
            return None

    def _reduce_dims(inpt, method):
        # print(inpt)
        try:
            assert method in ['min','max']
        except:
            logger.warning('Reduction method {} is not valid.'.format(method))
            method = 'max'

        if isinstance(inpt, int):
            return inpt

        if isinstance(method, str):
            if method == 'min':
                return min(inpt)
            elif method == 'max':
                return max(inpt)
        else:
            logger.warning('Reduction method must be a string of ["min", "max"]')
        
    def _resize_imgs(inpt, width, height, channels):
        b,w,h,c = inpt.shape
        if (c != channels):
            pass

        if (w != width) or (h != height):
            # return tf.image.resize(inpt,
            #                     (width, height),
            #                     method=interp).numpy()
            return resize(inpt, (width, height), anti_aliasing=aa)
        
        return inpt

    """
    List of images, should be n dimensional numpy arrays
    Image array (xres, yres, channels) | (64,64,3)
    TF array (batch, xres, yres, channels) | (1, 64, 64, 3)
    Could also be list of TF arrays...
    """

    # FLATTEN THE INPUT TO A SINGLE LIST
    imgs_flat = _recursive_flatten(imgs)

    # CONVERT ALL TO NUMPY ARRAYS
    imgs_nmpy = [_to_numpy(v) for v in imgs_flat]

    # CHECK THE INPUT DIMENSIONS
    imgs_shp = [_chk_dims(v) for v in imgs_nmpy]

    imgs_dms, shps = zip(*[v for v in imgs_shp if v is not None])
    
    # GET THE MINIMUM OR MAXIMUM VALUE FOR EACH: [BATCH, WIDTH, HEIGHT, CHANNELS]
    b,w,h,c = [_reduce_dims(v,dim_reduce.get(n,'max')) for v,n in zip(zip(*shps), ['batch','width','height','channel'])]
    
    # RESIZE IMAGES TO MATCH WIDTH, HEIGHT, AND CHANNELS
    imgs_dms = [_resize_imgs(v,w,h,3) for v in imgs_dms]

    # Reshape batch dim to rows then concat columns
    out_img = np.concatenate([np.reshape(v, ((w*b),h,c)) for v in imgs_dms], axis=1)

    if (color is not "None") and (color is not "none"):
        _c  = get_color(color)
        out_img = _c.color_out(out_img)

    if srgb:
        _srgb_c = get_color("SRGBLIN")
        out_img = _srgb_c.color_out(out_img)

    out_img = (np.clip(out_img, 0, 1)*255).astype(np.uint8)

    if rtrn:
        return np.expand_dims(out_img, axis=0)

    rows, cols = b, len(imgs_dms)

    # Set the resolution by the dpi scale
    if actual_size:
        res = (w/float(dpi), h/float(dpi))

    # Scale the horizontal axis by the number of images
    # Scale the vertical axis by the number of rows
    res = (res[0]*cols, res[1]*rows)

    f, ax = plt.subplots(nrows=1, ncols=1, figsize=res)
    ax.axis('off')
    f.subplots_adjust(hspace=0, wspace=0) # Remove spacing
    f.subplots_adjust(bottom=0, top=1, left=0, right=1)

    plt.imshow(out_img, interpolation=interp)

    # Need this here for running in the fit loop
    # otherwise it won't show the images
    plt.show()
    return
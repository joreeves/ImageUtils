# ImageUtils

install
```
!pip install git+https://github.com/joreeves/ImageUtils.git
```

example usage
```
from imageutils import viewImg
import numpy as np

imglist = []

imgs = np.random.uniform(size=[5,64,64,3])

imglist.append(imgs * np.random.uniform(size=[5,1,1,3]))
imglist.append(imgs * np.random.uniform(size=[5,1,1,3]))
imglist.append(imgs * np.random.uniform(size=[5,1,1,3]))

viewImg(imglist, actual_size=True, srgb=False)
```

from setuptools import setup

setup(name='ImageUtils',
      version='0.1',
      description='Image utilities for easy viewing of images and datasets',
      url='',
      author='Josiah Reeves',
      author_email='',
      license='MIT',
      packages=['imageutils'],
      install_requires=['numpy', 'matplotlib', 'scikit-image',
      'lazyloader @ git+ssh://git@github.com/joreeves/LazyLoader.git'],
      zip_safe=False)
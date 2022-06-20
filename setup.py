from setuptools import setup, find_packages

setup(name='ImageUtils',
      version='0.1',
      description='Image utilities for easy viewing of images and datasets',
      url='',
      author='Josiah Reeves',
      author_email='',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy', 'matplotlib', 'scikit-image',
      'lazyloader @ git+https://github.com/joreeves/LazyLoader.git'],
      zip_safe=False)
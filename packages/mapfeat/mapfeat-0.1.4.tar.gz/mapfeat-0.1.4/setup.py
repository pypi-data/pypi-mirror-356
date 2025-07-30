from setuptools import setup
from Cython.Build import cythonize

setup(
    name="mapfeat",
    version="0.1.4",
    packages=["mapfeat"],
    ext_modules=cythonize("mapfeat/cyparser.pyx", language_level=3),
    zip_safe=False,
)
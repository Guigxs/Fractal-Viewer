from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Compute',
    ext_modules=cythonize("compute.pyx"),
    zip_safe=False,
)
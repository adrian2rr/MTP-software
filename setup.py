from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

examples_extension = Extension(
    name="pytransciever",
    sources=["pytransciever.pyx"],
    libraries=["transciever"],
    library_dirs=["clib"],
    include_dirs=["clib"]
)
setup(
    name="pytransciever",
    ext_modules=cythonize([examples_extension])
)

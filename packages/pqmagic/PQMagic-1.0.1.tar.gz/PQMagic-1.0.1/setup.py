from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="pqmagic",
        sources=["pqmagic.pyx"],
        libraries=["pqmagic"],  # Link the compiled PQMagic-C library
        library_dirs=["PQMagic-C/lib"],  # Path to the compiled library
        include_dirs=["PQMagic-C/include"],  # Path to the header files
    )
]

setup(
    name='PQMagic',
    version='1.0.1',
    description='The python bindings for PQMagic https://github.com/pqcrypto-cn/PQMagic',
    ext_modules=cythonize(extensions),
    options={"bdist_wheel": {"universal": True}},
)
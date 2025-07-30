from setuptools import setup, Extension
from Cython.Build import cythonize

with open("README.md", "r", encoding = "utf-8") as fh:
    ld = fh.read()

extensions = [
    Extension(
        name="pqmagic",
        sources=["pqmagic.pyx"],  # Correct path to pqmagic.pyx
        libraries=["pqmagic"],  # Link the compiled PQMagic-C library
        library_dirs=["PQMagic-C/lib"],  # Path to the compiled library
        include_dirs=["PQMagic-C/include"],  # Path to the header files
    )
]

setup(
    name='pqmagic',
    version='1.0.2',
    requires=['Cython'],  # Optional, for metadata
    install_requires=['Cython'],  # Automatically install Cython
    description='The python bindings for PQMagic https://github.com/pqcrypto-cn/PQMagic',
    long_description=ld,
    long_description_content_type="text/markdown",
    ext_modules=cythonize(extensions),
    options={"bdist_wheel": {"universal": True}},
)
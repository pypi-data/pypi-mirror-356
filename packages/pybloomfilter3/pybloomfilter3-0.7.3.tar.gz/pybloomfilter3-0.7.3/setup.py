from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "pybloomfilter",
        sources=[
            "src/pybloomfilter.pyx",
            "src/mmapbitarray.c",
            "src/bloomfilter.c",
            "src/md5.c",
            "src/primetester.c",
            "src/MurmurHash3.c",
        ],
        include_dirs=["src"],
        language="c"
    )
]

setup(
    name="pybloomfilter",
    ext_modules=cythonize(ext_modules),
)

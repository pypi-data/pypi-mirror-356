from setuptools import setup, Extension
from Cython.Build import cythonize  #type: ignore

ext_modules = [
    Extension(
        "fastmath.fastmath",
        sources=["fastmath/fastmath.pyx", "fastmath/cfastmath.c"],
        include_dirs=["fastmath"],
        extra_compile_args=["-O2", "-std=c11"],
        libraries=["m"],
    )
]

setup(
    name="fastmathx",
    version="0.1.0",
    description="High performance math functions with C and Cython",
    author="Aaron Dsouza",
    author_email="aarondsouza109@gmail.com",
    ext_modules=cythonize(ext_modules),   #type: ignore
    packages=["fastmath"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

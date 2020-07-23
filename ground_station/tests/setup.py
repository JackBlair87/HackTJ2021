from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("./ground_station/WallMapCython.pyx", compiler_directives={'language_level': 3})
    # ext_modules = cythonize("./ground_station/tests/CythonTest.pyx")
)

#, build_dir="./ground_station/build"

# python3 ./ground_station/setup.py build_ext --inplace
# python3 ./ground_station/tests/setup.py build_ext --inplace

# cythonize -a -i ground_station/WallMapCython.pyx
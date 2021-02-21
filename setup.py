#!/usr/bin/env cython

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import sys,numpy as np

from setuptools import setup, Extension
from Cython.Build import cythonize

# Main setup
setup(
	name="Basins",
	ext_modules=cythonize([
			Extension('basic' ,sources=['basic.pyx'], language='c',include_dirs=[np.get_include()]),
		],
		language_level = str(sys.version_info[0]), # This is to specify python 3 synthax
		annotate=True         # This is to generate a report on the conversion to C code
	)
)
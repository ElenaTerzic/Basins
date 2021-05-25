#!/usr/bin/env cython

# Edited by amiro and eterzic 21.02.2021
from __future__ import print_function, division

import sys,numpy as np

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

with open('README.md') as f:
	readme = f.read()

# Main setup
setup(
	name="Basins",
	version="1.2.0",
	ext_modules=cythonize([
		Extension('Basins.basic',
				  sources=['Basins/basic.pyx','Basins/src/geometry.cpp'],
				  language='c++',
				  include_dirs=['Basins/src/',np.get_include()]
				 ),
		],
		language_level = str(sys.version_info[0]), # This is to specify python 3 synthax
		annotate       = True                      # This is to generate a report on the conversion to C code
	),
    long_description=readme,
    url='https://github.com/ArnauMiro/MEP.git',
    packages=find_packages(exclude=('Examples','doc')),
	include_package_data=True,
	install_requires=['numpy','cython']
)
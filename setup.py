#!/usr/bin/python

import os
from setuptools import setup

def get_long_description():
	return open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(name='Unidecode',
      version='0.04.17',
      description='ASCII transliterations of Unicode text',
      license='GPL',
      long_description=get_long_description(),
      author='Tomaz Solc',
      author_email='tomaz.solc@tablix.org',

      packages = [ 'unidecode' ],

      test_suite = 'tests',

      entry_points = {
		'console_scripts': [
			'unidecode = unidecode.util:main'
		]
      },

      classifiers = [
	"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
	"Programming Language :: Python",
	"Programming Language :: Python :: 2",
	"Programming Language :: Python :: 3",
	"Topic :: Text Processing",
	"Topic :: Text Processing :: Filters",
	],
)

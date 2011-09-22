#!/usr/bin/python
# vim: set fileencoding=utf8 :

from distutils.core import Command, setup
from sys import version_info
import unittest

UNITTESTS = [
		"tests", 
	]

class TestCommand(Command):
	user_options = [ ]

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		suite = unittest.TestSuite()

		suite.addTests( 
			unittest.defaultTestLoader.loadTestsFromNames( 
								UNITTESTS ) )

		result = unittest.TextTestRunner(verbosity=2).run(suite)

author = "Tomaž Šolc"
if version_info[0] < 3:
	author = author.decode('utf8')

setup(name='Unidecode',
      version='0.04.8',
      description='ASCII transliterations of Unicode text',
      license='GPL',
      long_description=open("README").read(),
      author=author,
      author_email='tomaz.solc@tablix.org',

      packages = [ 'unidecode' ],

      provides = [ 'unidecode' ],

      cmdclass = { 'test': TestCommand }
)

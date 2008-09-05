#!/usr/bin/python

from distutils.core import Command, setup
import unittest

UNITTESTS = [
		"tests.basic", 
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

setup(name='Unidecode',
      version='0.04.1',
      description='US-ASCII transliterations of Unicode text',
      author='Tomaz Solc',
      author_email='tomaz.solc@tablix.org',

      packages = [ 'unidecode' ],

      provides = [ 'unidecode' ],

      cmdclass = { 'test': TestCommand }
)

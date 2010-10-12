# -*- coding: utf-8 -*-
import unittest
from unidecode import unidecode

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		for n in range(0,128):
			t = chr(n)

			self.failUnlessEqual(unidecode(t), t)

	def test_bmp(self):
		for n in range(0,0x10000):
			# Just check that it doesn't throw an exception
			t = unichr(n)
			unidecode(t)

	def test_specific(self):

		TESTS = [
				("Hello, World!", 
				"Hello, World!"),

				("'\"\r\n",
				 "'\"\r\n"),

				("ČŽŠčžš",
				 "CZSczs"),

				("ア",
				 "a"),

				("α",
				"a"),

				("а",
				"a"),

				('ch\xe2teau',
				"chateau"),

				('vi\xf1edos',
				"vinedos"),
				
				("\u5317\u4EB0",
				"Bei Jing "),

				("Efﬁcient",
				"Efficient"),

				# Table that doesn't exist
				('\ua500',
				''),
				
				# Table that has less than 256 entriees
				('\u1eff',
				''),

				# Non-BMP character
				('\U0001d5a0',
				''),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

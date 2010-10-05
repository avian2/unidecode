# -*- coding: utf-8 -*-
import unittest
from unidecode import unidecode

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		for n in range(0,128):
			t = chr(n)

			self.failUnlessEqual(unidecode(t), t)

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
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

# -*- coding: utf-8 -*-
import unittest
from unidecode import unidecode

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		for n in xrange(0,128):
			t = chr(n)

			self.failUnlessEqual(unidecode(t), t)

	def test_specific(self):

		TESTS = [
				(u"Hello, World!", 
				"Hello, World!"),

				(u"'\"\r\n",
				 "'\"\r\n"),

				(u"ČŽŠčžš",
				 "CZSczs"),

				(u"ア",
				 "a"),

				(u"α",
				"a"),

				(u"а",
				"a"),

				(u'ch\xe2teau',
				"chateau"),

				(u'vi\xf1edos',
				"vinedos"),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

# -*- coding: utf-8 -*-
import unittest
from unidecode import unidecode

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):
		for n in xrange(0,128):
			t = chr(n)

			self.failUnlessEqual(unidecode(t), t)

	def test_bmp(self):
		for n in xrange(0,0x10000):
			# Just check that it doesn't throw an exception
			t = unichr(n)
			unidecode(t)

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
				
				(u"\u5317\u4EB0",
				"Bei Jing "),

				(u"Efﬁcient",
				"Efficient"),

				# Table that doesn't exist
				(u'\ua500',
				''),
				
				# Table that has less than 256 entriees
				(u'\u1eff',
				''),

				# Non-BMP character
				(u'\U0001d5a0',
				''),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

if __name__ == "__main__":
    unittest.main()

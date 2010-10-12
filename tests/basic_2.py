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

	def test_mathematical_latin(self):
		# 13 consecutive sequences of A-Z, a-z with some codepoints
		# undefined. We just count the undefined ones and don't check
		# positions.
		empty = 0
		for n in xrange(0x1d400, 0x1d6a4):
			if n % 52 < 26:
				a = chr(ord('A') + n % 26)
			else:
				a = chr(ord('a') + n % 26)
			b = unidecode(unichr(n))

			if not b:
				empty += 1
			else:
				self.failUnlessEqual(unidecode(b), a)

		self.failUnlessEqual(empty, 24)

	def test_mathematical_digits(self):
		# 5 consecutive sequences of 0-9
		for n in xrange(0x1d7ce, 0x1d800):
			a = chr(ord('0') + (n-0x1d7ce) % 10)
			b = unidecode(unichr(n))

			self.failUnlessEqual(unidecode(b), a)

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
				'A'),

				# Mathematical
				(u'\U0001d5c4\U0001d5c6/\U0001d5c1',
				'km/h'),
			]

		for input, output in TESTS:
			self.failUnlessEqual(unidecode(input), output)

if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
import unittest
import sys
from unidecode import unidecode
import warnings

# workaround for Python < 2.7
if not hasattr(unittest, 'skipIf'):
	def skipIf(condition, reason):
		def d(f):
			def df(*args):
				if condition:
					print "skipped %r" % (reason,)
				else:
					return f(*args)
			return df
		return d
	unittest.skipIf = skipIf

class TestUnidecode(unittest.TestCase):
	def test_ascii(self):

		log = []
		def showwarning_new(message, category, *args):
			if ("not an unicode object" in str(message)) and \
					(category is RuntimeWarning):
				log.append((message, category))
			else:
				showwarning_old(message, category, *args)

		showwarning_old = warnings.showwarning
		warnings.showwarning = showwarning_new
		warnings.filterwarnings("always")

		for n in xrange(0,128):
			t = chr(n)
			self.assertEqual(unidecode(t), t)

		# Passing string objects to unidecode should raise a warning
		self.assertEqual(128, len(log))
		log = []

		for n in xrange(0,128):
			t = unichr(n)
			self.assertEqual(unidecode(t), t)

		# unicode objects shouldn't raise warnings
		self.assertEqual(0, len(log))

		warnings.showwarning = showwarning_old

	def test_bmp(self):
		for n in xrange(0,0x10000):
			# Just check that it doesn't throw an exception
			t = unichr(n)
			unidecode(t)

	def test_circled_latin(self):
		# 1 sequence of a-z
		for n in xrange(0, 26):
			a = chr(ord('a') + n)
			b = unidecode(unichr(0x24d0 + n))

			self.assertEqual(b, a)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
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
				self.assertEqual(b, a)

		self.assertEqual(empty, 24)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_mathematical_digits(self):
		# 5 consecutive sequences of 0-9
		for n in xrange(0x1d7ce, 0x1d800):
			a = chr(ord('0') + (n-0x1d7ce) % 10)
			b = unidecode(unichr(n))

			self.assertEqual(b, a)

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

				# https://github.com/iki/unidecode/commit/4a1d4e0a7b5a11796dc701099556876e7a520065
				(u'příliš žluťoučký kůň pěl ďábelské ódy',
				'prilis zlutoucky kun pel dabelske ody'),

				(u'PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ PĚL ĎÁBELSKÉ ÓDY',
				'PRILIS ZLUTOUCKY KUN PEL DABELSKE ODY'),

				# Table that doesn't exist
				(u'\ua500',
				''),
				
				# Table that has less than 256 entriees
				(u'\u1eff',
				''),
			]

		for input, correct_output in TESTS:
			test_output = unidecode(input)
			self.assertEqual(test_output, correct_output)
			self.assertTrue(isinstance(test_output, str))

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_specific_wide(self):

		TESTS = [
				# Non-BMP character
				(u'\U0001d5a0',
				'A'),

				# Mathematical
				(u'\U0001d5c4\U0001d5c6/\U0001d5c1',
				'km/h'),
			]

		for input, correct_output in TESTS:
			test_output = unidecode(input)
			self.assertEqual(test_output, correct_output)
			self.assertTrue(isinstance(test_output, str))

	def test_wordpress_remove_accents(self):
		# This is the table from remove_accents() WordPress function.
		# https://core.trac.wordpress.org/browser/trunk/wp-includes/formatting.php

		wp_remove_accents = {
			# Decompositions for Latin-1 Supplement
			chr(194)+chr(170) : 'a', chr(194)+chr(186) : 'o',
			chr(195)+chr(128) : 'A', chr(195)+chr(129) : 'A',
			chr(195)+chr(130) : 'A', chr(195)+chr(131) : 'A',
			chr(195)+chr(133) : 'A',
			chr(195)+chr(134) : 'AE',chr(195)+chr(135) : 'C',
			chr(195)+chr(136) : 'E', chr(195)+chr(137) : 'E',
			chr(195)+chr(138) : 'E', chr(195)+chr(139) : 'E',
			chr(195)+chr(140) : 'I', chr(195)+chr(141) : 'I',
			chr(195)+chr(142) : 'I', chr(195)+chr(143) : 'I',
			chr(195)+chr(144) : 'D', chr(195)+chr(145) : 'N',
			chr(195)+chr(146) : 'O', chr(195)+chr(147) : 'O',
			chr(195)+chr(148) : 'O', chr(195)+chr(149) : 'O',
			chr(195)+chr(153) : 'U',
			chr(195)+chr(154) : 'U', chr(195)+chr(155) : 'U',
			chr(195)+chr(157) : 'Y',
			chr(195)+chr(160) : 'a', chr(195)+chr(161) : 'a',
			chr(195)+chr(162) : 'a', chr(195)+chr(163) : 'a',
			chr(195)+chr(165) : 'a',
			chr(195)+chr(166) : 'ae',chr(195)+chr(167) : 'c',
			chr(195)+chr(168) : 'e', chr(195)+chr(169) : 'e',
			chr(195)+chr(170) : 'e', chr(195)+chr(171) : 'e',
			chr(195)+chr(172) : 'i', chr(195)+chr(173) : 'i',
			chr(195)+chr(174) : 'i', chr(195)+chr(175) : 'i',
			chr(195)+chr(176) : 'd', chr(195)+chr(177) : 'n',
			chr(195)+chr(178) : 'o', chr(195)+chr(179) : 'o',
			chr(195)+chr(180) : 'o', chr(195)+chr(181) : 'o',
			chr(195)+chr(184) : 'o',
			chr(195)+chr(185) : 'u', chr(195)+chr(186) : 'u',
			chr(195)+chr(187) : 'u',
			chr(195)+chr(189) : 'y', chr(195)+chr(190) : 'th',
			chr(195)+chr(191) : 'y', chr(195)+chr(152) : 'O',
			# Decompositions for Latin Extended-A
			chr(196)+chr(128) : 'A', chr(196)+chr(129) : 'a',
			chr(196)+chr(130) : 'A', chr(196)+chr(131) : 'a',
			chr(196)+chr(132) : 'A', chr(196)+chr(133) : 'a',
			chr(196)+chr(134) : 'C', chr(196)+chr(135) : 'c',
			chr(196)+chr(136) : 'C', chr(196)+chr(137) : 'c',
			chr(196)+chr(138) : 'C', chr(196)+chr(139) : 'c',
			chr(196)+chr(140) : 'C', chr(196)+chr(141) : 'c',
			chr(196)+chr(142) : 'D', chr(196)+chr(143) : 'd',
			chr(196)+chr(144) : 'D', chr(196)+chr(145) : 'd',
			chr(196)+chr(146) : 'E', chr(196)+chr(147) : 'e',
			chr(196)+chr(148) : 'E', chr(196)+chr(149) : 'e',
			chr(196)+chr(150) : 'E', chr(196)+chr(151) : 'e',
			chr(196)+chr(152) : 'E', chr(196)+chr(153) : 'e',
			chr(196)+chr(154) : 'E', chr(196)+chr(155) : 'e',
			chr(196)+chr(156) : 'G', chr(196)+chr(157) : 'g',
			chr(196)+chr(158) : 'G', chr(196)+chr(159) : 'g',
			chr(196)+chr(160) : 'G', chr(196)+chr(161) : 'g',
			chr(196)+chr(162) : 'G', chr(196)+chr(163) : 'g',
			chr(196)+chr(164) : 'H', chr(196)+chr(165) : 'h',
			chr(196)+chr(166) : 'H', chr(196)+chr(167) : 'h',
			chr(196)+chr(168) : 'I', chr(196)+chr(169) : 'i',
			chr(196)+chr(170) : 'I', chr(196)+chr(171) : 'i',
			chr(196)+chr(172) : 'I', chr(196)+chr(173) : 'i',
			chr(196)+chr(174) : 'I', chr(196)+chr(175) : 'i',
			chr(196)+chr(176) : 'I', chr(196)+chr(177) : 'i',
			chr(196)+chr(178) : 'IJ',chr(196)+chr(179) : 'ij',
			chr(196)+chr(180) : 'J', chr(196)+chr(181) : 'j',
			chr(196)+chr(182) : 'K', chr(196)+chr(183) : 'k',
			chr(196)+chr(184) : 'k', chr(196)+chr(185) : 'L',
			chr(196)+chr(186) : 'l', chr(196)+chr(187) : 'L',
			chr(196)+chr(188) : 'l', chr(196)+chr(189) : 'L',
			chr(196)+chr(190) : 'l', chr(196)+chr(191) : 'L',
			chr(197)+chr(128) : 'l', chr(197)+chr(129) : 'L',
			chr(197)+chr(130) : 'l', chr(197)+chr(131) : 'N',
			chr(197)+chr(132) : 'n', chr(197)+chr(133) : 'N',
			chr(197)+chr(134) : 'n', chr(197)+chr(135) : 'N',
			chr(197)+chr(136) : 'n',
			chr(197)+chr(140) : 'O', chr(197)+chr(141) : 'o',
			chr(197)+chr(142) : 'O', chr(197)+chr(143) : 'o',
			chr(197)+chr(144) : 'O', chr(197)+chr(145) : 'o',
			chr(197)+chr(146) : 'OE',chr(197)+chr(147) : 'oe',
			chr(197)+chr(148) : 'R',chr(197)+chr(149) : 'r',
			chr(197)+chr(150) : 'R',chr(197)+chr(151) : 'r',
			chr(197)+chr(152) : 'R',chr(197)+chr(153) : 'r',
			chr(197)+chr(154) : 'S',chr(197)+chr(155) : 's',
			chr(197)+chr(156) : 'S',chr(197)+chr(157) : 's',
			chr(197)+chr(158) : 'S',chr(197)+chr(159) : 's',
			chr(197)+chr(160) : 'S', chr(197)+chr(161) : 's',
			chr(197)+chr(162) : 'T', chr(197)+chr(163) : 't',
			chr(197)+chr(164) : 'T', chr(197)+chr(165) : 't',
			chr(197)+chr(166) : 'T', chr(197)+chr(167) : 't',
			chr(197)+chr(168) : 'U', chr(197)+chr(169) : 'u',
			chr(197)+chr(170) : 'U', chr(197)+chr(171) : 'u',
			chr(197)+chr(172) : 'U', chr(197)+chr(173) : 'u',
			chr(197)+chr(174) : 'U', chr(197)+chr(175) : 'u',
			chr(197)+chr(176) : 'U', chr(197)+chr(177) : 'u',
			chr(197)+chr(178) : 'U', chr(197)+chr(179) : 'u',
			chr(197)+chr(180) : 'W', chr(197)+chr(181) : 'w',
			chr(197)+chr(182) : 'Y', chr(197)+chr(183) : 'y',
			chr(197)+chr(184) : 'Y', chr(197)+chr(185) : 'Z',
			chr(197)+chr(186) : 'z', chr(197)+chr(187) : 'Z',
			chr(197)+chr(188) : 'z', chr(197)+chr(189) : 'Z',
			chr(197)+chr(190) : 'z', chr(197)+chr(191) : 's',
			# Decompositions for Latin Extended-B
			chr(200)+chr(152) : 'S', chr(200)+chr(153) : 's',
			chr(200)+chr(154) : 'T', chr(200)+chr(155) : 't',

			# Vowels with diacritic (Vietnamese)
			# unmarked
			chr(198)+chr(160) : 'O', chr(198)+chr(161) : 'o',
			chr(198)+chr(175) : 'U', chr(198)+chr(176) : 'u',
			# grave accent
			chr(225)+chr(186)+chr(166) : 'A', chr(225)+chr(186)+chr(167) : 'a',
			chr(225)+chr(186)+chr(176) : 'A', chr(225)+chr(186)+chr(177) : 'a',
			chr(225)+chr(187)+chr(128) : 'E', chr(225)+chr(187)+chr(129) : 'e',
			chr(225)+chr(187)+chr(146) : 'O', chr(225)+chr(187)+chr(147) : 'o',
			chr(225)+chr(187)+chr(156) : 'O', chr(225)+chr(187)+chr(157) : 'o',
			chr(225)+chr(187)+chr(170) : 'U', chr(225)+chr(187)+chr(171) : 'u',
			chr(225)+chr(187)+chr(178) : 'Y', chr(225)+chr(187)+chr(179) : 'y',
			# hook
			chr(225)+chr(186)+chr(162) : 'A', chr(225)+chr(186)+chr(163) : 'a',
			chr(225)+chr(186)+chr(168) : 'A', chr(225)+chr(186)+chr(169) : 'a',
			chr(225)+chr(186)+chr(178) : 'A', chr(225)+chr(186)+chr(179) : 'a',
			chr(225)+chr(186)+chr(186) : 'E', chr(225)+chr(186)+chr(187) : 'e',
			chr(225)+chr(187)+chr(130) : 'E', chr(225)+chr(187)+chr(131) : 'e',
			chr(225)+chr(187)+chr(136) : 'I', chr(225)+chr(187)+chr(137) : 'i',
			chr(225)+chr(187)+chr(142) : 'O', chr(225)+chr(187)+chr(143) : 'o',
			chr(225)+chr(187)+chr(148) : 'O', chr(225)+chr(187)+chr(149) : 'o',
			chr(225)+chr(187)+chr(158) : 'O', chr(225)+chr(187)+chr(159) : 'o',
			chr(225)+chr(187)+chr(166) : 'U', chr(225)+chr(187)+chr(167) : 'u',
			chr(225)+chr(187)+chr(172) : 'U', chr(225)+chr(187)+chr(173) : 'u',
			chr(225)+chr(187)+chr(182) : 'Y', chr(225)+chr(187)+chr(183) : 'y',
			# tilde
			chr(225)+chr(186)+chr(170) : 'A', chr(225)+chr(186)+chr(171) : 'a',
			chr(225)+chr(186)+chr(180) : 'A', chr(225)+chr(186)+chr(181) : 'a',
			chr(225)+chr(186)+chr(188) : 'E', chr(225)+chr(186)+chr(189) : 'e',
			chr(225)+chr(187)+chr(132) : 'E', chr(225)+chr(187)+chr(133) : 'e',
			chr(225)+chr(187)+chr(150) : 'O', chr(225)+chr(187)+chr(151) : 'o',
			chr(225)+chr(187)+chr(160) : 'O', chr(225)+chr(187)+chr(161) : 'o',
			chr(225)+chr(187)+chr(174) : 'U', chr(225)+chr(187)+chr(175) : 'u',
			chr(225)+chr(187)+chr(184) : 'Y', chr(225)+chr(187)+chr(185) : 'y',
			# acute accent
			chr(225)+chr(186)+chr(164) : 'A', chr(225)+chr(186)+chr(165) : 'a',
			chr(225)+chr(186)+chr(174) : 'A', chr(225)+chr(186)+chr(175) : 'a',
			chr(225)+chr(186)+chr(190) : 'E', chr(225)+chr(186)+chr(191) : 'e',
			chr(225)+chr(187)+chr(144) : 'O', chr(225)+chr(187)+chr(145) : 'o',
			chr(225)+chr(187)+chr(154) : 'O', chr(225)+chr(187)+chr(155) : 'o',
			chr(225)+chr(187)+chr(168) : 'U', chr(225)+chr(187)+chr(169) : 'u',
			# dot below
			chr(225)+chr(186)+chr(160) : 'A', chr(225)+chr(186)+chr(161) : 'a',
			chr(225)+chr(186)+chr(172) : 'A', chr(225)+chr(186)+chr(173) : 'a',
			chr(225)+chr(186)+chr(182) : 'A', chr(225)+chr(186)+chr(183) : 'a',
			chr(225)+chr(186)+chr(184) : 'E', chr(225)+chr(186)+chr(185) : 'e',
			chr(225)+chr(187)+chr(134) : 'E', chr(225)+chr(187)+chr(135) : 'e',
			chr(225)+chr(187)+chr(138) : 'I', chr(225)+chr(187)+chr(139) : 'i',
			chr(225)+chr(187)+chr(140) : 'O', chr(225)+chr(187)+chr(141) : 'o',
			chr(225)+chr(187)+chr(152) : 'O', chr(225)+chr(187)+chr(153) : 'o',
			chr(225)+chr(187)+chr(162) : 'O', chr(225)+chr(187)+chr(163) : 'o',
			chr(225)+chr(187)+chr(164) : 'U', chr(225)+chr(187)+chr(165) : 'u',
			chr(225)+chr(187)+chr(176) : 'U', chr(225)+chr(187)+chr(177) : 'u',
			chr(225)+chr(187)+chr(180) : 'Y', chr(225)+chr(187)+chr(181) : 'y',
			# Vowels with diacritic (Chinese, Hanyu Pinyin)
			chr(201)+chr(145) : 'a',
			# macron
			chr(199)+chr(149) : 'U', chr(199)+chr(150) : 'u',
			# acute accent
			chr(199)+chr(151) : 'U', chr(199)+chr(152) : 'u',
			# caron
			chr(199)+chr(141) : 'A', chr(199)+chr(142) : 'a',
			chr(199)+chr(143) : 'I', chr(199)+chr(144) : 'i',
			chr(199)+chr(145) : 'O', chr(199)+chr(146) : 'o',
			chr(199)+chr(147) : 'U', chr(199)+chr(148) : 'u',
			chr(199)+chr(153) : 'U', chr(199)+chr(154) : 'u',
			# grave accent
			chr(199)+chr(155) : 'U', chr(199)+chr(156) : 'u',

			# Known differences:

			#chr(195)+chr(158) : 'TH',
			#chr(197)+chr(137) : 'N',
			#chr(197)+chr(138) : 'n',
			#chr(197)+chr(139) : 'N',

			# Euro Sign
			#chr(226)+chr(130)+chr(172) : 'E',

			# GBP (Pound) Sign
			#chr(194)+chr(163) : '',

			# unidecode uses German transliterations for umlauts:

			#chr(195)+chr(132) : 'A',
			#chr(195)+chr(150) : 'O',
			#chr(195)+chr(156) : 'U',
			#chr(195)+chr(159) : 's',
			#chr(195)+chr(164) : 'a',
			#chr(195)+chr(182) : 'o',
			#chr(195)+chr(188) : 'u',
		}

		for utf8_input, correct_output in wp_remove_accents.iteritems():
			input = utf8_input.decode('utf8')
			output = unidecode(input)

			self.assertEqual(correct_output, output)

if __name__ == "__main__":
    unittest.main()

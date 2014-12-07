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

			chr(195)+chr(132) : 'A',
			chr(195)+chr(150) : 'O',
			chr(195)+chr(156) : 'U',
			#chr(195)+chr(159) : 's',
			chr(195)+chr(164) : 'a',
			chr(195)+chr(182) : 'o',
			chr(195)+chr(188) : 'u',

			# Known differences:

			#chr(195)+chr(158) : 'TH',
			#chr(197)+chr(137) : 'N',
			#chr(197)+chr(138) : 'n',
			#chr(197)+chr(139) : 'N',

			# Euro Sign
			#chr(226)+chr(130)+chr(172) : 'E',

			# GBP (Pound) Sign
			#chr(194)+chr(163) : '',
		}

		for utf8_input, correct_output in wp_remove_accents.iteritems():
			input = utf8_input.decode('utf8')
			output = unidecode(input)

			self.assertEqual(correct_output, output)

	def test_unicode_text_converter(self):
		# Examples from http://www.panix.com/~eli/unicode/convert.cgi
		lower = [
			# Fullwidth
			u'\uff54\uff48\uff45 \uff51\uff55\uff49\uff43\uff4b \uff42\uff52\uff4f\uff57\uff4e \uff46\uff4f\uff58 \uff4a\uff55\uff4d\uff50\uff53 \uff4f\uff56\uff45\uff52 \uff54\uff48\uff45 \uff4c\uff41\uff5a\uff59 \uff44\uff4f\uff47 \uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19\uff10',
			# Double-struck
			u'\U0001d565\U0001d559\U0001d556 \U0001d562\U0001d566\U0001d55a\U0001d554\U0001d55c \U0001d553\U0001d563\U0001d560\U0001d568\U0001d55f \U0001d557\U0001d560\U0001d569 \U0001d55b\U0001d566\U0001d55e\U0001d561\U0001d564 \U0001d560\U0001d567\U0001d556\U0001d563 \U0001d565\U0001d559\U0001d556 \U0001d55d\U0001d552\U0001d56b\U0001d56a \U0001d555\U0001d560\U0001d558 \U0001d7d9\U0001d7da\U0001d7db\U0001d7dc\U0001d7dd\U0001d7de\U0001d7df\U0001d7e0\U0001d7e1\U0001d7d8',
			# Bold
			u'\U0001d42d\U0001d421\U0001d41e \U0001d42a\U0001d42e\U0001d422\U0001d41c\U0001d424 \U0001d41b\U0001d42b\U0001d428\U0001d430\U0001d427 \U0001d41f\U0001d428\U0001d431 \U0001d423\U0001d42e\U0001d426\U0001d429\U0001d42c \U0001d428\U0001d42f\U0001d41e\U0001d42b \U0001d42d\U0001d421\U0001d41e \U0001d425\U0001d41a\U0001d433\U0001d432 \U0001d41d\U0001d428\U0001d420 \U0001d7cf\U0001d7d0\U0001d7d1\U0001d7d2\U0001d7d3\U0001d7d4\U0001d7d5\U0001d7d6\U0001d7d7\U0001d7ce',
			# Bold italic
			u'\U0001d495\U0001d489\U0001d486 \U0001d492\U0001d496\U0001d48a\U0001d484\U0001d48c \U0001d483\U0001d493\U0001d490\U0001d498\U0001d48f \U0001d487\U0001d490\U0001d499 \U0001d48b\U0001d496\U0001d48e\U0001d491\U0001d494 \U0001d490\U0001d497\U0001d486\U0001d493 \U0001d495\U0001d489\U0001d486 \U0001d48d\U0001d482\U0001d49b\U0001d49a \U0001d485\U0001d490\U0001d488 1234567890',
			# Bold script
			u'\U0001d4fd\U0001d4f1\U0001d4ee \U0001d4fa\U0001d4fe\U0001d4f2\U0001d4ec\U0001d4f4 \U0001d4eb\U0001d4fb\U0001d4f8\U0001d500\U0001d4f7 \U0001d4ef\U0001d4f8\U0001d501 \U0001d4f3\U0001d4fe\U0001d4f6\U0001d4f9\U0001d4fc \U0001d4f8\U0001d4ff\U0001d4ee\U0001d4fb \U0001d4fd\U0001d4f1\U0001d4ee \U0001d4f5\U0001d4ea\U0001d503\U0001d502 \U0001d4ed\U0001d4f8\U0001d4f0 1234567890',
			# Fraktur
			u'\U0001d599\U0001d58d\U0001d58a \U0001d596\U0001d59a\U0001d58e\U0001d588\U0001d590 \U0001d587\U0001d597\U0001d594\U0001d59c\U0001d593 \U0001d58b\U0001d594\U0001d59d \U0001d58f\U0001d59a\U0001d592\U0001d595\U0001d598 \U0001d594\U0001d59b\U0001d58a\U0001d597 \U0001d599\U0001d58d\U0001d58a \U0001d591\U0001d586\U0001d59f\U0001d59e \U0001d589\U0001d594\U0001d58c 1234567890',
		]

		for s in lower:
			o = unidecode(s)

			self.assertEqual('the quick brown fox jumps over the lazy dog 1234567890', o)

		upper = [
			# Fullwidth
			u'\uff34\uff28\uff25 \uff31\uff35\uff29\uff23\uff2b \uff22\uff32\uff2f\uff37\uff2e \uff26\uff2f\uff38 \uff2a\uff35\uff2d\uff30\uff33 \uff2f\uff36\uff25\uff32 \uff34\uff28\uff25 \uff2c\uff21\uff3a\uff39 \uff24\uff2f\uff27 \uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19\uff10',
			# Double-struck
			u'\U0001d54b\u210d\U0001d53c \u211a\U0001d54c\U0001d540\u2102\U0001d542 \U0001d539\u211d\U0001d546\U0001d54e\u2115 \U0001d53d\U0001d546\U0001d54f \U0001d541\U0001d54c\U0001d544\u2119\U0001d54a \U0001d546\U0001d54d\U0001d53c\u211d \U0001d54b\u210d\U0001d53c \U0001d543\U0001d538\u2124\U0001d550 \U0001d53b\U0001d546\U0001d53e \U0001d7d9\U0001d7da\U0001d7db\U0001d7dc\U0001d7dd\U0001d7de\U0001d7df\U0001d7e0\U0001d7e1\U0001d7d8',
			# Bold
			u'\U0001d413\U0001d407\U0001d404 \U0001d410\U0001d414\U0001d408\U0001d402\U0001d40a \U0001d401\U0001d411\U0001d40e\U0001d416\U0001d40d \U0001d405\U0001d40e\U0001d417 \U0001d409\U0001d414\U0001d40c\U0001d40f\U0001d412 \U0001d40e\U0001d415\U0001d404\U0001d411 \U0001d413\U0001d407\U0001d404 \U0001d40b\U0001d400\U0001d419\U0001d418 \U0001d403\U0001d40e\U0001d406 \U0001d7cf\U0001d7d0\U0001d7d1\U0001d7d2\U0001d7d3\U0001d7d4\U0001d7d5\U0001d7d6\U0001d7d7\U0001d7ce',
			# Bold italic
			u'\U0001d47b\U0001d46f\U0001d46c \U0001d478\U0001d47c\U0001d470\U0001d46a\U0001d472 \U0001d469\U0001d479\U0001d476\U0001d47e\U0001d475 \U0001d46d\U0001d476\U0001d47f \U0001d471\U0001d47c\U0001d474\U0001d477\U0001d47a \U0001d476\U0001d47d\U0001d46c\U0001d479 \U0001d47b\U0001d46f\U0001d46c \U0001d473\U0001d468\U0001d481\U0001d480 \U0001d46b\U0001d476\U0001d46e 1234567890',
			# Bold script
			u'\U0001d4e3\U0001d4d7\U0001d4d4 \U0001d4e0\U0001d4e4\U0001d4d8\U0001d4d2\U0001d4da \U0001d4d1\U0001d4e1\U0001d4de\U0001d4e6\U0001d4dd \U0001d4d5\U0001d4de\U0001d4e7 \U0001d4d9\U0001d4e4\U0001d4dc\U0001d4df\U0001d4e2 \U0001d4de\U0001d4e5\U0001d4d4\U0001d4e1 \U0001d4e3\U0001d4d7\U0001d4d4 \U0001d4db\U0001d4d0\U0001d4e9\U0001d4e8 \U0001d4d3\U0001d4de\U0001d4d6 1234567890',
			# Fraktur
			u'\U0001d57f\U0001d573\U0001d570 \U0001d57c\U0001d580\U0001d574\U0001d56e\U0001d576 \U0001d56d\U0001d57d\U0001d57a\U0001d582\U0001d579 \U0001d571\U0001d57a\U0001d583 \U0001d575\U0001d580\U0001d578\U0001d57b\U0001d57e \U0001d57a\U0001d581\U0001d570\U0001d57d \U0001d57f\U0001d573\U0001d570 \U0001d577\U0001d56c\U0001d585\U0001d584 \U0001d56f\U0001d57a\U0001d572 1234567890',
		]

		for s in upper:
			o = unidecode(s)

			self.assertEqual('THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 1234567890', o)

if __name__ == "__main__":
    unittest.main()

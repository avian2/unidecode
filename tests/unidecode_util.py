import locale
import unittest
import subprocess as sp
import sys

PY3 = sys.version_info[0] >= 3


class TestUnidecodeUtility(unittest.TestCase):
	EXPECTED_MIXED = 'n Zhong a na\nn Zhong a na -ba -ba\n\n'

	def test_sjis_error(self):
		p = sp.Popen([sys.executable, 'bin/unidecode', 'tests/data/test-sjis'], stderr=sp.PIPE)
		out = p.communicate()[1]
		expected = 'Unable to decode input: invalid start byte, start: 0, end: 1\n'
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		self.assertEqual(out, expected)

	def test_sjis(self):
		args = [sys.executable, 'bin/unidecode', '-e', 'sjis', 'tests/data/test-sjis']
		p = sp.Popen(args, stdout=sp.PIPE)
		out = p.communicate()[0]
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		expected = ('Ge Ming  Ri Ben Yu  m-flonoXin Qu de, DXnioite, Yi Fan '
		            'Zui Hou noShou Lu ninatsutaQu desu. \n')
		self.assertEqual(out, expected)

	def test_mixed(self):
		p = sp.Popen([sys.executable, 'bin/unidecode', 'tests/data/test-utf8'], stdout=sp.PIPE)
		out = p.communicate()[0]
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		self.assertEqual(out, self.EXPECTED_MIXED)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_mixed_utf16(self):
		args = [sys.executable, 'bin/unidecode', '-e', 'utf-16', 'tests/data/test-utf16']
		p = sp.Popen(args, stdout=sp.PIPE)
		out = p.communicate()[0]
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		self.assertEqual(out, self.EXPECTED_MIXED)

	@unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
	def test_mixed_utf32(self):
		args = [sys.executable, 'bin/unidecode', '-e', 'utf-32', 'tests/data/test-utf32']
		p = sp.Popen(args, stdout=sp.PIPE)
		out = p.communicate()[0]
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		self.assertEqual(out, self.EXPECTED_MIXED)

	def test_mixed_piped(self):
		p1 = sp.Popen(['cat', 'tests/data/test-utf8'], stdout=sp.PIPE)
		p2 = sp.Popen([sys.executable, 'bin/unidecode'],
					  stdout=sp.PIPE, stdin=p1.stdout)
		out = p2.communicate()[0]
		if PY3:
			out = out.decode(locale.getpreferredencoding())
		self.assertEqual(out, self.EXPECTED_MIXED)

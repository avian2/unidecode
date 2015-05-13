# vim:ts=4 sw=4 expandtab softtabstop=4
import os
import locale
import unittest
import subprocess
import sys

PY3 = sys.version_info[0] >= 3

here = os.path.dirname(__file__)

def get_cmd():
    sys_path = os.path.join(here, "..")

    return [sys.executable, "-c",
            "import sys; sys.path.insert(0, '%s'); from unidecode.util import main; main()" % (sys_path,)]

def run(argv):
    cmd = get_cmd()
    p = subprocess.Popen(cmd + argv, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate()

class TestUnidecodeUtility(unittest.TestCase):
    EXPECTED_MIXED = 'n Zhong a na\nn Zhong a na -ba -ba\n\n'

    def test_sjis_error(self):
        out = run(['tests/data/test-sjis'])[1]
        expected = 'Unable to decode input: invalid start byte, start: 0, end: 1\n'
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        self.assertEqual(out, expected)

    def test_sjis(self):
        out = run(['-e', 'sjis', 'tests/data/test-sjis'])[0]
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        expected = ('Ge Ming  Ri Ben Yu  m-flonoXin Qu de, DXnioite, Yi Fan '
                    'Zui Hou noShou Lu ninatsutaQu desu. \n')
        self.assertEqual(out, expected)

    def test_mixed(self):
        out = run(['tests/data/test-utf8'])[0]
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        self.assertEqual(out, self.EXPECTED_MIXED)

    @unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
    def test_mixed_utf16(self):
        out = run(['-e', 'utf-16', 'tests/data/test-utf16'])[0]
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        self.assertEqual(out, self.EXPECTED_MIXED)

    @unittest.skipIf(sys.maxunicode < 0x10000, "narrow build")
    def test_mixed_utf32(self):
        out = run(['-e', 'utf-32', 'tests/data/test-utf32'])[0]
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        self.assertEqual(out, self.EXPECTED_MIXED)

    def test_mixed_piped(self):
        cmd = get_cmd()
        p1 = subprocess.Popen(['cat', 'tests/data/test-utf8'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=p1.stdout)

        out = p2.communicate()[0]
        p1.communicate()
        if PY3:
            out = out.decode(locale.getpreferredencoding())
        self.assertEqual(out, self.EXPECTED_MIXED)

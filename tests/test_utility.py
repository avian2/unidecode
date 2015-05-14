# vim:ts=4 sw=4 expandtab softtabstop=4
import os
import locale
import unittest
import subprocess
import sys
import tempfile

PY3 = sys.version_info[0] >= 3

here = os.path.dirname(__file__)

if PY3:
    def _u(x):
        return x
else:
    def _u(x):
        return x.decode('unicode-escape')

def get_cmd():
    sys_path = os.path.join(here, "..")

    return [sys.executable, "-c",
            "import sys; sys.path.insert(0, '%s'); from unidecode.util import main; main()" % (sys_path,)]

def run(argv):
    cmd = get_cmd()
    p = subprocess.Popen(cmd + argv, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    out, err = p.communicate()

    return out.decode('ascii'), err.decode('ascii')

def temp(content):
    f = tempfile.NamedTemporaryFile()
    f.write(content)
    f.flush()
    return f

class TestUnidecodeUtility(unittest.TestCase):

    TEST_UNICODE = _u('\u9769')
    TEST_ASCII = 'Ge '

    def test_encoding_error(self):
        f = temp(self.TEST_UNICODE.encode('sjis'))
        out, err = run(['-e', 'utf8', f.name])

        expected = 'Unable to decode input: invalid start byte, start: 0, end: 1\n'
        self.assertEqual(err, expected)

    def test_file_specified_encoding(self):
        f = temp(self.TEST_UNICODE.encode('sjis'))

        out, err = run(['-e', 'sjis', f.name])
        self.assertEqual(out, self.TEST_ASCII)

    def test_file_default_encoding(self):
        f = temp(self.TEST_UNICODE.encode(locale.getpreferredencoding()))
        out, err = run([f.name])
        self.assertEqual(out, self.TEST_ASCII)

    def test_file_stdin(self):
        cmd = get_cmd()
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        out, err = p.communicate(self.TEST_UNICODE.encode(locale.getpreferredencoding()))
        self.assertEqual(out.decode('ascii'), self.TEST_ASCII)

    def test_commandline(self):
        out = run(['-e', 'sjis', '-c', self.TEST_UNICODE.encode('sjis')])[0]
        self.assertEqual(out, self.TEST_ASCII + '\n')

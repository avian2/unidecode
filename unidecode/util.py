# vim:ts=4 sw=4 expandtab softtabstop=4
from __future__ import print_function
import optparse
import locale
import os
import sys
import warnings

from unidecode import unidecode

PY3 = sys.version_info[0] >= 3

def main():
    default_encoding = locale.getpreferredencoding()

    parser = optparse.OptionParser('%prog [options] [FILE]',
            description="Transliterate Unicode text into ASCII. FILE is path to file to transliterate. "
            "If omitted, standard input is used.")
    parser.add_option('-e', '--encoding', metavar='ENCODING', default=default_encoding,
            help='Specify an encoding (default is %s)' % (default_encoding,))

    options, args = parser.parse_args()

    encoding = options.encoding

    if args:
        with open(args[0], 'rb') as f:
            stream = f.read()
    else:
        if PY3:
            stream = sys.stdin.buffer.read()
        else:
            stream = sys.stdin.read()

    try:
        stream = stream.decode(encoding)
    except UnicodeDecodeError as e:
        msg = 'Unable to decode input: %s, start: %d, end: %d' % (e.reason, e.start, e.end)
        print(msg, file=sys.stderr)
        sys.exit(1)

    print(unidecode(stream))

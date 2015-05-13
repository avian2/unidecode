# vim:ts=4 sw=4 expandtab softtabstop=4
from __future__ import print_function
import argparse
import locale
import os
import sys
import warnings

from unidecode import unidecode

PY3 = sys.version_info[0] >= 3

def main():
    parser = argparse.ArgumentParser('unidecode')
    parser.add_argument('-e',
                        '--encoding',
                        nargs=1,
                        metavar='ENCODING',
                        help='Specify an encoding, overriding system default')
    parser.add_argument('file',
                        nargs='?',
                        metavar='FILE',
                        help='File to transliterate')

    args = parser.parse_args()
    if args.encoding:
        encoding = args.encoding[0]
    else:
        encoding = locale.getpreferredencoding()

    if args.file:
        with open(args.file, 'rb') as f:
            stream = f.read()
    else:
        # In Python 3, stdin.read() is read in the system's locale and returns type str
        # This returns bytes on Python 3 and str on Python 2
        f = os.fdopen(sys.stdin.fileno(), 'rb')
        stream = f.read()
        f.close()

    try:
        stream = stream.decode(encoding)
    except UnicodeDecodeError as e:
        msg = ('Unable to decode input: {}, start: {:d}, '
            'end: {:d}').format(e.reason, e.start, e.end)
        print(msg, file=sys.stderr)
        sys.exit(1)

    print(unidecode(stream))

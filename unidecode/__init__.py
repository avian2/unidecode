# -*- coding: utf-8 -*-
# vi:tabstop=4:expandtab:sw=4
"""Transliterate Unicode text into plain 7-bit ASCII.

Example usage:
>>> from unidecode import unidecode:
>>> unidecode(u"\u5317\u4EB0")
"Bei Jing "

The transliteration uses a straightforward map, and doesn't have alternatives
for the same character based on language, position, or anything else.

In Python 3, a standard string object will be returned. If you need bytes, use:
>>> unidecode("Κνωσός").encode("ascii")
b'Knosos'
"""
import warnings
import codecs
from sys import version_info

PY3 = version_info[0] >= 3
_u = str if PY3 else unicode

Cache = {}


def _handle_unidecode(exception):
    substr = exception.object[exception.start:exception.end]
    return (_u(unidecode(substr)), exception.end)

codecs.register_error('unidecode', _handle_unidecode)


def unidecode_fast(string):
    """
    Transliterate an Unicode object into an ASCII string trying to decode the
    string using the ASCII charmap, falling back to the original table-based
    transliteration function for non-ASCII chars.

    This function is about an order or magnitude faster when working with
    all-ASCII strings, but slightly slower otherwise.
    """
    encoded = string.encode("ASCII", "unidecode")
    if PY3:
        return encoded.decode("ASCII")
    else:
        return encoded


def unidecode(string):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "
    """

    if not PY3 and not isinstance(string, unicode):
        warnings.warn(  "Argument %r is not an unicode object. "
                        "Passing an encoded string will likely have "
                        "unexpected results." % (type(string),),
                        RuntimeWarning, 2)

    retval = []

    for char in string:
        codepoint = ord(char)

        if codepoint < 0x80: # Basic ASCII
            retval.append(str(char))
            continue
        
        if codepoint > 0xeffff:
            continue # Characters in Private Use Area and above are ignored

        if 0xd800 <= codepoint <= 0xdfff:
            warnings.warn(  "Surrogate character %r will be ignored. "
                            "You might be using a narrow Python build." % (char,),
                            RuntimeWarning, 2)

        section = codepoint >> 8   # Chop off the last two hex digits
        position = codepoint % 256 # Last two hex digits

        try:
            table = Cache[section]
        except KeyError:
            try:
                mod = __import__('unidecode.x%03x'%(section), globals(), locals(), ['data'])
            except ImportError:
                Cache[section] = None
                continue   # No match: ignore this character and carry on.

            Cache[section] = table = mod.data

        if table and len(table) > position:
            retval.append( table[position] )

    return ''.join(retval)

# -*- coding: utf-8 -*-
# vi:tabstop=4:expandtab:sw=4
"""Transliterate Unicode text into plain 7-bit ASCII.

Example usage:
>>> from unidecode import unidecode
>>> unidecode(u"\u5317\u4EB0")
"Bei Jing "

The transliteration uses a straightforward map, and doesn't have alternatives
for the same character based on language, position, or anything else.

In Python 3, a standard string object will be returned. If you need bytes, use:
>>> unidecode("Κνωσός").encode("ascii")
b'Knosos'
"""
import warnings
from sys import version_info

Cache = {}


def _warn_if_not_unicode(string):
    if version_info[0] > 2:
        unicode = str
    if not isinstance(string, unicode) and version_info[0] < 3:
        warnings.warn(  "Argument %r is not a unicode object. "
                        "Passing an encoded string will likely have "
                        "unexpected results." % (type(string),),
                        RuntimeWarning, 2)


def unidecode_expect_ascii(string,errors='ignore'):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "

    This function first tries to convert the string using ASCII codec.
    If it fails (because of non-ASCII characters), it falls back to
    transliteration using the character tables.

    This is approx. five times faster if the string only contains ASCII
    characters, but slightly slower than using unidecode directly if non-ASCII
    chars are present.
    """

    _warn_if_not_unicode(string)
    try:
        bytestring = string.encode('ASCII')
    except UnicodeEncodeError:
        return _unidecode(string,errors)
    if version_info[0] >= 3:
        return string
    else:
        return bytestring

def unidecode_expect_nonascii(string,errors='ignore'):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "
    """

    _warn_if_not_unicode(string)
    return _unidecode(string,errors=errors)

unidecode = unidecode_expect_ascii

def _unidecode(string,errors='ignore'):
    """
        Decode the string using the tables set up in the x???.py files in this project.

          errors
            The error handling scheme to use for encoding errors.
            The default is 'ignore' meaning that characters are dropped if no replacements are found in the tables.
            Other possible values are 'strict' an exception is thrown if no value is found,
            'replace' a ? is substituted if no replacement is found and 'preserve' the existing unicode character is kept.
        """
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
                Cache[section] = table = mod.data
            except ImportError as e:
                Cache[section] = table = None
                if errors=='strict':
                    raise e

        # set return value to the found charace
        if table and len(table) > position and table[position] != '' :
            return_char = table[position]
        elif errors == 'ignore':
            return_char = ''
        elif errors == 'strict':
            raise KeyError
        elif errors == 'replace':
            return_char = '?'
        else: # preserve
            return_char = char

        retval.append(return_char)

    return ''.join(retval)

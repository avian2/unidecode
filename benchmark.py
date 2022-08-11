# -*- coding: utf-8 -*-
from __future__ import print_function
import timeit

def main():
	print("unidecode_expect_ascii, ASCII string")
	timeit.main([
		'-s',
		'from unidecode import unidecode_expect_ascii',
		'unidecode_expect_ascii(u"Hello, World")'])

	print("unidecode_expect_ascii, non-ASCII string")
	timeit.main([
		'-s',
		'from unidecode import unidecode_expect_ascii',
		'unidecode_expect_ascii(u"¡Hola mundo!")'])

	print("unidecode_expect_nonascii, ASCII string")
	timeit.main([
		'-s',
		'from unidecode import unidecode_expect_nonascii',
		'unidecode_expect_nonascii(u"Hello, World")'])

	print("unidecode_expect_nonascii, non-ASCII string")
	timeit.main([
		'-s',
		'from unidecode import unidecode_expect_nonascii',
		'unidecode_expect_nonascii(u"¡Hola mundo!")'])

main()

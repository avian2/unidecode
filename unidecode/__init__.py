Char = {}

NULLMAP = [ '' * 0x100 ]

def unidecode(string):
	retval = []

	for char in string:
		o = ord(char)

		if o < 0x80:
			retval.append(char)
			continue

		h = o >> 8
		l = o & 0xff

		c = Char.get(h, None)
		
		if c == None:
			try:
				mod = __import__('unidecode.x%02x'%(h), [], [], ['data'])
			except ImportError:
				Char[h] = NULLMAP
				retval.append('')
				continue

			Char[h] = mod.data

			try:
				retval.append( mod.data[l] )
			except IndexError:
				retval.append( '' )
		else:
			try:
				retval.append( c[l] )
			except IndexError:
				retval.append( '' )

	return ''.join(retval)

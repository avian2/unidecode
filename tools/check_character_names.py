import sys
import re
import unidecode

all = 0
good = 0
for line in open("NamesList.txt"):
	f = line.split('\t')
	try:
		cp = int(f[0], 16)
	except ValueError:
		continue
	name = f[1]

	g = re.search("LATIN (SMALL|CAPITAL) LETTER (?:.* )?([A-Z])(?: .*)?$", name)
	if g:
		cap = g.group(1)
		letter = g.group(2)

		if cap == 'SMALL':
			letter = letter.lower()

		char = unichr(cp)
		letteru = unidecode.unidecode(char)

		if letteru != letter:
			print letteru, letter, char, "%05x" % cp, name.strip()
		else:
			good += 1

		all += 1

print 100.0*good/all

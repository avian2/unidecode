import re
import unidecode

name_re = re.compile("LATIN (SMALL|CAPITAL) LETTER (?:.* )?([A-Z])(?: .*)?$")

total = 0
good = 0
with open("NamesList.txt") as fp:
    for line in fp:
        f = line.split('\t')
        try:
            cp = int(f[0], 16)
        except ValueError:
            continue
        name = f[1]

        g = name_re.search(name)
        if g:
            cap = g.group(1)
            letter = g.group(2)

            if cap == 'SMALL':
                letter = letter.lower()

            char = chr(cp)
            letteru = unidecode.unidecode(char)

            if letteru != letter:
                print(letteru, letter, char, "%05x" % cp, name.strip())
            else:
                good += 1

            total += 1

print(100.0 * good / total)

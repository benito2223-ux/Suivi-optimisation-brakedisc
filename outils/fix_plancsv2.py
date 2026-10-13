# -*- coding: utf-8 -*-
"""Fix : le return de planCSV porte BOM et CRLF reels au lieu des echappements JS."""

p = 'bilan_economique.html'
s = open(p, encoding='utf-8', newline='').read()
q = chr(39)
BOM = chr(0xFEFF)
CRLF = chr(13) + chr(10)

def bs_escape():
    return chr(92) + 'ufeff'

def bs_crlf():
    return chr(92) + 'r' + chr(92) + 'n'

av = ('return ' + q + chr(34) + BOM + chr(34) + ' + L.join(' + q + chr(34) + CRLF + chr(34) + ');')
ap = ('return ' + q + chr(34) + bs_escape() + chr(34) + ' + L.join(' + q + chr(34) + bs_crlf() + chr(34) + ');')

def bs_escape():
    return chr(92) + 'ufeff'

def bs_crlf():
    return chr(92) + 'r' + chr(92) + 'n'

assert av in s, 'return casse introuvable'
s = s.replace(av, ap, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('return de planCSV repare : escapes JS retablis')

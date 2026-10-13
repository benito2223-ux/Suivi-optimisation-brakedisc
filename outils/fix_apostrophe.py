# -*- coding: utf-8 -*-
"""Fix definitif : l'apostrophe de « l'outil » doit etre echappee dans la chaine JS."""

p = 'bilan_economique.html'
s = open(p, encoding='utf-8', newline='').read()

AV = "(prix divergents dans l" + chr(39) + "outil"
AP = "(prix divergents dans l" + chr(92) + chr(39) + "outil"   # backslash + quote

n = s.count(AV)
print("occurrences non echappees :", n)
assert n >= 1, "rien a corriger"
s = s.replace(AV, AP)
open(p, 'w', encoding='utf-8', newline='').write(s)

s2 = open(p, encoding='utf-8', newline='').read()
i = s2.find("divergents dans")
print("apres relecture :", repr(s2[i:i+30]))
print("backslash present :", (chr(92) + chr(39)) in s2[i:i+30])
assert (chr(92) + chr(39)) in s2[i:i+30], "LA CORRECTION N'A PAS PERSISTE"
print("persistance verifiee")

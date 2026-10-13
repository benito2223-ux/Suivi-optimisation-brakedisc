# -*- coding: utf-8 -*-
"""Fix par ligne : le return de planCSV (BOM/CRLF reels -> escapes JS)."""

p = 'bilan_economique.html'
s = open(p, encoding='utf-8', newline='').read()
l = s.split(chr(10))          # lignes (le return casse est sur 2 lignes physiques ?)

# retrouver la ligne contenant L.join dans la fonction planCSV
depart = None
idx = None
for k, ligne in enumerate(l):
    if 'function planCSV' in ligne:
        depart = k
    if depart is not None and k >= depart and k <= depart + 12 and 'L.join(' in ligne:
        idx = k
print('ligne du return L.join :', (idx or -1) + 1)
print('avant :', repr(l[idx]))

q = chr(39); bs = chr(92); dq = chr(34)
BOM = chr(0xFEFF); CRLF = chr(13) + chr(10)
# la ligne peut contenir le BOM et le CRLF reels, ou des morceaux : on reconstruit
# la ligne entiere a partir du mot-clef return
if 'return' in l[idx] and 'L.join' in l[idx]:
    l[idx] = ('  return ' + q + dq + bs + 'ufeff' + dq + ' + L.join(' + q + dq + bs + 'r' + bs + 'n' + dq + ');')
else:
    # le return est a la ligne precedente et la chaine deborde sur celle-ci
    l[idx - 1] = ('  return ' + q + dq + bs + 'ufeff' + dq + ' + L.join(' + q + dq + bs + 'r' + bs + 'n' + dq + ');')
    del l[idx]

open(p, 'w', encoding='utf-8', newline='').write(chr(10).join(l))
s2 = open(p, encoding='utf-8', newline='').read()
assert (bs + 'ufeff') in s2[s2.find('function planCSV'):s2.find('function planExporter')]
print('return reconstruit avec les escapes JS')

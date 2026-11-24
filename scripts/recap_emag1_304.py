"""Recap Excel EMAG 1 / DV304x28 — OP20 seulement, côtés 1 et 2 (L120_1 / L120_2).
Les balises M870 sont écrites M700 / M670 sur T521 (coquilles) : on les lit comme M870 (voir l'onglet Anomalies).

Usage : python scripts/recap_emag1_304.py "Programmes/EMAG1 - 304x28" Programmes/RECAP_TEMPS_COUPE_DV304_EMAG1_OP20.xlsx
        (ajouter --json pour imprimer les valeurs à saisir dans le suivi)
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spf_temps
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = sys.argv[1]
OUT = sys.argv[2]
FILES = (('L120_1.SPF', 1), ('L120_2.SPF', 2))
ALIAS = ('700', '670')
ORDRE = [('T521', 2), ('T521', 1), ('T523', 2), ('T523', 1), ('T527', 1), ('T527', 2), ('T525', 1)]
LABEL = {('T521', 2): 'ébauche diamètre extérieur', ('T521', 1): 'chanfreins haut et bas (« FASE OBEN / UNTEN »)',
         ('T523', 2): 'ébauche (Ø intérieur, congé)', ('T523', 1): 'ébauche face',
         ('T527', 1): 'finition Ø, gorge et face', ('T527', 2): 'finition fond de gorge',
         ('T525', 1): "gorge d'isolation thermique (R4,76)"}


def lire(sans_limite=False):
    res = {}
    for f, side in FILES:
        path = os.path.join(D, f)
        if sans_limite:
            import re, tempfile
            t = open(path, encoding='latin-1').read()
            tmp = os.path.join(tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(OUT))), f)
            open(tmp, 'w', encoding='latin-1').write(re.sub(r'LIMS\s*=\s*\d+', 'LIMS=1000000', t))
            path = tmp
        segs, dwell, hors = spf_temps.run(path, False, ALIAS)
        res[side] = (segs, dwell, hors)
        if sans_limite:
            import shutil
            shutil.rmtree(os.path.dirname(path))
    return res


cap = lire()
nol = lire(True)


def agg(res):
    out = {}
    for side, (segs, dwell, hors) in res.items():
        for s in segs:
            g = out.setdefault((s['T'], s['D'], side), dict(t=0.0, c={}, segs=[]))
            g['t'] += s['t']
            g['segs'].append(s)
            key = (s['Vc'], s['F'])
            g['c'][key] = g['c'].get(key, 0) + s['t']
        for d in dwell:
            if d['mon']:
                k = (d['T'], d['D'], side)
                if k in out:
                    out[k]['t'] += d['t']
    return out


A = agg(cap)
N = agg(nol)


def dom(g):
    return max(g['c'], key=g['c'].get)


def txt(g):
    vs, fs = [], []
    for (vc, f) in g['c']:
        if vc not in vs:
            vs.append(vc)
        if f not in fs:
            fs.append(f)
    return 'G96 Vc ' + ' / '.join('%g' % v for v in vs) + ' · f ' + ' / '.join(('%g' % f).replace('.', ',') for f in fs)


if '--json' in sys.argv:
    print(json.dumps({'%s %d' % (T, d): dict(t=round(A[(T, d, 1)]['t'], 2), vc=dom(A[(T, d, 1)])[0], f=dom(A[(T, d, 1)])[1],
                                              t2=round(A[(T, d, 2)]['t'], 2)) for T, d in ORDRE}, indent=1))

H = PatternFill('solid', fgColor='1F4E8C')
HF = Font(bold=True, color='FFFFFF')
B = Font(bold=True)
thin = Side(style='thin', color='BBBBBB')
BD = Border(left=thin, right=thin, top=thin, bottom=thin)


def head(ws, row, cols):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row, i, c)
        x.fill = H
        x.font = HF
        x.alignment = Alignment(wrap_text=True, vertical='center')
        x.border = BD
    ws.row_dimensions[row].height = 46


def widths(ws, w):
    for i, v in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = v


wb = Workbook()
ws = wb.active
ws.title = 'Coupe par logement'
ws['A1'] = 'DV304x28 — EMAG 1, OP20 : temps de coupe pur par disque et par côté, depuis les programmes CN'
ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ("Côté 1 = L120_1, côté 2 = L120_2 (droite / gauche à rattacher). Fenêtre de coupe = M870 → M890, avec M700 / M670 lus comme M870 "
            "sur T521 (coquilles, voir « Anomalies »). Limite de broche LIMS=2800 appliquée. Hors rapides, chargement, changements d'outil.")
ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells('A2:J2')
ws.row_dimensions[2].height = 46
head(ws, 4, ['OP', 'Outil', 'Logement', 'Opération', 'Côté 1 (s)', 'Conditions côté 1', 'Côté 2 (s)', 'Conditions côté 2',
             'Écart côté 2 − côté 1 (s)', 'Écart (%)'])
r = 5
first = r
for T, d in ORDRE:
    g1, g2 = A[(T, d, 1)], A[(T, d, 2)]
    vals = [20, T, 'D%d' % d, LABEL[(T, d)], round(g1['t'], 2), txt(g1), round(g2['t'], 2), txt(g2),
            '=G%d-E%d' % (r, r), '=IF(E%d<>0,(G%d-E%d)/E%d,"")' % (r, r, r, r)]
    for i, x in enumerate(vals, 1):
        c = ws.cell(r, i, x)
        c.border = BD
    ws.cell(r, 5).number_format = '0.00'
    ws.cell(r, 7).number_format = '0.00'
    ws.cell(r, 9).number_format = '0.00'
    ws.cell(r, 10).number_format = '0%'
    r += 1
last = r - 1
r += 1
ws.cell(r, 1, 'OP20 (somme, outils en série)').font = B
ws.cell(r, 5, '=SUM(E%d:E%d)' % (first, last)).number_format = '0.00'
ws.cell(r, 7, '=SUM(G%d:G%d)' % (first, last)).number_format = '0.00'
ws.cell(r, 9, '=G%d-E%d' % (r, r)).number_format = '0.00'
for c in (5, 7, 9):
    ws.cell(r, c).font = B
r += 2
for n in ("Seul T521 diffère vraiment : côté 1 en G96 Vc 1500 / f 0,35, côté 2 en G96 Vc 800 / f 0,30 (ébauche) — c'est tout l'écart de l'OP. "
          "T523, T525 et T527 sont identiques aux 0,1 s près (côté 2 : rayon 2,5 au lieu de 2,3 sur T523 D2).",
          "T525 (gorge) : trois avances successives (0,15 / 0,1 / 0,3) ; T527 D1 : limite de broche atteinte sur la face (voir l'onglet « Limite broche »).",
          "Tous les logements travaillent en G96. Aucune comparaison EMAG 2 : cette référence (304x28) n'a pas de programme EMAG 2 ici."):
    ws.cell(r, 1, n).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
    ws.row_dimensions[r].height = 34
    r += 1
widths(ws, [8, 9, 10, 40, 11, 30, 11, 30, 14, 10])
ws.freeze_panes = 'A5'

# limite de broche
w2 = wb.create_sheet('Limite broche')
w2['A1'] = 'Opérations où la limite de broche LIMS=2800 est atteinte'
w2['A1'].font = Font(bold=True, size=13)
head(w2, 3, ['Côté', 'Outil', 'Logement', 'Ø mini (mm)', 'Ø maxi (mm)', 'Vc programmée', 'tr/min demandé au Ø mini', 'LIMS (tr/min)',
             'Temps avec limite (s)', 'Temps sans limite (s)', 'Écart (s)', 'Vc réelle au Ø mini', 'Vc réelle au plus grand Ø'])
r = 4
for (T, d, side), g in sorted(A.items(), key=lambda k: (k[0][2], ORDRE.index((k[0][0], k[0][1])))):
    if not any(s['capped'] for s in g['segs']):
        continue
    gn = N[(T, d, side)]
    vc = dom(g)[0]
    dmin = min(min(s['x0'], s['x1']) for s in g['segs'])
    dmax = max(max(s['x0'], s['x1']) for s in g['segs'])
    vals = [side, T, 'D%d' % d, round(dmin, 1), round(dmax, 1), vc, '=ROUND(1000*F%d/(PI()*D%d),0)' % (r, r), 2800,
            round(g['t'], 2), round(gn['t'], 2), '=J%d-I%d' % (r, r), '=ROUND(MIN(F%d,PI()*D%d*H%d/1000),0)' % (r, r, r),
            '=ROUND(MIN(F%d,PI()*E%d*H%d/1000),0)' % (r, r, r)]
    for i, x in enumerate(vals, 1):
        w2.cell(r, i, x).border = BD
    r += 1
widths(w2, [7, 9, 10, 11, 11, 12, 14, 12, 12, 12, 10, 12, 14])

# anomalies
w3 = wb.create_sheet('Anomalies programmes')
w3['A1'] = 'À signaler aux méthodes'
w3['A1'].font = Font(bold=True, size=13)
head(w3, 3, ['Programme', 'Ligne', 'Constat', 'Conséquence'])
rows = [
    ('L120_1', 'N110', "T521 D2 : « G1 X300 F0.35 H5002 M700 » — M700 au lieu de M870", "la surveillance Montronix ne démarre pas sur T521 D2 (le M890 de fin est bien là)"),
    ('L120_1', 'N190', "T521 D1 : « M670 » au lieu de M870 sur le chanfrein haut", "idem pour T521 D1"),
    ('L120_2', 'N110 / N190', "mêmes coquilles : M670 sur les deux lignes de T521", "idem côté 2"),
    ('L120_1 / L120_2', 'N700', "« G4F0.2 » (soufflage) hors fenêtre : 0,2 s non comptée", "aucune"),
    ('L120_1 / L120_2', 'T521', "côté 1 en Vc 1500 / f 0,35, côté 2 en Vc 800 / f 0,30 sur l'ébauche du Ø extérieur", "3,66 s contre 8,15 s : à confirmer lequel est la bonne référence"),
]
for i, rw in enumerate(rows, 4):
    for j, x in enumerate(rw, 1):
        c = w3.cell(i, j, x)
        c.border = BD
        c.alignment = Alignment(wrap_text=True, vertical='top')
widths(w3, [18, 14, 70, 60])

wb.save(OUT)
print('OK', OUT)

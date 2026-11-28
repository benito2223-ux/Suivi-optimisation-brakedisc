"""Recap Excel EMAG 1 / DV304x28 — OP10, OP20, OP30, OP40, côtés 1 et 2 (Lignes complètes).
Les balises M870 sont écrites M700 / M670 sur T521 (coquilles) : on les lit comme M870 (ouvre_extra).
Sur OP40 côté 2, le fichier est nommé L150_1.SPF sur la machine (confirmé par Matis).

Usage : python scripts/recap_emag1_304.py "Programmes/EMAG1 - 304x28" Programmes/RECAP_TEMPS_COUPE_DV304_EMAG1.xlsx [--json]
"""
import os, re, sys, json, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spf_temps
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = sys.argv[1]
OUT = sys.argv[2]
FILES = {
    10: ('L110_1_CBN.SPF', 'L110_2_CBN.SPF'),
    20: ('L120_1.SPF', 'L120_2.SPF'),
    30: ('L130_11_S.SPF', 'L130_12_S.SPF'),
    40: ('L140_1.SPF', 'L150_1.SPF')
}
ALIAS = ('700', '670')
HOLES = {'T532S': 5, 'T533S': 3}

LABEL = {
    (10, 'T511', 1): 'Chanfrein alésage / face (S-Platte R1.6)',
    (10, 'T511', 2): 'Ébauche Ø intérieur (C-Platte R1.6)',
    (10, 'T513', 2): 'Ébauche grande face et Ø int (C-Platte R1.6)',
    (10, 'T513', 1): 'Dégagement bol / épaulement (C-Platte R1.6)',
    (10, 'T515', 2): 'Ébauche (S-Platte R1.6)',
    (10, 'T515', 1): 'Ébauche (S-Platte R1.6)',
    (20, 'T521', 2): 'Ébauche diamètre extérieur (SNMX 120716)',
    (20, 'T521', 1): 'Chanfreins haut et bas (« FASE OBEN / UNTEN »)',
    (20, 'T523', 2): 'Ébauche (Ø intérieur, congé)',
    (20, 'T523', 1): 'Ébauche face',
    (20, 'T525', 1): "Gorge d'isolation thermique (R4,76)",
    (20, 'T527', 1): 'Finition Ø, gorge et face',
    (20, 'T527', 2): 'Finition fond de gorge',
    (30, 'T532S', 1): 'Foret carbure monobloc D13,1 (5 trous)',
    (30, 'T533S', 1): 'Foret D8,6 (3 trous)',
    (40, 'T543', 2): 'Finition alésage D71,05',
    (40, 'T543', 1): 'Finition face / chanfrein',
    (40, 'T546', 1): 'Finition rayon R8 (C-Platte R1.6)',
    (40, 'T549', 1): 'Finition pistes (straddle S-Platte R0.8)'
}

def lire(nolimit=False):
    res = {}
    tmp = None
    src = D
    if nolimit:
        tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(OUT)))
        for f in os.listdir(D):
            if f.upper().endswith('.SPF'):
                t = open(os.path.join(D, f), encoding='latin-1').read()
                open(os.path.join(tmp, f), 'w', encoding='latin-1').write(re.sub(r'LIMS\s*=\s*\d+', 'LIMS=1000000', t))
        src = tmp
    for op, fs in FILES.items():
        for side, f in enumerate(fs, 1):
            res[(op, side)] = spf_temps.run(os.path.join(src, f), balises_commentees=False, ouvre_extra=ALIAS)
    if tmp:
        shutil.rmtree(tmp)
    return res

cap = lire()
nol = lire(True)

def agg(res):
    out = {}
    for (op, side), (segs, dwell, hors) in res.items():
        for s in segs:
            k = (op, s['T'], s['D'])
            g = out.setdefault(k, {}).setdefault(side, dict(t=0.0, cond=[], seg=[]))
            g['t'] += s['t']
            g['seg'].append(s)
            c = ('G96 Vc %g' % s['Vc']) if s['Vc'] is not None else ('G97 %d tr/min' % round(s['N']))
            if (c, s['F']) not in g['cond']:
                g['cond'].append((c, s['F']))
        for d in dwell:
            if d['mon']:
                k = (op, d['T'], d['D'])
                if k in out and side in out[k]:
                    out[k][side]['t'] += d['t']
    for (op, T, Dd), sides in out.items():
        for sd in sides.values():
            sd['t'] *= HOLES.get(T, 1)
    return out

A = agg(cap)

def condtxt(g):
    if not g: return ''
    modes = []
    fs = []
    for c, f in g['cond']:
        if c not in modes:
            modes.append(c)
        if f not in fs:
            fs.append(f)
    return ' / '.join(modes) + ' · f ' + ' / '.join(('%g' % f).replace('.', ',') for f in fs)

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
ws['A1'] = 'DV304x28 — EMAG 1 (ligne double) : temps de coupe pur par disque et par côté, depuis les programmes CN'
ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ("Côté 1 = L110_1 / L120_1 / L130_11_S / L140_1 ; côté 2 = L110_2 / L120_2 / L130_12_S / L150_1. "
            "Les balises M870/M890 sont actives (coquilles M700/M670 sur T521 lues comme M870). "
            "Limite de broche LIMS appliquée. Hors rapides, chargement, changements d'outil.")

head(ws, 4, ['OP', 'Outil', 'Logement', 'Opération', 'Côté 1 (s)', 'Conditions côté 1', 'Côté 2 (s)',
             'Conditions côté 2', 'Écart côté 2 − côté 1 (s)', 'Écart (%)'])

order = []
for op in (10, 20, 30, 40):
    for s in cap[(op, 1)][0]:
        k = (op, s['T'], s['D'])
        if k not in order:
            order.append(k)
    for k in A:
        if k[0] == op and k not in order:
            order.append(k)

r = 5
for k in order:
    op, T, Dd = k
    g1 = A[k].get(1)
    g2 = A[k].get(2)
    vals = [op, T, 'D%d' % Dd, LABEL.get(k, ''), round(g1['t'], 2) if g1 else None,
            condtxt(g1) if g1 else '', round(g2['t'], 2) if g2 else None, condtxt(g2) if g2 else '']
    for i, v in enumerate(vals, 1):
        ws.cell(r, i, v).border = BD
    ws.cell(r, 9, f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(G{r})),G{r}-E{r},"")').border = BD
    ws.cell(r, 10, f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(G{r}),E{r}<>0),(G{r}-E{r})/E{r},"")').border = BD
    ws.cell(r, 10).number_format = '0%'
    for c in (5, 7, 9):
        ws.cell(r, c).number_format = '0.00'
    r += 1

last = r - 1
r += 1
ws.cell(r, 1, 'Total par OP').font = B
r += 1
t0 = r
for op in (10, 20, 30, 40):
    ws.cell(r, 1, f'OP{op}').font = B
    for col, L in ((5, 'E'), (7, 'G')):
        c = ws.cell(r, col, f'=SUMIF($A$5:$A${last},{op},{L}$5:{L}${last})')
        c.number_format = '0.0'
        c.font = B
    ws.cell(r, 9, f'=G{r}-E{r}').number_format = '0.0'
    ws.cell(r, 10, f'=(G{r}-E{r})/E{r}').number_format = '0%'
    r += 1

ws.cell(r, 1, 'Ligne (4 OP)').font = B
for col, L in ((5, 'E'), (7, 'G')):
    c = ws.cell(r, col, f'=SUM({L}{t0}:{L}{r - 1})')
    c.number_format = '0.0'
    c.font = B
ws.cell(r, 9, f'=G{r}-E{r}').number_format = '0.0'
ws.cell(r, 10, f'=(G{r}-E{r})/E{r}').number_format = '0%'

ws.cell(r + 2, 1, "OP30 : perçages multipliés par le nombre de trous (5 et 3). "
                  "OP40 côté 2 : programme nommé L150_1.SPF sur CN (expliqué par Matis). "
                  "Attention : sur L140_1 (OP40 côté 1), la passe d'ébauche/finition T549 de X307 à X236 a son M870 placé après (7,99 s hors balises).")

widths(ws, [6, 9, 10, 38, 12, 32, 12, 32, 14, 10])
ws.freeze_panes = 'E5'

# Sheet 2 : Écarts
w2 = wb.create_sheet('Écarts entre côtés')
w2['A1'] = 'Logements dont les conditions ou le temps diffèrent entre les deux côtés — DV304x28'
w2['A1'].font = Font(bold=True, size=13)
head(w2, 3, ['OP', 'Outil', 'Logement', 'Opération', 'Conditions côté 1', 'Conditions côté 2', 'Côté 1 (s)',
             'Côté 2 (s)', 'Écart (s)', 'Plus rapide'])
r = 4
for k in order:
    op, T, Dd = k
    g1 = A[k].get(1)
    g2 = A[k].get(2)
    if not (g1 and g2): continue
    if condtxt(g1) == condtxt(g2) and abs(g1['t'] - g2['t']) < 0.1: continue
    vals = [op, T, 'D%d' % Dd, LABEL.get(k, ''), condtxt(g1), condtxt(g2), round(g1['t'], 2), round(g2['t'], 2)]
    for i, v in enumerate(vals, 1):
        w2.cell(r, i, v).border = BD
    w2.cell(r, 9, f'=H{r}-G{r}').number_format = '0.00'
    w2.cell(r, 10, f'=IF(ABS(I{r})<0.005,"=",IF(I{r}<0,"côté 2","côté 1"))')
    for c in (7, 8):
        w2.cell(r, c).number_format = '0.00'
    r += 1

widths(w2, [6, 9, 10, 34, 34, 34, 11, 11, 10, 11])
w2.freeze_panes = 'A4'

# Sheet 3 : Hors balises
w3 = wb.create_sheet('Hors balises & Anomalies')
w3['A1'] = 'Avances et temporisations en dehors des fenêtres de coupe M870-M890'
w3['A1'].font = Font(bold=True, size=13)
head(w3, 3, ['OP', 'Côté', 'Outil', 'Logement', 'Nature', 'Longueur (mm)', 'Avance (mm/tr)', 'Temps (s)', 'Commentaire / Impact'])
r = 4
for (op, side), (segs, dwell, hors) in cap.items():
    for h in hors:
        com = ""
        if op == 40 and h['T'] == 'T549':
            com = "COQUILLE MAJEURE : M870 placé après la passe X307->X236 (7,99s de coupe non surveillée)"
        elif op == 10 and h['T'] == 'T513':
            com = ";M870 commenté en ligne N510 (1,45s non surveillée)"
        for i, x in enumerate([op, side, h['T'], 'D%d' % h['D'], 'avance hors balises', round(h['L'], 2), h['F'],
                               round(h['t'], 2), com], 1):
            w3.cell(r, i, x).border = BD
        r += 1
widths(w3, [6, 7, 9, 10, 30, 14, 14, 10, 50])
w3.freeze_panes = 'A4'

wb.save(OUT)
print(f"Excel généré : {OUT}")

# Dump JSON if requested
json_data = {}
for op in (10, 20, 30, 40):
    json_data[f"OP{op}"] = {}
    for (o, T, Dd), sides in A.items():
        if o == op:
            g1 = sides.get(1, {'t': 0.0, 'cond': []})
            g2 = sides.get(2, {'t': 0.0, 'cond': []})
            json_data[f"OP{op}"][f"{T}_D{Dd}"] = {
                "label": LABEL.get((o, T, Dd), ''),
                "t_cote1": round(g1['t'], 2),
                "cond_cote1": condtxt(g1),
                "t_cote2": round(g2['t'], 2),
                "cond_cote2": condtxt(g2)
            }

json_path = os.path.join(os.path.dirname(OUT), "temps_coupe_DV304_EMAG1.json")
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump(json_data, jf, indent=2, ensure_ascii=False)
print(f"JSON généré : {json_path}")

tot = {}
for k, sides in A.items():
    for s, g in sides.items():
        tot[(k[0], s)] = tot.get((k[0], s), 0) + g['t']
print("Totaux temps par OP et côté :")
print({k: round(v, 2) for k, v in sorted(tot.items())})

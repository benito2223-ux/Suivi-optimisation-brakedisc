"""Recap Excel EMAG 1 (ligne double, 356x26) : temps de coupe par logement et par côté, comparaison des côtés,
limite de broche, avances/temporisations hors balises. Lit les .SPF de Programmes/EMAG1 356x26/ (balises commentées).

Usage : python scripts/recap_emag1.py "Programmes/EMAG1 356x26" Programmes/RECAP_TEMPS_COUPE_DV356_EMAG1.xlsx
"""
import os, re, sys, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spf_temps
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = sys.argv[1]
OUT = sys.argv[2]
FILES = {10: ('L110_1_CBN_50013.SPF', 'L110_2_CBN_50013.SPF'), 20: ('L120_11.SPF', 'L120_22.SPF'),
         30: ('L130_11_K_SUB1.SPF', 'L130_11_K_SUB2.SPF'), 40: ('L140_1.SPF', 'L140_2.SPF')}
HOLES = {'T535S': 5, 'T533S': 3}
LABEL = {('T517', 1): 'ébauche intérieure', ('T517', 2): 'ébauche intérieure (alésage, face)',
         ('T50013', 2): 'ébauche piste (CBN)', ('T50013', 1): 'finition intérieure et face appui',
         ('T519', 2): 'alésage moyeu ébauche', ('T519', 1): 'face arrière moyeu',
         ('T521', 2): 'ébauche chanfrein piste, finition D356', ('T521', 1): 'finition chanfreins entrée piste',
         ('T529', 1): 'ébauche piste', ('T525', 1): 'Ø ext. moyeu, fond gorge ébauche',
         ('T5211', 1): 'Ø ext. moyeu finition', ('T535S', 1): 'foret Ø15,3 — 5 trous',
         ('T533S', 1): 'foret Ø8,6 — 3 trous', ('T543', 1): 'finition chanfrein, face avant',
         ('T543', 2): 'alésage moyeu', ('T546', 1): 'finition R114', ('T549', 1): 'finition piste, 1 passe'}
# EMAG 2 (calcul du 23/11) pour comparaison ; T50013 (EMAG 1) mis en regard de T513 (EMAG 2)
EMAG2 = {('T517', 1): 5.2, ('T517', 2): 3.9, ('T50013', 2): 11.1, ('T50013', 1): 4.0, ('T519', 2): 0.6,
         ('T519', 1): 4.7, ('T521', 2): 5.5, ('T521', 1): 2.4, ('T529', 1): 10.3, ('T525', 1): 7.9,
         ('T5211', 1): 4.5, ('T535S', 1): 8.0, ('T533S', 1): 6.8, ('T543', 1): 5.8, ('T543', 2): 0.7,
         ('T546', 1): 8.3, ('T549', 1): 21.8}


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
            res[(op, side)] = spf_temps.run(os.path.join(src, f), True)
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
ws['A1'] = 'DV356x26 — EMAG 1 (ligne double) : temps de coupe pur par disque et par côté, depuis les programmes CN'
ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ("Côté 1 = L110_1 / L120_11 / L130_SUB1 / L140_1 ; côté 2 = L110_2 / L120_22 / L130_SUB2 / L140_2. "
            "Les balises M870/M890 sont en commentaire dans ces programmes : la fenêtre de coupe est lue à leur emplacement. "
            "Limite de broche LIMS appliquée. Hors rapides, chargement, changements d'outil.")
head(ws, 4, ['OP', 'Outil', 'Logement', 'Opération', 'Côté 1 (s)', 'Conditions côté 1', 'Côté 2 (s)',
             'Conditions côté 2', 'Écart côté 2 − côté 1 (s)', 'Écart (%)', 'EMAG 2 (s)',
             'Écart côté 1 vs EMAG 2 (s)'])
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
    vals = [op, T, 'D%d' % Dd, LABEL.get((T, Dd), ''), round(g1['t'], 2) if g1 else None,
            condtxt(g1) if g1 else '', round(g2['t'], 2) if g2 else None, condtxt(g2) if g2 else '']
    for i, v in enumerate(vals, 1):
        ws.cell(r, i, v).border = BD
    ws.cell(r, 9, f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(G{r})),G{r}-E{r},"")').border = BD
    ws.cell(r, 10, f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(G{r}),E{r}<>0),(G{r}-E{r})/E{r},"")').border = BD
    ws.cell(r, 10).number_format = '0%'
    ws.cell(r, 11, EMAG2.get((T, Dd))).border = BD
    ws.cell(r, 12, f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(K{r})),E{r}-K{r},"")').border = BD
    for c in (5, 7, 9, 11, 12):
        ws.cell(r, c).number_format = '0.0'
    r += 1
last = r - 1
r += 1
ws.cell(r, 1, 'Total par OP').font = B
r += 1
t0 = r
for op in (10, 20, 30, 40):
    ws.cell(r, 1, f'OP{op}').font = B
    for col, L in ((5, 'E'), (7, 'G'), (11, 'K')):
        c = ws.cell(r, col, f'=SUMIF($A$5:$A${last},{op},{L}$5:{L}${last})')
        c.number_format = '0.0'
        c.font = B
    ws.cell(r, 9, f'=G{r}-E{r}').number_format = '0.0'
    ws.cell(r, 10, f'=(G{r}-E{r})/E{r}').number_format = '0%'
    r += 1
ws.cell(r, 1, 'Ligne (4 OP)').font = B
for col, L in ((5, 'E'), (7, 'G'), (11, 'K')):
    c = ws.cell(r, col, f'=SUM({L}{t0}:{L}{r - 1})')
    c.number_format = '0.0'
    c.font = B
ws.cell(r, 9, f'=G{r}-E{r}').number_format = '0.0'
ws.cell(r, 10, f'=(G{r}-E{r})/E{r}').number_format = '0%'
ws.cell(r + 2, 1, "OP30 : perçages multipliés par le nombre de trous (5 et 3). T50013 (EMAG 1) mis en regard de T513 (EMAG 2). "
                  "Pas de T5211 D2 (fond de gorge finition) dans les programmes EMAG 1 : il n'est pas comparé. "
                  "Colonne EMAG 2 = calcul du 23/11 (T548 simultané à T549, non cumulé).")
ws.cell(r + 3, 1, "L'en-tête de L110_1 mentionne encore le chemin DV304X28 (copie d'un programme du 304) alors que son titre dit 356 x 26 : à confirmer avec les méthodes.")
widths(ws, [6, 9, 10, 36, 11, 30, 11, 30, 14, 9, 11, 15])
ws.freeze_panes = 'E5'

w2 = wb.create_sheet('Écarts entre côtés')
w2['A1'] = 'Logements dont les conditions ou le temps diffèrent entre les deux côtés'
w2['A1'].font = Font(bold=True, size=13)
head(w2, 3, ['OP', 'Outil', 'Logement', 'Opération', 'Conditions côté 1', 'Conditions côté 2', 'Côté 1 (s)',
             'Côté 2 (s)', 'Écart (s)', 'Plus rapide'])
r = 4
for k in order:
    op, T, Dd = k
    g1 = A[k].get(1)
    g2 = A[k].get(2)
    if not (g1 and g2):
        continue
    if condtxt(g1) == condtxt(g2) and abs(g1['t'] - g2['t']) < 0.1:
        continue
    vals = [op, T, 'D%d' % Dd, LABEL.get((T, Dd), ''), condtxt(g1), condtxt(g2), round(g1['t'], 2), round(g2['t'], 2)]
    for i, v in enumerate(vals, 1):
        w2.cell(r, i, v).border = BD
    w2.cell(r, 9, f'=H{r}-G{r}').number_format = '0.00'
    w2.cell(r, 10, f'=IF(ABS(I{r})<0.005,"=",IF(I{r}<0,"côté 2","côté 1"))')
    for c in (7, 8):
        w2.cell(r, c).number_format = '0.00'
    r += 1
r += 1
w2.cell(r, 1, 'Totaux par OP').font = B
r += 1
head(w2, r, ['OP', '', '', '', '', '', 'Côté 1 (s)', 'Côté 2 (s)', 'Écart (s)', 'Écart (%)'])
r += 1
for op in (10, 20, 30, 40):
    w2.cell(r, 1, f'OP{op}')
    w2.cell(r, 7, f"=SUMIF('Coupe par logement'!$A$5:$A${last},{op},'Coupe par logement'!$E$5:$E${last})").number_format = '0.0'
    w2.cell(r, 8, f"=SUMIF('Coupe par logement'!$A$5:$A${last},{op},'Coupe par logement'!$G$5:$G${last})").number_format = '0.0'
    w2.cell(r, 9, f'=H{r}-G{r}').number_format = '0.0'
    w2.cell(r, 10, f'=(H{r}-G{r})/G{r}').number_format = '0%'
    r += 1
w2.cell(r + 1, 1, "Les écarts viennent des conditions programmées (avances, vitesses, cotes d'arrêt), pas de la géométrie : voir les colonnes « Conditions ».")
widths(w2, [6, 9, 10, 34, 34, 34, 11, 11, 10, 11])
w2.freeze_panes = 'A4'

w3 = wb.create_sheet('Limite broche (LIMS)')
w3['A1'] = 'Passes où la limite de broche (LIMS) réduit la vitesse de coupe réelle — EMAG 1'
w3['A1'].font = Font(bold=True, size=13)
w3['A2'] = "LIMS : 2300 tr/min en OP10, 2800 en OP20, 3000 en OP40. Temps « sans limite » = temps théorique qui n'existe pas sur la machine."
head(w3, 4, ['OP', 'Côté', 'Outil', 'Logement', 'Diamètre début (mm)', 'Diamètre fin (mm)', 'Vc programmée (m/min)',
             'Broche demandée (tr/min)', 'Broche réelle max (tr/min)', 'Temps avec limite (s)', 'Temps sans limite (s)',
             'Écart (s)', 'Vc réelle au plus petit Ø (m/min)', 'Vc réelle au plus grand Ø (m/min)'])
r = 5
LIM = {10: 2300, 20: 2800, 40: 3000}
for (op, side), (segs, dwell, hors) in cap.items():
    nsegs = nol[(op, side)][0]
    for a, b in zip(segs, nsegs):
        if abs(a['t'] - b['t']) > 1e-6 and a['Vc'] is not None:
            lim = LIM[op]
            v = [op, side, a['T'], 'D%d' % a['D'], round(a['x0']), round(a['x1']), a['Vc'], round(b['N']),
                 round(a['N']), round(a['t'], 2), round(b['t'], 2)]
            for i, x in enumerate(v, 1):
                w3.cell(r, i, x).border = BD
            w3.cell(r, 12, f'=J{r}-K{r}').border = BD
            w3.cell(r, 13, f'=ROUND(MIN(G{r},PI()*MIN(E{r},F{r})*{lim}/1000),0)').border = BD
            w3.cell(r, 14, f'=ROUND(MIN(G{r},PI()*MAX(E{r},F{r})*{lim}/1000),0)').border = BD
            for c in (10, 11, 12):
                w3.cell(r, c).number_format = '0.00'
            r += 1
w3.cell(r + 1, 1, "Broche demandée / réelle : valeurs moyennes sur la passe (la limite n'agit qu'aux petits diamètres). "
                  "Vc réelle = π × D × tr/min limite / 1000, plafonnée à la Vc programmée.")
widths(w3, [6, 7, 9, 10, 11, 11, 13, 13, 13, 12, 12, 9, 15, 15])
w3.freeze_panes = 'A5'

w4 = wb.create_sheet('Hors balises')
w4['A1'] = 'Avances et temporisations en dehors des fenêtres de coupe (non comptées dans les temps)'
w4['A1'].font = Font(bold=True, size=13)
w4['A2'] = 'Approches, retraits en avance, temporisations de soufflage : à classer (approche ou coupe réelle) avec les opérateurs.'
head(w4, 4, ['OP', 'Côté', 'Outil', 'Logement', 'Nature', 'Longueur (mm)', 'Avance (mm/tr)', 'Temps (s)'])
r = 5
for (op, side), (segs, dwell, hors) in cap.items():
    for h in hors:
        for i, x in enumerate([op, side, h['T'], 'D%d' % h['D'], 'avance hors balises', round(h['L'], 2), h['F'],
                               round(h['t'], 2)], 1):
            w4.cell(r, i, x).border = BD
        r += 1
    for d in dwell:
        if not d['mon']:
            for i, x in enumerate([op, side, d['T'], 'D%d' % d['D'], 'temporisation hors balises (soufflage…)', None,
                                   None, round(d['t'], 2)], 1):
                w4.cell(r, i, x).border = BD
            r += 1
widths(w4, [6, 7, 9, 10, 38, 14, 14, 10])
w4.freeze_panes = 'A5'
wb.save(OUT)

tot = {}
for k, sides in A.items():
    for s, g in sides.items():
        tot[(k[0], s)] = tot.get((k[0], s), 0) + g['t']
print({k: round(v, 1) for k, v in sorted(tot.items())})

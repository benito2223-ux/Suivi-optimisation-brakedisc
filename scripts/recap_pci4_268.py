"""Recap Excel PCI 4 / DP268x12 : temps de coupe pur par logement depuis les programmes Fanuc,
limite de broche (G50), fenêtres Montronix. Lit Programmes/PCI 4 - DP268X12/ (4 fichiers).

Usage : python scripts/recap_pci4_268.py "Programmes/PCI 4 - DP268X12" Programmes/RECAP_TEMPS_COUPE_DP268_PCI4.xlsx
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fanuc_temps as ft
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = sys.argv[1]
OUT = sys.argv[2]
FILES = {10: ('O2681 - OP10', False), 20: ('O2682 - OP20', False), 30: ('O2681-OP30', True), 40: ('O2687 - OP40', False)}

# (OP, T du programme, élément) -> (outil du suivi, logement du suivi, opération)
MAP = [
    (10, 'T01', None, 'T6101', 'T0101', 'ébauche diamètre bol'),
    (10, 'T11', None, 'T6101', 'T0111', 'ébauche fond de bol'),
    (10, 'T03', None, 'T6103', 'T0303', 'ébauche piste intérieure'),
    (10, 'T13', None, 'T6103', 'T0313', 'finition intérieure bol + dégagement piste'),
    (10, 'T15', None, 'T6105', 'T0515', 'ébauche diamètre moyeu'),
    (10, 'T25', None, 'T6105', 'T0525', 'ébauche appui jante'),
    (20, 'T03', None, 'T6203', 'T0303', 'ébauche piste'),
    (20, 'T17', None, 'T6207', 'T0717', 'face appui jante'),
    (20, 'T11', None, 'T6201', 'T0111', 'diamètre extérieur (avec temporisation 1 s)'),
    (20, 'T01', None, 'T6201', 'T0101', 'chanfrein'),
    (30, 'T105', 'percage', 'T6305', 'Logement 1', 'perçage Ø8,5 — 2 trous'),
    (30, 'T105', 'fraisurage', 'T6305', 'Logement 2', 'fraisurage / chanfrein arrière Ø8,5 — 2 trous'),
    (30, 'T104', 'percage', 'T6304', 'Logement 1', 'perçage Ø13,2 — 4 trous'),
    (30, 'T104', 'fraisurage', 'T6304', 'Logement 2', 'fraisurage / chanfrein arrière Ø13,2 — 4 trous'),
    (40, 'T01', None, 'T6401', 'T0101', 'alésage / face moyeu'),
    (40, 'T11', None, 'T6401', 'T0111', 'finition chanfrein, face avant (plaquette R1,6)'),
    (40, 'T07', 'passe1', 'T6407', 'T0707', 'finition piste — 1re passe'),
    (40, 'T07', 'passe2', 'T6417', 'T0707', 'finition piste — 2e passe'),
]


def lire(sans_limite=False):
    res = {}
    for op, (f, fr) in FILES.items():
        segs, dwell, hors = ft.run(os.path.join(D, f), fr, sans_limite)
        # fraisage : on prend TOUS les trous (la fenêtre Montronix n'en couvre qu'un par outil)
        allsegs = segs + hors if fr else segs
        for s in allsegs:
            s['fen'] = s in segs
        # passes de T07 en OP40 : on numérote les avances longues
        if op == 40:
            n = 0
            for s in allsegs:
                if s['T'] == 'T07' and s['L'] > 50:
                    n += 1
                    s['elt'] = 'passe%d' % n
        for s in allsegs:
            s.setdefault('elt', s.get('kind'))
        res[op] = (allsegs, [d for d in dwell if d['mon']], hors if not fr else [])
    return res


cap = lire()
nol = lire(True)


def agg(res):
    out = {}
    for op, (segs, dwell, hors) in res.items():
        for s in segs:
            out.setdefault((op, s['T'], s['elt']), dict(t=0.0, segs=[]))
            out[(op, s['T'], s['elt'])]['t'] += s['t']
            out[(op, s['T'], s['elt'])]['segs'].append(s)
        for d in dwell:
            for k in out:
                if k[0] == op and k[1] == d['T']:
                    out[k]['t'] += d['t']
                    break
    return out


A = agg(cap)
N = agg(nol)


def dominante(g):
    c = {}
    for s in g['segs']:
        if s['mode'] in ('G1',) and s.get('kind') == 'percage':
            key = ('G97', s['S'], s['F'])
        elif s.get('kind') == 'fraisurage':
            key = ('G97', s['S'], s['F'])
        elif s.get('Vc') is not None:
            key = ('G96', s['Vc'], s['F'])
        else:
            key = ('G97', s['S'], s['F'])
        c[key] = c.get(key, 0) + s['t']
    return max(c, key=c.get), list(c)


def condtxt(g, fraisage):
    _, allk = dominante(g)
    mots = []
    for m, v, f in allk:
        if fraisage:
            txt = ('G97 %d tr/min · F %g mm/min (≈ f %.2f mm/tr)' % (v, f, f / v)).replace('.', ',', 0)
            txt = txt[:txt.index('≈')] + txt[txt.index('≈'):].replace('.', ',')
        else:
            txt = ('G96 Vc %g' % v if m == 'G96' else 'G97 %d tr/min' % v) + ' · f %s' % ('%g' % f).replace('.', ',')
        if txt not in mots:
            mots.append(txt)
    return ' / '.join(mots)


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
ws['A1'] = 'DP268x12 — PCI 4 : temps de coupe pur par disque, depuis les programmes CN (Fanuc)'
ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ("Programmes : O2681 (OP10), O2682 (OP20), O2681-OP30, O2687 (OP40). Fenêtre de coupe = entre M2908 et M2909 (enregistrement Montronix). "
            "Limite de broche G50 appliquée. Hors rapides, chargement, changements d'outil. "
            "OP30 : tous les trous sont comptés (la fenêtre Montronix n'en couvre qu'un par outil).")
ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells('A2:K2')
ws.row_dimensions[2].height = 48
head(ws, 4, ['OP', 'Outil (suivi)', 'Logement (suivi)', 'Opération', 'Temps de coupe (s)', 'Conditions programmées',
             'Vc (m/min)', 'f (mm/tr)', 'tr/min (G97)', 'Broche limitée (G50)', "Temps compté dans l'OP (s)"])
SIMUL = {(40, 'T07', 'passe2')}   # T6417 simultané de T6407 (confirmé par Benjamin) : le groupe vaut le plus long
r = 5
first = r
rows = []
for op, T, elt, outil, log, label in MAP:
    g = A.get((op, T, elt))
    if not g:
        continue
    fr = (op == 30)
    (m, v, f), _ = dominante(g)
    ws.cell(r, 1, op)
    ws.cell(r, 2, outil)
    ws.cell(r, 3, log)
    ws.cell(r, 4, label)
    ws.cell(r, 5, round(g['t'], 2))
    ws.cell(r, 6, condtxt(g, fr))
    if m == 'G96':
        ws.cell(r, 7, v)
        ws.cell(r, 8, f)
    else:
        ws.cell(r, 9, v)
        ws.cell(r, 8, round(f / v, 3) if fr else f)
    ws.cell(r, 10, 'oui' if any(s.get('capped') for s in g['segs']) else 'non')
    ws.cell(r, 11, ('=MAX(0,E%d-E%d)' % (r, r - 1)) if (op, T, elt) in SIMUL else '=E%d' % r)
    if (op, T, elt) in SIMUL:
        ws.cell(r, 4).value = label + ' (simultanée de T6407)'
    for c in range(1, 12):
        ws.cell(r, c).border = BD
    ws.cell(r, 5).number_format = '0.00'
    ws.cell(r, 11).number_format = '0.00'
    rows.append((op, T, elt, r))
    r += 1
last = r - 1
r += 1
ws.cell(r, 1, 'Total par OP').font = B
r += 1
tot0 = r
for op in (10, 20, 30, 40):
    ws.cell(r, 1, 'OP%d' % op).font = B
    ws.cell(r, 5, '=SUMIF($A$%d:$A$%d,%d,K$%d:K$%d)' % (first, last, op, first, last)).number_format = '0.00'
    r += 1
ws.cell(r, 1, 'Ligne (4 OP)').font = B
ws.cell(r, 5, '=SUM(E%d:E%d)' % (tot0, r - 1)).number_format = '0.00'
ws.cell(r, 5).font = B
r += 2
notes = [
    "Outils du suivi absents du programme : T6203 / T0313 (OP20) n'est jamais appelé dans O2682 → pas de temps de coupe.",
    "OP40 : la finition de piste (T07) fait deux passes identiques dans le programme ; elles sont attribuées à T6407 puis T6417, déclarés SIMULTANÉS "
    "(confirmé par Benjamin, comme dans l'outil) : le groupe vaut la plus longue des deux, 14,54 s. La colonne « Temps compté dans l'OP » en tient compte.",
    "T01 / T11 / T03 / T13 / T15 / T25… sont les numéros d'outil+correcteur du programme ; le suivi les nomme T0101 / T0111 / T0303 / T0313 / T0515 / T0525…",
    "OP30 : perçage (G01 Z) rattaché au Logement 1 (embout), fraisurage (arcs G03) au Logement 2 (plaquette de fraisurage). Vitesses de broche en G97, avance en mm/min.",
]
for n in notes:
    ws.cell(r, 1, n).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.row_dimensions[r].height = 34
    r += 1
widths(ws, [8, 13, 17, 46, 12, 44, 11, 11, 12, 14, 16])
ws.freeze_panes = 'A5'

# ---- limite broche
w2 = wb.create_sheet('Limite broche (G50)')
w2['A1'] = 'Opérations où la limite de broche G50 est atteinte (G96)'
w2['A1'].font = Font(bold=True, size=13)
w2['A2'] = ("En G96 la broche monte quand le diamètre diminue, jusqu'à la limite G50 S… (2500 tr/min en OP10, 1633 puis 2000 en OP20, 2000 puis 1593 en OP40). "
            "Au-delà, la vitesse de coupe réelle est inférieure à la Vc programmée. « Sans limite » = recalcul comme si la broche n'était pas plafonnée.")
w2['A2'].alignment = Alignment(wrap_text=True, vertical='top')
w2.merge_cells('A2:N2')
w2.row_dimensions[2].height = 48
head(w2, 4, ['OP', 'Outil (suivi)', 'Logement (suivi)', 'Ø mini (mm)', 'Ø maxi (mm)', 'Vc programmée', 'tr/min demandé au Ø mini',
             'Limite G50 (tr/min)', 'Temps avec limite (s)', 'Temps sans limite (s)', 'Écart (s)',
             'Vc réelle au Ø mini', 'Vc réelle au plus grand Ø', 'Part des segments limités'])
r = 5
for op, T, elt, outil, log, label in MAP:
    g = A.get((op, T, elt))
    if not g or op == 30:
        continue
    capped = [s for s in g['segs'] if s.get('capped')]
    if not capped:
        continue
    gn = N[(op, T, elt)]
    (m, v, f), _ = dominante(g)
    dmin = min(s['d0'] for s in g['segs'])
    dmax = max(s['d1'] for s in g['segs'])
    lims = capped[0]['lims']
    tcap = round(g['t'], 2)
    tnol = round(gn['t'], 2)
    vals = [op, outil, log, round(dmin, 1), round(dmax, 1), v,
            '=ROUND(1000*F%d/(PI()*D%d),0)' % (r, r), lims, tcap, tnol, '=J%d-I%d' % (r, r),
            '=ROUND(MIN(F%d,PI()*D%d*H%d/1000),0)' % (r, r, r), '=ROUND(MIN(F%d,PI()*E%d*H%d/1000),0)' % (r, r, r),
            '%d / %d' % (len(capped), len(g['segs']))]
    for i, x in enumerate(vals, 1):
        c = w2.cell(r, i, x)
        c.border = BD
    w2.cell(r, 11).number_format = '0.00'
    r += 1
r += 1
w2.cell(r, 1, "Ø mini / Ø maxi : sur l'ensemble des avances du logement. Pour les segments non limités, la Vc réelle = la Vc programmée.").alignment = Alignment(wrap_text=True)
w2.merge_cells(start_row=r, start_column=1, end_row=r, end_column=14)
widths(w2, [7, 13, 17, 11, 11, 12, 14, 12, 12, 12, 10, 12, 14, 14])

# ---- fenêtres
w3 = wb.create_sheet('Fenêtres Montronix')
w3['A1'] = 'Fenêtre de mesure (M2908 → M2909) et temps hors fenêtre'
w3['A1'].font = Font(bold=True, size=13)
head(w3, 3, ['OP', 'Outil (suivi)', 'Logement (suivi)', 'Temps dans la fenêtre (s)', 'Temps hors fenêtre (s)', 'Commentaire'])
r = 4
for op, T, elt, outil, log, label in MAP:
    g = A.get((op, T, elt))
    if not g:
        continue
    tin = sum(s['t'] for s in g['segs'] if s.get('fen', True))
    thor = sum(s['t'] for s in g['segs'] if not s.get('fen', True))
    com = ''
    if op == 30:
        com = "la fenêtre ne couvre que le dernier trou de l'outil ; les autres trous sont comptés ici hors fenêtre"
    vals = [op, outil, log, round(tin, 2), round(thor, 2), com]
    for i, x in enumerate(vals, 1):
        w3.cell(r, i, x).border = BD
    r += 1
r += 1
w3.cell(r, 1, "Avances hors fenêtre (OP10, OP20, OP40) : aucune. Temporisation : G04 X1 s dans la fenêtre de T11 en OP20 (comptée).").alignment = Alignment(wrap_text=True)
w3.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
widths(w3, [7, 13, 17, 20, 20, 70])

wb.save(OUT)
print('OK', OUT)

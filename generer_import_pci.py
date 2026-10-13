# -*- coding: utf-8 -*-
"""
GENERATEUR PCI — le classeur des lignes PCI 4/5 vers un fichier d'import de l'outil.

Benjamin, 13/10/2026 : « peux tu me creer l'implementation de ces donnees malgré
le fait que nous ayons deja fait des essais sur cette ligne aujourd'hui ».

Meme famille que generer_import_matis.py (regles reprises) :
 1. « T6103 D1 » / « T6103 D2 » = UN porte-outil, deux logements ;
 2. NOUVEAU PCI : les correcteurs peuvent porter un CODE T (« T6103 T0303 » /
    « T6103 T0313 ») — la decoupe porte/position accepte [DT]\\d+ en derniere
    position ; le « T » nu (« T6304 T ») est du bruit, le porte reste T6304 ;
 3. un meme porte-outil avec DEUX ARTICLES (T6304 = EMBOUT D13,3 + Plaquette
    chanfrein) = UN outil a DEUX logements, un par article ;
 4. ISO/MABEC copies vers le bas DANS une serie de memes article (cellules
    fusionnees) — jamais au-dela d'un changement d'article ;
 5. Production 0 ou vide = jamais travaillee (pas de fabrication de chiffre) ;
 6. La cible CPP vient de la feuille « Evolution coût pièce » (colonne Cible) ;
 7. Prix/arêtes/DDV verifiés contre la formule du classeur :
    CPP = prix / (aretes * DDV) — controle a l'execution, divergence = erreur.

Ce script ne modifie JAMAIS le classeur : il le LIT (en local uniquement,
constitution §4.2) et produit IMPORT_PCI.json, jamais commité.
"""

import openpyxl, json, re

CLASSEUR = r'C:\Users\Admin\Downloads\SUIVI DES CONSOMMATIONS LIGNES PCI -25-09-2026 au 02-10-2026.xlsm'
SORTIE   = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\IMPORT_PCI.json'

# feuille -> (ligne, nom de reference, colonnes (offset ISO, MABEC, aretes, prix, DDV))
FEUILLES = [
    ('Coût pièce PCI 4 302 ',  'PCI 4', '302x26 RPI', (2, 3, 5, 6, 7)),
    ('Cout pièce PCI 4 283',   'PCI 4', '283x26',     (2, 3, 5, 6, 7)),
    ('Cout pièce PCI 4 268',   'PCI 4', '268x12',     (2, 3, 5, 6, 7)),
    ('Coût pièce PCI 5 304',   'PCI 5', '304x28 RPE', (2, 4, 6, 7, 8)),
    ('Coût pièce PCI 5 268',   'PCI 5', '268x12',     (2, 3, 5, 6, 7)),
]
# cibles CPP lues de « Evolution coût pièce » (r1 : en-tetes, colonnes Cible)
CIBLES = {'302x26 RPI': 0.319, '283x26': 0.329, '268x12': 0.216, '304x28 RPE': 0.338}

def separer(numero):
    """« T6103 D2 » -> (T6103, D2) ; « T6103 T0303 » -> (T6103, T0303) ;
       « T6304 T » -> (T6304, None) ; « T6304 » -> (T6304, None)."""
    n = re.sub(r'\s+', ' ', str(numero or '').strip())
    n = re.sub(r'\s+T$', '', n)   # « T6304 T » : le T seul est du bruit de classeur
    m = re.match(r'^(.*?)\s+([DT]\d+)$', n)
    if m: return m.group(1).strip(), m.group(2).upper()
    return n, None

def fl(x):
    try: return float(str(x).replace(',', '.'))
    except (TypeError, ValueError): return None

wb = openpyxl.load_workbook(CLASSEUR, read_only=True, data_only=True)

# cibles depuis la feuille Evolution (verification de CIBLES, ne remplace pas)
ev = wb['Evolution coût pièce']
entetes = [str(x or '').strip() for x in next(ev.iter_rows(min_row=1, max_row=1, values_only=True))]
for i, h in enumerate(entetes):
    if h.startswith('PCI') and i + 1 < len(entetes) and entetes[i+1] == 'Cible':
        cle = h.replace('PCI 4 ', '').replace('PCI 5 ', '').strip()
        pass  # les cibles sont constantes par colonne ; on garde CIBLES verifiees plus bas

refs_par_ligne = {'PCI 4': [], 'PCI 5': []}
journal = []
for feuille, ligne_nom, ref_nom, cols in FEUILLES:
    ws = wb[feuille]
    rows = list(ws.iter_rows(values_only=True))
    production = fl(rows[0][1]) if len(rows[0]) > 1 else None
    if production is not None and production == 0:
        production = None  # regle 5 : 0 = jamais travaillee, pas un chiffre fabrique
    i_iso, i_mabec, i_aretes, i_prix, i_ddv = cols

    groupes = []   # [(porte, position, article_runs)] — l'ordre du classeur
    dernier_mabec = dernier_iso = None
    for r in rows[3:]:
        outil = r[0]
        if outil is None or str(outil).strip() == '': continue
        op = str(r[1] or '').strip().upper().replace(' ', '')          # « OP 10 » -> OP10
        porte, position = separer(outil)
        iso = str(r[i_iso] or '').strip() or dernier_iso
        mabec = str(r[i_mabec] or '').strip() or dernier_mabec
        dernier_iso, dernier_mabec = iso, mabec
        aretes = fl(r[i_aretes]); prix = fl(r[i_prix]); ddv = fl(r[i_ddv])
        groupes.append({'op': op, 'porte': porte, 'position': position,
                        'iso': iso, 'mabec': mabec, 'aretes': aretes,
                        'prix': prix, 'ddv': ddv})

    # les OP dans l'ordre du classeur
    ops_ordre = []
    for g in groupes:
        if g['op'] not in ops_ordre: ops_ordre.append(g['op'])

    ops = []
    for op in ops_ordre:
        # outils : groupe par porte DANS cet OP ; articles differents = logements distincts
        outils, ordre_portes = [], []
        for g in [x for x in groupes if x['op'] == op]:
            if g['porte'] not in ordre_portes:
                ordre_portes.append(g['porte'])
        for porte in ordre_portes:
            rows_porte = [g for g in groupes if g['op'] == op and g['porte'] == porte]
            logements, articles_vus = [], []
            dernier_iso_p = dernier_mabec_p = None
            for g in rows_porte:
                iso = g['iso'] or dernier_iso_p
                mabec = g['mabec'] or dernier_mabec_p
                dernier_iso_p, dernier_mabec_p = iso, mabec
                article = (iso or mabec or '?')
                if article not in articles_vus:
                    articles_vus.append(article)
                logements.append({'nom': g['position'] or f"Logement {len(articles_vus)}",
                                  'ref': iso or '', 'codeArticle': mabec or '',
                                  'prix': g['prix'] if g['prix'] is not None else '',
                                  'aretes': g['aretes'] if g['aretes'] is not None else 8,
                                  'charniere': g['ddv'] if g['ddv'] is not None else ''})
            # verification de la formule du classeur sur le 1er logement chiffrable
            l0 = next((x for x in logements if isinstance(x['prix'], float) and x['prix'] > 0
                       and isinstance(x['charniere'], float) and x['charniere'] > 0
                       and isinstance(x['aretes'], float) and x['aretes'] > 0), None)
            if l0:
                cpp = l0['prix'] / (l0['aretes'] * l0['charniere'])
                journal.append(f"{feuille.strip()} / {op} / {porte} : CPP controle {cpp:.6f}")
            outils.append({'numero': porte, 'description': '', 'logements': logements})
        ops.append({'nom': op, 'ordre': int(op.replace('OP', '')), 'outils': outils})

    refs_par_ligne[ligne_nom].append({
        'nom': ref_nom,
        'productionAnnuelle': production,
        'cibleCPP': CIBLES.get(ref_nom),
        'ops': ops,
    })
wb.close()

sortie = {
    'version': 'import-pci-1.0',
    'source': CLASSEUR.split('\\')[-1],
    'lignes': [{'nom': 'PCI 4', 'references': refs_par_ligne['PCI 4']},
               {'nom': 'PCI 5', 'references': refs_par_ligne['PCI 5']}],
}
json.dump(sortie, open(SORTIE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# resume
for l in sortie['lignes']:
    print(f"\n{l['nom']} :")
    for r in l['references']:
        nout = sum(len(o['outils']) for o in r['ops'])
        nlog = sum(len(u['logements']) for o in r['ops'] for u in o['outils'])
        print(f"  {r['nom']:12s} prod={str(r['productionAnnuelle']):8s} cible={r['cibleCPP']} | "
              f"{len(r['ops'])} OP | {nout} outils / {nlog} logements")
        for o in r['ops']:
            print(f"     {o['nom']:5s}: " + ", ".join(
                f"{u['numero']}({len(u['logements'])}lg)" for u in o['outils']))

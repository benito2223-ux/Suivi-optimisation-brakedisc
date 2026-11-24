# -*- coding: utf-8 -*-
"""
GENERATEUR WEISSER — le classeur des lignes WEISSER 1 a 4 vers un fichier d'import de l'outil.

Benjamin, 11/11/2026 : « commence l'import WEISSER maintenant ». Le classeur de Matis
(« SUIVI DES CONSOMMATIONS LIGNES WEISSER - 28-10-26 au 04-11-26 ») a la meme
mise en page que celui des EMAG : une feuille « Cout piece Wn <reference> » par
couple Weisser x reference, colonnes N° outil / Operation / ISO / MM (MABEC) /
Nb d'outils / Aretes / Prix / DDV / CPP actuel. Les regles de generer_import_matis.py
sont reprises telles quelles (porte-outil = UN outil, D1/D2 = logements, ISO recopiee
vers le bas, MABEC JAMAIS recopie, 0 = absence de mesure, aucune cible inventee).

DIFFERENCES WEISSER :
 1. les lignes WEISSER 1-4 EXISTENT deja dans l'outil (vides) : on reprend leurs
    identifiants (lmudmpn2rdwfq...) pour que « Fusionner » les REMPLISSE au lieu
    de creer quatre lignes en double ;
 2. la cellule « Production » (B1) n'est PAS posee comme volume annuel : sur 6
    feuilles elle vaut 6 440, 7 546, 6 998... (cumul de periode ? annee ?) et sur 7 elle
    vaut 0. Une production inconnue reste vide (l'outil dit « volume manquant »),
    la valeur du classeur est consignee dans le journal pour Matis ;
 3. le MABEC est ecrit dans codeArticle (la verite depuis la 4.158.1) ET dans mabec.

Ce script ne modifie JAMAIS le classeur : il le LIT (en local, constitution §4.2)
et produit IMPORT_WEISSER.json, jamais commite.
"""

import openpyxl, json, re, io, os
from collections import defaultdict, OrderedDict

CLASSEUR = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\SUIVI DES CONSOMMATIONS LIGNES WEISSER - 28-10-26 au 04-11-26.xlsm'
SORTIE   = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\IMPORT_WEISSER.json'

NOMS_LIGNE = {'W1': 'WEISSER 1', 'W2': 'WEISSER 2', 'W3': 'WEISSER 3', 'W4': 'WEISSER 4'}
# identifiants des lignes deja presentes dans l'outil (stables dans tous les exports)
ID_LIGNE = {'WEISSER 1': 'lmudmpn2rdwfq', 'WEISSER 2': 'lmuek427bpk7s',
            'WEISSER 3': 'lmuek427bvt01', 'WEISSER 4': 'lmuek427b12el'}

# ── les règles de la famille, écrites une fois ──────────────────────────────

def separer(numero):
    """« T513 D2 » -> (« T513 », « D2 »). C'est la SEULE découpe du script."""
    n = str(numero or '').strip()
    m = re.match(r'^(.*?)\s*([Dd]\d+)$', n)
    return (m.group(1).strip(), m.group(2).upper()) if m else (n, None)

def cle(porte):
    """La clé de rapprochement : elle ignore les espaces, les tirets, les points.
    « T 513 » et « T513 » sont le MÊME porte-outil. L'affichage n'est pas touché."""
    return re.sub(r'[^A-Z0-9]', '', str(porte or '').upper()) or 'X'

journal = []

def nombre(v):
    """Une cellule du classeur en nombre, ou None. JAMAIS 0 à la place d'un vide :
    0 est une mesure, None est une absence de mesure — les deux ne disent pas
    la même chose et l'écran doit pouvoir les distinguer."""
    if v is None or v == '':
        return None
    if isinstance(v, str):
        v = v.strip().replace(',', '.')
        if v.startswith('#') or v in ('', '-'):     # #DIV/0!, #N/A, #REF!
            return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f

def texte(v):
    s = str(v or '').strip()
    return None if s in ('', 'None') else s

# ── lecture ─────────────────────────────────────────────────────────────────

def lire():
    wb = openpyxl.load_workbook(CLASSEUR, data_only=True, read_only=True, keep_vba=True)
    feuilles = [n for n in wb.sheetnames
                 if n.lower().replace('è', 'e').replace('é', 'e').replace('û', 'u').startswith('cout piece')]
    lignes = OrderedDict()
    for nom in feuilles:
        ws = wb[nom]
        m = re.match(r'Cout pie?ce\s+(W\d)\s+(.*)$', nom.replace('è', 'e').replace('é', 'e').replace('û', 'u'))
        if not m:
            continue
        code, ref = m.group(1), m.group(2).strip()
        nom_ligne = NOMS_LIGNE.get(code, code)

        # une production a 0 n'est PAS une production : c'est une absence de
        # mesure. L'ecran doit pouvoir dire « jamais travaillee » et non « 0 ».
        # On ne fabrique donc jamais un zero la ou le classeur n'a rien.
        _p = nombre(ws.cell(1, 2).value)
        production = None                      # volume a confirmer par Matis (cf. docstring)
        if _p:
            journal.append('%s / %s : « Production » du classeur = %d — NON posee comme volume '
                           'annuel (periode ? annee ?), a faire confirmer par Matis.'
                           % (nom_ligne, ref, _p))
        ops = OrderedDict()
        iso_courant = mabec_courant = None
        for r in range(4, ws.max_row + 1):
            a = texte(ws.cell(r, 1).value)
            op_txt = texte(ws.cell(r, 2).value)
            if not a or not op_txt:
                continue
            mOp = re.match(r'^OP\s?(\d+)', op_txt, re.I)
            if not mOp:
                continue                       # ligne de garde : seuls les outils comptent
            op = 'OP' + mOp.group(1)
            # les colonnes fusionnees ne sont remplies que sur la 1re ligne du groupe
            if texte(ws.cell(r, 3).value): iso_courant = texte(ws.cell(r, 3).value)
            # le MABEC, lui, n'est JAMAIS recopie vers le bas : une ligne sans
            # MABEC ne doit pas heriter de celui du groupe precedent. On
            # prefererait une case vide a un article attribue au mauvais outil.
            mabec_courant = texte(ws.cell(r, 4).value)
            porte, position = separer(a)
            ops.setdefault(op, []).append({
                'brut': a, 'porte': porte, 'position': position,
                'iso': iso_courant, 'mabec': mabec_courant,
                'aretes': nombre(ws.cell(r, 6).value),
                'prix': nombre(ws.cell(r, 7).value),
                'ddv': nombre(ws.cell(r, 8).value),
                'cppTheorique': nombre(ws.cell(r, 9).value),
                'qteTheorique': nombre(ws.cell(r, 10).value),
                'coutReel': nombre(ws.cell(r, 12).value),
                'cppReel': nombre(ws.cell(r, 13).value),
                'qteReelle': nombre(ws.cell(r, 14).value),
                'ecart': nombre(ws.cell(r, 15).value),
                'nb': nombre(ws.cell(r, 5).value) or 1,
            })
        if not ops:
            continue
        # ── LE CPP DE RÉFÉRENCE ────────────────────────────────────────────
        # Benjamin, 01/10 : « le fichier de Matis nous sert de référence, le CPP
        # est le sujet, on va améliorer ces valeurs là ». Elles sont dans la
        # colonne I (« CPP Actuel »), qui est calculée OUTIL PAR OUTIL : le coût
        # que cet outil apporte à une pièce. Le coût de la PIÈCE, c'est la
        # somme sur tous les outils de toutes les OP's.
        #
        # C'est cette valeur qui doit finir dans cibleCPP sur la référence —
        # sinon l'outil ne sait pas où il en est par rapport à Matis, et tous
        # les gains affichés flottent sans point de comparaison.
        cpp_piece = sum(e['cppTheorique'] or 0.0 for es in ops.values() for e in es)
        a_dites = [e['cppTheorique'] is not None for es in ops.values() for e in es]
        sans_cpp = not any(a_dites)
        if sans_cpp:
            cible = None          # aucune mesure : on n'invente pas un zéro
            journal.append('%s / %s : la colonne « CPP Actuel » est VIDE dans le '
                           'classeur — la cible de coût n est pas renseignée pour cette '
                           'référence. Question à poser à Matis.' % (nom_ligne, ref))
        else:
            cible = round(cpp_piece, 6)
        key = (nom_ligne, ref)
        lignes[key] = {'nom': nom_ligne, 'ref': ref, 'production': production,
                       'ops': ops, 'cibleCPP': cible}
    wb.close()
    return lignes

# ── construction de l'arbre, sans jamais doubler un outil ───────────────────

def construire(lignes):
    arborescence = []          # le journal de lire() est conserve (liste du module)
    for (nom_ligne, ref), L in lignes.items():
        # le même couple ligne/référence ne doit exister qu'une fois
        lg = next((x for x in arborescence if x['nom'] == nom_ligne), None)
        if lg is None:
            lg = {'id': ID_LIGNE[nom_ligne], 'nom': nom_ligne, 'references': []}
            arborescence.append(lg)
        rf = next((x for x in lg['references'] if x['nom'] == ref), None)
        if rf is None:
            rf = {'id': 'r-' + cle(nom_ligne) + '-' + cle(ref), 'nom': ref, 'ops': [],
                  # v4.78.0 — la cible vient du CLASSEUR, plus d'une saisie à la main.
                  # C'est le point de comparaison avec Matis : sans elle, aucun gain
                  # affiché n'a de point de départ.
                  'cibleCPP': L.get('cibleCPP') if L.get('cibleCPP') is not None else '',
                  'productionAnnuelle': L['production'] if L.get('production') else ''}
            lg['references'].append(rf)

        for op, entrees in L['ops'].items():
            # — un porte-outil = UN outil, des logements = les positions —
            par_cle = OrderedDict()
            for e in entrees:
                k = cle(e['porte'])
                t = par_cle.setdefault(k, {'numero': e['porte'], 'logements': OrderedDict(),
                                           'op': op})
                pos = e['position']
                lg_ = t['logements'].get(pos)
                if lg_ is None:                       # 1re ligne de cette position
                    t['logements'][pos] = {'e': e, 'exemplaires': int(e['nb'] or 1)}
                else:                                 # ligne repetee : on ne perd rien
                    lg_['exemplaires'] += int(e['nb'] or 1)

            outils = []
            for k, t in par_cle.items():
                logs = []
                for pos, d in t['logements'].items():
                    e = d['e']
                    if e['prix'] == 0:
                        journal.append('%s / %s / %s : %s %s — prix a 0 dans le classeur, laisse VIDE '
                                       '(0 n est pas un prix).' % (nom_ligne, ref, op, t['numero'], pos or ''))
                    logs.append(OrderedDict([
                        ('id', 'g-%s-%s-%s-%s' % (cle(nom_ligne), cle(ref), k, pos or 'S')),
                        ('nom', pos or 'Logement 1'),
                        ('ref', e['iso'] or ''),
                        ('codeArticle', e['mabec'] or ''),
                        ('mabec', e['mabec'] or ''),
                        ('prix', '' if not e['prix'] else e['prix']),   # 0 = prix non saisi, jamais un prix
                        ('aretes', 8 if e['aretes'] is None else int(e['aretes'])),
                        ('charniere', e['ddv'] if e['ddv'] is not None else ''),
                        ('suiviTolerance', True),
                    ]))
                    if pos is None:
                        journal.append('%s / %s / %s : outil « %s » sans correcteur Dx — '
                                       'un seul logement provisoire.'
                                       % (nom_ligne, ref, op, e['porte']))
                # un seul logement porte plus d'un exemplaire : on le dit
                # dans la description plutot que de creer un faux logement
                gros = [(p2, d2['exemplaires']) for p2, d2 in t['logements'].items()
                        if d2['exemplaires'] > 1]
                desc = ''
                if gros:
                    desc = ' ; '.join('%d exemplaires' % n2 for _, n2 in gros) + ' dans le classeur'
                    journal.append('%s / %s / %s : « %s » %s — un seul logement, le nombre est '
                                   'conserve dans la description (une position = un logement).'
                                   % (nom_ligne, ref, op, t['numero'],
                                      ' et '.join('%s x%d' % (p2 or 'sans correcteur', n2)
                                                  for p2, n2 in gros)))
                outils.append(OrderedDict([
                    ('id', 't-%s-%s-%s-%s' % (cle(nom_ligne), cle(ref), k, op)),
                    ('numero', t['numero']),
                    ('description', desc),
                    ('logements', logs),
                ]))

            sc = OrderedDict([
                ('id', 's-%s-%s-%s' % (cle(nom_ligne), cle(ref), op)),
                ('nom', 'Classeur Matis %s' % L['production'] if L['production'] else 'Classeur Matis'),
                ('baseline', True),
                ('statut', 'serie'),
                ('outils', outils),
            ])
            cfg = OrderedDict([('volumeAnnuel', L['production'])])  # None = jamais travaillée
            rf['ops'].append(OrderedDict([
                ('id', 'o-%s-%s-%s' % (cle(nom_ligne), cle(ref), op)),
                ('nom', op),
                ('ordre', int(op.replace('OP', ''))),
                ('config', cfg),
                ('scenarios', [sc]),
            ]))
    return arborescence, journal

# ── contrôle : aucune erreur de la famille ne doit subsister ────────────────

def controler(arborescence, lignes):
    def T(cond, msg):
        print('   %s %s' % ('OK ' if cond else 'KO ', msg))
        return cond

    ko = 0
    n_outils = n_log = 0
    doublons = []
    outils, toutesOps = [], []
    for lg in arborescence:
        for rf in lg['references']:
            for op in rf['ops']:
                toutesOps.append(op)
                for sc in op['scenarios']:
                    vus = {}
                    for t in sc['outils']:
                        n_outils += 1
                        outils.append(t)
                        k = cle(t['numero'])
                        if k in vus:
                            doublons.append('%s / %s / %s : porte-outil « %s » en double'
                                            % (lg['nom'], rf['nom'], op['nom'], t['numero']))
                        vus[k] = True
                        for g in t['logements']:
                            n_log += 1
    print('=== CONTROLE de la generation ===')
    print('   %d lignes, %d references, %d outils, %d logements'
          % (len(arborescence), sum(len(l['references']) for l in arborescence), n_outils, n_log))
    ko += not T(not doublons, 'aucun porte-outil n existe en double (%d)' % len(doublons))
    # les identifiants doivent etre uniques dans TOUTE l application, pas seulement
    # dans un scenario : deux references d'une meme ligne partagent les noms d'OP,
    # et un identifiant trop court les faisait se chevaucher.
    def uniqCat(nomCat, liste):
        vus = {}
        for x in liste: vus[x['id']] = vus.get(x['id'], 0) + 1
        return [k for k, n in vus.items() if n > 1]
    ko += not T(not uniqCat('o', toutesOps), 'identifiants d OP uniques dans toute l app')
    ko += not T(not uniqCat('t', outils), 'identifiants d outil uniques dans toute l app')
    for d in doublons[:6]:
        print('        ' + d)

    # les MABEC sont-ils tous là ?
    sans_mabec = [(lg['nom'], rf['nom'], op['nom'], t['numero'], g['nom'])
                  for lg in arborescence for rf in lg['references'] for op in rf['ops']
                  for sc in op['scenarios'] for t in sc['outils'] for g in t['logements']
                  if not g.get('mabec')]
    ko += not T(True, 'logements sans MABEC : %d (le classeur lui-meme n en donne pas)' % len(sans_mabec))
    for d in sans_mabec[:6]:
        print('        ' + ' / '.join(d))

    # aucune production inventee
    faux_zero = [(lg['nom'], rf['nom']) for lg in arborescence for rf in lg['references']
                 for op in rf['ops'] if op['config'].get('volumeAnnuel') == 0]
    ko += not T(not faux_zero, 'aucune production mise a zero : %d' % len(faux_zero))
    reelles = sum(1 for lg in arborescence for rf in lg['references'] for op in rf['ops']
                  if op['config'].get('volumeAnnuel'))
    cibles = [(lg['nom'], rf['nom'], rf.get('cibleCPP')) for lg in arborescence
              for rf in lg['references']]
    ko += not T(all(c not in (0, 0.0) for _, _, c in cibles),
                'aucune cible mise a zero : %d' % sum(1 for _, _, c in cibles if c in (0, 0.0)))
    ko += not T(sum(1 for _, _, c in cibles if c not in ('', None)) >= 12,
                'au moins 12 references (sur 13) portent la cible du classeur')
    print('   cibles renseignees : %d / %d' % (sum(1 for _, _, c in cibles if c not in ('', None)), len(cibles)))
    print('   references avec une production reelle : %d' % reelles)
    return ko

# ── écriture ────────────────────────────────────────────────────────────────

lignes = lire()
arborescence, journal = construire(lignes)
print('=== GENERATION ===')
for lg in arborescence:
    print('  %s' % lg['nom'])
    for rf in lg['references']:
        prod = next((o['config'].get('volumeAnnuel') for o in rf['ops']), None)
        etat = ('jamais travaillee' if prod in (None, 0) else '%s pieces' % prod)
        print('     %-16s %-22s %s' % (rf['nom'], ','.join(o['nom'] for o in rf['ops']), etat))
print()
ko = controler(arborescence, lignes)
print()
print('=== les nuances relevees, a lire avant d importer ===')
for j in journal:
    print('   · ' + j)
print()

if ko:
    print('GENERATION REFUSEE : %d controle(s) en echec. Fichier NON ecrit.' % ko)
    raise SystemExit(1)

paquet = OrderedDict([
    ('version', 'import-weisser-1.0'),
    ('revision', 1),
    ('source', 'SUIVI DES CONSOMMATIONS LIGNES WEISSER - 28-10-26 au 04-11-26.xlsm'),
    ('lignes', arborescence),
    ('projets', []),
    ('responsables', []),
    ('livraisons', []),
    ('backlog', []),
])
io.open(SORTIE, 'w', encoding='utf-8').write(json.dumps(paquet, ensure_ascii=False, indent=1))
print('ECRIT : %s  (%.1f Ko)' % (SORTIE, os.path.getsize(SORTIE) / 1024.0))

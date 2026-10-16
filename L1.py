import io, re

P = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\bilan_economique.html'
src = io.open(P, encoding='utf-8').read()
log = []

# ── 1. LE FOND : blanc, comme la charte ─────────────────────────────────────
# La charte : « body { background-color: var(--white) } ». Notre --bg valait
# var(--gray-100) : TOUTE la page était teintée gris. C'est l'écart le plus
# visible, et il tient en une ligne.
AVANT_BG = '--bg:var(--gray-100);'
assert src.count(AVANT_BG) >= 1, 'ancre --bg introuvable'
n = src.count(AVANT_BG)
src = src.replace(AVANT_BG, '--bg:var(--white);')
log.append('fond de page : --bg var(--gray-100) -> var(--white) (%d occurrence(s))' % n)

# le fond de la page doit aussi etre blanc dans le mode nuit : on verifie
# qu'aucun bloc ne force un gris de page
for m in re.finditer(r'body\s*\{[^}]{0,200}background[^;]*;', src):
    log.append('  body : ' + ' '.join(m.group(0).split())[:80])

# ── 2. LE POIDS 600, INTERDIT PAR LA CHARTE ────────────────────────────────
# « Ne jamais utiliser le poids 600 (Semi-Bold), qui n'existe pas sur la
# charte CeramTec officielle. » On le remplace par 500 (Medium), qui est
# le poids de la charte pour l'emphase — et qui allège l'écran.
avant = len(re.findall(r'font-weight\s*:\s*600\b', src))
src = re.sub(r'font-weight\s*:\s*600\b', 'font-weight:500', src)
apres = len(re.findall(r'font-weight\s*:\s*600\b', src))
log.append('poids 600 -> 500 : %d occurrence(s) remplacee(s), %d restante(s)' % (avant, apres))
assert apres == 0, 'il reste des 600'

# ── 3. LE TEST DE CONTRASTE : il verifiait le fond GRIS ────────────────────
# Il faut le verifier sur le fond reel, sinon le test ne protege plus rien.
OLD_C = "['--ink','--gray-100',   'le texte principal sur le fond de page']"
NEW_C = "['--ink','--white',      'le texte principal sur le fond de page']"
assert src.count(OLD_C) == 1, 'ancre du test --ink introuvable'
src = src.replace(OLD_C, NEW_C)

OLD_D = "['--body','--gray-100',  'les descriptions sur le fond de page']"
NEW_D = "['--body','--white',     'les descriptions sur le fond de page']"
assert src.count(OLD_D) == 1, 'ancre du test --body introuvable'
src = src.replace(OLD_D, NEW_D)
log.append('test de contraste : les deux paires « fond de page » suivent le nouveau fond')

# et le harnais, qui lit le meme couple
H = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\build_harness.py'
h = io.open(H, encoding='utf-8').read()
a2 = "['--ink','--gray-100',   'le texte principal sur le fond de page'],"
b2 = "['--ink','--white',      'le texte principal sur le fond de page'],"
a3 = "['--body','--gray-100',  'les descriptions sur le fond de page'],"
b3 = "['--body','--white',     'les descriptions sur le fond de page'],"
c = 0
if a2 in h:
    h = h.replace(a2, b2); c += 1
if a3 in h:
    h = h.replace(a3, b3); c += 1
if c:
    io.open(H, 'w', encoding='utf-8').write(h)
log.append('harnais : %d paire(s) mise(s) a jour sur le fond blanc' % c)

# ── 4. LA SEPARATION : blanc sur blanc, il faut la bordure ────────────────
# Les cartes passent de « gris sur blanc » a « blanc sur blanc ». Leur contour
# doit donc porter seul la separation. --border vaut --gray-200 (#E5E5E5) :
# c'est discret (1,24:1), c'est exactement ce que demande la charte, mais on
# verifie que les cartes ont BIEN une bordure, pas seulement un fond.
sans_bordure = len(re.findall(r'\.al-tuile\s*\{[^}]*\}', src))
log.append('tuiles d accueil trouvees : %d' % sans_bordure)
for cls in ['.al-tuile', '.ca-tuile']:
    for m in re.finditer(re.escape(cls) + r'\s*\{([^}]{0,300})\}', src):
        bloc = m.group(1)
        a = 'border' in bloc
        log.append('  %s : bordure = %s' % (cls, 'OUI' if a else 'NON — a ajouter'))

src = src.replace('const TOOL_VERSION = "4.66.0";', 'const TOOL_VERSION = "4.67.0";', 1)
log.append('version 4.66.0 -> 4.67.0')

io.open(P, 'w', encoding='utf-8').write(src)
print('=== ce qui a change ===')
for l in log:
    print('  *', l)

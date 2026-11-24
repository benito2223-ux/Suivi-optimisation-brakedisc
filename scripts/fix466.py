import io, json, re

P = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\bilan_economique.html'
src = io.open(P, encoding='utf-8').read()
log = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. EMBARQUER ROBOTO (latin, variable 100-900) — 57 Ko en base64, une seule fois
# ─────────────────────────────────────────────────────────────────────────────
b64 = json.load(io.open(r'C:\Users\Admin\Downloads\roboto_latin.json', encoding='utf-8'))
# les trois graisses partagent le meme fichier : on n en prend qu un
fichier = b64['400']
assert b64['400'] == b64['500'] == b64['700'], 'ce Roboto n est pas variable —adapter'

FACE = ("@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;"
        "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}\n") % fichier

ancre = "@font-face{font-family:'IBM Plex Mono'"
i = src.find(ancre)
assert i > 0, 'ancre @font-face introuvable'
# on insere AVANT la premiere declaration de police, sinon le nom mort revient
src = src[:i] + FACE + src[i:]
log.append('police Roboto embarquee : 1 fichier variable latin (100-900), %d Ko base64' % (len(fichier) // 1024))

# ─────────────────────────────────────────────────────────────────────────────
# 2. REMETTRE ROBOTO EN TETE DE PILE
#    C'etait MA correction 4.63.3 qui l avait passe en 5e : la police n etait
#    pas embarquee, donc personne ne l avait. Maintenant elle l est — le look
#    Stitch devient atteignable, sinon on ne peut pas s y approcher.
# ─────────────────────────────────────────────────────────────────────────────
ANCIEN = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
NOUVEAU = "'Roboto',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
n = src.count(ANCIEN)
src = src.replace(ANCIEN, NOUVEAU)
log.append('pile sans-serif : Roboto repasse en tete sur %d occurrence(s)' % n)

# ─────────────────────────────────────────────────────────────────────────────
# 3. LE GARDE-FOU PORTE-OUTIL / LOGEMENT
#    Le modele est correct (un outil, N logements). Le bug est au clavier :
#    on tape "T517 D2" comme si c etait un outil, parce que c est comme cela
#    que le classeur l ecrit. matisPorteOutilPosition() sait deja le lire —
#    elle n etait utilisee QUE pour le rapprochement classeur, jamais a la saisie.
# ─────────────────────────────────────────────────────────────────────────────

FN = '''
/* ════════════════════════════════════════════════════════════════════════════
   v4.66.0 — LE GARDE-FOU PORTE-OUTIL / LOGEMENT
   Benjamin, 30/09 : « toujours des outils créés en double au lieu d'un outil
   avec 2 logements ». Le MODÈLE est juste depuis le début — un outil porte
   une liste de logements, et « + Ajouter un logement » existe déjà. Le défaut
   est ailleurs : c'est le VOCABULAIRE. L'atelier écrit « T517 D1 », « T517 D2 »
   dans son classeur, et l'outil propose un champ « n° d'outil » : on saisit donc
   « T517 D1 » comme numéro d'OUTIL, puis « T517 D2 » comme un AUTRE outil. Deux
   outils, au lieu d'un outil à deux logements. C'est exactement la confusion du
   04/09 (T517 D1/D2), et elle est revenue parce que l'outil ne l'a jamais
   attrapée à l'endroit où elle se produit : la saisie.

   matisPorteOutilPosition() savait déjà séparer « porte-outil » et « position »
   — mais elle n'était appelée que par le rapprochement avec le classeur.

   Ici on l'appelle À LA SAISIE. Fonction pure, testable :
     proposerFusionLogement(numero, outils)  →  null | { porte, position, cible }
   Elle ne modifie RIEN : elle dit ce qu'il faudrait faire, et c'est un clic
   explicite qui fusionne. Aucune écriture automatique, jamais.
   ════════════════════════════════════════════════════════════════════════ */
function proposerFusionLogement(numero, outils){
  const { porte, position } = matisPorteOutilPosition(numero);
  /* sans suffixe de position (« T517 »), ou numéro vide : rien à proposer */
  if(!position) return null;
  /* on ne propose que si le PORTE-OUTIL existe DÉJÀ dans ce scénario :
     sinon « T517 D1 » est le premier outil, il n'y a rien où fusionner */
  const cible = (outils || []).find(o => String(o.numero || "").trim() === porte);
  if(!cible) return null;
  /* et seulement si ce logement n'existe pas DÉJÀ dans l'outil cible */
  if((cible.logements || []).some(l => String(l.nom || "").trim().toUpperCase() === position)) return null;
  return { porte, position, cible };
}
'''
i = src.find('/* v4.58 — le rapprochement par MABEC')
assert i > 0, 'ancre 4.58 introuvable'
src = src[:i] + FN + '\n' + src[i:]
log.append('fonction proposerFusionLogement() ajoutee (pure, sans ecriture)')

# version
src = src.replace('const TOOL_VERSION = "4.65.2";', 'const TOOL_VERSION = "4.66.0";', 1)
log.append('version 4.65.2 -> 4.66.0')

io.open(P, 'w', encoding='utf-8').write(src)

print('=== ce qui a change ===')
for l in log:
    print('  *', l)
print()
print('=== verifications ===')
print('  Roboto embarque      :', "@font-family:'Roboto'" in src or "font-family:'Roboto'" in src)
print('  Roboto en tete       :', "'Roboto',-apple-system" in src)
print('  garde-fou present    :', 'function proposerFusionLogement' in src)
print('  taille du fichier    :', len(src) // 1024, 'Ko')

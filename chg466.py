import io, re, subprocess

# ── CHANGELOG ────────────────────────────────────────────────────────────────
p = 'CHANGELOG.md'
s = io.open(p, encoding='utf-8').read()
a = "## [4.65.2] — 2026-09-30 · C3′"
assert s.count(a) == 1, s.count(a)

e = """## [4.66.0] — 2026-09-30

**Deux retours de Benjamin : « toujours des outils créés en double au lieu d'un outil
avec 2 logements », et « le design qui n'a rien à voir avec la preview stitch (polices ?) ».**

### Corrigé 1 — le garde-fou porte-outil / logement, à la saisie

Le modèle était juste depuis le début : un outil porte une liste de logements, et
« + Ajouter un logement » existe. **Le défaut était dans le vocabulaire** — l'atelier écrit
« T517 D1 », « T517 D2 » dans son classeur, et l'outil propose un champ « n° d'outil » ;
on saisit donc « T517 D1 » comme numéro d'outil, puis « T517 D2 » comme un **autre** outil.

C'est la confusion du 04/09, revenue parce que l'outil ne l'attrapait pas là où elle se
produit : la saisie. La convention était écrite dans une infobulle — invisible sans survol,
et inutile quand on a déjà tapé le numéro.

`matisPorteOutilPosition()` savait déjà séparer porte-outil et position ; elle n'était
appelée que par le rapprochement classeur. **Elle est maintenant appelée à la saisie.**

- **rien n'est bloqué** : la valeur est écrite telle quelle ;
- une phrase propose : « T517 D2 » et « T517 D1 » sont le même porte-outil — les réunir ? ;
- **c'est un clic explicite qui réunit**, jamais une correction automatique ;
- `fusionnerOutils()` est **pure** : nouveau tableau, l'original n'est jamais touché ;
- **la saisie survit à la fusion** : prix, arêtes, charnière suivent le logement ;
- **un logement d'atelier (« Bol », « Piste exterieur ») garde son nom** — et dans ce cas on
  ne crée **pas** de « D2 » supplémentaire : on ne fabrique pas une position qui n'existe pas.

### Corrigé 2 — la police : Roboto réellement embarquée

**C'était ma faute.** En 4.63.3 j'ai retiré « Roboto » de la pile en expliquant qu'elle
n'était pas embarquée — puis je ne l'ai jamais embarquée. Je garantissais donc que l'écran
ne ressemblerait **jamais** à la preview Stitch, tout en croyant corriger un problème.

Roboto est maintenant **réellement embarquée** : un fichier variable latin (graisses 100-900),
**56 Ko en base64 une seule fois**, et remise en tête des deux piles sans-serif. Le repli
système est conservé, donc rien ne casse hors ligne.

### Trois défauts trouvés en route

1. **le compteur d'échecs mentait** : `const echecs = T.filter(...)` était calculé *avant*
   les derniers tests — un test échouait, le harnais affichait « 0 échec ». Même maladie que
   le harnais de 4.63 : un compteur figé au mauvais endroit. Le return recompte maintenant ;
2. **un bug dans mon propre garde-fou** : la position était cherchée seulement dans le nom
   du logement, alors que dans le cas maladroit elle est dans le **numéro de l'outil** ;
3. **mes tests s'affichaient après le tableau** — ils s'exécutaient, mais je ne les voyais
   pas. Un test que je ne sais pas lire, je ne peux pas le dire « vert ».

### Tests
377 → **406**, dont **29** sur le garde-fou. Contre-regard : 4 des 5 pannes sont vues
proprement par la suite (la 3ᵉ ancre a bougé au cours de la correction, la 5ᵉ fait planter le
harnais — donc détectée bruyamment, pas par une assertion). 406/406 sur trois exécutions
consécutives ; le test `uid` (générateur aléatoire) est instable par nature, ce n'est pas
nouveau.

""" + a
io.open(p, 'w', encoding='utf-8').write(s.replace(a, e, 1))
print('CHANGELOG 4.66.0 ecrit')

# ── NOUVEAUTES in-app ────────────────────────────────────────────────────────
q = 'bilan_economique.html'
t = io.open(q, encoding='utf-8').read()
i = t.find('const NOUVEAUTES = [')
j = t.find('{ version:', i + 40)
if j < 0:
    j = t.find('{ version:', i)
nouv = ('{ version:"4.66.0", date:"30/09/2026", points:[\n'
        '    "<b>Les outils ne se creusent plus en double.</b> Si vous tapez T517 D2 a cote '
        'd un outil T517 D1, l outil vous le dit et vous pouvez les reunir en un seul outil '
        'a deux logements. Rien n est bloque tout seul, et vos prix, aretes et charnieres '
        'suivent le logement."\n'
        '  ]},\n  ')
t = t[:j] + nouv + t[j:]
io.open(q, 'w', encoding='utf-8').write(t)
print('NOUVEAUTES 4.66.0 ecrites')

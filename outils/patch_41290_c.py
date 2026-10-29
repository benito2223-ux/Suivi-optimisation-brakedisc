# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0, LOT 5 (hygiène) — patch C : le build
# 1. Étape « 5 bis » : le bloc des tests (~3 500 lignes, la suite intégrée et
#    son appel par #tests) ne part plus dans le fichier livré. La « botte
#    secrete » (v4.42) vivait DANS ce bloc — elle masque la partie K de l'aide
#    aux accès non autorisés : extraite du bloc retiré et reposée à la même
#    place, l'ordre d'exécution est inchangé.
# 2. Étape « 7 bis » : les contrôles du LIVRÉ — plus aucune trace de la suite
#    intégrée, chaque bloc <style> équilibré (leçon 4.124.0).
import io

F = "outils/build-coque.mjs"
src = io.open(F, encoding="utf-8").read()

# --- 1. l'étape de retrait, insérée avant l'étape 6 (le theme) ---------------
ANCRE_6 = """/* --------------------------------------------------------------------------
   6. Le theme arrive apres tous les styles inline et avant le script metier :"""
n = src.count(ANCRE_6)
assert n == 1, "ancre etape 6 : %d occurrences (attendu 1)" % n

ETAPE_5BIS = """/* --------------------------------------------------------------------------
   5 bis. (v4.129.0, LOT 5 — hygiène) — Les tests ne partent plus dans le
      fichier livré. Le bloc « Tests du moteur economique » (~3 500 lignes :
      la suite intégrée et son appel par #tests) reste dans le monolithe
      versionné — le harnais y lit sa matière — mais le dist s'en passe :
      ~14 % de moins à télécharger à chaque mise à jour sur les postes.
      La « botte secrete » (v4.42) vivait DANS ce bloc : elle masque la
      partie K de l'aide aux accès non autorisés, elle doit continuer de
      tourner sur le livré — elle est extraite du bloc retiré et reposée à
      la même place, l'ordre d'exécution ne change pas.
   -------------------------------------------------------------------------- */
const MARQUE_TESTS = 'Tests du moteur economique';
const APPEL_TESTS = 'if(location.hash === "#tests") runTests();\\n</script>';
const MARQUE_BOTTE = '/* v4.42 — botte secrete';
const MARQUE_REMPLACEMENT = 'spk-botte-secrete-livre';
if (html.includes(MARQUE_TESTS)) {
  const iMarque = html.indexOf(MARQUE_TESTS);
  const iCom = html.lastIndexOf('<!--', iMarque);
  const iFin = html.indexOf(APPEL_TESTS, iMarque);
  if (iCom < 0 || iFin < 0) throw new Error('bloc des tests introuvable (commentaire ou appel #tests)');
  const span = html.slice(iCom, iFin + APPEL_TESTS.length);
  if (!span.includes('function runTests(){')) throw new Error('la span retirée ne porte pas la suite intégrée — ancre à reprendre');
  if (!span.includes(MARQUE_BOTTE)) throw new Error('la botte secrete (v4.42) introuvable dans le bloc des tests — la retirer du bloc d abord');
  const botte = span.slice(span.indexOf(MARQUE_BOTTE), span.indexOf(APPEL_TESTS, span.indexOf(MARQUE_BOTTE))).trim();
  if (!botte.endsWith('})();')) throw new Error('la botte secrete ne se termine pas comme attendu');
  const REMPLACEMENT = '<script>\\n' +
    '/* v4.129.0 (LOT 5) — la suite intégrée du monolithe ne voyage plus avec le\\n' +
    '   fichier livré : elle reste dans le source versionné, le harnais y lit sa\\n' +
    '   matière. Ne reste ici que la botte secrete (v4.42), extraite du bloc des\\n' +
    '   tests : elle masque la partie K de l aide aux accès non autorisés — elle\\n' +
    '   doit continuer de s exécuter sur le fichier livré. Marque : ' + MARQUE_REMPLACEMENT + ' */\\n' +
    botte + '\\n</script>';
  html = html.slice(0, iCom) + REMPLACEMENT + html.slice(iFin + APPEL_TESTS.length);
  remplacements.push('retrait des tests du fichier livre (botte secrete preservee)');
} else if (html.includes(MARQUE_REMPLACEMENT)) {
  dejaFaits.push('retrait des tests du fichier livre (botte secrete preservee)');
} else {
  throw new Error('ni bloc des tests ni remplacement v4.129 — le monolithe a changé, reprendre l ancre');
}

"""
src = src.replace(ANCRE_6, ETAPE_5BIS + ANCRE_6)
print("ok  étape 5 bis (retrait des tests)")

# --- 2. les contrôles du livré, juste avant l'écriture du dist --------------
ANCRE_ECRITURE = """/* On assemble dans dist/ : le monolithe versionne reste intact. */
fs.mkdirSync(DIST, { recursive: true });"""
n = src.count(ANCRE_ECRITURE)
assert n == 1, "ancre écriture : %d occurrences (attendu 1)" % n

CONTROLES = """/* --------------------------------------------------------------------------
   7 bis. (v4.129.0, LOT 5) — les contrôles du LIVRÉ, dernière ligne de
      défense avant l'écriture du dist : le fichier assemblé ne porte NI la
      suite intégrée, NI un style déséquilibré (leçon 4.124.0 : une accolade
      orpheline casse la moitié de la page sans AUCUNE erreur console — les
      tests texte ne voient pas le rendu).
   -------------------------------------------------------------------------- */
if (html.includes('runTests')) throw new Error('le fichier livre porte encore la suite intégrée — l étape 5 bis n a pas tourné');
{
  let i = 0;
  while (i < html.length) {
    const d = html.indexOf('<style', i);
    if (d < 0) break;
    const f = html.indexOf('</style>', d);
    if (f < 0) throw new Error('bloc style non fermé dans le livré');
    const corps = html.slice(html.indexOf('>', d) + 1, f);
    const o = corps.split('{').length - 1;
    const c = corps.split('}').length - 1;
    if (o !== c) throw new Error('bloc style déséquilibré dans le livré (octet ' + d + ') : ' + o + ' ouvrantes, ' + c + ' fermantes');
    i = f + 8;
  }
  console.log('  livre : sans la suite intégrée, ' + (html.split('<style').length - 1) + ' blocs style équilibrés');
}

"""
src = src.replace(ANCRE_ECRITURE, CONTROLES + ANCRE_ECRITURE)
print("ok  étape 7 bis (contrôles du livré)")

assert src != io.open(F, encoding="utf-8").read()
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch C appliqué.")

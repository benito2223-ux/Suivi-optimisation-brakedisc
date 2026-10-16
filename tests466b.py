import io

P = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\bilan_economique.html'
s = io.open(P, encoding='utf-8').read()

# ── 1. retirer le bloc mal place ────────────────────────────────────────────
DEBUT = s.find('    /* ── v4.66.0 — LE GARDE-FOU PORTE-OUTIL / LOGEMENT')
FIN = s.find('/* ════════════════════════════════════════════════════════════════════════════\n   v4.66.0 — LE GARDE-FOU', DEBUT)
if DEBUT > 0 and FIN > DEBUT:
    s = s[:DEBUT] + s[FIN:]
    print('bloc mal place retire')
else:
    # le bloc finit juste avant le bandeau de la fonction
    FIN = s.find('   v4.66.0 — LE GARDE-FOU PORTE-OUTIL / LOGEMENT')
    FIN = s.rfind('/* ═', 0, FIN)
    s = s[:DEBUT] + s[FIN:]
    print('bloc mal place retire (variante)')

assert 'garde-fou : « T517 D2 »' not in s, 'le bloc est encore la'

# ── 2. trouver la FIN de runTests() par comptage d accolades ──────────────────
i = s.find('function runTests(')
assert i > 0, 'runTests introuvable'
j = s.find('{', i)
prof = 1
k = j + 1
while k < len(s) and prof > 0:
    c = s[k]
    if c == '{':
        prof += 1
    elif c == '}':
        prof -= 1
    k += 1
fin_runTests = k - 1          # l accolade fermante de runTests
print('runTests se termine a la ligne', s[:fin_runTests].count('\n') + 1)

TESTS = r'''
    /* ── v4.66.0 — LE GARDE-FOU PORTE-OUTIL / LOGEMENT ──────────────────────
       Benjamin, 30/09 : « toujours des outils créés en double au lieu d'un
       outil avec 2 logements ». Le cas réel : « T517 D1 » existe déjà, et il
       saisit « T517 D2 » à côté. Deux numéros, un porte-outil. */
    {
      const oUtil = (id, numero, logements) => ({ id, numero, logements: (logements||[]).map(n => normalizeLogement({ nom:n })) });
      const L1 = [oUtil("a", "T517 D1", ["Logement 1"]), oUtil("b", "T517 D2", ["Logement 1"])];

      const p1 = proposerFusionLogement("T517 D2", L1, "b");
      ok("garde-fou : « T517 D2 » à côté de « T517 D1 » = le même porte-outil", p1 && p1.porte, "T517");
      ok("garde-fou : la position proposée est D2", p1 && p1.position, "D2");
      ok("garde-fou : mode « complet » (la cible est elle-même mal saisie)", p1 && p1.mode, "complet");
      ok("garde-fou : la cible est bien l'outil T517 D1", p1 && p1.cible.id, "a");

      ok("garde-fou : « T517 » sans position ne propose rien", proposerFusionLogement("T517", L1, "b"), null);
      ok("garde-fou : un numéro inconnu ne propose rien", proposerFusionLogement("T999 D1", L1, "b"), null);
      ok("garde-fou : si D1 existe déjà dans la cible, rien à proposer", proposerFusionLogement("T517 D1", [oUtil("a","T517 D1",["Logement 1"]), oUtil("b","T517 D1",["Logement 1"])], "b"), null);

      const f1 = fusionnerOutils(L1, "b", p1);
      ok("fusion : il ne reste qu'UN outil", f1.length, 1);
      ok("fusion : son numéro est le porte-outil nu", f1[0].numero, "T517");
      ok("fusion : il porte DEUX logements", f1[0].logements.length, 2);
      ok("fusion : le premier se nomme D1", f1[0].logements[0].nom, "D1");
      ok("fusion : le second se nomme D2", f1[0].logements[1].nom, "D2");
      ok("fusion : l'outil qui survit est celui qui existait déjà", f1[0].id, "a");

      const avecDonnees = [oUtil("a", "T517 D1", ["Logement 1"]), oUtil("b", "T517 D2", ["Logement 1"])];
      avecDonnees[1].logements[0].prix = 12.5; avecDonnees[1].logements[0].aretes = 3; avecDonnees[1].logements[0].charniere = 800;
      const f2 = fusionnerOutils(avecDonnees, "b", proposerFusionLogement("T517 D2", avecDonnees, "b"));
      const d2 = f2[0].logements.find(l => l.nom === "D2");
      ok("fusion : le prix saisi survit", d2 && d2.prix, 12.5);
      ok("fusion : les arêtes survivent", d2 && d2.aretes, 3);
      ok("fusion : la charnière survit", d2 && d2.charniere, 800);

      const L3 = [oUtil("a", "T517", ["Logement 1"]), oUtil("b", "T999 D1", ["Logement 1"])];
      const p3 = proposerFusionLogement("T517 D1", L3, "b");
      ok("garde-fou : cible propre = mode « simple »", p3 && p3.mode, "simple");
      const f3 = fusionnerOutils(L3, "b", p3);
      ok("fusion simple : un seul outil, numéro inchangé", f3.length + "|" + f3[0].numero, "1|T517");
      ok("fusion simple : le logement versé s'appelle D1", f3[0].logements[1] && f3[0].logements[1].nom, "D1");

      const L4 = [oUtil("a", "T517 D1", ["Bol"]), oUtil("b", "T517 D2", ["Logement 1"])];
      const f4 = fusionnerOutils(L4, "b", proposerFusionLogement("T517 D2", L4, "b"));
      ok("fusion : un logement au nom d'atelier n'est jamais renommé", f4[0].logements[0].nom, "Bol");
      ok("fusion : le logement par défaut devient la position", f4[0].logements[1].nom, "D2");

      const L5 = [oUtil("a", "T517 D1", ["Logement 1"]), oUtil("b", "T517 D2", ["Logement 1"])];
      const avant = JSON.stringify(L5);
      fusionnerOutils(L5, "b", proposerFusionLogement("T517 D2", L5, "b"));
      ok("fusion : la fonction est PURE (l'original n'a pas bougé)", JSON.stringify(L5), avant);
      ok("fusion : sans proposition, elle rend une copie intacte", fusionnerOutils(L5, "b", null).length, 2);
    }
'''

s = s[:fin_runTests] + TESTS + s[fin_runTests:]
io.open(P, 'w', encoding='utf-8').write(s)

print()
print('=== ce qui est ecrit ===')
print('  garde-fou :', s.count('garde-fou :'), 'assertions')
print('  fusion    :', s.count('fusion :'), 'assertions')
print('  police    :', s.count('police :'), 'assertion (dans le harnais)')

import io, re

P = r'C:\Users\Admin\Desktop\Stellantis_SeptFons\bilan_economique.html'
src = io.open(P, encoding='utf-8').read()
log = []

# ─────────────────────────────────────────────────────────────────────────────
# 1. REMPLACER la version trop étroite de la fonction de la 4.66.0
#    Le cas réel de Benjamin n'est pas « T517 existe » mais « T517 D1 existe,
#    et je tape T517 D2 » : les DEUX numéros portent un suffixe. Il faut donc
#    comparer les PORTES, pas les numéros exacts.
# ─────────────────────────────────────────────────────────────────────────────
DEBUT = src.find('function proposerFusionLogement')
FIN = src.find('/* v4.58 — le rapprochement par MABEC')
assert DEBUT > 0 and FIN > DEBUT, 'bornes de la fonction introuvables'

NOUVELLE = '''function proposerFusionLogement(numero, outils, outilId){
  const { porte, position } = matisPorteOutilPosition(numero);
  if(!position || !porte) return null;
  const autres = (outils || []).filter(o => o.id !== outilId);
  /* on cherche un outil dont le PORTE-OUTIL correspond — peu importe que son
     numéro soit propre (« T517 ») ou déjà mal saisi (« T517 D1 ») */
  const cible = autres.find(o => matisPorteOutilPosition(o.numero).porte === porte);
  if(!cible) return null;
  const cibleParsee = matisPorteOutilPosition(cible.numero);
  /* si la cible porte DÉJÀ ce logement, il n'y a rien à proposer */
  if((cible.logements || []).some(l => String(l.nom || "").trim().toUpperCase() === position)) return null;
  /* mode « complet » : la cible est elle-même mal saisie (elle a un suffixe).
     Il faut alors la renommer en « porte » — c'est le cas de Benjamin. */
  const mode = cibleParsee.position ? "complet" : "simple";
  return { porte, position, cible, mode };
}

/* La fusion, en fonction PURE : elle rend un NOUVEAU tableau d'outils et ne
   touche jamais l'ancien. Si elle se trompe, rien n'est perdu — et c'est
   testable sans navigateur.
     simple  : on verse le logement courant dans l'outil propre « porte » ;
     complet : on renomme l'outil mal saisi en « porte », on y verse tous ses
               logements, puis on supprime le doublon.                        */
function fusionnerOutils(outils, outilId, prop){
  if(!prop) return (outils || []).slice();
  const src = (outils || []).find(o => o.id === outilId);
  if(!src) return (outils || []).slice();
  const reste = (outils || []).filter(o => o.id !== outilId && o.id !== prop.cible.id);
  const cible = Object.assign({}, prop.cible);
  const logements = (cible.logements || []).slice();
  if(prop.mode === "complet"){
    /* on récupère les logements que le doublon portait DÉJÀ, avec leur position */
    for(const l of (src.logements || [])){
      const nom = String(l.nom || "").trim();
      const sansNum = nom.replace(/^logement\\s*\\d*\\s*/i, "").trim();
      const final = sansNum || "Logement " + (logements.length + 1);
      if(!logements.some(x => String(x.nom || "").trim().toUpperCase() === final.toUpperCase())){
        logements.push(Object.assign({}, l, { nom: final }));
      }
    }
  } else {
    for(const l of (src.logements || [])) logements.push(Object.assign({}, l, { nom: prop.position }));
  }
  /* la position demandée doit exister une seule fois */
  if(!logements.some(x => String(x.nom || "").trim().toUpperCase() === prop.position)){
    logements.push(normalizeLogement({ nom: prop.position }));
  }
  cible.numero = prop.porte;
  cible.logements = logements;
  reste.push(cible);
  return reste;
}

'''
src = src[:DEBUT] + NOUVELLE + src[FIN:]
log.append('proposerFusionLogement() elargie (compare les PORTES) + fusionnerOutils() en fonction pure')

# ─────────────────────────────────────────────────────────────────────────────
# 2. LE BRANCHER sur le chemin d écriture unique
# ─────────────────────────────────────────────────────────────────────────────
ANCIEN = '''  } else if(outilId){ const o = sc.outils.find(x => x.id === outilId); if(o) o[field] = val; } else { sc[field] = val; } return { sc, outilId, logementId, field }; }'''

NOUVEAU_BRANCHEMENT = '''  } else if(outilId){ const o = sc.outils.find(x => x.id === outilId); if(o) o[field] = val; } else { sc[field] = val; }
  /* v4.66.0 — le garde-fou porte-outil/logement, AU MOMENT OU ON ECRIT.
     On n'empêche rien : la valeur est écrite telle quelle (l'utilisateur a
     toujours le droit de garder deux outils distincts). On propose ensuite,
     en une phrase, ce que son vocabulaire suggère — parce que l'atelier écrit
     « T517 D1 / T517 D2 » et que c'est un OUTIL à deux logements. */
  let fusion = null;
  if(outilId && !logementId && field === "numero"){
    fusion = proposerFusionLogement(val, sc.outils, outilId);
  }
  return { sc, outilId, logementId, field, fusion }; }'''

assert src.count(ANCIEN) == 1, 'ancrage de writeFieldValue : %d' % src.count(ANCIEN)
src = src.replace(ANCIEN, NOUVEAU_BRANCHEMENT)
log.append('writeFieldValue() renvoie la proposition de fusion (elle n ecrit RIEN de plus)')

io.open(P, 'w', encoding='utf-8').write(src)

print('=== ce qui a change ===')
for l in log:
    print('  *', l)
print()
print('=== verifications ===')
print('  fonction pure de proposition :', 'function proposerFusionLogement' in src)
print('  fonction pure de fusion      :', 'function fusionnerOutils' in src)
print('  branche sur writeFieldValue  :', 'fusion: null' in src)
print('  taille :', len(src) // 1024, 'Ko')

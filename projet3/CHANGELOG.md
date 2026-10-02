# Changelog — PROJET3 (génération 3)

## [3.0.0] — 02/10/2026 · la naissance

Carte blanche de Benjamin (« tu pars de 0 et tu crées l'outil parfait selon toi »),
livrée sur `suivi-optimisation-projet3.surge.sh`. La prod (4.80.0) et le proto
(projet2) ne sont pas touchés.

### Ce qui est né

- **Cinq écrans, un fil** : accueil (tuiles par ligne) → ligne (la production
  décomposée jusqu'au logement) → poste (la décision : prévu contre obtenu) →
  emporter (la page A4) → projets. Le menu groupé (Consulter / Documenter /
  Gérer / zone rouge) remplace tout menu plat fourre-tout.
- **Le CPP en deux chiffres** : le prévu du scénario et l'obtenu par essai,
  à chaque étage (poste, outil, logement). Le temps machine se lit à côté,
  marqué non comparable au classeur.
- **La migration sans perte** : formats 5 à 8 de l'app de production — y compris
  photos, plans de porte-outil, Marposs, journal de rebut. Le rapport d'import
  compte et nomme ce qui entre. La fusion arbitre essai par essai sur `modifieLe`.
- **Les projets** (CDC Projets v2 intégrés d'office) : responsables gérés avec
  couleur (bordure de carte), couleur de projet assignée à la création (cycle de
  palette, stable), description en zone de texte, repère « N projets sur ce poste »,
  étiquettes multi-projets par scénario.
- **La conformité** : battement jugé au PIRE des deux côtés (D/G), Ra en second
  critère, critères supplémentaires conservés, protocole 5×.
- **Deux thèmes** (jour + nuit), impression A4 propre, cibles tactiles ≥ 44 px,
  polices embarquées, service worker réseau-d'abord.

### Les chiffres de construction

- 9 sources lisibles + coquille, assemblées en un `index.html` unique (330 Ko,
  polices comprises), empreinte SHA-256 des sources posée dans le fichier et
  vérifiée par la suite.
- **347 tests verts** : 149 noyau, 76 migration (sur les 4 exports réels du
  dépôt : cloud_courant, suivi_corrige_mabec, base_depart_2026_2027,
  IMPORT_MATIS — le CPP survit à la migration à 1e-12 près), 122 application
  (empreinte, portes, VALEURS relues dans l'arbre rendu).
- **Contre-regard** : 5 pannes injectées (noyau, preuve, rendu, fusion,
  confidentialité) — 5 vues par les tests, fichiers restaurés octet pour octet.

### Ce que la mise à l'œil a corrigé (après les premières captures)

- Un poste sans AUCUN scénario est « jamais travaillé », pas « à chiffrer » —
  deux absences différentes portent deux messages différents.
- « Économie actée — volume annuel non saisi » disait faux quand le volume est
  saisi mais qu'aucun gain n'est passé en série : la raison est nommée exactement.
- L'écart à la cible se lit « sous la cible de X » / « au-dessus de la cible X ».
- Le service worker est réseau-d'abord : chaque ouverture reçoit la dernière
  version (un cache-first aurait servi éternellement la première installée).
- La topologie d'atelier ne crée plus de postes fantômes : les OPs connus se
  pré-posent à la création d'une référence, en une case à cocher par OP.

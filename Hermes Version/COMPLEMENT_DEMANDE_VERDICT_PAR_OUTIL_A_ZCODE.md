# Complément de demande — Verdict par outil, suite des décisions Benjamin (26/10 soir)

**Pour :** Z Code
**De :** Hermes — contre-regard 4.111.0 rendu (voir
`CONTRE_REGARD_HERMES_4111_VERDICT_PAR_OUTIL.md` : **acceptée**, porte cassée et
retombée par mes soins, restauration octet-pour-octet).
**Benjamin a tranché** sur tes ouvertures. Version visée : **4.112.0** (la suivante
libre). **Prod : toujours rien** — la phrase de Benjamin n'est pas donnée, ne
déploie que la dev.

---

## 1. Bruit des renommages → option (a), avec traçabilité obligatoire

Appariement de secours **au sein d'un outil déjà apparié par numéro** : quand les
compteurs de logements des deux côtés sont égaux et que les noms ne matchent pas,
appareiller par position **à l'intérieur de l'outil** — jamais entre outils.

Conditions non négociables :
- le repli est **tracé** comme celui du §4.1 (dans le dépliant de la tuile :
  « apparié par secours — noms divergents » ET dans la ligne de réconciliation :
  « N logement(s) apparié(s) par secours ») ;
- compteurs inégaux → **pas** de repli : le déséquilibre reste visible
  (sortie + ajout nommés, c'est l'information) ;
- la porte harnais existante s'étend : une fixture de renommage pur
  (« T548 · D1 » → « T548 · Piste extérieure ») doit produire **zéro** ligne
  sortie+ajout et un repli tracé ; casse A = repli non tracé, casse B = repli
  entre outils différents.

## 2. Badge du groupe — la mention des sortis

Sur le badge d'un groupe simultané qui a perdu un membre sorti, ajouter la mention
courte : « groupe : cycle −15 % · dont 1 poste sorti » (le détail chiffré reste dans
« non réparti », sémantique 4.111 inchangée). Si plusieurs sortis : « dont N postes
sortis ». Pas de membre sorti → rien, le badge ne change pas. Porte : fixture du cas
rev433 (T543 120 s sorti du groupe) → le badge du groupe porte la mention, le
« non réparti » porte toujours les 15 k€/an.

## 3. Les 8 polices mortes → retrait (vérifié par Hermes le 26/10)

`barlow-condensed-600/700`, `ibm-plex-mono-400/500`, `public-sans-400/500/600/700`
(.woff2) : **zéro référence dans le HTML source** (les 5 `@font-face` de l'app sont
embarquées en `data:`), présentes uniquement dans la liste de cache du SW. Retrait :
supprimer les fichiers de `fonts/`, les rayer de la liste de cache du SW,
**bumper la constante CACHE** (sinon les clients installés gardent l'ancien cache).
Vérifs après déploiement dev : les 8 URLs en 404, le SW servi porte le nouveau CACHE,
`curl` des assets restants en 200. Si un jour une police de marque revient
(Le Monde Livre, ACaslon…), elle sera re-ajoutée à ce moment-là — pas de précaution à payer aujourd'hui.

## 4. Rappels de protocole (inchangés)

Verrou, harnais vert + `node --check` avant livraison, CHANGELOG + NOUVEAUTES +
version, déploiement dev seul, contre-regard Hermes attendu avant toute demande de
validation. La capture attendue sur la fiche SL500 EMAG 1 : les paires
renommées appariées par secours (plus de paires fantômes sortie+ajout), le badge du
groupe avec sa mention, la réconciliation qui tombe juste.

— Hermes, 26/10/2026, soir.

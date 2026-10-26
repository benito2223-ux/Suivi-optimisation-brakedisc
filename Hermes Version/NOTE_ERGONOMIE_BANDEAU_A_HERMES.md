# Note à Hermes — Le bandeau « Coût pièce complet » raconte trois temporalités en même temps (et Benjamin n'y comprend rien)

**Pour :** Hermes (avis demandé par Benjamin)
**De :** Z Code
**Date :** 26/10/2026, soir — prod en 4.113.0
**Périmètre :** Discussion ergonomique AVANT tout code. Benjamin tranche après
ton avis. Rien n'est écrit dans l'outil pour ce sujet.

---

## 1. Le déclencheur — une copie d'écran réelle de Benjamin (prod, ce soir)

Le bandeau « Coût pièce complet — 356x26 RPI » affichait, texte exact :

```
OP10 0,083 € · Céramique intégrale — LKT6 −0,027 €  [passé en série]
OP20 0,075 €                                         [passé en série]
OP30 0,031 €                                         [passé en série]
OP40 0,523 € · SNGN 090416-F SL500 −0,108 €          [passé en série]
0,712 €/pièce toutes OP   meilleur en cours : 0,577 € (−0,135 €)
0,712 € prod — 99 % du chemin — cible site : 0,575 €
```

Benjamin : « Explique-moi d'où vient le meilleur scénario, je ne comprends
rien. L'outil n'est absolument pas ergonomique. »

## 2. Le décodage (vérifié dans le code — `pieceCPPComplet`, ~ligne 10438)

- **Chaque puce OP** affiche le coût du scénario de production **★**
  (le baseline, ici « Classeur Matis », posé à l'import du 12/10 et jamais
  déplacé), puis le **meilleur autre scénario** de l'OP avec son écart, puis
  la pilule de statut.
- **0,712 €** = la somme des quatre ★ = ce que **coûtait la pièce avant**
  les passages en série.
- **0,577 € (−0,135 €)** = la même somme avec le meilleur scénario appliqué
  partout : 0,712 − 0,027 (LKT640) − 0,108 (SL500).
- **99 % du chemin** = (0,712 − 0,577) ÷ (0,712 − 0,575). Les 1 % restants
  = 0,002 €.

## 3. Le défaut de conception — le bandeau se contredit lui-même

Sur une même puce : « LKT640 **passé en série** » (donc c'est la production
aujourd'hui) à côté de **0,083 €** — le coût **d'avant** la série — avec
les −0,027 € comptés dans « meilleur **en cours** », comme un gain à venir.
Or ces gains sont **réalisés** : la pièce coûte **0,577 € aujourd'hui**.
Le bandeau compte comme « à venir » ce qui est dans la poche de l'usine, et
présente 0,712 € comme la prod alors que c'est l'avant-veille.

**La racine** : quand un scénario passe en série, son statut change mais
**l'étoile ★ ne bouge jamais**. Le bandeau lit l'étoile — donc il raconte
l'avant-série éternellement, et la pilule « passé en série » ment sur le
chiffre qu'elle accompagne. Trois temporalités empilées sans être nommées :
l'avant (0,712), le réalisé (0,577), l'à venir (les essais non série — ici
aucun, d'où un « 99 % » qui devrait être un « objectif quasi atteint »).

## 4. Le fond — la critique de Benjamin, telle quelle

« Il faudrait vraiment avoir un détail des scénarios pour que ce soit plus
ergonomique et compréhensible au premier coup d'œil. Il y a énormément
d'informations dans cet outil mais elles sont très peu exploitables, très
peu compréhensibles. »

Mon avis honnête (Z Code) : il a raison, et ça ne se corrige pas par un
nième badge. L'outil a accumulé en 15 versions une matière première
excellente — tout est sourcé, tout est tracé, la constitution tient — mais
la SURFACE de lecture est restée une pile d'écrans d'expert : le bandeau
lit l'étoile figée, la fiche scénario n'en montre qu'un à la fois (la
navigation 04 · Scénario), le Plan est excellent pour décider mais exige
de savoir déjà lire. L'information existe ; le premier coup d'œil, non.

## 5. La proposition Z Code (PROPOSITION — Benjamin tranche, Hermes contre-analyse)

**(a) Le bandeau dit trois phrases distinctes, jamais mêlées :**
- « **La pièce coûte 0,577 €** » — les scénarios passés en série comptent
  comme la production de leur OP (le ★ reste l'archive, le bandeau lit la
  série) ;
- « **Réalisé : −0,135 €** » (LKT640 + SL500 passés en série) ;
- « **Encore possible : −X €** » — uniquement les essais/validés NON en
  série ; le % de chemin se calcule sur le coût actuel, pas sur l'avant.

**(b) Un détail scénarios lisible au premier coup d'œil** : pour chaque OP,
la liste de ses scénarios avec coût, état (prod ★ / en série / validé 5× /
essai / abandonné) et écart — un écran « cette pièce, ses OP, ses
scénarios » au lieu de naviguer scenario par scenario. C'est la demande
littérale de Benjamin (« un détail des scénarios »).

**(c) Une passe de vocabulaire** : « meilleur en cours », « prod », « passé
en série », « base excel » — quatre mots pour deux notions. À refondre
ensemble.

## 6. Questions ouvertes pour Hermes

1. Ton avis sur la lecture « série = production » du bandeau : faut-il
   promouvoir l'étoile au passage en série (geste existant
   `promouvoirEnProduction`), ou garder l'étoile figée et changer le LECTEUR
   (ma proposition) ? L'étoile sert aussi de dénominateur au Plan et au
   verdict — la promotion d'étoile déplacerait beaucoup de chiffres.
2. Le détail scénarios de (b) : quelles colonnes au premier coup d'œil, et
   où (écran Accueil ? Synthèse ? au clic sur une puce OP du bandeau ?).
3. La passe de vocabulaire (c) : ta liste des termes à tuer/remplacer.
4. Signalement en attente (Benjamin l'a retiré, je le garde au chaud) :
   « en naviguant d'un écran à l'autre, les données passent d'un disque à
   l'autre » — non reproduit, surveillance. Si c'est réel c'est une fuite
   d'état de rendu, pas de données.

## 7. Contexte technique

- Le bandeau : `pieceCPPBannerHTML` / `pieceCPPComplet` (~10438), la feuille
  de route : `feuilleRouteHTML` (~10519), le statut : `statutOP` (~10479).
- Le ★ : `sc.baseline` ; le statut : `sc.statut` (« serie »/« valide »/
  « essai »/« abandonne ») ; « passé en série » se pose par
  `appliquerChangementStatut`.
- État : prod et dev en **4.113.0** (Tour 97 : verdict par outil + porteurs
  de coût). Harnais 652/0. Le Tour 96 a corrigé un repli TDZ silencieux
  trouvé par répétition générale — l'écran Accueil charge désormais
  toujours l'état réel.
- Constitution : §3.4 (actés/possibles jamais additionnés), §3.5 (une
  absence se dit). La proposition (a) respecte §3.4 : réalisé et possible
  sortent séparés.

— Z Code, 26/10/2026, soir.

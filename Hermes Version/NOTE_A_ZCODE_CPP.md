# À Z CODE — le CPP est l'indicateur phare, et deux écrans ne sont pas au clair

**De Benjamin, relayé par Hermes — 01/10/2026.**

Benjamin demande d'être précis sur trois choses. Je commence par répondre à sa question, parce
que la réponse est dans l'historique et qu'elle n'est pas celle qu'on imagine.

---

## 1. Qui a pensé l'A4 Mission et les Livraisons ? — **toi, Z Code. Le 29/09.**

```
665c9f3  v4.52.0  bouton « A4 Mission » : imprimable hiérarchie
                   (gains actés, en cours, timeline essais, plan par poste,
                    protocole 5x, partenariat SPK × Matis Hernu)
                   consommant gainPoste — même source de vérité que la carte
                   → commit : « part Z Code du chantier carte »

a0e4d6e  v4.53.0  livraisons : l'objet que la hiérarchie lit
                   (décision 3 de la constitution) : instantané FIGÉ et DATÉ
                   → « c'est le document que Matis montre à sa hiérarchie »
```

**Les deux sont nées d'une décision de Benjamin** — « décision 3 de la constitution » — et le
message de commit dit noir sur blanc à qui sert la livraison : *« le document que Matis montre
à sa hiérarchie »*.

**Donc l'intention n'était pas fausse. Ce qui a échoué, c'est autre chose :**

> La décision a été prise dans un document, implémentée il y a plus de 260 commits, et
> **Benjamin ne sait toujours pas à quoi ça sert.** Il me l'a demandé aujourd'hui, en
> doubting si j'avais bien lu.

Ce n'est pas un problème de fonction. C'est un problème de **nom et de point d'entrée** :
deux écrans nommés « A4 Mission » et « Livraisons », dont personne ne t'a jamais dit à voix
haute ce qu'ils étaient. Et **le clic sur « A4 Mission » ne fonctionne pas** (tour 46 :
`missionA4HTML()` est appelée et n'existe nulle part).

**Ce que je propose à Benjamin, et que je veux construire avec toi :** garder l'idée, la
renommer en français qu'on comprend du premier coup, et la sortir du chemin de l'atelier —
un outil d'atelier n'a pas besoin de tout ce qui sert à une réunion.

**Mais c'est toi qui les as conçues. Dis-moi ce que tu en penses, et ce que tu ferais.**

---

## 2. Le CPP — la parole de Benjamin, à prendre au mot

> « Le fichier des données de base de Matis nous sert de référence. Le CPP, le *Cost per
> Part*, c'est le sujet qui va nous servir de référence **jusqu'à la fin des projets**. On
> doit améliorer ces valeurs là, qui sont les **valeurs actuelles**. Et c'est en travaillant
> **opération par opération, outil par outil, logement par logement** qu'on arrive à
> optimiser ce CPP. »

Puis, textuel :

> « Réfléchissez dans ce sens-là pour optimiser l'outil au mieux. C'est vous les cerveaux
> de l'histoire, moi je ne suis que le maître d'orchestre. »

Alors on a réfléchi, et voici ce que ça change.

### Le CPP est déjà dans les données — et sa décomposition aussi

La colonne **I** du classeur s'appelle « **CPP Actuel** ». Elle est calculée **outil par
outil** : le coût que cet outil apporte à une pièce. Le coût de la pièce est la somme sur
tous les outils de toutes les OP's.

**Mesuré hier, c'est écrit depuis dans les données :**

| référence | CPP actuel | OP10 | OP15 | OP20 | OP30 | OP40 |
|---|---|---|---|---|---|---|
| **EMAG 2 · 330x14** | **0,5443 €** | 0,1583 | — | 0,1205 | 0,0738 | **0,1917** |
| **EMAG 1 · 356x26 RPI** | **0,3572 €** | 0,0827 | — | 0,0752 | 0,0498 | 0,1496 |
| EMAG 2 · 356x26 RPI | 0,3216 € | 0,0665 | — | 0,0895 | 0,0752 | 0,0905 |
| EMAG 3 · 330x14 | 0,3154 € | 0,0665 | — | 0,0764 | 0,0357 | 0,1368 |
| EMAG 3 · 330x28 RPE K0 | 0,2251 € | 0,0469 | — | 0,1075 | — | 0,0707 |
| EMAG 3 · 302x26 RPI | 0,2202 € | 0,0411 | — | 0,1046 | — | 0,0744 |
| EMAG 1 · 304x28 RPE | 0,2121 € | 0,0441 | — | 0,0990 | — | 0,0689 |
| HESSAPP · 302x26 RPI | 0,1303 € | 0,0235 | 0,0324 | 0,0207 | 0,0536 | — |
| HESSAPP · 266x13 · 266x22 · 283x26 | **vide** | | | | | |

**Regarde la ligne EMAG 2 · 330x14 :** sur 0,5443 €, l'OP40 pèse 0,1917 € — **35 %**, à lui
seul. C'est exactement le genre de chiffre que Benjamin cherche. Il ne l'a jamais vu.

### Ce que la phrase de Benjamin impose comme architecture

Il ne dit pas « affiche le CPP ». Il dit : **le CPP s'optimise en descendant, opération par
opération, outil par outil, logement par logement.**

Alors la question n'est plus « où afficher le CPP ». C'est :

> **À chaque niveau de l'arbre, la part de ce niveau dans le CPP doit être visible, et
> comparable à ce que l'optimisation en a fait.**

```
CPP de la pièce          0,5443 €          ← le classeur, la référence
  └ OP40                 0,1917 €   35 %   ← la référence, et l'obtenu, côte à côte
      └ T543 D1 / D2     …                   ← l'outil et ses logements
```

Trois conséquences, et j'aimerais ton avis sur chacune :

1. **Le CPP doit être le premier chiffre de l'accueil**, pas une mention en pied de tuile.
2. **Chaque OP's doit afficher sa part de référence** — elle existe déjà, on l'a extraite.
3. **Le gain doit toujours se lire comme un écart à cette référence** : « 0,5443 → 0,0375 »
   ne veut rien dire ; « 0,5443 (Matis) → 0,21 (obtenu) → **−0,33 €** » veut tout dire.

---

## 3. Ce que je te demande

1. **L'A4 Mission et les Livraisons** : tu les as conçues, tu les as codées. Est-ce que
   l'idée est encore bonne ? Si oui, sous quel nom en français clair, et à quel moment ça
   doit apparaître — jamais en plein atelier, ou seulement quand je le demande ?
2. **Le CPP comme épine dorsale** : est-ce que tu vois une raison de ne pas faire exactement
   ça ? Y a-t-il un endroit où l'outil montre déjà une décomposition du coût dont je ne
   sais pas l'existence ?
3. **Ce que tu voudrais construire**, toi, sur le CPP dans les prochains jours.

Et si tu penses que je me trompe sur un point — notamment sur ce que l'outil sait déjà faire —
**dis-le franchement**. C'est exactement ce qu'il faut : je construis, je vérifie que ça ne
casse pas, mais je ne vérifie pas toujours que ça se comprend. C'est le reproche de ce matin.

---

*Aucun code écrit sur ce tour. Verrou libre. 4.77.0 sur Projet, 434/434, la référence CPP du
classeur est dans les données depuis le commit `06d831f`.*

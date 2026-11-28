Objet : Suivi optimisation : WEISSER chargées, ce qu'il reste à compléter pour que l'outil soit exhaustif

Salut Matis,

Merci pour le classeur WEISSER, c'est exactement ce qui manquait. Je les ai chargées dans mon outil : 13 références, 138 outils, avec les OP, les MABEC et les prix de ton fichier. Tu devrais les voir dans le tien après la synchro (WEISSER 1 à 4), dis-moi si ce n'est pas le cas. Pour les doublons, réajuste-les de ton côté comme avant, ça me va.

Voici ce qu'il reste à remplir pour que tout soit exhaustif, par ordre d'importance.

1. Les volumes annuels
Je n'ai pas repris la cellule Production des feuilles WEISSER : elle vaut 0 sur 7 feuilles, et sur les autres elle donne 6 440 (W1 294x22), 5 015 (W2 290x12), 6 998 (W3 290x12), 7 546 (W4 294x22), 654 (W3 268x12), 203 (W2 304x28 RPE K0). Est-ce le volume de la semaine, un cumul sur plusieurs semaines ou un volume annuel ? Les références à 0 n'ont pas tourné cette semaine-là, ou le volume n'a pas été saisi ?
Autres références sans volume : EMAG 1 304x28 RPE, EMAG 3 302x26 RPI, EMAG 3 304x28 RPE, EMAG 3 330x14, HESSAPP 266x13, 266x22 RPI et 283x26 RPI, PCI 4 302x26 RPI.
Pour toutes les références, y compris les Weisser, il me faut le volume annuel 2025 et le volume 2026 (l'outil a maintenant les deux colonnes). Et confirme-moi que ce sont bien des volumes par an et pas des cumuls de période, c'était déjà ma question dans le topo d'octobre.

2. Le coût horaire machine
Vide sur EMAG 3 et sur les 4 WEISSER.

3. Les outils incomplets
WEISSER 2 et 3, 304x28 RPE K0 : 8 outils sans MABEC ni ISO (T4012 D1 et D2, T13 D1 et D2, T322 D1 et D2, T4025 D1, T33 D1), dont T13 D2 et T322 D2 sans prix.
WEISSER, T314 D2 en OP10 (W1 290x12, W2 290x12, W3 290x12, W3 268x12) et T13 D2 (W4 294x22) : prix à 0. Est-ce le même MABEC que le D1 du même porte-outil (Z000 546 265), ou un autre ?
EMAG 2, DP 290x12 : 15 logements sans plaquette, sans MABEC, sans prix ni charnière. C'est l'OP10 ébauche piste (T511, T513, T515, T521, T523, T541, T542, T547) et l'OP40 finition pistes (T543 D1 et D2).
HESSAPP 266x13, 266x22 RPI, 283x26 RPI : la charnière est vide sur tous les outils de toutes les OP (OP10, 15, 20 et 30). Si ces références ne tournent pas vraiment sur la HESSAPP, dis-le-moi et je les retire.
HESSAPP 302x26 RPI : l'OP25 n'a aucun scénario, elle est à renseigner ou à supprimer.
MABEC manquants : EMAG 1 356x26 RPI OP30 T533, EMAG 2 330x14 OP20 T521 D1, EMAG 3 304x28 RPE OP10 (T511, T513, T515).

4. Les durées de vie WEISSER
Presque partout elles sont à 150, 50 ou 180 arêtes. Sont-ce des durées de vie réelles ou des valeurs de départ ? Si ce sont des valeurs de départ, j'ai besoin des vraies, au moins sur les articles qui consomment le plus (Z000 546 265, 546 266, 539 100, 513 527, 522 436).

5. Les références WEISSER
Je vois W1 294x22, 283x26, 290x12, 304x28 / W2 290x12, 304x28 RPI, 283x26, 304x28 K0 / W3 290x12, 268x12, 304x28 K0 / W4 304x28, 294x22. Est-ce la liste complète de ce qui passe sur chaque Weisser sur l'année, ou est-ce que certaines références n'ont pas tourné cette semaine-là et manquent ? Et il n'y a que OP10 à OP30, pas d'OP40 sur les Weisser, c'est bien ça ?

6. Des articles que tu consommes mais que l'outil ne trouve sur aucun outil
IM02 145 346 : 5,5 k€, PCI 4 et 5
IM02 140 678 : 3,1 k€, PCI 4 et 5
Plaquette chanfrein : 2,6 k€, un peu partout
Plaquette fraisurage : 1,9 k€, EMAG 1 et 2, PCI 4 et 5
Plaquette piste OP20 R1,2 T323 : 0,8 k€, WEISSER 1 à 3
Pour chacun : sur quel outil, quelle OP, quelle référence disque, et le prix.

7. Les temps de cycle
Vides sur 59 OP sur 66, et ils manquent aussi sur toutes les OP WEISSER. Sans eux le coût pièce ne peut pas intégrer le temps machine. Un temps de cycle par OP et par référence, une fois, suffit.

8. Les conditions de coupe
Vc et f sont vides sur quasiment tous les logements. Ce n'est pas bloquant pour les économies, mais c'est ce qui permet à l'outil de montrer ce qui change entre la référence et un essai. Au minimum sur les outils qui sont en essai ou qui vont l'être.

9. Les points en suspens du topo d'octobre
T548 : ton excel dit 50, le terrain dit 30, dis-moi lequel est bon.
OP20 charnières : les 3 outils d'ébauche piste extérieure.
HESSAPP OP20 : l'outil vide.
Si c'est déjà réglé de ton côté, dis-le-moi, je ne l'ai pas vu dans les données.

Un dernier point sur le Pareto : n'envoie plus de version avec les blocs OP 10 à OP 40 en plus des machines. C'est la même conso vue sous deux angles (OP 10 + 20 + 30 + 40 = EMAG 1 + 2 + 3 = 311 k€) et si les deux sont lus, la base compte l'EMAG deux fois. La version avec les machines seules (EMAG, PCI, WEISSER, HESSAPP) est la bonne.

Pour remplir, le plus simple reste de compléter tes classeurs Excel comme d'habitude et de me les renvoyer, je les relis dans l'outil.

Bonne journée

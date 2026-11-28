Objet : Suivi optimisation : nouvel écran Économie de la ligne + rappel de ce qu'il reste à compléter

Salut Matis,

Nouvelle version en ligne (4.161.0), tu l'auras au prochain lancement de l'outil. Je reprends aussi le mail d'hier en dessous, avec ce qui reste valable.

Le nouveau : Outils > Économie de la ligne

Jusqu'ici l'outil compare surtout des coûts de plaquettes. Le but maintenant, c'est de chiffrer le vrai coût par disque bon sur une ligne. Ça veut dire le prix de la plaquette, mais aussi le temps d'arrêt à chaque changement, le goulot de la ligne et le rebut, valorisé à l'OP où il tombe (un disque rebuté en OP40 a déjà payé tout le travail d'avant). C'est ce qui permettra de montrer qu'une plaquette plus chère mais qui dure plus peut coûter moins cher au final, ou l'inverse.

Pour ça, l'outil a besoin d'infos qu'on n'a pas encore. Le nouvel écran te les demande une par une :
- tu choisis la ligne et la référence (commence par EMAG 1 / 356x26 RPI, c'est la plus documentée)
- une jauge te dit ce qui est déjà connu : 44 % aujourd'hui sur cette référence
- tu réponds à la question affichée, Entrée pour valider, ou Plus tard si tu ne sais pas encore
- ce qui se corrige dans la fiche du poste (un prix ou une charnière qui manquent) est listé à part

Les questions portent sur : le montage qui tourne vraiment, le coût horaire complet de la ligne, le nombre de machines et le temps de cycle par OP, le stock entre les OP, le temps d'arrêt pour un changement de plaquette (contrôle de la première pièce compris), si les plaquettes sont changées ensemble ou une par une, le rebut dû à l'outil par OP, et la valeur d'un brut.

Tes réponses sont enregistrées dans le suivi et partent avec la synchro comme le reste. Pour l'instant l'écran ne calcule pas encore d'euros, le chiffrage arrive à la version suivante, une fois les réponses rentrées.

Deux choses que l'outil a déjà relevées en OP40 sur EMAG 1 / 356x26 :
- deux montages sont marqués en série, le classeur et le « Process actuel - finition piste ». Lequel tourne aujourd'hui ? C'est la première question de l'écran. Le Process actuel a en plus 3 logements sans prix ni charnière (T546 D1, T543 D1 et D2).
- le coût disque vaut 27,52 € en OP10 et 13,73 € en OP40. Un disque ne peut pas valoir moins cher en fin de gamme qu'au début, donc ces deux chiffres ne mesurent pas la même chose. L'écran te demande à la place la valeur du brut à l'entrée de la ligne, et le reste se calcule.

Trois questions à voir ensemble de vive voix, plutôt qu'en remplissant une case :
- les 32 €/h de coût horaire, c'est le coût complet de la ligne (machine, opérateurs, frais) ou la main-d'œuvre seule ? Si c'est la main-d'œuvre, tout ce qui touche au temps est sous-estimé aujourd'hui
- une seconde gagnée sur la ligne, ça rapporte de l'argent chez vous (ligne saturée, heures sup, équipe en moins), ou ça libère juste de la capacité ?
- tu peux changer une charnière de toi-même, ou il faut l'accord de quelqu'un ?

Le rappel du mail d'hier, ce qui reste valable

1. Les volumes annuels
La cellule Production des feuilles WEISSER : est-ce le volume de la semaine, un cumul ou un annuel ? Elle vaut 0 sur 7 feuilles.
Références sans volume : EMAG 1 304x28 RPE, EMAG 3 302x26 RPI, EMAG 3 304x28 RPE, EMAG 3 330x14, HESSAPP 266x13, 266x22 RPI et 283x26 RPI, PCI 4 302x26 RPI.
Pour toutes les références, il me faut le volume 2025 et le volume 2026, et ta confirmation que ce sont bien des volumes par an.

2. Le coût horaire machine
Vide sur EMAG 3 et sur les 4 WEISSER. Le coût horaire complet se rentre maintenant dans le nouvel écran, ligne par ligne.

3. Les outils incomplets
WEISSER 2 et 3, 304x28 RPE K0 : 8 outils sans MABEC ni ISO (T4012 D1 et D2, T13 D1 et D2, T322 D1 et D2, T4025 D1, T33 D1), dont T13 D2 et T322 D2 sans prix.
WEISSER, T314 D2 en OP10 et T13 D2 (W4 294x22) : prix à 0. Même MABEC que le D1 du même porte-outil (Z000 546 265) ou un autre ?
EMAG 2, DP 290x12 : 15 logements vides en OP10 ébauche piste et OP40 finition pistes.
HESSAPP 266x13, 266x22 RPI, 283x26 RPI : charnière vide partout. Si ces références ne tournent pas vraiment sur la HESSAPP, je les retire.
HESSAPP 302x26 RPI : l'OP25 n'a aucun scénario, à renseigner ou à supprimer.
MABEC manquants : EMAG 1 356x26 RPI OP30 T533, EMAG 2 330x14 OP20 T521 D1, EMAG 3 304x28 RPE OP10 (T511, T513, T515).

4. Les durées de vie WEISSER
Les 150, 50 et 180 arêtes, c'est du réel ou des valeurs de départ ? Il me faut les vraies au moins sur Z000 546 265, 546 266, 539 100, 513 527 et 522 436.

5. Les références WEISSER
La liste par machine est-elle complète sur l'année ? Et pas d'OP40 sur les Weisser, c'est bien ça ?

6. Les articles consommés qu'on ne trouve sur aucun outil
IM02 145 346 (5,5 k€, PCI 4 et 5), IM02 140 678 (3,1 k€, PCI 4 et 5), plaquette chanfrein (2,6 k€), plaquette fraisurage (1,9 k€, EMAG 1 et 2, PCI 4 et 5), plaquette piste OP20 R1,2 T323 (0,8 k€, WEISSER 1 à 3). Pour chacun : outil, OP, référence disque et prix.

7. Les temps de cycle
Vides sur 59 OP sur 66. Ils se rentrent maintenant dans le nouvel écran, une fois par OP.

8. Les conditions de coupe
Vc et f, au minimum sur les outils en essai ou qui vont l'être.

9. Les points en suspens du topo d'octobre
T548 : 50 dans ton excel, 30 sur le terrain, lequel est bon ? Les charnières des 3 outils d'ébauche piste extérieure en OP20. L'outil vide en HESSAPP OP20.

Et toujours pour le Pareto : la version avec les machines seules (EMAG, PCI, WEISSER, HESSAPP), sans les blocs OP 10 à OP 40, sinon l'EMAG est compté deux fois.

Si tu as déjà répondu à certains points depuis hier, ignore-les. Pour le reste, les classeurs Excel comme d'habitude, et le nouvel écran pour ce qu'il te demande.

Bonne journée

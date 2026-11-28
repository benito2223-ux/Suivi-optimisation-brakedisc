Objet : Programmes DV 304x28 RPE sur EMAG 1 : temps de coupe analysés et 2 points à corriger aux pupitres

Salut Matis,

Bien reçu les 8 programmes de la gamme complète du 304x28 sur EMAG 1, merci. C’est parfait d'avoir tout envoyé d'un coup, ça permet de caler les temps de coupe réels de la ligne entière et d'aligner le suivi d'optimisation sur ce qui tourne en machine. C'est bien noté pour le 50_1 qui correspond à l'OP40 côté droit, on l'a rattaché directement.

J'ai passé les programmes au crible pour mesurer les temps de coupe purs (hors temps morts) et vérifier la surveillance Montronix. Globalement la gamme est très propre, mais il y a deux coquilles de programmation et deux écarts entre les deux côtés qu'il faut que tu voies avec les méthodes ou les régleurs :

1. Le point critique : surveillance Montronix désactivée sur la finition piste OP40 gauche (L140_1)
Sur le poste straddle T549 (finition des deux faces de piste), la passe d'usinage est coupée en deux : de X307 à X236, puis de X236 à X165. Le problème, c'est que la balise M870 n'est appelée qu'à la deuxième moitié (à X165).
Résultat : la première passe (de X307 à X236, soit 8 secondes de coupe dans la matière) tourne complètement hors surveillance Montronix. Si une plaquette casse ou s'écaille en début de passe, le système ne verra rien. Il faut simplement remonter la ligne M870 avant le premier G1 à X307, exactement comme c'est fait sur le côté droit (L150_1).

2. Écart de vitesse sur la finition piste (T549)
Toujours sur cette finition de piste, le côté gauche est programmé à Vc 650 m/min alors que le côté droit tourne à Vc 750 m/min (avec la même avance f 0,35). Le côté gauche met 14 secondes à surfacer contre 12 secondes à droite. On peut aligner la gauche à 750 m/min sans risque pour récupérer ces 2 secondes.

3. OP20 : 5,7 secondes à récupérer sur le côté droit (T521)
Sur l'ébauche extérieure T521, le côté gauche tourne avec notre essai validé à Vc 1500 m/min et f 0,35 (3,7 s de coupe). Le côté droit est resté sur l'ancien réglage à Vc 800 m/min et f 0,30 (8,2 s de coupe). L'usure relevée étant strictement identique entre les deux côtés, on peut basculer le côté droit à Vc 1500 : c'est 5,7 secondes de gagnées nettes sur le cycle de l'OP20 droite.

4. Balise commentée en OP10 côté droit (L110_2_CBN)
Sur le poste T513 D1 (dégagement bol et épaulement), la balise est écrite « ;M870 » avec un point-virgule à la ligne N510. L'outil fait sa passe (1,5 s) sans surveillance d'effort. À décommenter si vous souhaitez que Montronix suive l'effort sur ce dégagement.

5. Outil réel en OP10 : T515 et non T517
Sur certains plans de phase théoriques, le poste d'ébauche intérieure était noté T517. En machine, c'est bien le poste T515 qui est appelé (en plaquettes carrées S-Platte R1.6). J'ai mis à jour notre nomenclature pour que nos fiches collent à la réalité de la tourelle.

Pour tes chiffres, voici les temps de coupe purs par opération (mesurés dans la matière) :
- OP10 : 25,4 s à gauche / 24,6 s à droite
- OP20 : 31,0 s à gauche (avec Vc 1500) / 36,7 s à droite (avec Vc 800)
- OP30 (perçage) : 9,1 s à gauche / 9,0 s à droite (5 trous Ø13,1 à 2500 tr/min + 3 trous Ø8,6 à 3700 tr/min)
- OP40 : 20,6 s réels à gauche / 18,9 s à droite

Je t'ai préparé le récapitulatif complet poste par poste avec toutes les conditions et les cotes dans un tableau Excel, dis-moi si tu veux que je te le pose ou si tu veux qu'on passe en revue les deux lignes de programme à modifier directement aux pupitres.

Bonne fin de journée,
Benjamin

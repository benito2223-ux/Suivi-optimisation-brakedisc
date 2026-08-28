# Suivi_optimisation_SPK

Outil de suivi d'essais et de bilan économique — plaquettes, outils, conditions de coupe.

Développé par **Benjamin Rouquette** (SPK by CeramTec) pour le projet OP10 — Stellantis Sept Fons.

## Ce que c'est

Un fichier HTML unique (`bilan_economique.html`), sans dépendance serveur ni base de données :
il s'ouvre directement dans un navigateur et fonctionne à 100 % en local. Aucune donnée saisie
ne quitte le poste de l'utilisateur — tout est stocké dans le navigateur (`localStorage`), avec
export/import manuel au format `.json` pour l'échange entre collègues.

Hiérarchie des données : **Ligne de production → Référence disque → OP → Scénario → Essai → Prélèvement**.

## Utilisation

Ouvrir `bilan_economique.html` dans un navigateur (Edge, Chrome...), ou accéder à la version
hébergée (URL communiquée en interne). Le mode d'emploi complet est dans
[`Suivi_optimisation_SPK_Mode_emploi.pdf`](./Suivi_optimisation_SPK_Mode_emploi.pdf).

## Confidentialité

Ce dépôt est privé. Les données d'essais réelles (prix, paramètres process, résultats) ne sont
**jamais** versionnées ici — seul le code de l'outil l'est. Échange de données entre utilisateurs
uniquement via export/import `.json`, en dehors de Git.

## Développement

Fichier unique, vanilla HTML/CSS/JS, aucune dépendance de build. Toute modification se teste en
ouvrant directement `bilan_economique.html` dans un navigateur.

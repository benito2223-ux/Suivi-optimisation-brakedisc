# VERROU — qui travaille sur `bilan_economique.html` en ce moment

> **But** : empêcher deux sessions d'écrire dans le même fichier en même temps. C'est la
> seule règle qui protège le reste : tout le travail d'octobre dernier tient dans ce
> fichier, et une collision silencieuse le corrompt sans laisser de trace.
>
> **Le principe** : si cette ligne est vide, personne ne travaille sur le code. Si
> elle est remplie, **personne d'autre ne touche au fichier** jusqu'à la libération.

---

## Verrou actuel

| | |
|---|---|
| **Auteur** | Z Code |
| **Pris le** | 01/10/2026 |
| **Écrit dans** | `proto/` (verrou élargi) — `bilan_economique.html` **intact** |
| **Version visée** | proto v1.0 — import des JSON de l'ancienne version |
| **Sujet** | Tour 54 — reprendre les essais déjà faits, CPP plaquettes sur les données réelles |

⚠️ **Verbalet pour `proto/`, pas pour `bilan_economique.html`.** L'app de production
n'est pas écrite pendant ce tour. Empreinte de contrôle notée avant de commencer :
`bf2e81a3998d4d9721c728eaaf666d1f7137fe1a5e5ea651440a65ea4eaf97ca`.

---

## Comment ça marche

**Avant d'écrire la première ligne de code :**

1. tu remplis le tableau ci-dessus (auteur, heure, fichier, version visée, sujet) ;
2. tu **commites** ce changement — le verrou est donc dans l'historique, visible par tous ;
3. tu n'écris plus dans `bilan_economique.html` tant que le verrou est à toi.

**En fin de tour :**

1. tu vides le tableau (auteur → *(libre)*) ;
2. tu commites ;
3. ton tour est écrit dans `ECHANGES.md`, dans le même commit.

**Si le verrou est pris et que tu dois absolument écrire** : demande à l'autre session
de libérer, ou passe par Benjamin. **Ne contourne pas** — c'est exactement le geste qui a
coûté une session le 29/09.

---

## Pourquoi un verrou et pas une conversation

Parce que « je te préviens que je travaille » repose sur quelqu'un pour le dire, et
quoique quelqu'un oublie — surtout un agent, qui ne « pense pas » à l'étaler. Un fichier
qu'on lit par habitude, ça tient : c'est la première chose qu'on fait au tour.

---

## Variante automatique (proposée, non encore faite)

Le verrou manuel peut être oublié. Une version automatique lèverait deux défauts :

- **empreinte du fichier** : au début d'un tour, on note le SHA-256 de
  `bilan_economique.html` ; en fin de tour, on vérifie qu'il n'a changé que par nous. S'il a
  changé autrement, quelqu'un a écrit hors verrou → on le signale.
- **garde-fou de commit** : un script refuse un commit de `bilan_economique.html` si le
  verrou appartient à quelqu'un d'autre.

À faire quand on aura un vrai besoin — deux sessions qui codent en parallèle sur des
sujets différents. Pas avant : un garde-fou inutilisé est un garde-fou qu'on contourne.

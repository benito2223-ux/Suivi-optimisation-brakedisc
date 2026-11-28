# Sauvegarde automatique du cloud (Supabase) — mise en place le 28/11/2026

**But : les données ne doivent jamais se perdre.** Le cloud Supabase (`sync_shards` = tous les scénarios, essais, arbre ; `checkup_*` ; `sync_blobs` = photos ; etc.) est copié automatiquement, vérifié, et déposé à deux endroits.

## Ce qui tourne
| Quoi | Détail |
|---|---|
| Script | `scripts/backup_supabase_auto.py` (versionné, **sans secret** : jeton lu dans `~/.supabase/access-token`) |
| Planification | Tâche Windows **« SeptFons Backup Supabase »** : tous les jours **12h30** et **18h30**, **5 min après chaque ouverture de session**, rattrape un passage manqué (PC éteint), réseau requis |
| Copie 1 (locale) | `C:\Users\Admin\SeptFons_Backups_local\` (hors dépôt git) |
| Copie 2 (cloud Google) | `Mon Drive\CERAMTEC\Suivi optimisation Sept Fons - Sauvegardes\auto\` (dossier synchronisé par Google Drive pour ordinateur, lecteur `G:`) |
| Fichiers | `supabase_AAAA-MM-JJ_HHMM.json.gz` (≈ 6 Mo) + **`LATEST_supabase.json.gz` toujours remplacé par la dernière version** + `STATUS.txt` (OK / AVERTISSEMENT / ECHEC) |
| Rotation | 14 dernières + 1 par mois sur 12 mois ; pas de doublon si rien n'a changé |
| Contenu | toutes les tables du schéma `public` (sauf `etat_historique`, historique legacy déjà sauvegardé le 26/11 ; option `--full` pour l'inclure) **+ le schéma** : fonctions, politiques RLS, déclencheurs, colonnes, droits |
| Vérification | après écriture, le fichier est relu et chaque table est comparée à un `count(*)` ; écart = **ECHEC** (code 1, `STATUS.txt`) |

## À regarder de temps en temps
- Ouvrir `STATUS.txt` (dans le dossier Drive `auto`) : doit dire **OK** avec une date du jour.
- Sauvegarde manuelle immédiate : `python scripts/backup_supabase_auto.py` (ou clic droit sur la tâche dans le Planificateur de tâches › Exécuter).

## Limites (honnêtes)
- **Le PC doit être allumé** (et Google Drive pour ordinateur lancé) au moins une fois par jour ; sinon la sauvegarde se fait au prochain démarrage. Si Drive n'est pas monté, la copie locale est faite et `STATUS` dit AVERTISSEMENT.
- Une seule machine : si ce PC est perdu, la copie **Google Drive** reste. Pour aller plus loin : activer les sauvegardes quotidiennes de Supabase (plan Pro) ou ajouter une 2e machine.
- **Jamais sur GitHub** : le dépôt est PUBLIC, ces fichiers contiennent des données réelles.

## Restaurer
1. Ouvrir `LATEST_supabase.json.gz` (ou un fichier daté) : `meta` (comptes), `tables` (lignes par table), `schema`.
2. Pour une ligne/un shard perdu : les anciennes versions des shards sont aussi dans `sync_historique` (déclencheur `sync_garder_historique`, 10 révisions).
3. Pour une restauration complète : recréer d'abord le schéma (`schema.fonctions` / `colonnes` / `politiques_rls` / `droits`), puis réinjecter chaque table ; **demander à Claude Code** (il sait faire, en sauvegardant l'état courant avant d'écrire).

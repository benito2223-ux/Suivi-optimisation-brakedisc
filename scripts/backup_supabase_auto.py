#!/usr/bin/env python3
"""Sauvegarde automatique du cloud Supabase du Suivi d'optimisation.

Ce que fait ce script (une exécution = une sauvegarde complète) :
  1. lit TOUTES les tables du schéma public (sauf l'historique legacy `etat_historique`, 107 Mo,
     déjà dans la sauvegarde du 26/11 — option --full pour l'inclure) + le SCHÉMA
     (fonctions, politiques RLS, déclencheurs, colonnes, droits) ;
  2. écrit un fichier compressé  supabase_AAAA-MM-JJ_HHMM.json.gz ;
  3. VÉRIFIE : relit le fichier et compare le nombre de lignes de chaque table avec un
     count(*) fait au moment du dump — sinon ÉCHEC (code de sortie 1, STATUS = ECHEC) ;
  4. dépose la copie à DEUX endroits : un dossier local (hors dépôt git) ET Google Drive
     (dossier synchronisé par Drive pour ordinateur) ; LATEST_supabase.json.gz est
     toujours remplacé par la dernière version ;
  5. rotation : garde les 14 dernières + 1 par mois sur 12 mois ; si rien n'a changé depuis
     la dernière sauvegarde, n'écrit pas de doublon (STATUS le dit) ;
  6. écrit STATUS.txt (OK / ECHEC / AVERTISSEMENT + date) à côté des sauvegardes.

Aucun secret dans ce fichier : le jeton de l'API Supabase est lu dans ~/.supabase/access-token.
NE JAMAIS pousser ces sauvegardes sur GitHub (dépôt public, données réelles).

Usage :  python scripts/backup_supabase_auto.py [--full] [--no-drive]
"""
import datetime as dt
import gzip
import hashlib
import json
import os
import shutil
import sys
import time
import urllib.request

PROJET = "cxjfyaorkkxemjnollnj"
API = f"https://api.supabase.com/v1/projects/{PROJET}/database/query"
LOCAL = os.path.join(os.path.expanduser("~"), "SeptFons_Backups_local")
DRIVE = r"G:\Mon Drive\CERAMTEC\Suivi optimisation Sept Fons - Sauvegardes\auto"
IGNORER = {"etat_historique"}
GARDER_RECENTES, GARDER_MOIS = 14, 12


def jeton():
    with open(os.path.join(os.path.expanduser("~"), ".supabase", "access-token"), encoding="utf-8") as f:
        return f.read().strip()


def sql(requete, essais=3):
    corps = json.dumps({"query": requete}).encode("utf-8")
    for n in range(essais):
        req = urllib.request.Request(API, data=corps, method="POST", headers={
            "Authorization": "Bearer " + jeton(), "Content-Type": "application/json",
            "User-Agent": "spk-backup/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # réseau / limite : on réessaie
            if n == essais - 1:
                raise
            time.sleep(3 * (n + 1))


def dump_table(t, total):
    """Lit une table par paquets ; réduit le paquet si la réponse est trop grosse."""
    lignes, pas, deb = [], 200, 0
    while deb < total:
        try:
            rep = sql(f'select coalesce(jsonb_agg(to_jsonb(x)), \'[]\'::jsonb) as r from '
                      f'(select * from public."{t}" order by ctid offset {deb} limit {pas}) x')
            paquet = rep[0]["r"]
            if isinstance(paquet, str):
                paquet = json.loads(paquet)
        except Exception:
            if pas == 1:
                raise
            pas = max(1, pas // 4)
            continue
        lignes.extend(paquet)
        deb += pas
    return lignes


def schema():
    req = {
        "fonctions": "select p.proname as nom, pg_get_functiondef(p.oid) as def from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.prokind in ('f','p') order by 1",
        "politiques_rls": "select tablename, policyname, cmd, roles, qual, with_check from pg_policies where schemaname='public' order by 1,2",
        "declencheurs": "select c.relname as table_name, t.tgname, pg_get_triggerdef(t.oid) as def from pg_trigger t join pg_class c on c.oid=t.tgrelid join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and not t.tgisinternal order by 1,2",
        "colonnes": "select table_name, column_name, data_type, column_default, is_nullable from information_schema.columns where table_schema='public' order by table_name, ordinal_position",
        "droits": "select grantee, table_name, privilege_type from information_schema.role_table_grants where table_schema='public' order by 1,2,3",
    }
    return {k: sql(v) for k, v in req.items()}


def principal(complet=False, drive=True):
    maintenant = dt.datetime.now()
    horodatage = maintenant.strftime("%Y-%m-%d_%H%M")
    os.makedirs(LOCAL, exist_ok=True)
    noms = [r["tablename"] for r in sql("select tablename from pg_tables where schemaname='public' order by 1")]
    noms = [n for n in noms if complet or n not in IGNORER]
    comptes, tables = {}, {}
    for t in noms:
        comptes[t] = int(sql(f'select count(*) as n from public."{t}"')[0]["n"])
        tables[t] = dump_table(t, comptes[t])
    contenu = {"tables": tables, "schema": schema()}
    brut_tables = json.dumps(tables, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    empreinte = hashlib.sha256(brut_tables.encode("utf-8")).hexdigest()
    meta = {"projet": PROJET, "date": maintenant.isoformat(timespec="seconds"), "comptes": comptes,
            "empreinte_tables": empreinte, "ignore": [] if complet else sorted(IGNORER)}
    doc = {"meta": meta, **contenu}
    nom = f"supabase_{horodatage}.json.gz"
    chemin_local = os.path.join(LOCAL, nom)
    with gzip.open(chemin_local, "wt", encoding="utf-8", compresslevel=6) as f:
        json.dump(doc, f, ensure_ascii=False)
    # vérification : on relit le fichier écrit et on compare aux count(*)
    with gzip.open(chemin_local, "rt", encoding="utf-8") as f:
        relu = json.load(f)
    ecarts = [t for t in noms if len(relu["tables"].get(t, [])) != comptes[t]]
    if ecarts:
        os.remove(chemin_local)
        raise RuntimeError("écart de lignes sur : " + ", ".join(ecarts))
    # pas de doublon si rien n'a changé depuis la dernière sauvegarde
    derniere = os.path.join(LOCAL, "derniere_empreinte.txt")
    ancienne = open(derniere).read().strip() if os.path.exists(derniere) else ""
    inchange = (ancienne == empreinte)
    cibles = [LOCAL]
    avert = ""
    if drive:
        if os.path.isdir(os.path.dirname(DRIVE)):
            os.makedirs(DRIVE, exist_ok=True)
            cibles.append(DRIVE)
        else:
            avert = "Google Drive (G:) indisponible : copie locale seulement"
    for dossier in cibles:
        if not inchange and dossier != LOCAL:
            shutil.copy2(chemin_local, os.path.join(dossier, nom))
        shutil.copy2(chemin_local, os.path.join(dossier, "LATEST_supabase.json.gz"))   # la dernière remplace l'ancienne
    if inchange:
        os.remove(chemin_local)
    else:
        open(derniere, "w").write(empreinte)
    for dossier in cibles:
        rotation(dossier)
    total = sum(comptes.values())
    etat = ("AVERTISSEMENT" if avert else "OK")
    msg = (f"{etat} {meta['date']} - {len(noms)} tables, {total} lignes, "
           f"{'inchange depuis la derniere sauvegarde (pas de doublon)' if inchange else nom}"
           + (f" - {avert}" if avert else ""))
    ecrire_status(cibles, msg)
    return 0


def rotation(dossier):
    fichiers = sorted(f for f in os.listdir(dossier) if f.startswith("supabase_") and f.endswith(".json.gz"))
    gardes = set(fichiers[-GARDER_RECENTES:])
    par_mois = {}
    for f in fichiers:
        par_mois.setdefault(f[9:16], f)          # le premier de chaque mois
    for m in sorted(par_mois)[-GARDER_MOIS:]:
        gardes.add(par_mois[m])
    for f in fichiers:
        if f not in gardes:
            os.remove(os.path.join(dossier, f))


def ecrire_status(cibles, msg):
    for dossier in cibles:
        try:
            with open(os.path.join(dossier, "STATUS.txt"), "w", encoding="utf-8") as f:
                f.write(msg + "\n")
        except OSError:
            pass
    with open(os.path.join(LOCAL, "backup.log"), "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)


if __name__ == "__main__":
    try:
        sys.exit(principal(complet="--full" in sys.argv, drive="--no-drive" not in sys.argv))
    except Exception as e:
        os.makedirs(LOCAL, exist_ok=True)
        ecrire_status([LOCAL] + ([DRIVE] if os.path.isdir(DRIVE) else []),
                      f"ECHEC {dt.datetime.now().isoformat(timespec='seconds')} - {type(e).__name__}: {e}")
        sys.exit(1)

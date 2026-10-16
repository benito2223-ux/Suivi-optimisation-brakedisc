# -*- coding: utf-8 -*-
"""Corrige le mapping ISO/MABEC des scénarios « base excel ».

Source excel : colonne ISO -> logement.ref (référence plaquette)
               colonne MABEC/MM -> logement.codeArticle (Art. Stellantis)
Les scénarios « base excel » sont reconstruits depuis l'excel ; tout le reste
de l'arbre cloud (scénarios Matis/Benjamin, essais, cibles, complétions) est
préservé tel quel.
"""
import openpyxl, json, re, sys, subprocess

P = r"C:\Users\Admin\Downloads\SUIVI DES CONSOMMATIONS LIGNES EMAG - 14-09-26 au 21-09-26.xlsm"
wb = openpyxl.load_workbook(P, data_only=True)

COMMUNES = {
    "Cout pièce E1 356x26 RPI": ("EMAG 1", "DV 356x26 RPI"),
    "Cout pièce H 302x26 RPI": ("HESSAPP", "DV302x26RPI"),
}
NOUVELLES = {
    "EMAG 1": [("DV 304x28 RPE", "Cout pièce E1 304x28 RPE")],
    "EMAG 2": [("DP 290x12", "Coût pièce E2 290x12"), ("DP 330x14", "Cout pièce E2 330x14")],
    "EMAG 3": [("DV 330x28 RPE K0", "Cout pièce E3 330x28 RPE K0")],
}

def natif(v):
    return re.sub(r"dv|dp", "", str(v or "").lower()).replace(" ", "").replace(".", "").replace("_", "").replace("-", "").strip()

def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower() if s is not None else ""

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def op_de(outil):
    n = str(outil)
    if re.match(r"T543|T546|T548|T549", n):
        return "OP40"
    if re.match(r"T533$|T535$", n):
        return "OP30"
    return "OP10"

NOMS_OP = {"OP10": ["op10", "ebauche"], "OP30": ["per", "30"], "OP40": ["op40", "finition"]}

def extraire(onglet):
    ws = wb[onglet]
    rows = list(ws.iter_rows(values_only=True))
    head_i, cols = None, {}
    for i, row in enumerate(rows[:10]):
        cells = [norm(c) for c in row]
        if "correcte" in " ".join(cells):
            head_i = i
            for j, c in enumerate(cells):
                if "correcte" in c: cols["outil"] = j
                elif c.startswith("opération"): cols["op"] = j
                elif c == "iso": cols["iso"] = j
                elif "mabec" in c or c == "mm": cols["mabec"] = j
                elif "aretes" in c: cols["aretes"] = j
                elif "prix uht" in c: cols["prix"] = j
                elif "ddv" in c: cols["ddv"] = j
                elif "cpp" in c and "actuel" in c: cols["cpp"] = j
            break
    prod = None
    for row in rows[:head_i]:
        if norm(row[0]) == "production":
            prod = num(row[1])
            break
    lignes = []
    for row in rows[head_i + 1:]:
        n = row[cols["outil"]]
        if n is None or norm(n) == "":
            continue
        prix, ddv = num(row[cols["prix"]]), num(row[cols["ddv"]])
        if not prix or not ddv:
            continue
        aretes = num(row[cols["aretes"]]) if "aretes" in cols else None
        cpp = num(row[cols["cpp"]]) if "cpp" in cols else None
        if cpp and cpp > 0:
            aretes = round(prix / (cpp * ddv), 2)
        lignes.append({
            "numero": str(n).strip(),
            "iso": (str(row[cols["iso"]]).strip() if "iso" in cols and row[cols["iso"]] else ""),
            "mabec": (str(row[cols["mabec"]]).strip() if "mabec" in cols and row[cols["mabec"]] else ""),
            "prix": prix, "aretes": aretes, "charniere": ddv, "op": op_de(str(n).strip()),
        })
    # regroupement multi-logements par numéro exact, dédoublonnage strict
    outils = []
    for lo in lignes:
        o = next((x for x in outils if x["numero"] == lo["numero"]), None)
        lg = {"nom": "Plaquette", "ref": lo["iso"], "codeArticle": lo["mabec"],
              "prix": lo["prix"], "aretes": lo["aretes"], "charniere": lo["charniere"],
              "vc": "", "f": "", "suiviTolerance": True}
        if o is None:
            outils.append({"numero": lo["numero"], "iso": lo["iso"], "op": lo["op"], "logements": [lg]})
        elif not any(x["ref"] == lg["ref"] and x["codeArticle"] == lg["codeArticle"]
                     and x["prix"] == lg["prix"] and x["charniere"] == lg["charniere"]
                     and x["aretes"] == lg["aretes"] for x in o["logements"]):
            o["logements"].append(lg)
    return prod, outils

# arbre source : cloud courant (passe en argument via stdin json) ou fichier
src = json.loads(sys.stdin.read())

ids = set()
def collecter(o):
    if isinstance(o, dict):
        if "id" in o and o["id"]:
            ids.add(str(o["id"]))
        for v in o.values():
            collecter(v)
    elif isinstance(o, list):
        for v in o:
            collecter(v)
collecter(src)
def id_unique(p):
    i = 1
    while "%s-%03d" % (p, i) in ids:
        i += 1
    ident = "%s-%03d" % (p, i)
    ids.add(ident)
    return ident

def trouve_ligne(nom):
    return next((l for l in src["lignes"] if natif(l["nom"]) == natif(nom)), None)

def remplace_scenarios_excel(onglet):
    """remplace les outils des scénarios « base excel » de la réf/ligne, OP par OP."""
    prod, outils = extraire(onglet)
    par_op = {}
    for o in outils:
        par_op.setdefault(o["op"], []).append(o)
    stats = []
    return par_op, prod, stats

# 1. communes : remplacer dans les scénarios existants « base excel »
n_sc, n_lg = 0, 0
for onglet, (lnom, rnom) in COMMUNES.items():
    par_op, prod, _ = remplace_scenarios_excel(onglet)
    lc = trouve_ligne(lnom)
    rc = next(r for r in lc["references"] if natif(r["nom"]) == natif(rnom))
    for opk, liste in par_op.items():
        motifs = NOMS_OP[opk]
        op = next((o for o in rc["ops"] if any(m in (o.get("nom") or "").lower() for m in motifs)), None)
        if op is None:
            continue
        for sc in list(op["scenarios"]):
            if not re.search("base excel", sc.get("name") or "", re.I):
                continue
            nouveaux = []
            for t in liste:
                lg2 = []
                for g in t["logements"]:
                    lg2.append(dict(g, id=id_unique("g-n")))
                nouveaux.append({"id": id_unique("t-n"), "numero": t["numero"],
                                 "description": t["iso"], "logements": lg2})
            for i, t in enumerate(nouveaux):
                if i > 0 and re.match(r"T549", t["numero"]) and re.match(r"T548", nouveaux[i - 1]["numero"]):
                    t["simultaneAvecPrecedent"] = True
            sc["outils"] = nouveaux
            n_sc += 1
            n_lg += sum(len(t["logements"]) for t in nouveaux)

# 2. nouvelles : idem sur leurs OPs
for lnom, refs in NOUVELLES.items():
    lc = trouve_ligne(lnom)
    for rnom, onglet in refs:
        par_op, prod, _ = remplace_scenarios_excel(onglet)
        rc = next(r for r in lc["references"] if natif(r["nom"]) == natif(rnom))
        for opk, liste in par_op.items():
            motifs = NOMS_OP[opk]
            op = next((o for o in rc["ops"] if any(m in (o.get("nom") or "").lower() for m in motifs)), None)
            if op is None:
                continue
            for sc in list(op["scenarios"]):
                if not re.search("base excel", sc.get("name") or "", re.I):
                    continue
                nouveaux = []
                for t in liste:
                    lg2 = [dict(g, id=id_unique("g-n")) for g in t["logements"]]
                    nouveaux.append({"id": id_unique("t-n"), "numero": t["numero"],
                                     "description": t["iso"], "logements": lg2})
                for i, t in enumerate(nouveaux):
                    if i > 0 and re.match(r"T549", t["numero"]) and re.match(r"T548", nouveaux[i - 1]["numero"]):
                        t["simultaneAvecPrecedent"] = True
                sc["outils"] = nouveaux
                n_sc += 1
                n_lg += sum(len(t["logements"]) for t in nouveaux)

print("scénarios excel reconstruits :", n_sc, "· logements corrigés :", n_lg, file=sys.stderr)
json.dump(src, sys.stdout, ensure_ascii=False)

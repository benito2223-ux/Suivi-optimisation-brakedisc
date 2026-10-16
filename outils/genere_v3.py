# -*- coding: utf-8 -*-
"""Générateur v3 : cloud Matis intact + excel ventilé par OP réelles + simultané T548/T549."""
import openpyxl, json, re, os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = r"C:\Users\Admin\Downloads\SUIVI DES CONSOMMATIONS LIGNES EMAG - 14-09-26 au 21-09-26.xlsm"
wb = openpyxl.load_workbook(P, data_only=True)

ONGLETS = {
    "EMAG 1": [("DV 304x28 RPE", 0.212, "Cout pièce E1 304x28 RPE")],
    "EMAG 2": [("DP 290x12", 0.232, "Coût pièce E2 290x12"), ("DP 330x14", 0.384, "Cout pièce E2 330x14")],
    "EMAG 3": [("DV 330x28 RPE K0", 0.218, "Cout pièce E3 330x28 RPE K0")],
}
COMMUNES = {
    "Cout pièce E1 356x26 RPI": ("EMAG 1", "DV 356x26 RPI", 0.575),
    "Cout pièce H 302x26 RPI": ("HESSAPP", "DV302x26RPI", 0.129),
}
NOMS_OP = {"OP10": "OP10 Ebauche piste", "OP30": "OP 30 Perçages", "OP40": "OP40 Finition Pistes"}

def norm(s): return re.sub(r"\s+"," ",str(s)).strip().lower() if s is not None else ""
def natif(v): return re.sub(r"dv|dp","",str(v or "").lower()).replace(" ","").replace(".","").replace("_","").replace("-","").strip()
def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None
def op_de(outil):
    n = str(outil)
    if re.match(r"T543|T546|T548|T549", n): return "OP40"
    if re.match(r"T533$|T535$", n): return "OP30"
    return "OP10"

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
        if norm(row[0]) == "production": prod = num(row[1]); break
    lignes_outils = []
    for row in rows[head_i+1:]:
        n = row[cols["outil"]]
        if n is None or norm(n) == "": continue
        prix, ddv = num(row[cols["prix"]]), num(row[cols["ddv"]])
        if not prix or not ddv: continue
        aretes = num(row[cols["aretes"]]) if "aretes" in cols else None
        cpp = num(row[cols["cpp"]]) if "cpp" in cols else None
        if cpp and cpp > 0: aretes = round(prix / (cpp * ddv), 2)
        lignes_outils.append({"numero": str(n).strip(),
            "iso": (str(row[cols["iso"]]).strip() if "iso" in cols and row[cols["iso"]] else ""),
            "ref": (str(row[cols["mabec"]]).strip() if "mabec" in cols and row[cols["mabec"]] else ""),
            "prix": prix, "aretes": aretes, "charniere": ddv, "op": op_de(str(n).strip())})
    outils = []
    for lo in lignes_outils:
        o = next((x for x in outils if x["numero"] == lo["numero"]), None)
        lg = {"nom":"Plaquette","ref":lo["ref"],"prix":lo["prix"],"aretes":lo["aretes"],
              "charniere":lo["charniere"],"vc":"","f":"","suiviTolerance":True}
        if o is None:
            outils.append({"numero": lo["numero"], "iso": lo["iso"], "op": lo["op"], "logements": [lg]})
        elif not any(x["ref"]==lg["ref"] and x["prix"]==lg["prix"] and x["charniere"]==lg["charniere"]
                     and x["aretes"]==lg["aretes"] for x in o["logements"]):
            o["logements"].append(lg)
    return prod, outils

cloud = json.load(open(os.path.join(RACINE, "cloud_matis_2026-09-28.json"), encoding="utf-8"))
ids = set()
def collecter(o):
    if isinstance(o, dict):
        if "id" in o and o["id"]: ids.add(str(o["id"]))
        for v in o.values(): collecter(v)
    elif isinstance(o, list):
        for v in o: collecter(v)
collecter(cloud)
def id_unique(p):
    i = 1
    while f"{p}-{i:03d}" in ids: i += 1
    ident = f"{p}-{i:03d}"; ids.add(ident); return ident

LISTE = {"EMAG 1": ["DV 356x26 RPI","DV 304x28 RPE"], "EMAG 2": ["DP 290x12","DP 330x14"],
         "EMAG 3": ["DV 330x28 RPE K0"], "HESSAPP": ["DV302x26RPI"]}
n_sup = 0
for l in cloud["lignes"]:
    aut = {natif(n) for n in LISTE.get(l["nom"], [])}
    avant = len(l["references"])
    l["references"] = [r for r in l.get("references", []) if natif(r.get("nom")) in aut]
    n_sup += avant - len(l["references"])
print("refs supprimées :", n_sup)

def trouver_op(ref, motif):
    return next((o for o in ref["ops"] if motif.lower() in (o.get("nom") or "").lower()), None)

def construire_scenarios_excel(onglet, baseline):
    prod, outils = extraire(onglet)
    par_op = {}
    for o in outils: par_op.setdefault(o["op"], []).append(o)
    out = {}
    for opk, liste in par_op.items():
        outils2 = []
        for t in liste:
            outils2.append({"id": id_unique("t-x"), "numero": t["numero"], "description": t["iso"],
                  "logements": [dict(lg, id=id_unique("g-x")) for lg in t["logements"]]})
        for i, t in enumerate(outils2):
            if i > 0 and re.match(r"T549", t["numero"]) and re.match(r"T548", outils2[i-1]["numero"]):
                t["simultaneAvecPrecedent"] = True
        out[opk] = {"id": id_unique("sc-x"), "name": "Prod actuelle (base excel 2026/2027)",
                    "baseline": baseline, "cycle": 100, "outils": outils2, "essais": [], "scrapLog": []}
    return out, prod

for onglet, (lnom, rnom, cible) in COMMUNES.items():
    scs, prod = construire_scenarios_excel(onglet, False)
    lc = next(l for l in cloud["lignes"] if natif(l["nom"]) == natif(lnom))
    rc = next(r for r in lc["references"] if natif(r["nom"]) == natif(rnom))
    rc["cibleCPP"] = cible
    for opk, sc in scs.items():
        op = trouver_op(rc, {"OP10":"op10","OP30":"perçage","OP40":"op40"}[opk])
        if op is None:
            op = {"id": id_unique("o-x"), "nom": NOMS_OP[opk], "ordre": int(opk[2:]), "scenarios": []}
            rc["ops"].append(op)
        op["scenarios"].append(sc)
        print(f"commune {rnom} : excel {opk} ({len(sc['outils'])} outils) -> « {op['nom']} »")
    if prod: rc["productionAnnuelle"] = rc.get("productionAnnuelle") or prod

lc = next(l for l in cloud["lignes"] if natif(l["nom"]) == natif("EMAG 1"))
rc = next(r for r in lc["references"] if natif(r["nom"]) == natif("DV 356x26 RPI"))
n_sim = 0
for o in rc["ops"]:
    if "op40" in (o.get("nom") or "").lower():
        for sc in o["scenarios"]:
            for i, t in enumerate(sc.get("outils", [])):
                if i > 0 and re.match(r"T549", t.get("numero","")) and re.match(r"T548", sc["outils"][i-1].get("numero","")):
                    t["simultaneAvecPrecedent"] = True; n_sim += 1
print("simultané T549 coché (scénarios Matis OP40) :", n_sim)

for lnom, refs in ONGLETS.items():
    lc = next((l for l in cloud["lignes"] if natif(l["nom"]) == natif(lnom)), None)
    if lc is None:
        lc = {"id": id_unique("l"), "nom": lnom, "references": []}
        cloud["lignes"].append(lc)
    for nom_final, cible, onglet in refs:
        scs, prod = construire_scenarios_excel(onglet, True)
        rc = {"id": id_unique("r-x"), "nom": nom_final, "cibleCPP": cible,
              "productionAnnuelle": prod or "", "ops": []}
        for opk, sc in scs.items():
            rc["ops"].append({"id": id_unique("o-x"), "nom": NOMS_OP[opk], "ordre": int(opk[2:]), "scenarios": [sc]})
        rc["ops"].sort(key=lambda a: a["ordre"] or 0)
        lc["references"].append(rc)
        print("nouvelle ref", nom_final, "->", [(o["nom"], len(o["scenarios"][0]["outils"])) for o in rc["ops"]])

payload = {"outil":"SPK Suivi optimisation","format":8,"toolVersion":"4.46.1",
    "revision": cloud.get("revision",1), "exporteLe":"2026-09-28T20:00:00.000Z",
    "exportePar":"Benjamin Rouquette","lignes": cloud["lignes"],"projets": cloud.get("projets",[]),
    "activeProjetId": cloud.get("activeProjetId"),"responsables": cloud.get("responsables",[]),"backlog": cloud.get("backlog",[])}
with open(os.path.join(RACINE, "suivi_assemble_2026-09-28_v3.json"), "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=1)
n_sc = n_out = n_ess = 0
for l in cloud["lignes"]:
    for r in l["references"]:
        for o in r["ops"]:
            for sc in o["scenarios"]:
                n_sc += 1; n_out += len(sc.get("outils",[])); n_ess += len(sc.get("essais",[]))
print("v3 : %d lignes, %d scénarios, %d outils, %d essais" % (len(cloud["lignes"]), n_sc, n_out, n_ess))

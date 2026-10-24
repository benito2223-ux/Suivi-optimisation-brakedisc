# -*- coding: utf-8 -*-
"""Tour 92 (4.109.1) — la palette de la coque passe au brand guide SPK.
Benjamin : « trop de noir ». Cause : l'auto-designer avait remappé --blue
(sur lequel reposent TOUS les accents de l'app) sur du graphite #23282b,
ajouté un signal orange, des bandeaux head/fill graphite et un fond crème.
Re-mappage complet sur le brand guide : fond neutre clair, surfaces blanches,
bleu #1B5EA6 en identité, rouge #E2001A en alerte, noir en TEXTE seulement.
Le rail graphite devient bleu SPK. Le mode nuit garde ses surfaces sombres
mais récupère un accent bleu lisible (plus d'orange)."""
import io

p = "spk-app.css"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)
compte = 0

def sub(avant, apres, label, count=1):
    global src, compte
    assert avant in src, "ANCRE INTROUVABLE : " + label
    src = src.replace(avant, apres, count)
    compte += 1
    print("ok :", label)

# ── 1. THÈME CLAIR : les tokens au brand guide ──
sub("    --spk-signal: #c2410c;\n    --spk-signal-strong: #9a3412;\n    --spk-signal-soft: #f8e3d7;",
    "    --spk-signal: #1B5EA6;   /* brand guide : le bleu est l'identité */\n    --spk-signal-strong: #154D8A;\n    --spk-signal-soft: #E8F0FB;",
    "signal orange -> bleu SPK")

sub("    --bg: #ece8df;\n    --spk-title-bg: rgba(236, 232, 223, .94);\n    --surface: #faf8f3;\n    --surface-alt: #e7e2d8;\n    --border: #d2ccbf;\n    --ink: #171a1c;\n    --ink-soft: #3d4347;\n    --ink-faint: #5f6569;",
    "    --bg: #e8eaed;   /* le gris neutre de l'app (brand guide : fond clair, noir en texte seulement) */\n    --spk-title-bg: rgba(232, 234, 237, .94);\n    --surface: #ffffff;\n    --surface-alt: #f4f4f4;\n    --border: #e5e5e5;\n    --ink: #1a1a1a;\n    --ink-soft: #4a5560;\n    --ink-faint: #5a6470;",
    "fond crème -> gris neutre, surfaces blanches")

sub("    --blue: #23282b;\n    --blue-dark: #171a1c;\n    --blue-bg: #f1ede4;",
    "    --blue: #1B5EA6;   /* LE bleu de la marque — tous les accents de l'app y reviennent */\n    --blue-dark: #154D8A;\n    --blue-bg: #E8F0FB;",
    "--blue noir -> bleu de la marque")

sub("    --red: #a3261b;\n    --red-dark: #7f1d15;\n    --red-bg: #f6e2df;",
    "    --red: #E2001A;\n    --red-dark: #B8001A;\n    --red-bg: #FCE8EA;",
    "rouge -> rouge CeramTec du guide")

sub("    --green: #2f6f4e;\n    --green-bg: #e3efe7;",
    "    --green: #1a7a3f;\n    --green-bg: #edf7f1;",
    "vert -> vert de l'app (déjà marque)")

sub("    --head: #23282b;\n    --head-ink: #f7f4ed;\n    --head-ink-soft: #c9c4b9;\n    --head-line: rgba(247, 244, 237, 0.18);",
    "    --head: #1B5EA6;   /* le bandeau de tête : le bleu de la marque, texte blanc */\n    --head-ink: #ffffff;\n    --head-ink-soft: rgba(255, 255, 255, 0.78);\n    --head-line: rgba(255, 255, 255, 0.28);",
    "bandeau tête graphite -> bleu SPK")

sub("    --fill: #23282b;\n    --fill-ink: #f7f4ed;\n    --fill-ink-soft: #c9c4b9;\n    --fill-line: rgba(247, 244, 237, 0.22);",
    "    --fill: #1B5EA6;   /* les blocs KPI : bleu de la marque, chiffres blancs */\n    --fill-ink: #ffffff;\n    --fill-ink-soft: rgba(255, 255, 255, 0.8);\n    --fill-line: rgba(255, 255, 255, 0.28);",
    "blocs fill graphite -> bleu SPK")

sub("    --on-accent: #fffdf8;", "    --on-accent: #ffffff;", "blanc chaud -> blanc pur")

# ── 2. THÈME NUIT : surfaces sombres conservées, l'accent orange devient bleu lisible ──
sub("      --blue: #f0733b;\n      --blue-dark: #ffb08a;\n      --blue-bg: #3a2118;",
    "      --blue: #8AB8DD;   /* nuit : un bleu lisible sur fond sombre (plus d'orange) */\n      --blue-dark: #B9D6ED;\n      --blue-bg: #16283c;",
    "nuit : accent orange -> bleu lisible")
sub("      --red: #ef8a7e;\n      --red-dark: #f7b5ad;\n      --red-bg: #3b1e1b;",
    "      --red: #F27B8A;\n      --red-dark: #F7B5AD;\n      --red-bg: #3b1e22;",
    "nuit : rouge lisible")
sub("      --spk-signal: #d4552a;", "      --spk-signal: #8AB8DD;", "nuit : signal -> bleu lisible") if "      --spk-signal: #d4552a;" in src else None

# ── 3. LE RAIL : graphite -> bleu SPK dégradé, signal orange -> blanc ──
sub("  --shell-2: #2a3134;\n  --shell-ink: #f7f4ec;\n  --shell-soft: #aeb6b3;\n  --shell-signal: #d4552a;",
    "  --shell-2: #154D8A;   /* rail : le bleu foncé de la marque */\n  --shell-ink: #ffffff;\n  --shell-soft: rgba(255, 255, 255, 0.72);\n  --shell-signal: #ffffff;",
    "rail graphite -> bleu SPK")

io.open(p, "w", encoding="utf-8").write(src)
print("substitutions:", compte, "| taille:", n0, "->", len(src))

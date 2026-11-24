# -*- coding: utf-8 -*-
"""Extrait les icônes du manifest data: historique de bilan_economique.html
et génère la variante maskable. Usage unique (v4.18) — gardé pour mémoire."""
import base64, io, json, re, sys

HTML = "bilan_economique.html"
with open(HTML, "r", encoding="utf-8") as f:
    src = f.read()

m = re.search(r'<link rel="manifest" href="data:application/manifest\+json;base64,([^"]+)"', src)
if not m:
    sys.exit("manifest data: introuvable (déjà remplacé ?)")
man = json.loads(base64.b64decode(m.group(1)).decode("utf-8"))

for ic in man["icons"]:
    taille = ic["sizes"].split("x")[0]
    data = ic["src"].split("base64,", 1)[1]
    chemin = f"icons/icon-{taille}.png"
    with open(chemin, "wb") as out:
        out.write(base64.b64decode(data))
    print("écrit", chemin, len(data) // 4 * 3, "octets environ")

# variante maskable : fond noir plein bord (couleur de l'icône elle-même) et le logo
# réduit pour tenir dans le cercle de sûreté (80 % du côté). Le carré noir redimensionné
# se fond dans le fond : aucune bordure visible quel que soit le masque (cercle, squircle).
from PIL import Image
img = Image.open("icons/icon-512.png").convert("RGB")
canvas = Image.new("RGB", (512, 512), (0, 0, 0))
interieur = 380
redim = img.resize((interieur, interieur), Image.LANCZOS)
canvas.paste(redim, ((512 - interieur) // 2, (512 - interieur) // 2))
canvas.save("icons/icon-512-maskable.png", "PNG")
print("écrit icons/icon-512-maskable.png")

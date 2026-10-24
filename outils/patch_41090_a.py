# -*- coding: utf-8 -*-
"""Tour 91 (4.109.0) — filigrane de ligne + polices du brand guide SPK.
- la coque tuait le filigrane (body background-image:none !important) ;
- --font-disp / --font-body passent à Open Sans Condensed / Open Sans
  (brand guide : --font-cond / --font), embarquées en base64 (zéro réseau).
"""
import io, re, base64, json, urllib.request

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
n0 = len(src)

# ── 1. les faces embarquées : Open Sans (variable 300-800) + Open Sans Condensed 700 ──
gardes = json.load(io.open("_fonts/liste.json", encoding="utf-8"))
urls = {}
for fam, weight, url in gardes:
    urls.setdefault((fam), url)
faces = []
# Open Sans : le fichier variable couvre 300-800 (même URL pour les 3 graisses)
url_os = urls["Open Sans"]
data = base64.b64encode(urllib.request.urlopen(urllib.request.Request(url_os, headers={"User-Agent": "Mozilla/5.0 Chrome/120"}), timeout=30).read()).decode()
faces.append("@font-face{font-family:'Open Sans';font-style:normal;font-weight:300 800;font-display:swap;src:url(data:font/woff2;base64," + data + ") format('woff2');}")
url_osc = urls["Open Sans Condensed"]
data = base64.b64encode(urllib.request.urlopen(urllib.request.Request(url_osc, headers={"User-Agent": "Mozilla/5.0 Chrome/120"}), timeout=30).read()).decode()
faces.append("@font-face{font-family:'Open Sans Condensed';font-style:normal;font-weight:700;font-display:swap;src:url(data:font/woff2;base64," + data + ") format('woff2');}")
faces_css = "\n".join(faces)

def remplace_fontface(famille):
    global src
    i = src.index("@font-face{font-family:'" + famille + "'")
    j = src.index("}", i) + 1
    return i, j

# remplacer le bloc Manrope par les DEUX faces Open Sans
i, j = remplace_fontface("Manrope")
src = src[:i] + faces_css + src[j:]
print("ok : Manrope remplacée par Open Sans + Open Sans Condensed (base64)")

# retirer le bloc Roboto (le corps passe sur Open Sans, déjà embarquée)
i, j = remplace_fontface("Roboto")
src = src[:i] + src[j:]
print("ok : bloc Roboto retiré")

# ── 2. les tokens de police ──
avant = "--font-disp:'Manrope','Archivo',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;"
apres = "--font-disp:'Open Sans Condensed','Open Sans',Arial,sans-serif;  /* v4.109 — brand guide SPK : --font-cond (titres, chiffres) */"
assert avant in src
src = src.replace(avant, apres, 1)
print("ok : --font-disp")

avant = "--font-body:'Roboto',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;"
apres = "--font-body:'Open Sans',Arial,sans-serif;  /* v4.109 — brand guide SPK : --font (corps, UI) */"
assert avant in src
src = src.replace(avant, apres, 1)
print("ok : --font-body")

# fallback 'Archivo' restants (filigrane, autres usages)
src = src.replace("font-family='Archivo,Arial,sans-serif'", "font-family='Open Sans Condensed,Arial,sans-serif'")
print("ok : filigrane en Open Sans Condensed")

io.open(p, "w", encoding="utf-8").write(src)
print("taille:", n0, "->", len(src))

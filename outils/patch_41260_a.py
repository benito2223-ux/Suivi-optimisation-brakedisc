# -*- coding: utf-8 -*-
"""Tour 103 — v4.126.0 — LOT 1 du brief complémentaire (priorité 1).

La vérification de version fetchait le HTML COMPLET (~1,8 Mo) toutes les
60 s — ~0,9 Go par journée de 8 h et par poste — et reloadait sans aucune
garde (perte possible de la dernière saisie, boucle possible si le serveur
sert deux versions). Fix :
  1. build-coque.mjs publie `dist/version.json` = {"v":"…"} (quelques octets) ;
  2. le fetch porte sur version.json — si absent (ancien déploiement), échec
     silencieux ;
  3. fréquence : 10 minutes + au retour d'onglet (plus à 60 s) ;
  4. le reload n'arrive que si : aucun champ de saisie n'a le focus, la
     sauvegarde est flushée (saveData appelée), et l'anti-boucle en
     sessionStorage a vu moins de 2 recharges pour cette version —
     sinon un bandeau « Nouvelle version disponible — Recharger ». """
import io

# ── 1. build-coque.mjs : version.json ────────────────────────────────────────
p = "outils/build-coque.mjs"
s = io.open(p, encoding="utf-8").read()


def remplace(fichier, avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(p,
"""  fins de ligne : CRLF (d origine)""",
"""  fins de ligne : CRLF (d origine)""") if False else None

# lire la version dans le HTML source et écrire version.json à côté
if "version.json" not in s:
    ancre = "fs.writeFileSync(path.join(DIST, '.surgeignore'), SURGEIGNORE, 'utf8');"
    ajout = """fs.writeFileSync(path.join(DIST, '.surgeignore'), SURGEIGNORE, 'utf8');

/* v4.126 (LOT 1 du brief complémentaire) — version.json : quelques octets que
   la page fetch pour détecter une nouvelle version, au lieu du HTML complet
   (~1,8 Mo) toutes les 60 s. La version lue dans le SOURCE, jamais une
   constante à maintenir à la main. */
const mVersion = html.match(/TOOL_VERSION\\s*=\\s*"([^"]+)"/);
fs.writeFileSync(path.join(DIST, 'version.json'),
  JSON.stringify({ v: mVersion ? mVersion[1] : '' }), 'utf8');"""
    assert s.count(ancre) == 1
    s = s.replace(ancre, ajout, 1)
    io.open(p, "w", encoding="utf-8").write(s)
    print("ok : build-coque génère version.json")
else:
    print("déjà présent")

# ── 2. bilan_economique.html : le vérificateur gardé et économe ──────────────
p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)

remplace(p,
"""  async function _spkVerifierVersion(){
    try{
      const r = await fetch("./bilan_economique.html", { cache: "no-store" });
      const txt = await r.text();
      const m = txt.match(/TOOL_VERSION\\s*=\\s*"([^"]+)"/);
      const serveur = m ? m[1] : null;
      if(!serveur) return;
      const locale = (typeof TOOL_VERSION !== "undefined") ? TOOL_VERSION : null;
      if(!locale) return;
      if(serveur !== locale){
        /* la page est plus ancienne que ce qui est servi : on purge et on
           recharge. Sans cela, l'utilisateur reste sur l'ancienne version
           jusqu'au prochain rechargement manuel. */
        if(window.caches && window.caches.keys){
          const cles = await window.caches.keys();
          await Promise.all(cles.map((c) => window.caches.delete(c)));
        }
        location.reload();
      }
    }catch(e){}
  }""",
"""  /* v4.126 (LOT 1 du brief complémentaire) — la vérification fetch un
     version.json de quelques octets (publié par le build) au lieu du HTML
     complet ; elle ne recharge que si AUCUNE saisie n'a le focus, après une
     sauvegarde flushée, et au plus 2 fois par version cible (anti-boucle en
     sessionStorage) — sinon un bandeau « Recharger » non bloquant. */
  function _spkSaisieAuFocus(){
    const ae = document.activeElement;
    return !!(ae && (ae.tagName === "INPUT" || ae.tagName === "TEXTAREA" || ae.tagName === "SELECT" || ae.isContentEditable));
  }
  function _spkMajBandeau(){
    if(document.getElementById("spkMajBand")) return;
    const b = document.createElement("div");
    b.id = "spkMajBand";
    b.style.cssText = "position:fixed; top:0; left:50%; transform:translateX(-50%); z-index:200; background:var(--fill,#1B5EA6); color:#fff; padding:9px 16px; border-radius:0 0 4px 4px; font-size:12.5px; box-shadow:0 4px 14px rgba(0,0,0,.25); display:flex; gap:12px; align-items:center;";
    b.innerHTML = '<span>Nouvelle version disponible — enregistre puis recharge pour l\\'appliquer.</span>';
    const btn = document.createElement("button");
    btn.textContent = "Recharger";
    btn.style.cssText = "background:#fff; color:var(--fill,#1B5EA6); border:none; border-radius:3px; padding:5px 12px; font-weight:600; cursor:pointer;";
    btn.addEventListener("click", () => { try{ saveData(); }catch(e){} location.reload(); });
    b.appendChild(btn);
    document.body.appendChild(b);
  }
  async function _spkVerifierVersion(){
    try{
      const r = await fetch("./version.json", { cache: "no-store" });
      if(!r.ok) return;                       /* ancien déploiement : rien à comparer */
      const j = await r.json();
      const serveur = j && j.v ? j.v : null;
      if(!serveur) return;
      const locale = (typeof TOOL_VERSION !== "undefined") ? TOOL_VERSION : null;
      if(!locale) return;
      if(serveur === locale) return;
      /* la page est plus ancienne que ce qui est servi. Le reload ne part
         QUE si le poste peut le faire sans risque : pas de saisie au focus,
         sauvegarde flushée, anti-boucle < 2 sur cette version cible. */
      if(_spkSaisieAuFocus()){ _spkMajBandeau(); return; }
      try{ saveData(); }catch(e){}
      const cle = "spk_maj_recharges_" + serveur;
      let n = 0;
      try{ n = parseInt(sessionStorage.getItem(cle) || "0", 10) || 0; }catch(e){}
      if(n >= 2){ _spkMajBandeau(); return; }
      try{ sessionStorage.setItem(cle, String(n + 1)); }catch(e){}
      if(window.caches && window.caches.keys){
        const cles = await window.caches.keys();
        await Promise.all(cles.map((c) => window.caches.delete(c)));
      }
      location.reload();
    }catch(e){}
  }""",
"2. le vérificateur économe et gardé")

remplace(p,
"""    if(_spkSW.timer) clearInterval(_spkSW.timer);
    _spkSW.timer = setInterval(() => { _spkForcerMAJ(); _spkVerifierVersion(); }, 60000);
    document.addEventListener("visibilitychange", () => {
      if(document.visibilityState === "visible"){ _spkForcerMAJ(); _spkVerifierVersion(); }
    });""",
"""    if(_spkSW.timer) clearInterval(_spkSW.timer);
    /* v4.126 : 10 minutes (plus 60 s) — la vérif ne pèse plus rien en données,
       et le retour d'onglet reste un déclencheur. */
    _spkSW.timer = setInterval(() => { _spkVerifierVersion(); }, 600000);
    document.addEventListener("visibilitychange", () => {
      if(document.visibilityState === "visible"){ _spkVerifierVersion(); }
    });""",
"3. la fréquence : 10 min + retour d'onglet")

# ── 3. version + NOUVEAUTES ──────────────────────────────────────────────────
assert s.count('const TOOL_VERSION = "4.125.1";') == 1
s = s.replace('const TOOL_VERSION = "4.125.1";', 'const TOOL_VERSION = "4.126.0";', 1)
print("ok : TOOL_VERSION")

ancre = 'const NOUVEAUTES = [\n'
assert s.count(ancre) == 1
entree = (
    '  { version:"4.126.0", date:"28/10/2026", points:[\n'
    '    "<b>La mise à jour ne pèse plus rien et ne coupe plus la saisie.</b> La vérification de nouvelle version reposait sur le re-téléchargement de l\\u2019outil complet toutes les 60 secondes (~1,8 Mo — près d\\u20191 Go par journée de 8 h et par poste) et rechargeait sans prévenir. Désormais elle lit un <b>version.json de quelques octets</b>, toutes les 10 minutes et au retour d\\u2019onglet ; si une nouvelle version existe pendant une saisie, un <b>bandeau discret propose de recharger</b> au lieu de couper — la sauvegarde est flushée avant tout rechargement automatique."\n'
    '  ]},\n'
)
s = s.replace(ancre, ancre + entree, 1)
print("ok : entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch html posé :", n0, "->", len(s))

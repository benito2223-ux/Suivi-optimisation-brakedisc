# -*- coding: utf-8 -*-
# Tour 108 — 4.129.1 — patch A : le source
# 1. TOOL_VERSION 4.129.0 -> 4.129.1
# 2. La porte TDZ (v4.112.1) n'utilise plus `global` (Node-only) : l'exception
#    « global is not defined » interrompait la suite entière au navigateur
#    (constat Benjamin, 471/472). globalThis + sonde : quand la substitution
#    localStorage ne prend pas (l'accesseur de window n'a pas de setter),
#    la porte le DIT au lieu d'échouer — elle est jouée pour de vrai au
#    harnais, où la substitution marche.
# 3. Le plancher atelier 56 px couvre tout élément saisissable ou cliquable :
#    inputs (texte, nombre), textarea, summary, .pcb-op, et les cases à
#    cocher (boîte 56 px, la case reste dessinée 28 px par
#    background-clip:content-box).
# 4. Entrée NOUVEAUTES.
import io

F = "bilan_economique.html"
src = io.open(F, encoding="utf-8").read()

def remplacer(avant, apres, label):
    global src
    n = src.count(avant)
    assert n == 1, "ancre %s : %d occurrences (attendu 1)" % (label, n)
    src = src.replace(avant, apres)
    print("ok  " + label)

# --- 1. version -------------------------------------------------------------
remplacer('const TOOL_VERSION = "4.129.0";',
          'const TOOL_VERSION = "4.129.1";', "TOOL_VERSION")

# --- 2. la porte TDZ navigable ----------------------------------------------
AVANT_TDZ = """        const mem = {};
        const lsAvant = localStorage;
        global.localStorage = { getItem: k => (k in mem ? mem[k] : null),
                                setItem: (k, v) => { mem[k] = String(v); },
                                removeItem: k => { delete mem[k]; },
                                clear: () => { Object.keys(mem).forEach(k => delete mem[k]); } };"""
APRES_TDZ = """        const mem = {};
        const lsAvant = localStorage;
        /* v4.129.1 — globalThis et non `global` : au navigateur, `global`
           n'existe pas — l'exception interrompait la suite entière ici
           (constat Benjamin, 471/472). Reste une différence
           d'environnement : l'accesseur localStorage de window n'a pas de
           setter, l'assignation y est sans effet — la sonde le détecte et
           la porte l'annonce au lieu d'échouer ; la substitution réelle
           est jouée par le harnais (globalThis === global en CommonJS). */
        const lsFaux = { getItem: k => (k in mem ? mem[k] : null),
                         setItem: (k, v) => { mem[k] = String(v); },
                         removeItem: k => { delete mem[k]; },
                         clear: () => { Object.keys(mem).forEach(k => delete mem[k]); } };
        globalThis.localStorage = lsFaux;
        /* la sonde passe par la GLOBALE, pas par lsFaux : lsFaux.setItem
           écrit toujours dans mem — elle ne prouve rien. Si la globale
           n'a pas changé (accesseur window sans setter), le setItem atterrit
           dans le vrai localStorage (clé _sonde, retirée aussitôt) et mem
           reste vide : lsSubstitue dit la vérité. */
        localStorage.setItem("_sonde", "1");
        const lsSubstitue = "_sonde" in mem;
        localStorage.removeItem("_sonde");"""
remplacer(AVANT_TDZ, APRES_TDZ, "porte TDZ : globalThis + sonde")

AVANT_OK = """          mem["spk_suivi_optimisation_v1"] = JSON.stringify({ format: 8,"""
APRES_OK = """          if(!lsSubstitue){
            ok("porte TDZ : la substitution localStorage n'est pas possible ici (accesseur window sans setter) — la porte est jouée pour de vrai au harnais",
               "porte jouée au harnais", "porte jouée au harnais");
          } else {
          mem["spk_suivi_optimisation_v1"] = JSON.stringify({ format: 8,"""
remplacer(AVANT_OK, APRES_OK, "porte TDZ : garde substitution")

AVANT_OK2 = """             [ 1, "lTdz", true, true, "Base TDZ" ]);
        } finally {
          delete mem["spk_suivi_optimisation_v1"];
          global.localStorage = lsAvant;"""
APRES_OK2 = """             [ 1, "lTdz", true, true, "Base TDZ" ]);
          }
        } finally {
          delete mem["spk_suivi_optimisation_v1"];
          globalThis.localStorage = lsAvant;"""
remplacer(AVANT_OK2, APRES_OK2, "porte TDZ : fermeture garde + restauration globalThis")

# --- 3. le plancher atelier 56 px étendu ------------------------------------
AVANT_CSS = '''    + "html[data-mode=\\"atelier\\"] select.cell, html[data-mode=\\"atelier\\"] select{ min-height:56px !important; }"'''
APRES_CSS = '''    + "html[data-mode=\\"atelier\\"] select.cell, html[data-mode=\\"atelier\\"] select{ min-height:56px !important; }"
    /* v4.129.1 — tout élément saisissable ou cliquable atteint 56 px : les
       inputs (texte, nombre) tous, pas seulement .cell ; textarea ; summary ;
       les lignes d opération (.pcb-op) ; les cases à cocher portent une
       boîte cliquable de 56 px dont la case dessinée reste 28 px
       (background-clip:content-box — le dessin natif suit la content box). */
    + "html[data-mode=\\"atelier\\"] input:not([type=\\"checkbox\\"]):not([type=\\"radio\\"]):not([type=\\"hidden\\"]){ min-height:56px !important; }"
    + "html[data-mode=\\"atelier\\"] textarea{ min-height:56px !important; }"
    + "html[data-mode=\\"atelier\\"] summary{ min-height:56px !important; }"
    + "html[data-mode=\\"atelier\\"] .pcb-op{ min-height:56px !important; }"
    + "html[data-mode=\\"atelier\\"] input[type=\\"checkbox\\"], html[data-mode=\\"atelier\\"] input[type=\\"radio\\"]{ width:56px !important; height:56px !important; min-width:56px !important; min-height:56px !important; border:14px solid transparent !important; background-clip:content-box !important; box-sizing:border-box !important; padding:0 !important; }"'''
remplacer(AVANT_CSS, APRES_CSS, "CSS atelier : cibles 56 px étendues")

# --- 4. NOUVEAUTES -----------------------------------------------------------
NOUV_ANCRE = 'const NOUVEAUTES = [\n'
NOUV_ENTREE = '''const NOUVEAUTES = [
  { version:"4.129.1", date:"29/10/2026", points:[
    "<b>Le mode atelier s\u2019adresse aux doigts partout.</b> Les cibles de 56 px ne sont plus réservées aux boutons : <b>champs texte et nombre, menus déroulants, zones de texte, résumés dépliables, lignes d\u2019opération</b> des tuiles — et les <b>cases à cocher</b> portent une zone de clic de 56 px autour d\u2019une case toujours dessinée à 28 px. Et en ouvrant la suite de tests interne (#tests), elle ne bloque plus sur une syntaxe réservée au harnais — elle va jusqu\u2019au bout au navigateur."
  ]},
'''
n = src.count(NOUV_ANCRE)
assert n == 1, "ancre NOUVEAUTES : %d occurrences (attendu 1)" % n
src = src.replace(NOUV_ANCRE, NOUV_ENTREE)
print("ok  NOUVEAUTES 4.129.1")

assert src != io.open(F, encoding="utf-8").read()
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch A (4.129.1) appliqué.")

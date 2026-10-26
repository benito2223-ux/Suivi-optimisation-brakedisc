# -*- coding: utf-8 -*-
"""Tour 93 — v4.110.0 — le harnais : export de `badgeCodifScenario` + porte
hors-suite « badge codif 4.110 » (lit le fichier réel : la fonction existe,
la fiche l'appelle, les trois libellés du sémantique sont là, le hors
exigence tient). Ancres exactes + assert."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()


def remplace(ancien, nouveau, nom):
    global s
    n = s.count(ancien)
    assert n == 1, "ancre %s : %d occurrences (attendu 1)" % (nom, n)
    s = s.replace(ancien, nouveau)
    print("ok  %s" % nom)


# ── 1. la fonction pure rejoint l'API exposée au harnais ─────────────────────
A1 = "etatCodification, articlesScenario, codificationScenario, dossierVisite, dateIsoMax, joursDepuis, decompositionLeviers, planPrioritesData, "
N1 = "etatCodification, articlesScenario, codificationScenario, badgeCodifScenario, dossierVisite, dateIsoMax, joursDepuis, decompositionLeviers, planPrioritesData, "
remplace(A1, N1, "1. liste d'export API")

# ── 2. la porte hors-suite, posée avant la porte 4.103 ───────────────────────
A2 = "  /* ── v4.103.0 — LE PRIX SPK PAR DÉFAUT N'EXISTE PLUS ─────────────────────\n"
N2 = (
    "  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──\n"
    "     Brique B (UI) : l'état dérivé de la 4.106 devient visible là où le\n"
    "     scénario est jugé. La fonction pure est testée dans runTests ; cette\n"
    "     porte lit le fichier réel : la fonction existe, la fiche l'appelle,\n"
    "     les trois libellés du sémantique Benjamin (codifié / attente X j /\n"
    "     non demandée) sont là, et le hors-exigence (base excel / sans\n"
    "     article) n'a pas fondu. */\n"
    "  (function badgeCodifFiches(){\n"
    "    const fs = require('fs');\n"
    "    const path = require('path');\n"
    "    const echecs = [];\n"
    "    const REPO = __REPO__;\n"
    "    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();\n"
    "    if (!html) { echecs.push('bilan_economique.html introuvable'); }\n"
    "    else {\n"
    "      const code = html;\n"
    "\n"
    "      /* (1) la fonction pure existe */\n"
    "      if (code.indexOf('function badgeCodifScenario(sc){') === -1)\n"
    "        echecs.push('badgeCodifScenario absente du source');\n"
    "\n"
    "      /* (2) la fiche scénario du Plan appelle le badge : un badge dérivé\n"
    "             qui n'est pas rendu est une donnée morte (leçon case PRIX). */\n"
    "      const iFiche = code.indexOf('function planScenariosHTML');\n"
    "      if (iFiche < 0) echecs.push('planScenariosHTML introuvable');\n"
    "      else {\n"
    "        const iSuiv = code.indexOf(String.fromCharCode(10) + 'function ', iFiche);\n"
    "        const bloc = code.slice(iFiche, iSuiv > 0 ? iSuiv : iFiche + 8000);\n"
    "        if (bloc.indexOf('badgeCodifScenario(sc)') === -1)\n"
    "          echecs.push('la fiche scénario n affiche plus l état de codification');\n"
    "        if (bloc.indexOf('l.codifB') === -1)\n"
    "          echecs.push('le badge dérivé nest plus rendu dans la cellule État');\n"
    "      }\n"
    "\n"
    "      /* (3) les trois libellés du sémantique + le hors-exigence */\n"
    "      const iBadge = code.indexOf('function badgeCodifScenario');\n"
    "      if (iBadge >= 0) {\n"
    "        const iFin = code.indexOf(String.fromCharCode(10) + 'function ', iBadge);\n"
    "        const bloc = code.slice(iBadge, iFin > 0 ? iFin : iBadge + 3000);\n"
    "        ['codification attendue', 'codification non demand', '>codifié<', 'pc-stat serie', 'pc-stat attente']\n"
    "          .forEach(function(m){ if (bloc.indexOf(m) === -1) echecs.push('le badge a perdu « ' + m + ' »'); });\n"
    "        if (bloc.indexOf('sansExigence') === -1 || bloc.indexOf('sansArticle') === -1)\n"
    "          echecs.push('le badge ne respecte plus le hors-exigence (base excel / sans article)');\n"
    "      }\n"
    "    }\n"
    "    if (echecs.length) r.echecs += echecs.length;\n"
    "    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'badge codif 4.110 : la fiche scénario porte l état de codification dérivé (codifié / attente X j / non demandée)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));\n"
    "  })();\n"
    "\n"
    "  /* ── v4.103.0 — LE PRIX SPK PAR DÉFAUT N'EXISTE PLUS ─────────────────────\n"
)
remplace(A2, N2, "2. porte hors-suite badge codif 4.110")

io.open(p, "w", encoding="utf-8").write(s)
print("patch harnais posé :", len(s))

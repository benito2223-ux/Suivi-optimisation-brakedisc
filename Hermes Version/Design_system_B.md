web application/stitch/projects/1873107962167371638/screens/7bf9973c5eeb431da0769dbca0feaf6a
# ARCHIVE PROJET : SUIVI OPTIMISATION USINAGE DISQUES FREIN (SEPT-FONS)
## SPK by CeramTec × Stellantis Sept-Fons — Suite UI & Règles Constitutionnelles
> Document structuré au format Markdown / JSON prêt à être transmis à Hermes Agent ou toute IA de développement.

---

### STRUCTURE DE L'ARCHIVE :
1. `CONSTITUTION_SUIVI_v1.md` (Règles constitutionnelles, source unique, gouvernance)
2. `DESIGN_SYSTEM_B.css` (Tokens CSS exacts du look CeramTec Industrial Campaign)
3. `DATA_MODEL_HIERARCHIE.json` (Matrice stricte des entités)
4. `SCREENS_CATALOG.md` (Spécifications des 4 écrans de la suite complète)
5. `CHANGELOG_HERMES_ZCODE.md` (Protocole de collaboration et verrou)

---

```markdown
### 1. CONSTITUTION DU SUIVI (RÈGLES D'OR DU PROJET)

# CONSTITUTION DU SUIVI — les règles du jeu · v1
Co-rédigée : Hermes (finalité) × Z Code (technique) · Arbitre : Benjamin
Adoptée le : 29/09/2026 · Socle : 4.53.0

1. CE QUE CET OUTIL EST :
   - Un suivi d'optimisation du coût de revient des disques de frein (usinage céramique Sept-Fons).
   - Publics prioritaires :
     1. L'atelier (Matis Guyon, régleurs) : tactile/desktop, capturer les essais, mesurer, décider.
     2. Matis pilote : plan d'action par OP et par poste, concrétisation des gains.
     3. La hiérarchie : rigueur de la démarche, gains actés, partenariat outillage SPK by CeramTec.

2. MATRICE STRICTE DES ENTITÉS :
   Ligne (machine, taux horaire fixe)
     └── Référence Pièce (disque, volume annuel, cibleCPP)
           └── OP (opCode : OP10, OP20, OP30 - clé immuable)
                 └── Scénario (configuration d'outils ; la production de référence = scénario ★)
                       └── Essai (lot qualifié, conditions de coupe, longévités mesurées)
                             └── Prélèvement métrologique (DTV, rugosité Ra, voile)
   * Règle absolue : Le POSTE est une entité dérivée ('gainPoste'), JAMAIS stockée directement.
   * La LIVRAISON est un instantané figé et daté pour la hiérarchie.

3. RÈGLES DE CALCUL MATHÉMATIQUES :
   - §3.1 Source unique : Une seule fonction déterministe calcule les gains et les CPP.
   - CPP_machine = (Temps de cycle (s) / 3600) * Taux horaire machine (€/h)
   - CPP_outils = Somme [ Prix plaquette / (Arêtes * Longévité pcs) ]
   - Delta CPP = CPP_référence - CPP_SPK (+0.315 €/pce sur OP10)
   - Gain Annuel = Delta CPP * Volume Annuel (+37 800 €/an sur OP10)
   - §3.4 Non-mélange : Les gains qualifiés série (+84 250 €/an) et les gains projetés (+26 600 €/an) ne sont JAMAIS sommés sans étiquetage distinct.
   - §3.5 Déclaration exhaustive des postes : Tous les postes sont affichés (un poste non impacté porte explicitement ±0.000 €).
   - Coupe simultanée (EMAG Bi-broche) : Le couplage T01 + T02 annule les poussées axiales et économise 12 s en temps masqué (badge ambre).

4. CONFIDENTIALITÉ & VOCABULAIRE :
   - Jamais de grandeurs internes K ni P_req affichées.
   - Terme officiel : 'épaisseur de copeau' (jamais 'Hex').
   - Nuances exclusives SPK : SH20, WG300, FC-900, HC-600.
```

---

```css
/* 2. DESIGN SYSTEM B : CERAMTEC INDUSTRIAL CAMPAIGN LOOK (CSS TOKENS) */
:root {
  /* Core */
  --ink:        #000000;   /* H1/H2, grands montants, typographie dominante */
  --body:       #5C5D62;   /* Paragraphes, descriptions, légendes */
  --label:      #9A9A9A;   /* Intitulés de champs, colonnes, métadonnées */
  --line:       #535357;   /* Soulignement des champs de saisie (border-bottom) */

  /* Accents officiels */
  --red:        #E30045;   /* Rouge CeramTec : CTA primaires, statuts actifs */
  --red-dark:   #B8003A;
  --blue:       #006AB3;   /* Bleu SPK : filets décoratifs 2px, barres d'en-tête */
  --blue-light: #EAF4FB;

  /* Surfaces & Neutres */
  --white:      #FFFFFF;   /* Fond de page et cartes */
  --gray-50:    #FAFAFA;   /* Fond des conteneurs de formulaire */
  --gray-100:   #F4F4F4;   /* Filets de tableaux et séparateurs */
  --gray-200:   #E5E5E5;   /* Bordures discrètes */
  --gray-300:   #CFCFCF;   /* Puces inactives */

  /* Sémantique atelier */
  --green:      #1A7A3F;   /* Gains validés, conformité métrologique CMM */
  --green-bg:   #EDF7F1;
  --amber:      #B45309;   /* Coupe simultanée T01+T02, essais en cours */
  --amber-bg:   #FFF8ED;

  /* Typographie & Formes */
  --font:       'Roboto', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
  --radius:     2px;       /* Esthétique industrielle épurée quasi-plate */
}

/* RÈGLE ERGONOMIQUE DES BOUTONS :
   Cercle + chevron ('›') aligné à gauche. Pas de grands rectangles massifs. */
.btn-icon-circle {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-family: var(--font);
  font-weight: 500;
  font-size: 14px;
}
.btn-icon-circle .circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
.btn-icon-circle.primary .circle { background: var(--ink); color: #fff; }
.btn-icon-circle.cta .circle { background: var(--red); color: #fff; }

/* RÈGLE ERGONOMIQUE DES FORMULAIRES :
   Border-bottom uniquement (aucun encadrement fermé). */
.input-underline {
  border: none;
  border-bottom: 1px solid var(--line);
  background: transparent;
  padding: 6px 2px 8px;
  font-size: 15px;
  color: var(--ink);
  font-family: var(--font);
}
```

---

```json
{
  "3. DATA_MODEL_HIERARCHIE": {
    "site": "Stellantis Sept-Fons - Atelier Usinage Disques",
    "partenaire": "SPK by CeramTec",
    "lignes": [
      {
        "id": "EMAG_1",
        "nom": "EMAG 1 · Bi-broche Inversée VSC 400 DS",
        "taux_horaire": 85.00,
        "operations": [
          {
            "opCode": "OP10",
            "titre": "Ébauche & Finition Pistes",
            "piece": "DV 356x26 RPI",
            "volume_annuel": 120000,
            "cibleCPP": 1.200,
            "statut": "Qualifié Série (§3.4)",
            "gain_unitaire_eur": 0.315,
            "gain_annuel_eur": 37800,
            "postes": {
              "T01": { "nom": "Ébauche Face A", "nuance": "SPK SH20", "gain": 0.063 },
              "T02": { "nom": "Ébauche Face B", "nuance": "SPK SH20", "gain": 0.058, "simultane": "T01" },
              "T03": { "nom": "Finition Piste", "nuance": "SPK WG300", "gain": 0.031 },
              "T04": { "nom": "Chanfrein K20", "nuance": "Carbure Neutre", "gain": 0.000 }
            }
          },
          {
            "opCode": "OP30",
            "titre": "Perçage Ventilations & Fixations",
            "statut": "Poste Neutre Déclaré (§3.5)",
            "gain_annuel_eur": 0.000
          }
        ]
      },
      {
        "id": "EMAG_2",
        "nom": "EMAG 2 · Bi-broche Inversée",
        "taux_horaire": 85.00,
        "operations": [
          {
            "opCode": "OP10",
            "titre": "Tournage complet DV 300x24 Ventilée",
            "statut": "Essais en cours (§3.4)",
            "gain_potentiel_eur": 26600
          }
        ]
      },
      {
        "id": "HESSAPP",
        "nom": "HESSAPP · Tour Vertical",
        "taux_horaire": 92.00,
        "operations": [
          {
            "opCode": "OP20",
            "titre": "Finition Pistes DV 380x30 HP",
            "nuance": "SPK WG300 Whisker",
            "statut": "Qualifié Série (§3.4)",
            "gain_annuel_eur": 19850
          }
        ]
      }
    ],
    "bilan_consolide": {
      "gain_acté_série_eur_an": 84250,
      "gain_projeté_essais_eur_an": 26600,
      "ralliement_cible_moyen_pct": 88.4,
      "cadence_globale_pcs_h": 92
    }
  }
}
```

---

```markdown
### 4. CATALOGUE DES 4 ÉCRANS DE LA SUITE (LOOK CERAMTEC CAMPAIGN)

1. **ÉCRAN 1 — Tableau de bord des Lignes (EMAG / HESSAPP)** :
   - Vue d'ensemble du parc machines.
   - Cartes par ligne avec cinématique broche, cadence, gain acté vs projeté.
   - Matrice récapitulative des opérations (§3.5).

2. **ÉCRAN 2 — Comparateur de Scénarios & Postes d'outils (OP10)** :
   - Confrontation Scénario A (Carbure Prod ★) vs Scénario SPK v3 (Céramique Mixte).
   - Chronométrage (36.0 s vs 48.0 s) et décomposition des postes T01 à T04.
   - Encart cinématique de coupe simultanée T01 + T02 en ambre.
   - Courbe d'usure VB et rugosité d'état de surface.

3. **ÉCRAN 3 — Saisie Essais Atelier & Métrologie CMM** :
   - Saisie rapide par le régleur (Matis Guyon) des paramètres de coupe réels (Vc, f, ap).
   - Contrôle tridimensionnel instantané : DTV (4.2 µm < 8.0 µm), Rugosité Ra (1.22 µm < 1.60 µm).
   - Journal des 3 derniers essais archivés.

4. **ÉCRAN 4 — Bilan Économique & Export A4 Hiérarchie** :
   - Journal des livraisons figées et datées (Q1, Q2, Q3-2026).
   - Fiche A4 officielle pour direction et validation contractuelle Stellantis × SPK.
   - Boutons d'export PDF haute résolution et synthèse JSON.
```

---

```markdown
### 5. PROTOCOLE DE CO-DÉVELOPPEMENT (GOUVERNANCE HERMES × Z CODE)

Conformément à la section §6 de la Constitution :
1. `VERROU.md` : Avant toute modification de `bilan_economique.html`, vérifier que le verrou est vide. Si vide, déclarer sa session.
2. Un tour = un commit : Chaque assistant documente son tour dans `ECHANGES.md` et libère le verrou.
3. Règle du Tour 4 : Relecture intégrale du tour précédent avant toute écriture pour garantir l'absence de régression.
```

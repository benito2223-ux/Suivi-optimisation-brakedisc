# Spécification technique — Outil d'optimisation AESH

> **Version** : 1.0 (brouillon)
> **Date** : septembre 2026
> **Auteur** : Benjamin Rouquette
> **Statut** : À valider avant implémentation

---

## 1. 🏗️ Architecture & Stack technique

### 1.1 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATEUR (utilisateur)                 │
│                                                             │
│   ┌─────────────┐   ┌──────────────┐   ┌────────────────┐  │
│   │  UI React   │ ←→│  Moteur TS   │ ←→│  IndexedDB     │  │
│   │  (Vite)     │   │  (optim.)    │   │  (persistance) │  │
│   └─────────────┘   └──────────────┘   └────────────────┘  │
│          ↑                                       ↓          │
│          │          Import / Export (XLS/PDF/Word)          │
│          └──────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↕ HTTPS
                    ┌──────────────────┐
                    │   Surge.sh       │  (CDN statique)
                    │   (build statique│
                    │    React/Vite)   │
                    └──────────────────┘
```

**Tout tourne dans le navigateur.** Pas de backend, pas de serveur applicatif. Le moteur d'optimisation est un module TypeScript pur, exécuté côté client.

### 1.2 Stack

| Couche | Techno | Pourquoi |
|---|---|---|
| **UI** | React 18 + TypeScript + Vite | Stack moderne, build rapide, HMR dev |
| **UI lib** | Tailwind CSS + shadcn/ui | Composants sobres et accessibles, pas de design system à inventer |
| **Routing** | React Router v6 | Standard |
| **State** | Zustand | Léger, simple, parfait pour ce volume |
| **Persistance** | IndexedDB via `idb` | Base locale navigateur, exportable en JSON |
| **Parsing XLS** | SheetJS (xlsx) | Standard de facto |
| **Parsing PDF** | pdf.js (Mozilla) + Tesseract.js (OCR) | Texte natif + OCR fallback |
| **Parsing Word** | mammoth.js | Conversion .docx → HTML/texte structuré |
| **Export Excel** | ExcelJS | Génère des .xlsx riches (multi-onglets, styles) |
| **Export PDF** | jsPDF + html2canvas | Génération côté client |
| **Optimisation** | Module TypeScript custom (glouton + local search) | Pas de lib externe, contrôle total |
| **Déploiement** | Surge.sh (gratuit, commande `surge dist/`) | Zéro config, CDN mondial |
| **Mode local USB** | Script `.bat`/`.sh` qui lance `npx serve dist` + ouvre navigateur | Simple, pas d'install |

### 1.3 Structure du projet

```
aesh-scheduler/
├── public/
├── src/
│   ├── ui/                  # Composants React
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Etablissement.tsx
│   │   │   ├── ImportEDT.tsx
│   │   │   ├── AESH.tsx
│   │   │   ├── Eleves.tsx
│   │   │   ├── Optimisation.tsx
│   │   │   └── Resultats.tsx
│   │   ├── components/
│   │   └── App.tsx
│   ├── core/                # Logique métier pure (testable)
│   │   ├── models/
│   │   │   ├── Etablissement.ts
│   │   │   ├── Classe.ts
│   │   │   ├── AESH.ts
│   │   │   ├── Eleve.ts
│   │   │   ├── EDT.ts
│   │   │   └── Scenario.ts
│   │   ├── parser/
│   │   │   ├── parseXLS.ts
│   │   │   ├── parsePDF.ts
│   │   │   └── parseWord.ts
│   │   ├── optimizer/
│   │   │   ├── greedy.ts         # Construction initiale
│   │   │   ├── localSearch.ts    # Amélioration itérative
│   │   │   ├── score.ts          # Fonction de score
│   │   │   └── topN.ts           # Extraction des Top N
│   │   └── export/
│   │       ├── exportExcel.ts
│   │       ├── exportPDF.ts
│   │       └── exportJSON.ts
│   ├── store/               # Zustand stores
│   │   ├── etablissement.ts
│   │   ├── aesh.ts
│   │   ├── eleves.ts
│   │   └── scenarios.ts
│   ├── db/                  # IndexedDB layer
│   │   └── indexedDB.ts
│   └── main.tsx
├── tests/
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## 2. 📊 Modèle de données

### 2.1 Entités principales

```typescript
// Établissement
interface Etablissement {
  id: string;
  nom: string;
  type: 'college' | 'primaire';
  classes: Classe[];
  aesh: AESH[];
  elevesAI: EleveAI[];
  elevesAM: EleveAM[];
  edts: Map<string, EDT>; // key = classeId + 'paire'|'impaire'
  createdAt: Date;
  updatedAt: Date;
}

// Classe
interface Classe {
  id: string;
  nom: string; // ex: "6èmeA"
  niveau: string; // ex: "6ème"
}

// AESH
interface AESH {
  id: string;
  nom: string;
  heuresHebdo: number; // ex: 24
  // Pas d'autres attributs à ce stade
}

// Élève en accompagnement individuel
interface EleveAI {
  id: string;
  nom: string;
  classeId: string;
  blocsRequis: number; // nb de blocs ½ journée/semaine
  soins: Soin[]; // créneaux d'indisponibilité
}

interface Soin {
  jour: 'lundi' | 'mardi' | 'mercredi' | 'jeudi' | 'vendredi';
  moment: 'matin' | 'apres-midi';
}

// Élève en accompagnement mutualisé
interface EleveAM {
  id: string;
  nom: string;
  classeId: string;
  heuresRequises: number; // nb d'heures/semaine
}

// Emploi du temps d'une classe
interface EDT {
  classeId: string;
  semaine: 'paire' | 'impaire';
  creneaux: Creneau[];
}

interface Creneau {
  jour: 'lundi' | 'mardi' | 'mercredi' | 'jeudi' | 'vendredi';
  moment: 'matin' | 'apres-midi'; // bloc ½ journée
  // OU granularité horaire pour certaines classes
  heureDebut?: number; // 8, 9, 10, 14, 15, 16...
  heureFin?: number;
  matieres: Matiere[]; // 1 ou plusieurs (cas bloc)
}

interface Matiere {
  nom: string; // "Maths", "Histoire-Géo", "Français"...
  priorite: 1 | 2 | 3 | 4 | 5; // 1=H/Géo, 2=Français, 3=Maths, 4=SVT, 5=Physique
}

// Scénario d'attribution
interface Scenario {
  id: string;
  score: number;
  attributions: Attribution[];
  trous: Trou[];
}

interface Attribution {
  aeshId: string;
  eleveId: string; // peut être AI ou AM
  type: 'AI' | 'AM';
  creneau: Creneau;
}

interface Trou {
  classeId: string;
  creneau: Creneau;
  raison: string; // "Pas d'AESH disponible" / "Hors capacité" / etc.
}
```

### 2.2 Persistance IndexedDB

**Stores** (équivalent tables) :
- `etablissements` (keyPath: id)
- `aesh` (keyPath: id, index: etablissementId)
- `eleves_ai` (keyPath: id, index: etablissementId)
- `eleves_am` (keyPath: id, index: etablissementId)
- `edts` (keyPath: classeId+semaine, index: etablissementId)
- `scenarios` (keyPath: id, index: etablissementId)

**Export/import JSON** : un bouton dans l'UI permet de télécharger toute la base en `.json`, et de la recharger. C'est ce qui permet le **mode clé USB** sans dépendre du navigateur.

---

## 3. 📥 Pipeline d'import EDT

### 3.1 Vue d'ensemble

```
Fichier (XLS/PDF/Word)
       ↓
   [Détection format]
       ↓
   ┌────┴────┬────────┐
   XLS      PDF      Word
   ↓         ↓        ↓
[SheetJS] [pdf.js] [mammoth.js]
   ↓         ↓        ↓
   └────┬────┴────────┘
        ↓
   [Normalisation]
        ↓
   [Détection grille (jours × heures)]
        ↓
   [Mapping matières → priorités]
        ↓
   [Validation utilisateur]
        ↓
   [Stockage IndexedDB]
```

### 3.2 Parsing XLS

**Hypothèse** : le fichier est structuré en grille (lignes = heures, colonnes = jours), ou en liste de séances (1 ligne = 1 cours avec jour/heure/matière/classe).

**Stratégie** : on tente les deux parsings, on présente à l'utilisateur, il valide ou ajuste.

### 3.3 Parsing PDF

**2 cas** :
- **PDF textuel** (export Pronote) → `pdf.js` extrait le texte, on parse en regex
- **PDF scanné** (image) → `Tesseract.js` fait de l'OCR, même parsing ensuite

### 3.4 Parsing Word

`mammoth.js` convertit le `.docx` en texte structuré, on parse ensuite de la même manière que le PDF textuel.

### 3.5 Mapping matières → priorités

L'utilisateur configure une fois pour toutes la liste de ses matières :

| Matière | Priorité |
|---|---|
| Histoire-Géo | 1 |
| Français | 2 |
| Maths | 3 |
| SVT | 4 |
| Physique-Chimie | 5 |
| Anglais | 6 (par défaut) |
| EPS | 6 |
| Technologie | 6 |
| Arts plastiques | 6 |
| Musique | 6 |
| Autre | 6 |

Cette table est sauvegardée dans IndexedDB et modifiable.

---

## 4. 🧠 Algorithme d'optimisation (détail)

### 4.1 Formulation mathématique (informelle)

**Entrées** :
- E : ensemble des élèves (AI ∪ AM)
- A : ensemble des AESH
- C : ensemble des créneaux (jour × moment/heure)
- P_e,c : besoin de l'élève e sur le créneau c (booléen)
- M_c : matière(s) sur le créneau c (avec priorités)
- cap_a : capacité hebdo de l'AESH a (heures)

**Objectif** : maximiser Σ_e Σ_c (couverture_e,c × poids_matiere_c)
avec poids_matiere_c inversement proportionnel à la priorité (H/Géo = 5, Français = 4, Maths = 3, SVT = 2, Physique = 1, autres = 0.5)

**Contraintes** :
1. Pour tout créneau c, pour toute AESH a : Σ_e X_a,e,c ≤ 1 (exclusivité)
2. Pour tout AI e : couverture sur des **blocs complets** (pas de fractionnement au milieu)
3. Pour tout AM e : couverture à l'**heure**
4. Pour toute AESH a : Σ_c (durée_c × Σ_e X_a,e,c) ≤ cap_a (capacité)
5. Soins : P_e,c = 0 si l'élève e a un soin sur c
6. Portefeuille : chaque AESH a ≤ 2 AI et ≤ 3 classes AM (référence pour l'initialisation)

### 4.2 Algorithme — Phase 1 : Construction gloutonne

```typescript
function greedyConstruction(seed: number): Scenario {
  // 1. Constituer les portefeuilles AESH
  //    - Trier les AI par nb de blocs décroissant
  //    - Pour chaque AI, affecter à l'AESH qui a le moins de charge
  //    - Vérifier la contrainte "≤ 2 AI par AESH"
  // 2. Pour chaque classe AM, affecter à une AESH (≤ 3 classes AM par AESH)
  // 3. Pour chaque créneau d'un AI, allouer le bloc complet à son AESH
  // 4. Pour chaque créneau AM, allouer par ordre de priorité matière
  //    en respectant les heures restantes de chaque AESH
}
```

**Complexité** : O(|E| × |A| × |C|) — négligeable pour 1 collège.

### 4.3 Algorithme — Phase 2 : Local search

```typescript
function localSearch(scenario: Scenario, iterations: number): Scenario {
  let best = scenario;
  for (let i = 0; i < iterations; i++) {
    // Voisinage : on choisit aléatoirement parmi
    const move = pickRandom([
      swapAIAffectation,      // Échanger 2 AI entre 2 AESH
      swapAMClasseAffectation, // Échanger une classe AM entre 2 AESH
      moveAI,                  // Déplacer un AI d'une AESH à une autre
      rebalanceCharge,         // Rééquilibrer la charge entre AESH
    ]);
    const candidate = move(best);
    if (score(candidate) > score(best)) {
      best = candidate;
    }
  }
  return best;
}
```

**Nombre d'itérations** : 10 000 par scénario (suffisant, < 2 secondes).

### 4.4 Extraction du Top 3

```typescript
function extractTopN(n: number): Scenario[] {
  // On lance la construction gloutonne avec 20 seeds différents
  // On applique local search sur chacun
  // On garde les N meilleurs (distincts, hash sur les attributions)
  // Si < N scénarios distincts, on relance avec de nouvelles seeds
}
```

### 4.5 Score (fonction objectif)

```typescript
function score(scenario: Scenario): number {
  let s = 0;
  for (const attr of scenario.attributions) {
    const matiere = getMatiere(attr.creneau);
    s += POIDS_MATIERE[matiere.priorite];
  }
  // Pénalité pour les trous non couverts
  s -= 100 * scenario.trous.length;
  return s;
}
```

---

## 5. 🔌 API du moteur (TypeScript)

```typescript
// src/core/optimizer/index.ts
export interface OptimizationInput {
  etablissement: Etablissement;
  options?: {
    topN?: number;          // défaut: 3
    iterations?: number;    // défaut: 10000
    seeds?: number;         // défaut: 20
  };
}

export interface OptimizationOutput {
  scenarios: Scenario[];    // longueur = topN, triés par score décroissant
  metadata: {
    dureeMs: number;
    iterationsTotales: number;
    scoreMax: number;
    scoreMin: number;
  };
}

export async function optimize(
  input: OptimizationInput
): Promise<OptimizationOutput>;
```

**Le moteur est async** même s'il est synchrone — ça permet de le migrer vers un Web Worker si on veut paralléliser en v2 sans changer l'API.

---

## 6. 🎨 UI / Wireframes textuels

### 6.1 Page d'accueil / Dashboard
```
┌─────────────────────────────────────────────────────┐
│ 🏫 AESH Scheduler                                  │
│                                                     │
│ Établissement en cours : Collège Victor Hugo       │
│                                                     │
│ [Modifier] [Exporter] [Importer] [Nouveau]         │
│                                                     │
│ ┌────────────┬────────────┬────────────┬─────────┐ │
│ │ 8 classes  │ 8 AESH     │ 12 AI      │ 15 AM   │ │
│ └────────────┴────────────┴────────────┴─────────┘ │
│                                                     │
│ [⚡ Lancer l'optimisation]                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 6.2 Page Import EDT
```
┌─────────────────────────────────────────────────────┐
│ Importer un emploi du temps                         │
│                                                     │
│ Classe : [6èmeA ▼]   Semaine : [Paire ▼]           │
│                                                     │
│ [📁 Choisir un fichier] (XLS, PDF, Word)           │
│                                                     │
│ Aperçu détecté :                                    │
│ ┌─────┬─────┬─────┬─────┬─────┬─────┐             │
│ │     │ Lun │ Mar │ Mer │ Jeu │ Ven │             │
│ ├─────┼─────┼─────┼─────┼─────┼─────┤             │
│ │ 8h  │Maths│Fr   │HG   │Maths│EPS  │             │
│ │ 9h  │Maths│Fr   │HG   │Maths│EPS  │             │
│ │ ... │     │     │     │     │     │             │
│ └─────┴─────┴─────┴─────┴─────┴─────┘             │
│                                                     │
│ [✅ Valider]  [❌ Annuler]                          │
└─────────────────────────────────────────────────────┘
```

### 6.3 Page Optimisation (en cours)
```
┌─────────────────────────────────────────────────────┐
│ ⚡ Optimisation en cours...                         │
│                                                     │
│ [████████████░░░░░░░] 60%                           │
│                                                     │
│ Scénario 1 : score 487 (en cours d'amélioration)   │
│ Scénario 2 : score 472 (en cours d'amélioration)   │
│ Scénario 3 : score 468 (en cours d'amélioration)   │
└─────────────────────────────────────────────────────┘
```

### 6.4 Page Résultats (Top 3)
```
┌─────────────────────────────────────────────────────┐
│ 📊 3 scénarios proposés                            │
│                                                     │
│ [Scénario 1 - 487] [Scénario 2 - 472] [Scénario 3 - 468] │
│                                                     │
│ Scénario 1 : "Couvre 95% des matières prioritaires" │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ AESH │ Lun AM │ Mar Mat │ Mer AM │ Jeu AM │ ...│ │
│ │ A1   │ 6A-AI1 │ 6A-AM   │ libre  │ 6A-AI1 │    │ │
│ │ A2   │ 5A-AI1 │ 5A-AM   │ 5A-AI1 │ libre  │    │ │
│ │ ...                                              │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Trous restants : 2 (voir détail)                    │
│                                                     │
│ [📊 Exporter Excel] [📄 Exporter PDF] [💾 Sauver]   │
└─────────────────────────────────────────────────────┘
```

---

## 7. 📅 Plan d'implémentation par phases

### Phase 0 — Bootstrap (1 jour)
- Init projet Vite + React + TS + Tailwind
- Config Surge.sh (`surge` CLI + `surge.json`)
- Structure de dossiers
- Script clé USB (`launch-usb.bat` / `launch-usb.sh`)
- README

### Phase 1 — Modèle de données + persistance (2 jours)
- Interfaces TypeScript (`core/models/*`)
- Wrapper IndexedDB avec `idb`
- Stores Zustand
- Export/import JSON

### Phase 2 — Saisie manuelle (3 jours)
- Page Établissement (CRUD classes)
- Page AESH (CRUD)
- Page Élèves AI / AM (CRUD)
- Pas encore d'import EDT — tout en saisie manuelle

### Phase 3 — Import EDT XLS (3 jours)
- Parser XLS avec SheetJS
- Détection de grille vs liste
- UI de validation
- Mapping matières → priorités

### Phase 4 — Import EDT PDF + Word (3 jours)
- Parser PDF (pdf.js + Tesseract OCR)
- Parser Word (mammoth)
- UI unifiée d'import

### Phase 5 — Moteur d'optimisation v1 (5 jours)
- Construction gloutonne
- Local search
- Score
- Top N
- Tests unitaires (≥80% coverage sur `core/optimizer`)

### Phase 6 — Page Optimisation + Résultats (3 jours)
- UI lancement optimisation (avec barre de progression)
- Affichage Top 3 côte à côte
- Détail planning par AESH / par classe / par élève
- Liste des trous

### Phase 7 — Exports (2 jours)
- Export Excel multi-onglets
- Export PDF
- Export JSON

### Phase 8 — Polish + Deploy (2 jours)
- Tests E2E (Playwright)
- Optimisations perfs
- Déploiement Surge.sh
- Création du `.bat` / `.sh` clé USB
- Documentation utilisateur

**Total estimé** : ~24 jours de dev (≈ 5 semaines à temps partiel, 1 mois plein).

### Phase 9 — v2 Primaire (à planifier après)
- Adaptateur `PrimaireEDTParser` (granularité ¼ journée)
- Suppression de la notion de matière (priorité par défaut partout)
- Tests sur cas primaire réel

---

## 8. ⚠️ Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| **PDF scannés** : qualité OCR variable | Élevé | UI de validation manuelle obligatoire après import |
| **EDT hétérogènes** : formats non standard | Moyen | Plusieurs stratégies de parsing, fallback saisie manuelle |
| **Solveur** : qualité des Top 3 décevante | Moyen | Tests sur cas réels tôt, itération sur les heuristiques |
| **Surge.sh** : limite de taille du bundle | Faible | Bundle < 5 MB attendu, pas de risque |
| **Clé USB** : compatibilité Windows/Mac/Linux | Moyen | Test sur les 3 OS, doc claire pour l'utilisateur |

---

## 9. ❓ Questions ouvertes (à trancher avant code)

1. **Fallback matière** : si un AI n'est pas couvert sur H/Géo, l'AESH référente peut-elle couvrir une autre matière (ex : Maths) ou on laisse le trou ?
2. **Mode dégradé** : s'il manque 1 AESH, l'outil propose quand même un plan partiel, ou il refuse ?
3. **Différences entre scénarios** : afficher un diff visuel entre les 3, ou juste le meilleur de chacun ?
4. **Recalcul EDT** : si l'EDT change en cours d'année, on relance tout ou on fait un diff incrémental ?
5. **Persistance des scénarios** : on garde les anciens scénarios en historique, ou on écrase ?

---

## 10. 📚 Annexes

### A. Dépendances npm prévues

```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0",
    "zustand": "^4.5.0",
    "idb": "^8.0.0",
    "xlsx": "https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js",
    "pdfjs-dist": "^4.5.0",
    "tesseract.js": "^5.1.0",
    "mammoth": "^1.8.0",
    "exceljs": "^4.4.0",
    "jspdf": "^2.5.0",
    "html2canvas": "^1.4.0",
    "tailwindcss": "^3.4.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "vite": "^5.4.0",
    "@types/react": "^18.3.0",
    "vitest": "^2.0.0",
    "@testing-library/react": "^16.0.0",
    "playwright": "^1.45.0"
  }
}
```

### B. Commandes utiles

```bash
# Dev
npm run dev

# Build
npm run build

# Tests
npm run test

# Deploy Surge (1ère fois : surge login)
npx surge dist/

# Mode clé USB (Windows)
./launch-usb.bat

# Mode clé USB (Mac/Linux)
./launch-usb.sh
```

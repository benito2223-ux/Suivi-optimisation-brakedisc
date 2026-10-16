<!DOCTYPE html>

<html lang="fr"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1.0" name="viewport"/><meta content="web_standard" name="shell-type"/><link href="https://fonts.googleapis.com/css2?family=Roboto+Flex:wght@300;400;500;700&amp;display=swap" rel="stylesheet"/><link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/><style>@layer base{html,body{margin:0;padding:0;}body{overscroll-behavior:none;}main>:first-child{margin-top:0!important;}main>:last-child{margin-bottom:0!important;}}::-webkit-scrollbar{display:none;}</style><script src="https://cdn.tailwindcss.com"></script><script id="tailwind-config">tailwind.config={"darkMode":"class","theme":{"extend":{"colors":{"on-primary":"#ffffff","on-primary-fixed":"#1b1b1b","tertiary-fixed":"#ffdadb","on-tertiary-fixed-variant":"#920029","on-surface":"#1a1b20","on-tertiary":"#ffffff","secondary-fixed":"#d2e4ff","surface-container-lowest":"#ffffff","on-surface-variant":"#4c4546","surface-container-high":"#e5e5e5","tertiary-container":"#40000d","error-container":"#ffdad6","surface-container-highest":"#e2e2e8","on-secondary-fixed-variant":"#00497e","inverse-primary":"#c6c6c6","on-error-container":"#93000a","secondary-container":"#6bb2ff","on-primary-fixed-variant":"#474747","tertiary":"#000000","secondary":"#0061a5","on-tertiary-fixed":"#40000d","on-tertiary-container":"#fd2655","surface-container-low":"#f4f3f9","outline-variant":"#cfc4c5","primary-fixed-dim":"#c6c6c6","surface-tint":"#5e5e5e","on-error":"#ffffff","on-background":"#1a1b20","primary-container":"#f4f4f4","secondary-fixed-dim":"#9fcaff","on-secondary-container":"#004375","inverse-surface":"#2f3035","tertiary-fixed-dim":"#ffb2b6","outline":"#e5e5e5","surface-bright":"#f9f9ff","error":"#E30045","on-primary-container":"#000000","on-secondary-fixed":"#001d36","background":"#f9f9ff","surface":"#ffffff","surface-dim":"#dad9df","surface-container":"#f4f4f4","on-secondary":"#ffffff","primary-fixed":"#e2e2e2","primary":"#000000","inverse-on-surface":"#f1f0f6","surface-variant":"#e2e2e8"},"borderRadius":{"DEFAULT":"0.125rem","lg":"0.25rem","xl":"0.5rem","full":"0.75rem"},"spacing":{"space-lg":"1.5rem","gutter-sm":"1rem","gutter":"1.5rem","space-md":"1rem","margin-sm":"1rem","space-xs":"0.25rem","space-sm":"0.5rem","space-xl":"2.5rem","margin":"2rem"},"fontFamily":{"headline-xl":["Roboto Flex"],"title-md":["Roboto Flex"],"label-md":["Roboto Flex"],"headline-xl-mobile":["Roboto Flex"],"label-sm":["Roboto Flex"],"body-md":["Roboto Flex"],"headline-lg":["Roboto Flex"],"headline-md":["Roboto Flex"],"body-lg":["Roboto Flex"]},"fontSize":{"headline-xl":["36px",{"lineHeight":"41px","fontWeight":"700"}],"title-md":["18px",{"lineHeight":"24px","fontWeight":"500"}],"label-md":["13px",{"lineHeight":"18px","fontWeight":"300"}],"headline-xl-mobile":["30px",{"lineHeight":"36px","fontWeight":"700"}],"label-sm":["11px",{"lineHeight":"16px","letterSpacing":"0.05em","fontWeight":"400"}],"body-md":["14px",{"lineHeight":"22px","fontWeight":"400"}],"headline-lg":["27px",{"lineHeight":"32px","fontWeight":"700"}],"headline-md":["20px",{"lineHeight":"26px","fontWeight":"300"}],"body-lg":["15px",{"lineHeight":"24px","fontWeight":"400"}]}}}};</script></head><body class="bg-surface-bright font-body-md text-on-surface antialiased"><header class="fixed top-0 left-0 right-0 z-50 bg-surface shadow-[0_1px_6px_rgba(0,0,0,0.08)]"><div class="h-16 max-w-[1280px] mx-auto px-margin flex items-center justify-between gap-gutter"><div class="flex items-center gap-space-md shrink-0"><div class="flex items-baseline gap-space-xs"><span class="font-headline-lg text-headline-lg text-primary tracking-tight">SPK</span><span class="font-label-md text-label-md text-on-surface-variant font-light hidden sm:inline">| Suivi d'optimisation Sept-Fons</span></div></div><nav class="hidden xl:flex items-center gap-space-lg h-full" data-active-classes="text-on-surface font-headline-md border-b-2 border-error pb-[18px] pt-[20px]"><a class="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors py-space-sm" data-path="tableau-de-bord-lignes" href="#">Tableau de bord Lignes</a><a class="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors py-space-sm" data-path="comparateur-scenarios-postes" href="#">Comparateur Scénarios &amp; Postes</a><a class="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors py-space-sm" data-path="saisie-essais-atelier" href="#">Saisie Essais Atelier</a><a class="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors py-space-sm" data-path="bilan-economique-livraisons" href="#">Bilan Économique &amp; Livraisons</a></nav><div class="flex items-center gap-space-sm shrink-0"><div class="hidden md:flex items-center gap-space-xs bg-surface-container px-space-sm py-space-xs rounded-DEFAULT"><span class="material-symbols-outlined text-[14px] text-secondary">precision_manufacturing</span><span class="font-label-sm text-label-sm text-on-surface uppercase tracking-wider font-medium">Ligne EMAG 1 · DV 356x26 RPI</span></div><div class="flex items-center gap-space-xs bg-surface-container-low px-space-sm py-space-xs rounded-DEFAULT"><span class="w-1.5 h-1.5 rounded-full bg-secondary"></span><span class="font-label-sm text-label-sm text-on-surface-variant">Local / JSON</span></div><button class="w-8 h-8 rounded-full flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-colors" type="button"><span class="material-symbols-outlined text-[18px]">help_outline</span></button><div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><span class="material-symbols-outlined text-on-primary text-[18px]">person</span></div></div></div><div class="h-[2px] w-full flex"><div class="w-48 bg-error"></div><div class="flex-1 bg-secondary"></div></div></header><main class="w-full pt-16 bg-surface-bright min-h-screen"><div class="max-w-[1280px] mx-auto px-margin py-space-lg"><div class="flex flex-col w-full">
<!-- Main Spec Container (DS B Architecture) -->
<div class="bg-surface rounded-DEFAULT shadow-sm p-6 sm:p-10 lg:p-12 mb-space-xl">
<!-- Hero Section -->
<div class="flex flex-col gap-space-xs mb-space-xl">
<!-- Decorative Thin Blue Rule -->
<div class="w-[60px] h-[2px] bg-secondary mb-space-xs"></div>
<!-- Sub-headline / Context -->
<div class="font-label-md text-[19px] leading-[26px] text-primary font-light">
        Usinage disques de frein Sept-Fons — Ébauche &amp; Finition Pistes DV 356x26 RPI
      </div>
<!-- Bold H1 with Red Highlight -->
<h1 class="font-headline-xl text-headline-xl text-primary tracking-tight font-bold">
        Comparateur de Scénarios &amp; Postes d'outils <span class="text-error">OP10</span>
</h1>
<p class="font-label-md text-label-md text-on-surface-variant font-light mt-1">
        Validation industrielle usine Sept-Fons · Référentiel technique Céramiques SPK (SH20 &amp; WG300) vs Carbure Standard.
      </p>
</div>
<!-- Filter & Simulation Bar (Material-style underline inputs) -->
<div class="bg-surface-container-low rounded-DEFAULT p-space-lg mb-space-xl">
<div class="flex items-center justify-between gap-space-md mb-space-md flex-wrap">
<div class="font-headline-md text-headline-md text-on-surface-variant font-light flex items-center gap-space-xs">
<span class="material-symbols-outlined text-[20px] text-secondary">tune</span>
          Paramètres de Ligne &amp; Filtrage
        </div>
<div class="flex items-center gap-space-xs font-label-sm text-label-sm uppercase tracking-wider text-secondary bg-surface px-space-sm py-1 rounded-DEFAULT shadow-sm">
<span class="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
          Synchronisation Données Ligne EMAG 1 Active
        </div>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-lg">
<!-- Field 1 -->
<div class="flex flex-col relative">
<label class="font-label-md text-label-md text-on-surface-variant font-light mb-1">Référence Pièce</label>
<input class="bg-transparent font-body-md text-body-md text-primary font-normal py-1 px-0 focus:outline-none cursor-default" readonly="" type="text" value="DV 356x26 RPI"/>
<div class="h-[1px] w-full bg-outline-variant"></div>
<span class="font-label-sm text-[10px] text-on-surface-variant mt-1 font-light">Fonte GS perlito-ferritique</span>
</div>
<!-- Field 2 -->
<div class="flex flex-col relative">
<label class="font-label-md text-label-md text-on-surface-variant font-light mb-1">Opération Usinage</label>
<input class="bg-transparent font-body-md text-body-md text-primary font-normal py-1 px-0 focus:outline-none cursor-default" readonly="" type="text" value="OP10 Ébauche/Finition"/>
<div class="h-[1px] w-full bg-outline-variant"></div>
<span class="font-label-sm text-[10px] text-on-surface-variant mt-1 font-light">Tournage bi-broche inversée</span>
</div>
<!-- Field 3 -->
<div class="flex flex-col relative">
<label class="font-label-md text-label-md text-on-surface-variant font-light mb-1">Taux Horaire Machine</label>
<div class="flex items-baseline justify-between">
<input class="bg-transparent font-body-md text-body-md text-primary font-normal py-1 px-0 focus:outline-none w-full" id="taux-input" type="text" value="85.00 €/h"/>
<span class="font-label-sm text-[11px] text-secondary font-medium">MODIFIABLE</span>
</div>
<div class="h-[1px] w-full bg-secondary"></div>
<span class="font-label-sm text-[10px] text-on-surface-variant mt-1 font-light">Amortissement + Énergie + Main d'œuvre</span>
</div>
<!-- Field 4 -->
<div class="flex flex-col relative">
<label class="font-label-md text-label-md text-on-surface-variant font-light mb-1">Lot d'Essai Qualifié</label>
<input class="bg-transparent font-body-md text-body-md text-primary font-normal py-1 px-0 focus:outline-none cursor-default" readonly="" type="text" value="500 pièces"/>
<div class="h-[1px] w-full bg-outline-variant"></div>
<span class="font-label-sm text-[10px] text-on-surface-variant mt-1 font-light">Validation R&amp;R Géométrie 100% OK</span>
</div>
</div>
</div>
<!-- Core Metrics Banner (3 Cards, 3px Left Accent) -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-space-lg mb-space-xl">
<!-- Metric 1: Économie / Disque -->
<div class="bg-surface p-space-lg rounded-DEFAULT shadow-md relative overflow-hidden flex flex-col justify-between transition-transform duration-150 hover:-translate-y-0.5">
<div class="absolute left-0 top-0 bottom-0 w-[3px] bg-secondary"></div>
<div>
<div class="flex items-center justify-between mb-space-xs">
<span class="font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">Économie / Disque</span>
<span class="font-label-sm text-label-sm px-2 py-0.5 rounded-DEFAULT bg-secondary-fixed text-on-secondary-fixed-variant font-medium">Validé Série</span>
</div>
<div class="font-headline-xl text-[38px] leading-[44px] font-bold text-primary my-1">
            +0.315 €
          </div>
</div>
<div class="pt-space-xs mt-space-xs">
<p class="font-label-md text-label-md text-on-surface-variant font-light">Décroissance CPP net (-20.4%)</p>
<div class="flex items-center gap-1 mt-1 text-secondary font-label-sm text-label-sm font-medium">
<span class="material-symbols-outlined text-[14px]">trending_down</span>
            Base unitaire garantie
          </div>
</div>
</div>
<!-- Metric 2: Gain Consolidé Annuel -->
<div class="bg-surface p-space-lg rounded-DEFAULT shadow-md relative overflow-hidden flex flex-col justify-between transition-transform duration-150 hover:-translate-y-0.5">
<div class="absolute left-0 top-0 bottom-0 w-[3px] bg-secondary"></div>
<div>
<div class="flex items-center justify-between mb-space-xs">
<span class="font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">Gain Consolidé Annuel</span>
<span class="font-label-sm text-label-sm px-2 py-0.5 rounded-DEFAULT bg-surface-container font-light text-on-surface-variant">120 000 pcs/an</span>
</div>
<div class="font-headline-xl text-[38px] leading-[44px] font-bold text-primary my-1">
            +37 800 € <span class="font-label-md text-label-md font-light text-on-surface-variant">/ an</span>
</div>
</div>
<div class="pt-space-xs mt-space-xs">
<p class="font-label-md text-label-md text-on-surface-variant font-light">Postes T01 + T02 + T03 synchronisés</p>
<div class="flex items-center gap-1 mt-1 text-on-surface-variant font-label-sm text-label-sm font-light">
<span class="material-symbols-outlined text-[14px] text-secondary">factory</span>
            Calculé sur capacité nominale 2x8h
          </div>
</div>
</div>
<!-- Metric 3: Ralliement Cible CPP -->
<div class="bg-surface p-space-lg rounded-DEFAULT shadow-md relative overflow-hidden flex flex-col justify-between transition-transform duration-150 hover:-translate-y-0.5">
<div class="absolute left-0 top-0 bottom-0 w-[3px] bg-error"></div>
<div>
<div class="flex items-center justify-between mb-space-xs">
<span class="font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">Ralliement Cible CPP</span>
<span class="font-label-sm text-label-sm px-2 py-0.5 rounded-DEFAULT bg-tertiary-fixed text-on-tertiary-fixed-variant font-medium">Objectif 1.200 €</span>
</div>
<div class="font-headline-xl text-[38px] leading-[44px] font-bold text-primary my-1 flex items-baseline gap-2">
            91.3 %
            <span class="font-label-md text-label-md text-on-surface-variant font-light">(Actuel 1.230 €)</span>
</div>
</div>
<div class="pt-space-xs mt-space-xs">
<!-- Progress Bar with CeramTec Red fill -->
<div class="w-full bg-surface-container-high h-2 rounded-DEFAULT overflow-hidden mb-1.5">
<div class="bg-error h-full rounded-DEFAULT" style="width: 91.3%;"></div>
</div>
<div class="flex items-center justify-between font-label-sm text-label-sm text-on-surface-variant font-light">
<span>Reste à capter : 0.030 € / pce</span>
<span class="text-error font-medium">Écart cible: -2.4%</span>
</div>
</div>
</div>
</div>
<!-- Simultanéité Alert / Technical Architecture Callout -->
<div class="bg-surface-container-low p-space-md rounded-DEFAULT mb-space-xl relative overflow-hidden flex items-start gap-space-md shadow-sm">
<div class="absolute left-0 top-0 bottom-0 w-[3px] bg-secondary"></div>
<div class="w-8 h-8 rounded-full bg-secondary-fixed flex items-center justify-center shrink-0 mt-0.5">
<span class="material-symbols-outlined text-[18px] text-secondary">bolt</span>
</div>
<div class="flex-1">
<div class="flex items-center gap-space-xs">
<span class="font-title-md text-title-md text-primary font-medium">Coupe simultanée engagée</span>
<span class="font-label-sm text-label-sm px-2 py-0.5 bg-secondary-fixed text-on-secondary-fixed-variant rounded-DEFAULT font-medium uppercase tracking-wider">Synchronisme EMAG</span>
</div>
<p class="font-body-md text-body-md text-on-surface-variant font-light mt-0.5">
          Outil 1 (T01) + Outil 2 (T02) synchronisés sur broche EMAG. Annulation active des poussées axiales de tournage opposé, garantissant l'absence totale de battement résiduel et la tenue dimensionnelle de l'épaisseur de piste (<span class="font-medium text-primary">DTV &lt; 8 µm</span>).
        </p>
</div>
</div>
<!-- Scenario Comparison: 2 Technical Cards Side-by-Side -->
<div class="mb-space-xl">
<div class="flex items-baseline justify-between mb-space-md">
<div>
<h2 class="font-headline-md text-headline-md text-primary font-light">Bilan Comparatif Direct des Stratégies</h2>
<p class="font-label-md text-label-md text-on-surface-variant font-light">Impact sur le temps de cycle pièce et décomposition des postes de coûts directs</p>
</div>
<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant hidden md:inline">Norme Usine Sept-Fons · Const. §3.2</span>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-space-lg">
<!-- Left Panel: Scenario A (Standard Carbure) -->
<div class="bg-surface p-space-lg rounded-DEFAULT shadow-md flex flex-col justify-between">
<div>
<div class="flex items-start justify-between mb-space-sm">
<div>
<span class="font-label-md text-label-md text-on-surface-variant font-light">Référence Atelier Existante</span>
<h3 class="font-headline-md text-headline-md text-primary font-normal mt-0.5">Scénario A · Carbure Standard (Prod ★)</h3>
</div>
<span class="px-2 py-1 bg-surface-container font-label-sm text-label-sm text-on-surface-variant rounded-DEFAULT">Séquentiel</span>
</div>
<p class="font-label-md text-label-md text-on-surface-variant font-light mb-space-md">
              Passes séquentielles lentes. Risque d'échauffement thermique et d'usure en cratère rapide sur fonte GS abrasive.
            </p>
<!-- Metrics Block -->
<div class="grid grid-cols-2 gap-space-sm bg-surface-container-low p-space-md rounded-DEFAULT mb-space-md">
<div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light uppercase">Temps de cycle</div>
<div class="font-headline-md text-headline-md text-primary font-normal">48.0 s</div>
<div class="font-label-sm text-[11px] text-on-surface-variant font-light">Cadence: 75 pces / h</div>
</div>
<div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light uppercase">CPP Machine</div>
<div class="font-headline-md text-headline-md text-primary font-normal">1.133 €</div>
<div class="font-label-sm text-[11px] text-on-surface-variant font-light">Taux 85.00 €/h</div>
</div>
</div>
<!-- Cost breakdown table -->
<div class="space-y-space-xs font-body-md text-body-md mb-space-md">
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">CPP Machine nominal</span>
<span class="font-normal text-primary">1.133 €</span>
</div>
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">CPP Plaquettes &amp; Outils</span>
<span class="font-normal text-primary">0.412 €</span>
</div>
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">Taux d'engagement broche</span>
<span class="font-normal text-primary">68 %</span>
</div>
</div>
</div>
<!-- Total CPP -->
<div class="bg-surface-container p-space-md rounded-DEFAULT flex items-baseline justify-between mt-auto">
<div>
<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant block font-light">Coût Par Pièce Global</span>
<span class="font-headline-md text-headline-md font-bold text-primary">1.545 € <span class="font-label-md text-label-md font-light text-on-surface-variant">/ pce</span></span>
</div>
<span class="font-label-sm text-label-sm text-on-surface-variant font-light italic">Statut: En cours de substitution</span>
</div>
</div>
<!-- Right Panel: Scenario SPK v3 (Ceramic Optimized) -->
<div class="bg-surface-container-low p-space-lg rounded-DEFAULT shadow-md flex flex-col justify-between relative overflow-hidden">
<div class="absolute top-0 right-0 bg-secondary text-on-secondary px-3 py-1 font-label-sm text-label-sm font-medium tracking-wide uppercase rounded-bl-DEFAULT">
            Recommandé · Optimisation Validée
          </div>
<div>
<div class="flex items-start justify-between mb-space-sm">
<div>
<span class="font-label-md text-label-md text-secondary font-light">Solution Recommandée SPK</span>
<h3 class="font-headline-md text-headline-md text-primary font-normal mt-0.5">Scénario SPK v3 · Céramique Mixte</h3>
</div>
</div>
<p class="font-label-md text-label-md text-on-surface-variant font-light mb-space-md">
              Passes simultanées T01/T02 en céramique mixte Al2O3/TiC + Finition ultra-rapide sous plaquette Whisker SiCw.
            </p>
<!-- Metrics Block -->
<div class="grid grid-cols-2 gap-space-sm bg-surface p-space-md rounded-DEFAULT mb-space-md shadow-sm">
<div>
<div class="font-label-sm text-label-sm text-secondary font-medium uppercase">Temps de cycle</div>
<div class="font-headline-md text-headline-md text-primary font-normal flex items-baseline gap-1">
                  36.0 s
                  <span class="font-label-sm text-label-sm text-secondary font-medium">-12.0 s</span>
</div>
<div class="font-label-sm text-[11px] text-on-surface-variant font-light">Cadence: 100 pces / h (+33%)</div>
</div>
<div>
<div class="font-label-sm text-label-sm text-secondary font-medium uppercase">CPP Machine</div>
<div class="font-headline-md text-headline-md text-primary font-normal flex items-baseline gap-1">
                  0.850 €
                  <span class="font-label-sm text-label-sm text-secondary font-medium">-0.283 €</span>
</div>
<div class="font-label-sm text-[11px] text-on-surface-variant font-light">Gain temps brut direct</div>
</div>
</div>
<!-- Cost breakdown table -->
<div class="space-y-space-xs font-body-md text-body-md mb-space-md">
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">CPP Machine optimisé</span>
<span class="font-normal text-primary">0.850 €</span>
</div>
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">CPP Plaquettes &amp; Outils</span>
<span class="font-normal text-primary">0.380 € <span class="text-secondary text-label-sm">(-0.032 €)</span></span>
</div>
<div class="flex justify-between py-1">
<span class="text-on-surface-variant font-light">Équilibrage dynamique d'effort</span>
<span class="font-normal text-primary text-secondary">Optimal (Fz équilibré)</span>
</div>
</div>
</div>
<!-- Total CPP -->
<div class="bg-surface p-space-md rounded-DEFAULT flex items-baseline justify-between mt-auto shadow-sm">
<div>
<span class="font-label-sm text-label-sm uppercase tracking-wider text-secondary block font-medium">Coût Par Pièce Cible SPK</span>
<span class="font-headline-md text-headline-md font-bold text-primary">1.230 € <span class="font-label-md text-label-md font-light text-on-surface-variant">/ pce</span></span>
</div>
<div class="text-right">
<span class="inline-block px-2.5 py-1 bg-secondary-fixed text-on-secondary-fixed-variant rounded-DEFAULT font-label-md text-label-md font-medium">
                Gain direct : +0.315 € net
              </span>
</div>
</div>
</div>
</div>
</div>
<!-- Operational Breakdown Table / List for Tool Stations (T01 à T04) -->
<div class="mb-space-xl">
<div class="flex items-center justify-between mb-space-md flex-wrap gap-space-xs">
<div>
<h2 class="font-headline-md text-headline-md text-primary font-light">Ventilation Opérationnelle des Postes d'Outils (T01 à T04)</h2>
<p class="font-label-md text-label-md text-on-surface-variant font-light">Paramètres de coupe, longévités mesurées et gains unitaire par station de tourelle</p>
</div>
<div class="flex items-center gap-space-xs">
<span class="font-label-sm text-label-sm text-on-surface-variant font-light">Tri par : Position tourelle</span>
</div>
</div>
<!-- Tabular Container -->
<div class="overflow-x-auto bg-surface rounded-DEFAULT shadow-md">
<table class="w-full text-left font-body-md text-body-md border-collapse">
<thead>
<tr class="bg-surface-container font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">
<th class="py-space-sm px-space-md">Poste &amp; Opération</th>
<th class="py-space-sm px-space-md">Nuances &amp; Outil</th>
<th class="py-space-sm px-space-md">Régime de coupe</th>
<th class="py-space-sm px-space-md">Longévité arête</th>
<th class="py-space-sm px-space-md">CPP Poste</th>
<th class="py-space-sm px-space-md text-right">Gain Poste Net</th>
<th class="py-space-sm px-space-md text-center">Actions Atelier</th>
</tr>
</thead>
<tbody class="divide-y-0">
<!-- Row T01 -->
<tr class="hover:bg-surface-container-low transition-colors duration-100">
<td class="py-space-md px-space-md align-top">
<div class="flex items-center gap-2">
<span class="w-6 h-6 rounded-DEFAULT bg-primary text-on-primary flex items-center justify-center font-label-sm text-label-sm font-medium">T01</span>
<div>
<div class="font-medium text-primary">Ébauche Face A</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Côté Cloche</div>
</div>
</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="font-medium text-primary">SPK SH20</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Céramique Al2O3/TiC</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">850 m/min</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">f = 0.35 mm/tr · ap 2.2 mm</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">140 pcs/arête</div>
<div class="font-label-sm text-label-sm text-secondary font-medium">+115% vs carbure</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">0.082 €</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">vs 0.145 € antér.</div>
</td>
<td class="py-space-md px-space-md align-top text-right">
<span class="inline-block font-label-md text-label-md text-on-secondary-fixed-variant bg-secondary-fixed px-2 py-0.5 rounded-DEFAULT font-medium">
                  +0.063 € / pce
                </span>
</td>
<td class="py-space-md px-space-md align-top text-center">
<button class="inline-flex items-center gap-1.5 px-3 py-1 bg-surface-container hover:bg-surface-container-high text-primary font-label-sm text-label-sm rounded-DEFAULT transition-colors" type="button">
<span class="w-4 h-4 rounded-full bg-primary text-on-primary inline-flex items-center justify-center text-[10px]">›</span>
                  Voir essais (3)
                </button>
</td>
</tr>
<!-- Row T02 -->
<tr class="bg-surface-container-low/50 hover:bg-surface-container-low transition-colors duration-100">
<td class="py-space-md px-space-md align-top">
<div class="flex items-center gap-2">
<span class="w-6 h-6 rounded-DEFAULT bg-primary text-on-primary flex items-center justify-center font-label-sm text-label-sm font-medium">T02</span>
<div>
<div class="font-medium text-primary">Ébauche Face B</div>
<div class="font-label-sm text-label-sm text-secondary font-medium">Simultanéité T01 active</div>
</div>
</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="font-medium text-primary">SPK SH20</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Céramique Al2O3/TiC</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">850 m/min</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">f = 0.35 mm/tr · ap 2.0 mm</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">135 pcs/arête</div>
<div class="font-label-sm text-label-sm text-secondary font-medium">+107% vs carbure</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">0.084 €</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">vs 0.142 € antér.</div>
</td>
<td class="py-space-md px-space-md align-top text-right">
<span class="inline-block font-label-md text-label-md text-on-secondary-fixed-variant bg-secondary-fixed px-2 py-0.5 rounded-DEFAULT font-medium">
                  +0.058 € / pce
                </span>
</td>
<td class="py-space-md px-space-md align-top text-center">
<button class="inline-flex items-center gap-1.5 px-3 py-1 bg-surface-container hover:bg-surface-container-high text-primary font-label-sm text-label-sm rounded-DEFAULT transition-colors" type="button">
<span class="w-4 h-4 rounded-full bg-primary text-on-primary inline-flex items-center justify-center text-[10px]">›</span>
                  Voir essais (2)
                </button>
</td>
</tr>
<!-- Row T03 -->
<tr class="hover:bg-surface-container-low transition-colors duration-100">
<td class="py-space-md px-space-md align-top">
<div class="flex items-center gap-2">
<span class="w-6 h-6 rounded-DEFAULT bg-primary text-on-primary flex items-center justify-center font-label-sm text-label-sm font-medium">T03</span>
<div>
<div class="font-medium text-primary">Finition Piste Frottement</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Ra &lt; 1.6 µm requis</div>
</div>
</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="font-medium text-primary">SPK WG300</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Whisker SiCw haute ténacité</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">1 100 m/min</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">f = 0.18 mm/tr · ap 0.4 mm</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">220 pcs/arête</div>
<div class="font-label-sm text-label-sm text-secondary font-medium">+83% vs carbure</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">0.054 €</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">vs 0.085 € antér.</div>
</td>
<td class="py-space-md px-space-md align-top text-right">
<span class="inline-block font-label-md text-label-md text-on-secondary-fixed-variant bg-secondary-fixed px-2 py-0.5 rounded-DEFAULT font-medium">
                  +0.031 € / pce
                </span>
</td>
<td class="py-space-md px-space-md align-top text-center">
<button class="inline-flex items-center gap-1.5 px-3 py-1 bg-surface-container hover:bg-surface-container-high text-primary font-label-sm text-label-sm rounded-DEFAULT transition-colors" type="button">
<span class="w-4 h-4 rounded-full bg-primary text-on-primary inline-flex items-center justify-center text-[10px]">›</span>
                  Voir essais (4)
                </button>
</td>
</tr>
<!-- Row T04 -->
<tr class="bg-surface-container-low/50 hover:bg-surface-container-low transition-colors duration-100">
<td class="py-space-md px-space-md align-top">
<div class="flex items-center gap-2">
<span class="w-6 h-6 rounded-DEFAULT bg-surface-container-highest text-on-surface-variant flex items-center justify-center font-label-sm text-label-sm font-medium">T04</span>
<div>
<div class="font-medium text-primary">Chanfrein &amp; Gorge Évacuation</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Profil standard</div>
</div>
</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="font-medium text-on-surface-variant">Carbure Standard K20</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Inchangé (hors périmètre céram.)</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-on-surface-variant font-normal">380 m/min</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">f = 0.15 mm/tr</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">350 pcs/arête</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Stable</div>
</td>
<td class="py-space-md px-space-md align-top">
<div class="text-primary font-normal">0.040 €</div>
<div class="font-label-sm text-label-sm text-on-surface-variant font-light">Conforme Constitution §3.5</div>
</td>
<td class="py-space-md px-space-md align-top text-right">
<span class="inline-block font-label-md text-label-md text-on-surface-variant bg-surface-container px-2 py-0.5 rounded-DEFAULT font-light">
                  ±0.000 €
                </span>
</td>
<td class="py-space-md px-space-md align-top text-center">
<span class="font-label-sm text-label-sm text-on-surface-variant font-light italic">Poste neutre</span>
</td>
</tr>
</tbody>
</table>
</div>
</div>
<!-- Visual Industrial Context & Sensor Inspection Panel -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-space-lg mb-space-xl">
<div class="md:col-span-2 bg-surface p-space-lg rounded-DEFAULT shadow-md flex flex-col justify-between">
<div>
<div class="flex items-center justify-between mb-space-sm">
<span class="font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">Topographie d'Usinage &amp; Débit Copeaux</span>
<span class="font-label-sm text-label-sm text-secondary font-medium">Contrôle Rugosité Piste DV</span>
</div>
<p class="font-body-md text-body-md text-on-surface-variant font-light mb-space-md">
            L'engagement simultané de la nuance <strong class="font-normal text-primary">SPK SH20</strong> permet une réduction draconienne des micro-vibrations d'ébauche. Les profils d'usure en dépouille mesurés après 140 disques consécutifs révèlent une bande de frottement régulière sans écaillage thermique.
          </p>
<!-- Simple SVG Graph: Wear progression vs Standard -->
<div class="bg-surface-container-low p-space-md rounded-DEFAULT">
<div class="flex items-center justify-between text-label-sm font-label-sm text-on-surface-variant mb-2">
<span>Évolution de l'usure de dépouille VB (µm) vs Quantité usinée</span>
<span class="text-error font-medium">Limite admissible VBmax: 200 µm</span>
</div>
<svg class="w-full h-28 overflow-visible" fill="none" viewbox="0 0 600 100">
<!-- Grid lines -->
<line class="text-outline" stroke="currentColor" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="600" y1="20" y2="20"></line>
<line class="text-outline" stroke="currentColor" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="600" y1="50" y2="50"></line>
<line class="text-outline" stroke="currentColor" stroke-dasharray="4 4" stroke-width="1" x1="0" x2="600" y1="80" y2="80"></line>
<!-- Curve A: Carbure Standard -->
<path d="M 0 90 Q 200 70 300 20" fill="none" stroke="#000000" stroke-linecap="round" stroke-width="2"></path>
<circle cx="300" cy="20" fill="#000000" r="4"></circle>
<text class="text-[10px] fill-current text-primary font-mono" x="310" y="24">Carbure: Rebut à 65 pcs</text>
<!-- Curve B: Céramique SPK SH20 -->
<path d="M 0 90 Q 250 85 550 45" fill="none" stroke="#0061a5" stroke-linecap="round" stroke-width="2.5"></path>
<circle cx="550" cy="45" fill="#0061a5" r="4"></circle>
<text class="text-[10px] fill-current text-secondary font-mono" x="460" y="40">SPK SH20: Stable à 140 pcs</text>
</svg>
<div class="flex items-center justify-between text-[11px] text-on-surface-variant font-light mt-2 pt-1">
<span>0 pcs</span>
<span>50 pcs</span>
<span>100 pcs</span>
<span class="text-secondary font-medium">140 pcs (Cible atteinte)</span>
</div>
</div>
</div>
</div>
<!-- Workshop Observation / Metallurgical Micro-image -->
<div class="bg-surface p-space-lg rounded-DEFAULT shadow-md flex flex-col justify-between">
<div>
<div class="flex items-center justify-between mb-space-sm">
<span class="font-label-md text-label-md text-on-surface-variant font-light uppercase tracking-wider">État de Surface Atelier</span>
<span class="material-symbols-outlined text-[18px] text-on-surface-variant">smb_share</span>
</div>
<div class="relative w-full h-36 rounded-DEFAULT overflow-hidden mb-space-sm bg-surface-container">
<img class="w-full h-full object-cover" data-alt="High precision industrial optical microscope close-up of machined grey cast iron brake disc surface showing uniform fine grooves without micro-cracks under clean laboratory lighting with technical engineering graticule overlay." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAPEpYwQxxFNDMf6wC0xK3Oz_i4rWtuL78l9jznTHA_ii_flFkfdnQKOZlQO4dRyXn_i146lpDH9FOUQjfHRGfVkt9Rdw3WqINE1r3hqBRud4oB8oHbect3HZ-1kZEANy7eU4Tpg1UExwGtdzApJuHQvUt1fcN98TZ24Ls3ZeWftsPF8SYrn3Si8pao3YusX2GCQbyB9lmSKnfV5HEjAz8ypXQ2cyv39DYPpyMprDU0kPorNErZo1am"/>
<div class="absolute bottom-1 right-1 bg-primary text-on-primary font-label-sm text-[10px] px-1.5 py-0.5 rounded-DEFAULT">
              Zoom 200x · Ra 1.22 µm
            </div>
</div>
<p class="font-label-sm text-label-sm text-on-surface-variant font-light">
            Finition sous arête SPK WG300 à 1 100 m/min. Absence de bavures dans la gorge d'évacuation, respect absolu de la tolérance d'alignement axial.
          </p>
</div>
<div class="pt-space-xs mt-space-xs flex items-center justify-between font-label-sm text-label-sm text-on-surface-variant">
<span>Prélèvement lot #500</span>
<span class="text-secondary font-medium">Conforme ISO 2768-mK</span>
</div>
</div>
</div>
<!-- Form / Interactive Action Bar (DS B Style with Circular Glyphs) -->
<div class="p-space-lg bg-surface-container rounded-DEFAULT flex flex-col sm:flex-row items-center justify-between gap-space-md">
<div class="flex flex-col">
<span class="font-title-md text-title-md text-primary font-medium">Décision de Ligne · Transition Série</span>
<span class="font-label-md text-label-md text-on-surface-variant font-light">Procéder à l'engagement formel sur ligne EMAG 1 Sept-Fons</span>
</div>
<div class="flex flex-wrap items-center gap-space-sm w-full sm:w-auto justify-end">
<!-- Button 3 (Ghost / Outline) -->
<button class="inline-flex items-center font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors py-2 px-3" type="button">
<span class="w-[36px] h-[36px] rounded-full inline-flex items-center justify-center mr-[10px] text-on-surface-variant bg-surface shadow-sm">›</span>
          Simuler nouvelle variante d'essai
        </button>
<!-- Button 2 (Primary Black) -->
<button class="inline-flex items-center bg-primary hover:bg-neutral-800 text-on-primary font-body-md text-body-md font-medium px-4 py-2 rounded-DEFAULT shadow-md transition-colors" type="button">
<span class="w-[36px] h-[36px] rounded-full bg-surface text-primary inline-flex items-center justify-center mr-[10px] font-bold">›</span>
          Fiche de Réglage Atelier (Impression A4)
        </button>
<!-- Button 1 (CTA Solid CeramTec Red) -->
<button class="inline-flex items-center bg-error hover:bg-red-700 text-on-error font-body-md text-body-md font-medium px-5 py-2 rounded-DEFAULT shadow-md transition-colors" type="button">
<span class="w-[36px] h-[36px] rounded-full bg-on-error text-error inline-flex items-center justify-center mr-[10px] font-bold">›</span>
          Promouvoir en Production (★)
        </button>
</div>
</div>
</div>
</div>
<script>
  // Simple interactive simulator for Machine Hourly Rate adjustment
  const tauxInput = document.getElementById('taux-input');
  if (tauxInput) {
    tauxInput.addEventListener('change', function(e) {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        // Micro feedback interaction: flash input briefly
        tauxInput.classList.add('text-secondary');
        setTimeout(() => {
          tauxInput.classList.remove('text-secondary');
        }, 300);
      }
    });
  }
</script></div></main><footer class="w-full bg-surface-container border-t border-outline py-space-lg"><div class="max-w-[1280px] mx-auto px-margin flex flex-col sm:flex-row items-center justify-between gap-space-sm text-on-surface-variant"><div class="font-label-md text-label-md">CeramTec Industrial · SPK Cutting Tools · Conforme Constitution v1</div><div class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Usine de Sept-Fons · Performance Outillage</div></div></footer></body></html>
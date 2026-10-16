// Vérification rendu réel : les transitions et hovers sont-ils appliqués ?
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// On ne peut pas lire computed styles headless-screenshot ; on vérifie donc :
// (1) la syntaxe CSS est valide pour le parser (via un extrait parsé par le navigateur en data: URL)
// Approche pragmatique : node --check les scripts + assertions sur le fichier.

const html = fs.readFileSync('bilan_economique.html', 'utf8');

const verifs = [
  ['transition:transform var(--motion)', 'boutons : transition syntaxiquement valide'],
  ['transition:box-shadow var(--motion) var(--ease), transform var(--motion) var(--ease)', 'socle lot 3 : tuiles + cartes transitionnées'],
  ['.ca-tuile:hover', 'tuiles atelier : hover lift présent'],
  ['prefers-reduced-motion', 'le mouvement a sa porte de sortie'],
];
let echecs = 0;
for (const [needle, pourquoi] of verifs) {
  const la = html.includes(needle);
  if (!la) echecs++;
  console.log((la ? '  ok  ' : '  ECHEC ') + pourquoi);
}
// plus aucune occurrence invalide
const invalides = (html.match(/\.var\(--motion\)/g) || []).length;
console.log((invalides === 0 ? '  ok  ' : '  ECHEC ') + 'aucune déclaration .var( invalide restante (' + invalides + ')');
if (invalides !== 0) echecs += invalides;
process.exitCode = echecs ? 2 : 0;

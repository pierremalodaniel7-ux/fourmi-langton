// test_circuits.js — chaque circuit : le simulateur (moteur v6, JavaScript) redonne-t-il la table de nos rapports ?
// node test_circuits.js [rapide]   (rapide : 4 lignes par circuit au plus)
const Langton = require('./engine.js'); const Circuit = require('./circuit.js'); const fs = require('fs');
const C = JSON.parse(fs.readFileSync(__dirname + '/sources/circuits.json', 'utf8'));
const rapide = process.argv[2] === 'rapide'; const seul = process.argv[3];
let ok = 0, ko = 0; const echecs = [];
for (const c of C) {
  if (seul && !c.id.includes(seul)) continue;
  const t0 = Date.now(); let lignes = c.table;
  const lourd = c.table.length * c.sorties[0].pas > 6e6 && (c.id.includes('R67') || c.id.includes('R53') || c.id.includes('R39'));
  if (rapide || lourd) { const pas = Math.max(1, Math.floor(c.table.length / (rapide ? 4 : 8))); lignes = c.table.filter((_, i) => i % pas === 0); }
  let bon = 0;
  for (const l of lignes) {
    const r = Circuit.verifier(Langton, c, l.e);
    const tous = Object.values(r.sorties).every((s) => s.ok !== false);
    if (tous) bon++; else echecs.push(c.id + ' ' + JSON.stringify(l.e) + ' ' + JSON.stringify(r.sorties));
  }
  const tot = lignes.length; if (bon === tot) ok++; else ko++;
  console.log(`${bon === tot ? 'ok  ' : 'ÉCHEC'} ${c.id} : ${bon}/${tot}${tot < c.table.length ? ' (échantillon sur ' + c.table.length + ')' : ''} — ${((Date.now() - t0) / 1000).toFixed(1)} s`);
}
console.log(`\n${ok} circuit(s) justes, ${ko} en échec.`);
if (echecs.length) { console.log('Détail des échecs :'); echecs.slice(0, 40).forEach((e) => console.log('  ' + e)); }
fs.writeFileSync(__dirname + '/resultats_tests_circuits.txt', echecs.join('\n'));
process.exitCode = ko ? 1 : 0;

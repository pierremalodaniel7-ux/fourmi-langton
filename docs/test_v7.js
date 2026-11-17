// test_v7.js — contrôles de la bibliothèque v7 (node test_v7.js)
//  1. aucun germe de la v6 n'a disparu ; 2. chaque fichier source est entièrement présent ; 3. les 236 bêtes des bestiaires sont là ;
//  4. aucun identifiant d'une version précédente n'a disparu ; 5. tous les germes se lisent ; 6. les doublons pointent vers un germe existant ;
//  7. résultats attendus : cycles exacts et autoroutes annoncés dans les fiches, redonnés par le moteur.
const fs = require('fs'); const Langton = require('./engine.js');
const B = JSON.parse(fs.readFileSync(__dirname + '/bibliotheque.json', 'utf8'));
const src = (f) => JSON.parse(fs.readFileSync(__dirname + '/sources/' + f, 'utf8'));
let ok = 0, ko = 0; const echecs = [];
function verif(nom, cond, detail) { if (cond) { ok++; } else { ko++; echecs.push(nom + (detail ? ' — ' + detail : '')); } console.log((cond ? 'ok   ' : 'ÉCHEC ') + nom + (detail && !cond ? ' — ' + detail : '')); }
const parId = new Map(B.germes.map((g) => [g.id, g]));
// 1. v6
const v6 = src('germes_v6.json'); let perdus = [];
v6.forEach((g, i) => { const e = parId.get('v6-' + String(i).padStart(3, '0')); if (!e || e.nom !== g.nom || e.fourmis !== String(g.fourmis || '') || e.points !== String(g.points || '')) perdus.push(g.nom); });
verif('aucun germe de la v6 perdu (' + v6.length + ' germes comparés nom + fourmis + cases)', perdus.length === 0, perdus.slice(0, 10).join(' ; '));
// 2. sources
const FICHIERS = { v6: 'germes_v6.json', racine: 'germes_racine_15-11.json', r20: 'germes_r20_dossiers.json', nuit: 'germes_nuit.json', r35: 'germes_autoroutes.json',
  r36cyc: 'germes_2026-11-16_10-100fourmis.json', cat: 'catalogue.json', r36ord: 'germes_ordinateur_R36-R38.json', r39: 'germe_ordinateur_R39.json',
  r40: 'germes_ordinateur_2026-11-17.json', r45: 'germes_ordinateur2_2026-11-17.json', fdf: 'germes_fourmi_dans_fourmi_2026-11-17.json', circ: 'circuits.json' };
for (const [cle, f] of Object.entries(FICHIERS)) {
  const n = src(f).length; const m = B.germes.filter((g) => g.origine && g.origine.fichier === cle).length;
  verif(`fichier ${f} : ${n} germe(s), ${m} dans la bibliothèque`, m >= n);
}
// 3. bestiaires
const cat = src('catalogue.json'); const absentes = cat.filter((b) => !parId.has('cat-' + b.id)).map((b) => b.id);
verif('les ' + cat.length + ' bêtes des bestiaires 1 à 10 sont dans le simulateur', absentes.length === 0, absentes.join(', '));
// 4. versions précédentes
for (const f of fs.readdirSync(__dirname + '/sources').filter((x) => /^ids_v.*\.txt$/.test(x))) {
  const ids = fs.readFileSync(__dirname + '/sources/' + f, 'utf8').split('\n').filter(Boolean); const manque = ids.filter((i) => !parId.has(i));
  verif(`aucun identifiant de ${f} (${ids.length}) n'a disparu`, manque.length === 0, manque.slice(0, 10).join(', '));
}
// 5. lecture
const illisibles = B.germes.filter((g) => !g.vide && (String(g.fourmis).trim() || String(g.points).trim()) && !String(g.points).startsWith('germe:')).filter((g) => {
  const M = Langton.analyserRegle(g.regle).M; const f = Langton.lireFourmis(g.fourmis, M); const p = Langton.lirePoints(g.points);
  return (f.length === 0 && p.points.length === 0) || p.erreurs.length > 0; // zéro fourmi permis s'il y a des cases (croisement 0,0)
}).map((g) => g.id);
verif('tous les germes se lisent (fourmis et cases)', illisibles.length === 0, illisibles.slice(0, 10).join(', '));
// 6. doublons
const orphelins = B.germes.filter((g) => g.doublon_de && !parId.has(g.doublon_de)).map((g) => g.id);
verif('chaque doublon pointe vers un germe existant (' + B.germes.filter((g) => g.doublon_de).length + ' doublons)', orphelins.length === 0, orphelins.join(', '));
// 7. résultats attendus (fiches du catalogue)
const nb = (s) => Number(String(s).replace(/[\s  ]/g, ''));
for (const b of cat) {
  const g = parId.get('cat-' + b.id); if (!g || String(g.points).startsWith('germe:')) continue;
  const M = Langton.analyserRegle(g.regle).M;
  const mc = /[Cc]ycle exact de période ([\d   ]+)/.exec(b.mesures || '');
  const ma = /[Pp]ériode ([\d   ]+), déplacement/.exec(b.mesures || '');
  const md = /dès le pas ([\d   ]+)/.exec(b.mesures || '');
  const nf = Langton.lireFourmis(g.fourmis, M).length;
  if (mc) {
    const P = nb(mc[1]); if (P * nf > 2.5e7) { console.log('saut ' + b.id + ' (cycle ' + P + ' trop long pour le test)'); continue; }
    if (/^O-PIEGE/.test(b.id)) {   // piège : cycle LOCAL des fourmis piégées (une autre fourmi part à l'infini)
      const sim = new Langton.Simulation({ regle: g.regle, fourmis: Langton.lireFourmis(g.fourmis, M), dessin: Langton.lirePoints(g.points).points });
      sim.avancer(180000); const avant = sim.fourmis.map((f) => [f.x, f.y]); sim.avancer(20000);
      const pris = sim.fourmis.map((f, i) => i).filter((i) => Math.abs(sim.fourmis[i].x - avant[i][0]) + Math.abs(sim.fourmis[i].y - avant[i][1]) < 400);
      const etat = () => pris.map((i) => [sim.fourmis[i].x, sim.fourmis[i].y, sim.fourmis[i].d].join(',')).join(';');
      const e0 = etat(); sim.avancer(P); const e1 = etat();
      verif(`${b.id} « ${b.nom} » : ${pris.length} fourmi(s) piégée(s), cycle local de période ${P}`, pris.length > 0 && e0 === e1, 'état des fourmis piégées différent après ' + P + ' pas');
      continue;
    }
    const sim = new Langton.Simulation({ regle: g.regle, fourmis: Langton.lireFourmis(g.fourmis, M), dessin: Langton.lirePoints(g.points).points });
    let reste = P + 8; while (reste > 0 && !sim.cycle) { const k = Math.min(reste, 50000); sim.avancer(k); reste -= k; }
    verif(`${b.id} « ${b.nom} » : cycle exact de période ${P}`, sim.cycle && sim.cycle.periode === P, sim.cycle ? 'période trouvée ' + sim.cycle.periode : 'pas de retour à l\'état initial en ' + (P + 8) + ' pas');
  } else if (ma && md && nf === 1) {
    const P = nb(ma[1]); const D = nb(md[1]); if (D > 3e6) continue;
    const sim = new Langton.Simulation({ regle: g.regle, fourmis: Langton.lireFourmis(g.fourmis, M), dessin: Langton.lirePoints(g.points).points });
    sim.avancer(D + 25 * P + 5000); const a = sim.fourmis[0].autoroute;
    verif(`${b.id} « ${b.nom} » : autoroute de période ${P}`, a && a.periode === P, a ? 'période ' + a.periode : 'pas d\'autoroute détectée');
  }
}
console.log(`\n${ok} contrôle(s) réussi(s), ${ko} échec(s).`);
if (echecs.length) { console.log('ÉCHECS :'); echecs.forEach((e) => console.log('  ' + e)); }
fs.writeFileSync(__dirname + '/resultats_tests_v7.txt', `${ok} réussis, ${ko} échecs\n` + echecs.join('\n') + '\n');
process.exitCode = ko ? 1 : 0;

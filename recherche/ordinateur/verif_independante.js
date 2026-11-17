// verif_independante.js — 2e programme, indépendant du moteur C/Python : lit germe_ordinateur.json
// et entrees.json, recalcule avec sa propre grille (Map par blocs), lit les directions aux pas indiqués.
// node verif_independante.js        -> germe 3+2 seulement ;  node verif_independante.js tout -> 256 entrées
const fs = require('fs');
const G = JSON.parse(fs.readFileSync(__dirname + '/germe_ordinateur.json'))[0];
const E = JSON.parse(fs.readFileSync(__dirname + '/entrees.json'));
const DX = [0, 1, 0, -1], DY = [-1, 0, 1, 0], CAP = { H: 0, D: 1, B: 2, G: 3 };
function parsePts(s) { return s.trim() ? s.split(';').map(p => p.trim().split(',').map(Number)) : []; }
function parseAnts(s) { return s.split(';').map(p => { const [x, y, d] = p.trim().split(','); return [+x, +y, CAP[d.trim()]]; }); }
function simule(points, fourmis, lecture) {
  const blocs = new Map();                  // bloc 256x256 -> Uint8Array
  const cell = (x, y) => { const bx = x >> 8, by = y >> 8, k = bx * 1000003 + by;
    let b = blocs.get(k); if (!b) { b = new Uint8Array(65536); blocs.set(k, b); } return [b, ((y & 255) << 8) | (x & 255)]; };
  for (const [x, y] of points) { const [b, i] = cell(x, y); b[i] ^= 1; }
  const A = fourmis.map(a => a.slice());
  const Tfin = Math.max(...Object.values(lecture));
  const fen = new Map();                    // fourmi -> positions sur les 31 dernières périodes avant sa lecture
  for (const i of Object.keys(lecture)) fen.set(+i, []);
  for (let t = 1; t <= Tfin; t++) {
    for (let i = 0; i < A.length; i++) {
      const a = A[i]; const [b, j] = cell(a[0], a[1]);
      a[2] = (a[2] + (b[j] ? 3 : 1)) & 3; b[j] ^= 1; a[0] += DX[a[2]]; a[1] += DY[a[2]];
    }
    for (const [i, L] of fen) { const tl = lecture[i]; if (t <= tl && t >= tl - 31 * 104 && (tl - t) % 104 === 0) L.push([A[i][0], A[i][1]]); }
  }
  const out = {};
  for (const [i, L] of fen) {               // déplacement identique (±2,±2) sur chacune des 30 dernières périodes
    let d = null, ok = true;
    for (let k = 1; k < L.length; k++) { const dx = L[k][0] - L[k - 1][0], dy = L[k][1] - L[k - 1][1];
      const s = dx + ',' + dy; if (d === null) d = s; else if (s !== d) ok = false; }
    out[i] = ok ? { '-2,2': '↙', '-2,-2': '↖', '2,-2': '↗', '2,2': '↘' }[d] || '?' : '?';
  }
  return out;
}
const noms = E.noms, n = E.n;
const lect = {}; for (const [nom, t] of Object.entries(E.lecture)) lect[noms.indexOf(nom)] = t;
function germe(a, b) {
  let p = E.fixes.slice();
  for (let m = 0; m < n; m++) { if ((a >> m) & 1) p = p.concat(E.si_a1[m]); if ((b >> m) & 1) p = p.concat(E.si_b1[m]); else p = p.concat(E.si_b0[m]); }
  return p;
}
function lit(r) { let v = 0;
  for (let m = 0; m < n; m++) { const d = r[noms.indexOf('S' + m)]; if (d === '↙') v |= 1 << m; else if (d !== '↘') return -1; }
  const k = r[noms.indexOf('K' + (n - 1))]; if (k === '↗') v |= 1 << n; else if (k !== '↘') return -1; return v; }
// 1) le germe publié = fixes + entrées de 3+2
const pg = parsePts(G.points).map(String).sort().join('|'), pe = germe(3, 2).map(String).sort().join('|');
console.log('germe publié = table des entrées pour 3+2 :', pg === pe);
const fourmis = parseAnts(G.fourmis);
const r = simule(parsePts(G.points), fourmis, lect);
console.log('germe 3+2 :', noms.map((nm, i) => i in r ? nm + ' ' + r[i] : '').filter(Boolean).join('  '), '-> lu', lit(r));
if (process.argv[2] === 'tout') {
  let bad = 0, t0 = Date.now();
  for (let a = 0; a < (1 << n); a++) for (let b = 0; b < (1 << n); b++) {
    const v = lit(simule(germe(a, b), fourmis, lect)); if (v !== a + b) { bad++; console.log('ECHEC', a, b, v); } }
  console.log(`toutes les entrées : ${1 << 2 * n}, échecs : ${bad} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
}

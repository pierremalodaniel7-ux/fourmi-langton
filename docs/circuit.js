// circuit.js — lecture des circuits (portes et ordinateurs) : composer le germe selon les interrupteurs, simuler jusqu'au
// pas de lecture, lire la sortie (direction, voie, nombre de fourmis) et comparer à la table attendue.
// Marche dans le navigateur (window.Circuit) et sous Node (module.exports).
(function (racine) {
  'use strict';
  const W = 1872;          // fenêtre de mesure de la direction : multiple de 104 (RL) et de 18 (LLR)
  const WV = 936;          // fenêtre de mesure de la voie : ppcm(104, 18)
  function cleVariante(valeurs) {
    return Object.keys(valeurs).sort().map((k) => k + '=' + valeurs[k]).join(',');
  }
  // Germe complet pour des valeurs d'entrée données. Les fourmis des entrées passent AVANT celles de la base.
  function composer(spec, valeurs) {
    if (spec.variantes) {
      const v = spec.variantes[cleVariante(valeurs)];
      if (!v) throw new Error('variante absente : ' + cleVariante(valeurs));
      return { regle: spec.regle, fourmis: v.fourmis.slice(), points: v.points.slice(), nbEntrees: 0, parEntree: {} };
    }
    const fourmis = []; const points = []; const parEntree = {};
    for (const e of spec.entrees) {
      const part = valeurs[e.nom] ? e.si1 : e.si0;
      parEntree[e.nom] = [fourmis.length, part.fourmis.length];
      for (const f of part.fourmis) fourmis.push(f);
      for (const p of part.points) points.push(p);
    }
    const nbEntrees = fourmis.length;
    for (const f of spec.base.fourmis) fourmis.push(f);
    for (const p of spec.base.points) points.push(p);
    return { regle: spec.regle, fourmis, points, nbEntrees, parEntree };
  }
  function texteGerme(g) {
    return {
      regle: g.regle,
      fourmis: g.fourmis.map((f) => f.join(',')).join(' ; '),
      points: g.points.map((p) => (p[2] === 1 || p[2] === undefined ? p[0] + ',' + p[1] : p.join(','))).join(' ; '),
    };
  }
  function fleche(dx, dy) {
    if (Math.abs(dx) < 4 && Math.abs(dy) < 4) return '·';
    if (Math.abs(dx) < 4) return dy > 0 ? '↓' : '↑';
    if (Math.abs(dy) < 4) return dx > 0 ? '→' : '←';
    return dy > 0 ? (dx < 0 ? '↙' : '↘') : (dx < 0 ? '↖' : '↗');
  }
  function indexFourmi(ref, g) {
    if (ref.startsWith('base:')) return g.nbEntrees + Number(ref.slice(5));
    if (ref.startsWith('entree:')) { const [, nom, k] = ref.split(':'); return g.parEntree[nom][0] + Number(k); }
    return -1;
  }
  // Simule et lit toutes les sorties. Langton = le moteur (engine.js). rappel(pas, total) pour la progression.
  function lire(Langton, spec, valeurs, rappel) {
    const g = composer(spec, valeurs);
    const M = Langton.analyserRegle(g.regle).M;
    const t = texteGerme(g);
    const sim = new Langton.Simulation({ regle: g.regle, fourmis: Langton.lireFourmis(t.fourmis, M), dessin: Langton.lirePoints(t.points).points });
    const sorties = spec.sorties.slice().sort((a, b) => a.pas - b.pas);
    const lu = {};
    if (g.fourmis.length === 0) {                 // aucune fourmi (toutes les entrées à 0 sans base) : rien ne bouge
      for (const s of sorties) lu[s.nom] = s.type === 'compte' ? { valeur: 0, texte: '0' } : { valeur: { fleche: '·', voie: null }, texte: '·' };
      return { lu, germe: g, pas: 0 };
    }
    const n = sim.fourmis.length;
    const enregistrements = new Map();            // un enregistrement par pas de lecture
    for (const p of [...new Set(sorties.map((s) => s.pas))]) {
      const debut = p - W;
      while (sim.pas < debut) { const k = Math.min(20000, debut - sim.pas); sim.avancer(k); if (rappel) rappel(sim.pas, p); }
      const xs = []; const ys = [];
      for (let i = 0; i < n; i++) { xs.push([]); ys.push([]); }
      while (sim.pas < p) {
        sim.avancer(1);
        for (let i = 0; i < n; i++) { xs[i].push(sim.fourmis[i].x); ys[i].push(sim.fourmis[i].y); }
      }
      enregistrements.set(p, { xs, ys });
    }
    for (const s of sorties) {
      const { xs, ys } = enregistrements.get(s.pas);
      const lireFourmi = (i) => {
        const X = xs[i]; const Y = ys[i]; const L = X.length;
        const f = fleche(X[L - 1] - X[0], Y[L - 1] - Y[0]);
        let voie = null;
        if (f === '↙' || f === '↗' || f === '↘' || f === '↖') {
          voie = Infinity;
          for (let k = L - WV; k < L; k++) voie = Math.min(voie, (f === '↙' || f === '↗') ? X[k] + Y[k] : X[k] - Y[k]);
        }
        return { fleche: f, voie, x: X[L - 1], y: Y[L - 1] };
      };
      if (s.type === 'compte') {
        let c = 0; for (let i = 0; i < n; i++) if (lireFourmi(i).fleche === s.fleche) c++;
        lu[s.nom] = { valeur: c, texte: String(c) };
      } else {
        const i = indexFourmi(s.fourmi, g);
        if (i < 0 || i >= n) throw new Error('fourmi de sortie introuvable : ' + s.fourmi + ' (' + n + ' fourmis)');
        const r = lireFourmi(i);
        lu[s.nom] = { valeur: r, texte: s.type === 'dirvoie' && r.voie !== null ? r.fleche + ' ' + r.voie : r.fleche, x: r.x, y: r.y };
      }
    }
    return { lu, germe: g, pas: sim.pas };
  }
  function conforme(attendu, l, tol) {
    tol = tol === undefined ? 4 : tol;
    if (typeof attendu === 'number') return l.valeur === attendu;
    let neg = false; let a = String(attendu);
    if (a.startsWith('≠')) { neg = true; a = a.slice(1); }
    const [fa, va] = a.split(' ');
    const r = l.valeur;
    let egal = r.fleche === fa;
    if (egal && va !== undefined) egal = r.voie !== null && Math.abs(r.voie - Number(va)) <= tol;
    return neg ? !egal : egal;
  }
  function ligneAttendue(spec, valeurs) {
    const k = cleVariante(valeurs);
    return spec.table.find((l) => cleVariante(l.e) === k);
  }
  function verifier(Langton, spec, valeurs, rappel) {
    const r = lire(Langton, spec, valeurs, rappel);
    const ligne = ligneAttendue(spec, valeurs);
    const res = {};
    for (const s of spec.sorties) {
      const a = ligne ? ligne.a[s.nom] : undefined;
      res[s.nom] = { lu: r.lu[s.nom].texte, attendu: a, ok: a === undefined ? null : conforme(a, r.lu[s.nom], spec.tolerance_voie) };
    }
    return { sorties: res, germe: r.germe, valeurs, affichage: afficher(spec, valeurs, r.lu) };
  }
  // Résultat « en clair » pour les additionneurs : « 2 + 3 = 5 ».
  function afficher(spec, valeurs, lu) {
    const a = spec.affichage; if (!a) return null;
    const nombre = (bits) => bits.reduce((s, b, i) => s + (valeurs[b] ? 1 << i : 0), 0);
    if (a.type === 'somme' && a.termes) {
      const v = a.lecture[lu[spec.sorties[0].nom].texte];
      return a.termes.map((t) => valeurs[t] ? 1 : 0).join(' + ') + ' = ' + (v === undefined ? '?' : v);
    }
    if (a.type === 'somme') {
      const t = lu[spec.sorties[0].nom].texte;
      let v; for (const k in a.lecture) { const [f, vv] = k.split(' '); const [fl, vl] = t.split(' '); if (f === fl && Math.abs(Number(vv) - Number(vl)) <= 4) v = a.lecture[k]; }
      return nombre(a.a) + ' + ' + nombre(a.b) + ' = ' + (v === undefined ? '?' : v);
    }
    if (a.type === 'somme_bits') {
      let v = 0; a.bits.forEach((b, i) => { if (lu[b] && lu[b].texte === a.un[i]) v += 1 << i; });
      return nombre(a.a) + ' + ' + nombre(a.b) + ' = ' + v;
    }
    return null;
  }
  const Circuit = { composer, texteGerme, lire, verifier, conforme, cleVariante, fleche };
  if (typeof module !== 'undefined' && module.exports) module.exports = Circuit; else racine.Circuit = Circuit;
})(typeof self !== 'undefined' ? self : this);

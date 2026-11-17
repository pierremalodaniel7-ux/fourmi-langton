'use strict';
// =============================================================================
//  v7.js — ce que la v7 ajoute à la v6 (chargé après ui.js, sans le réécrire)
//    1. bibliothèque (bibliotheque.js) : dossiers, pastilles, statuts, recherche, « Mes germes »
//    2. mode circuit : interrupteurs, Calculer, Toute la table (Web Worker), couleurs
//    3. « Aller au pas N »
//    4. grille tournée de 45°
//    5. téléphone : zoom à deux doigts
//    6. atelier « Construire » : palette, aimant (R-50 / R-60), brancher, enregistrer
// =============================================================================

const BIB = window.BIBLIOTHEQUE || { germes: [], circuits: [], ordre: [], avancement: [], version: '?' };
const CIRCUITS = new Map((BIB.circuits || []).map((c) => [c.id, c]));
const PAR_ID = new Map(BIB.germes.map((g) => [g.id, g]));

// ---------- stockage local (seulement pour « Mes germes » et des préférences : jamais indispensable) ----------
function lireLocal(cle, defaut) {
  try { const v = localStorage.getItem(cle); return v ? JSON.parse(v) : defaut; } catch (e) { return defaut; }
}
function ecrireLocal(cle, v) { try { localStorage.setItem(cle, JSON.stringify(v)); } catch (e) { /* stockage indisponible */ } }
let mesGermes = lireLocal('fourmi-v7-mes-germes', []);

// =============================================================================
// 1. Bibliothèque
// =============================================================================
window.listeGermes = function () { return BIB.germes.concat(mesGermes); };

const COULEUR_PASTILLE = { vert: '#16a34a', rouge: '#dc2626', gris: '#9ca3af' };
const SENS_PASTILLE = { vert: 'à nous (pas trouvé ailleurs)', rouge: 'déjà connu ailleurs', gris: 'pas encore cherché' };

function pastille(g) {
  const p = g.pastille || { c: 'gris', t: 'Pas encore cherché dans la littérature.' };
  const s = document.createElement('span');
  s.className = 'pastille';
  s.style.background = COULEUR_PASTILLE[p.c] || COULEUR_PASTILLE.gris;
  s.title = SENS_PASTILLE[p.c] + ' — ' + p.t;
  s.setAttribute('role', 'img');
  s.setAttribute('aria-label', s.title);
  // Au doigt : toucher la pastille montre la source sans charger le germe.
  s.addEventListener('click', (ev) => { ev.stopPropagation(); $('noteGerme').textContent = '● ' + s.title; });
  return s;
}

window.construireArbreGermes = function (filtre) {
  const arbre = $('arbreGermes');
  arbre.textContent = '';
  const f = String(filtre || '').trim().toLowerCase();
  const racine = { enfants: new Map(), germes: [], total: 0 };
  const placer = (chemin, i, renvoi) => {
    let noeud = racine; noeud.total++;
    for (const m of chemin.split('/').map((x) => x.trim()).filter(Boolean)) {
      if (!noeud.enfants.has(m)) noeud.enfants.set(m, { enfants: new Map(), germes: [], total: 0 });
      noeud = noeud.enfants.get(m); noeud.total++;
    }
    noeud.germes.push({ i, renvoi });
  };
  const liste = listeGermes();
  liste.forEach((g, i) => {
    const texte = [g.nom, (g.autres_noms || []).join(' '), g.regle, g.dossier, (g.refs || []).join(' '), g.statut || ''].join(' ').toLowerCase();
    if (f && !texte.includes(f)) return;
    placer(g.dossier || 'Divers', i, false);
    for (const a of new Set(g.aussi || [])) if (!a.startsWith('Archives') && a !== g.dossier && !String(g.dossier).startsWith(a + '/')) placer(a, i, true);
  });
  // ordre des dossiers du haut : celui de la bibliothèque, puis les autres
  const ordre = BIB.ordre || [];
  const tries = new Map([...racine.enfants].sort((a, b) => {
    const ia = ordre.indexOf(a[0]); const ib = ordre.indexOf(b[0]);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  }));
  racine.enfants = tries;
  const remplir = (parent, noeud, chemin) => {
    for (const [nom, enfant] of noeud.enfants) {
      const details = document.createElement('details');
      if (f) details.open = true;
      const resume = document.createElement('summary');
      resume.textContent = nom + ' ';
      const nb = document.createElement('span'); nb.className = 'nb'; nb.textContent = '(' + enfant.total + ')';
      resume.append(nb); details.append(resume);
      const ch = chemin ? chemin + '/' + nom : nom;
      if (ch === 'Ordinateur') details.append(boutonAvancement());
      remplir(details, enfant, ch);
      parent.append(details);
    }
    for (const { i, renvoi } of noeud.germes) {
      const g = liste[i];
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'germe' + (i === germeChoisi ? ' choisi' : '') + (g.mis_en_avant ? ' avant' : '');
      b.append(pastille(g));
      const t = document.createElement('span');
      t.textContent = (renvoi ? '↪ ' : '') + (g.circuit ? '⚡ ' : '') + g.nom + (g.doublon_de ? ' — doublon de « ' + ((PAR_ID.get(g.doublon_de) || {}).nom || g.doublon_de) + ' »' : '');
      b.append(t);
      if (g.statut && g.statut !== 'non précisé') { const s = document.createElement('span'); s.className = 'statut s-' + g.statut; s.textContent = g.statut; b.append(s); }
      if (g.avancement) { const s = document.createElement('span'); s.className = 'statut av'; s.textContent = g.avancement; b.append(s); }
      b.title = (g.note || '') + (g.autres_noms ? '\nAussi appelé : ' + g.autres_noms.join(', ') : '');
      b.addEventListener('click', () => {
        germeChoisi = i;
        for (const x of arbre.querySelectorAll('button.germe.choisi')) x.classList.remove('choisi');
        b.classList.add('choisi');
        chargerGerme(g);
      });
      parent.append(b);
    }
  };
  remplir(arbre, racine, '');
  if (f && racine.total === 0) arbre.textContent = 'Aucun germe ne correspond.';
  $('compteGermes').textContent = liste.length + ' éléments (' + liste.filter((g) => !String(g.dossier).startsWith('Archives')).length +
    ' hors archives) — bibliothèque v' + BIB.version;
};

function boutonAvancement() {
  const b = document.createElement('button');
  b.type = 'button'; b.className = 'germe avant';
  b.textContent = '📋 Avancement « fourmi dans fourmi » (feuille de route)';
  b.addEventListener('click', () => {
    const z = $('ficheGerme'); z.textContent = '';
    const h = document.createElement('p'); h.innerHTML = '<b>Feuille de route — fourmi dans fourmi</b> (reconstruite à partir des rapports R-61 à R-67 ; le document du projet n\'est pas dans le Drive).';
    z.append(h);
    const tab = document.createElement('table'); tab.className = 'table';
    tab.innerHTML = '<tr><th>Étape</th><th>État</th><th>Statut</th><th>Réf.</th></tr>' +
      (BIB.avancement || []).map((a) => `<tr><td>${a.etape}</td><td class="etat-${a.etat.split(' ')[0].replace('à', 'a')}">${a.etat}</td><td>${a.statut}</td><td>${a.ref}</td></tr>`).join('');
    z.append(tab); z.hidden = false;
  });
  return b;
}

const chargerGermeV6 = window.chargerGerme;
window.chargerGerme = function (g) {
  if (g.circuit && CIRCUITS.has(g.circuit)) {
    ouvrirCircuit(CIRCUITS.get(g.circuit));
  } else {
    fermerCircuit();
    chargerGermeV6(g);
  }
  afficherFiche(g);
};

function afficherFiche(g) {
  const z = $('ficheGerme'); z.textContent = ''; z.hidden = false;
  const ligne = (titre, valeur) => {
    if (!valeur) return;
    const p = document.createElement('p'); const b = document.createElement('b'); b.textContent = titre + ' : ';
    p.append(b, document.createTextNode(valeur)); z.append(p);
  };
  const p = g.pastille || { c: 'gris', t: '' };
  const tete = document.createElement('p'); tete.append(pastille(g)); const n = document.createElement('b'); n.textContent = ' ' + g.nom; tete.append(n); z.append(tete);
  ligne('Statut', g.statut_detail || g.statut);
  ligne('Littérature', SENS_PASTILLE[p.c] + ' — ' + p.t);
  ligne('Source', [(g.refs || []).join(', '), g.date, g.origine ? 'fichier ' + g.origine.fichier : ''].filter(Boolean).join(' · '));
  if (g.autres_noms) ligne('Aussi appelé', g.autres_noms.join(', '));
  if (g.doublon_de) ligne('Doublon de', (PAR_ID.get(g.doublon_de) || {}).nom || g.doublon_de);
  if (g.avancement) ligne('Avancement', g.avancement);
  if (g.fiche) for (const [k, v] of Object.entries(g.fiche)) ligne({ situation: 'Situation', deroulement: 'Déroulement', mesures: 'Mesures', interet: 'Intérêt' }[k] || k, v);
}

// « Mes germes » : ajoutés, jamais à la place d'un autre
function enregistrerMonGerme(nom, note) {
  const cfg = sim.exporterConfig();
  const g = {
    id: 'moi-' + Date.now(), nom, regle: cfg.regle,
    fourmis: Langton.ecrireFourmis(cfg.fourmis, sim.M), points: Langton.ecrirePoints(cfg.dessin),
    note: note || 'Germe enregistré dans le simulateur.', dossier: 'Mes germes', date: new Date().toISOString().slice(0, 10),
    statut: 'non précisé', pastille: { c: 'gris', t: 'Pas encore cherché.' }, origine: { fichier: 'navigateur', index: mesGermes.length },
  };
  mesGermes.push(g); ecrireLocal('fourmi-v7-mes-germes', mesGermes);
  construireArbreGermes($('filtreGermes').value);
  const blob = new Blob([JSON.stringify([g], null, 1)], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'mon_germe_' + g.id + '.json'; a.click();
  return g;
}

// =============================================================================
// 2. Mode circuit
// =============================================================================
const circuit = { spec: null, valeurs: {}, germe: null, lecture: null, travailleur: null, travail: 0 };

function fermerCircuit() { circuit.spec = null; circuit.lecture = null; $('panneauCircuit').hidden = true; }

function ouvrirCircuit(spec) {
  circuit.spec = spec; circuit.lecture = null;
  circuit.valeurs = {}; for (const e of spec.entrees) circuit.valeurs[e.nom] = 0;
  const z = $('interrupteurs'); z.textContent = '';
  for (const e of spec.entrees) {
    const l = document.createElement('label'); l.className = 'interrupteur';
    const c = document.createElement('input'); c.type = 'checkbox';
    c.addEventListener('change', () => { circuit.valeurs[e.nom] = c.checked ? 1 : 0; poserCircuit(false); });
    const s = document.createElement('span'); s.textContent = e.nom;
    l.append(c, s); z.append(l);
  }
  $('titreCircuit').textContent = '⚡ ' + spec.nom;
  const pas = Math.max(...spec.sorties.map((s) => s.pas));
  $('infoCircuit').textContent = 'Lecture au pas ' + fr(pas) + ' ; sortie(s) : ' + spec.sorties.map((s) => s.nom).join(', ') +
    ' ; table : ' + spec.table.length + ' ligne(s). Coche une entrée pour la mettre à 1.';
  $('resultatCircuit').textContent = ''; $('tableCircuit').textContent = '';
  $('panneauCircuit').hidden = false;
  poserCircuit(true);
}

function poserCircuit(cadrerAussi) {
  const g = Circuit.composer(circuit.spec, circuit.valeurs);
  circuit.germe = g; circuit.lecture = null;
  const t = Circuit.texteGerme(g);
  const M = Langton.analyserRegle(g.regle).M;
  definirLecture(false);
  const fourmis = Langton.lireFourmis(t.fourmis, M);
  nouvelleSimulation({ regle: g.regle, fourmis, zeroFourmi: fourmis.length === 0, dessin: Langton.lirePoints(t.points).points });
  if (cadrerAussi) cadrer($('cadrage').value);
  $('resultatCircuit').textContent = '';
  aRedessiner = true;
}

function travailleur() {
  if (circuit.travailleur === null) {
    try { circuit.travailleur = new Worker('worker.js'); } catch (e) { circuit.travailleur = false; } // file:// : pas de Worker
  }
  return circuit.travailleur;
}

// Lance des lignes de la table dans le Worker (ou, à défaut, ici, une ligne par tranche).
function calculerLignes(lignes, surLigne, surFin, surProgres) {
  const id = ++circuit.travail; const spec = circuit.spec;
  const w = travailleur();
  if (w) {
    w.onmessage = (ev) => {
      const m = ev.data; if (m.id !== circuit.travail) return;
      if (m.type === 'progres') surProgres(m.ligne, m.pas, m.total);
      else if (m.type === 'ligne') surLigne(m.i, m.res);
      else if (m.type === 'fin') surFin();
      else if (m.type === 'erreur') { $('resultatCircuit').textContent = 'Erreur : ' + m.message; }
    };
    w.postMessage({ id, spec, lignes });
  } else {
    let i = 0;
    const suite = () => {
      if (id !== circuit.travail) return;
      if (i >= lignes.length) { surFin(); return; }
      const res = Circuit.verifier(Langton, spec, lignes[i]);
      surLigne(i, { sorties: res.sorties, affichage: res.affichage, valeurs: lignes[i] }); i++;
      setTimeout(suite, 0);
    };
    setTimeout(suite, 0);
  }
}
function coutCircuit(spec) {
  const n = spec.base ? spec.base.fourmis.length + spec.entrees.reduce((s, e) => s + e.si1.fourmis.length, 0) : 1;
  return Math.max(...spec.sorties.map((s) => s.pas)) * Math.max(1, n);
}
function texteSorties(res) {
  return Object.entries(res.sorties).map(([k, s]) => `${k} = ${s.lu}` + (s.attendu !== undefined ? ` (attendu ${s.attendu}) ${s.ok ? '✔' : '✘'}` : '')).join(' ; ');
}

function calculer() {
  if (!circuit.spec) return;
  const z = $('resultatCircuit'); z.textContent = 'Calcul en cours…';
  const valeurs = Object.assign({}, circuit.valeurs);
  calculerLignes([valeurs], (i, res) => {
    z.textContent = (res.affichage ? res.affichage + '   —   ' : '') + texteSorties(res);
    z.className = Object.values(res.sorties).every((s) => s.ok !== false) ? 'bon' : 'faux';
    // marque la zone de lecture : on avance la vue jusqu'au pas de lecture (en tâche de fond)
    allerAuPas(Math.max(...circuit.spec.sorties.map((s) => s.pas)), () => { circuit.lecture = true; aRedessiner = true; });
  }, () => {}, (l, pas, total) => { z.textContent = 'Calcul… pas ' + fr(pas) + ' / ' + fr(total); });
}

function touteLaTable() {
  if (!circuit.spec) return;
  const spec = circuit.spec; const lignes = spec.table.map((l) => l.e);
  const cout = coutCircuit(spec) * lignes.length;
  if (cout > 5e8 && !confirm('Toute la table demande environ ' + Math.round(cout / 1e7) / 100 + ' milliard(s) de pas de fourmi (plusieurs minutes). Continuer ?')) return;
  const tab = $('tableCircuit'); tab.textContent = '';
  const t = document.createElement('table'); t.className = 'table';
  const noms = spec.entrees.map((e) => e.nom);
  t.innerHTML = '<tr>' + noms.map((n) => `<th>${n}</th>`).join('') + '<th>sortie lue</th><th>attendu</th><th></th></tr>';
  tab.append(t);
  let bons = 0; let faits = 0;
  const bilan = document.createElement('p'); tab.prepend(bilan);
  calculerLignes(lignes, (i, res) => {
    faits++; const ok = Object.values(res.sorties).every((s) => s.ok !== false); if (ok) bons++;
    const tr = document.createElement('tr');
    tr.innerHTML = noms.map((n) => `<td>${lignes[i][n]}</td>`).join('') +
      `<td>${(res.affichage ? res.affichage + ' ; ' : '') + Object.entries(res.sorties).map(([k, s]) => k + '=' + s.lu).join(' ; ')}</td>` +
      `<td>${Object.entries(res.sorties).map(([k, s]) => k + '=' + s.attendu).join(' ; ')}</td><td class="${ok ? 'bon' : 'faux'}">${ok ? '✔' : '✘'}</td>`;
    t.append(tr);
    bilan.textContent = faits + ' / ' + lignes.length + ' lignes calculées — ' + bons + ' justes' + (faits - bons ? ', ' + (faits - bons) + ' FAUSSE(S)' : '');
  }, () => { bilan.textContent += ' — terminé.'; }, (l, pas, total) => { bilan.textContent = 'Ligne ' + (faits + 1) + ' / ' + lignes.length + ' : pas ' + fr(pas) + ' / ' + fr(total); });
}

// Couleurs par-dessus le dessin v6 : entrées (orange), puissances / base (violet), lecture (vert), bande écran (jaune).
const dessinerV6 = window.dessiner;
window.dessiner = function () {
  dessinerV6();
  try { surcouche(); } catch (e) { /* la surcouche ne doit jamais casser le dessin */ }
};
function surcouche() {
  if (!circuit.spec || !circuit.germe || !$('couleursCircuit').checked) return;
  const dpr = window.devicePixelRatio || 1; const W = canvas.width; const H = canvas.height; const e = vue.echelle * dpr;
  const ex = (x) => (x + 0.5 - vue.cx) * e + W / 2; const ey = (y) => (y + 0.5 - vue.cy) * e + H / 2;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const g = circuit.germe; const r = Math.max(4 * dpr, e * 0.9);
  ctx.lineWidth = Math.max(1.5, 2 * dpr);
  // cases des entrées
  const casesEntree = new Set();
  if (circuit.spec.entrees && !circuit.spec.variantes) {
    for (const ent of circuit.spec.entrees) for (const p of (circuit.valeurs[ent.nom] ? ent.si1 : ent.si0).points) casesEntree.add(p[0] + ',' + p[1]);
  }
  if (e >= 2) {
    for (const p of g.points) {
      const ent = casesEntree.has(p[0] + ',' + p[1]);
      ctx.strokeStyle = ent ? '#f97316' : '#7c3aed';
      ctx.strokeRect(ex(p[0]) - e / 2, ey(p[1]) - e / 2, e, e);
    }
  }
  // fourmis : entrées en orange, puissances en violet (anneau autour de la position actuelle)
  sim.fourmis.forEach((f, i) => {
    ctx.strokeStyle = i < g.nbEntrees ? '#f97316' : '#7c3aed';
    ctx.beginPath(); ctx.arc(ex(f.x), ey(f.y), r, 0, 2 * Math.PI); ctx.stroke();
  });
  const aff = circuit.spec.affichage;
  if (aff && aff.ecran) { // bande écran
    ctx.strokeStyle = '#eab308'; ctx.lineWidth = Math.max(2, 3 * dpr);
    ctx.beginPath(); ctx.moveTo(0, ey(aff.ecran.y)); ctx.lineTo(W, ey(aff.ecran.y)); ctx.stroke();
    for (const [v, x] of Object.entries(aff.ecran.pixels)) {
      ctx.fillStyle = 'rgba(234,179,8,0.35)'; ctx.fillRect(ex(x) - 6 * e, ey(aff.ecran.y) - 6 * e, 12 * e, 12 * e);
      ctx.fillStyle = '#a16207'; ctx.font = (12 * dpr) + 'px sans-serif'; ctx.fillText(v, ex(x) - 3 * dpr, ey(aff.ecran.y) - 8 * e - 4 * dpr);
    }
  }
  if (circuit.lecture) { // zone de lecture : la fourmi de sortie au pas de lecture
    ctx.strokeStyle = '#16a34a'; ctx.lineWidth = Math.max(2, 3 * dpr);
    for (const s of circuit.spec.sorties) {
      let i = -1;
      if (String(s.fourmi).startsWith('base:')) i = g.nbEntrees + Number(s.fourmi.slice(5));
      if (i >= 0 && sim.fourmis[i]) { const f = sim.fourmis[i]; ctx.beginPath(); ctx.arc(ex(f.x), ey(f.y), r * 2.5, 0, 2 * Math.PI); ctx.stroke(); }
    }
  }
}

// =============================================================================
// 3. Aller au pas N (par tranches : la page reste utilisable ; « Stop » l'interrompt)
// =============================================================================
let allerTravail = 0;
function allerAuPas(N, fini) {
  N = Math.max(0, Math.floor(N));
  definirLecture(false);
  const id = ++allerTravail;
  if (N < sim.pas) retourAuDepart();
  const nf = Math.max(1, sim.fourmis.length);
  const tranche = Math.max(1000, Math.floor(3e6 / nf));
  const etape = () => {
    if (id !== allerTravail) return;
    const k = Math.min(tranche, N - sim.pas);
    if (k > 0) sim.avancer(k);
    $('etatAller').textContent = 'pas ' + fr(sim.pas) + ' / ' + fr(N);
    aRedessiner = true;
    if (sim.pas < N) setTimeout(etape, 0); else { $('etatAller').textContent = 'arrivé au pas ' + fr(N); if (fini) fini(); }
  };
  etape();
}

// =============================================================================
// 4. Grille tournée de 45° (mêmes calculs, seul l'affichage tourne)
// =============================================================================
const R2 = Math.SQRT1_2;
function appliquerRotation() {
  const tourne = $('vueTournee').checked && sim.M === 4;
  const cadre = $('cadre');
  cadre.classList.toggle('tourne', tourne);
  if (tourne) {
    const D = Math.ceil(Math.hypot(cadre.clientWidth, cadre.clientHeight));
    canvas.style.width = D + 'px'; canvas.style.height = D + 'px';
    window.ecranVersLocal = (dx, dy) => [(dx + dy) * R2, (dy - dx) * R2];
  } else {
    canvas.style.width = ''; canvas.style.height = '';
    window.ecranVersLocal = (dx, dy) => [dx, dy];
  }
  ecrireLocal('fourmi-v7-vue-tournee', $('vueTournee').checked);
  aRedessiner = true;
}

// =============================================================================
// 5. Téléphone : zoom et déplacement à deux doigts
// =============================================================================
const doigts = new Map();
let pince = null;
canvas.addEventListener('pointerdown', (ev) => {
  doigts.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
  if (doigts.size === 2) {
    glisse = null; // le geste à un doigt s'arrête
    const [a, b] = [...doigts.values()];
    pince = { d: Math.hypot(a.x - b.x, a.y - b.y), mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2 };
  }
}, true);
canvas.addEventListener('pointermove', (ev) => {
  if (!doigts.has(ev.pointerId)) return;
  doigts.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
  if (doigts.size === 2 && pince) {
    const [a, b] = [...doigts.values()];
    const d = Math.hypot(a.x - b.x, a.y - b.y); const mx = (a.x + b.x) / 2; const my = (a.y + b.y) / 2;
    const r = canvas.getBoundingClientRect();
    const [px, py] = ecranVersLocal(mx - r.left - r.width / 2, my - r.top - r.height / 2);
    if (pince.d > 0 && d > 0) zoomer(d / pince.d, px, py);
    const [dx, dy] = ecranVersLocal(mx - pince.mx, my - pince.my);
    vue.cx -= dx / vue.echelle; vue.cy -= dy / vue.echelle;
    pince = { d, mx, my }; glisse = null; aRedessiner = true;
    ev.stopImmediatePropagation();
  }
}, true);
const finDoigt = (ev) => { doigts.delete(ev.pointerId); if (doigts.size < 2) pince = null; };
canvas.addEventListener('pointerup', finDoigt, true);
canvas.addEventListener('pointercancel', finDoigt, true);

// =============================================================================
// 6. Atelier « Construire » : poser des portes, aimant, brancher, enregistrer
// =============================================================================
const atelier = { pose: null, portes: [] };
// réseau R-50 (RL) : translations (2a, 2b) avec a + b pair, soit (dx, dy) pairs et dx + dy ≡ 0 (mod 4) ; LLR (R-60) : tout est permis
function dansReseauRL(dx, dy) { return dx % 2 === 0 && dy % 2 === 0 && ((dx + dy) % 4 + 4) % 4 === 0; }
function aimanter(dx, dy, regle) {
  if (regle !== 'RL') return [dx, dy];
  let best = null;
  for (let a = -3; a <= 3; a++) for (let b = -3; b <= 3; b++) {
    const x = 2 * Math.round(dx / 2) + 2 * a; const y = 2 * Math.round(dy / 2) + 2 * b;
    if (!dansReseauRL(x, y)) continue;
    const d = Math.hypot(x - dx, y - dy); if (!best || d < best[2]) best = [x, y, d];
  }
  return [best[0], best[1]];
}
function remplirPalette() {
  const sel = $('palettePortes'); sel.textContent = '';
  for (const c of BIB.circuits || []) {
    if (c.variantes || coutCircuit(c) > 4e6) continue; // petites portes seulement
    const o = document.createElement('option'); o.value = c.id; o.textContent = c.regle + ' — ' + c.nom; sel.append(o);
  }
}
function commencerPose() {
  const spec = CIRCUITS.get($('palettePortes').value); if (!spec) return;
  atelier.pose = spec; $('messageAtelier').textContent = 'Touche la grille à l\'endroit où poser « ' + spec.nom + ' » (point d\'ancrage = sa 1re puissance).';
}
canvas.addEventListener('pointerup', (ev) => {
  if (!atelier.pose || pince) return;
  ev.stopImmediatePropagation();
  const spec = atelier.pose; atelier.pose = null;
  const valeurs = {}; for (const e of spec.entrees) valeurs[e.nom] = 0;
  const g = Circuit.composer(spec, valeurs);
  const ancre = spec.base.fourmis[0] || g.fourmis[0] || [0, 0];
  const { x, y } = caseSousPointeur(ev);
  let dx = x - ancre[0]; let dy = y - ancre[1];
  const regleActuelle = sim.regle;
  if (regleActuelle !== g.regle && sim.fourmis.length && atelier.portes.length) {
    $('messageAtelier').textContent = 'Refusé : la grille est en ' + regleActuelle + ', la porte en ' + g.regle + '.'; return;
  }
  if ($('aimant').checked) [dx, dy] = aimanter(dx, dy, g.regle);
  let avert = '';
  if (g.regle === 'RL') {
    for (const p of atelier.portes) {
      const rx = dx - p.dx; const ry = dy - p.dy;
      if (!dansReseauRL(rx, ry)) { avert = ' ⚠ Décalage (' + rx + ', ' + ry + ') par rapport à « ' + p.nom + ' » hors du réseau R-50 : la porte risque de ne plus marcher (vérifie).'; break; }
    }
  }
  const cfg = atelier.portes.length ? sim.exporterConfig() : { regle: g.regle, fourmis: [], dessin: [] };
  const M = Langton.analyserRegle(g.regle).M;
  const t = Circuit.texteGerme(g);
  for (const f of Langton.lireFourmis(t.fourmis, M)) cfg.fourmis.push({ x: f.x + dx, y: f.y + dy, d: f.d });
  for (const p of Langton.lirePoints(t.points).points) cfg.dessin.push([p[0] + dx, p[1] + dy, p[2]]);
  cfg.regle = g.regle;
  fermerCircuit(); definirLecture(false); nouvelleSimulation(cfg);
  atelier.portes.push({ id: spec.id, nom: spec.nom, dx, dy, nbF: g.fourmis.length });
  $('messageAtelier').textContent = 'Posée : « ' + spec.nom + ' » décalée de (' + dx + ', ' + dy + ').' + avert;
  afficherPortes();
}, true);
function afficherPortes() {
  $('listePortes').textContent = atelier.portes.map((p, i) => (i + 1) + '. ' + p.nom + ' (' + p.dx + ', ' + p.dy + ')').join('\n') || '(aucune porte posée)';
}
// « Brancher » (LLR) : ajoute une puissance qui lit la sortie de la dernière fourmi, d'après le gabarit de R-56
// (puissance ↘ en (−141,−40) lue par une puissance ↗ en (−250,450)) tourné selon le cap de la sortie. À vérifier en simulant.
function brancher() {
  if (sim.regle !== 'LLR' || !sim.fourmis.length) { $('messageAtelier').textContent = '« Brancher » marche pour l\'instant en LLR seulement (gabarit R-56).'; return; }
  const cfg = sim.exporterConfig();
  const f = cfg.fourmis[cfg.fourmis.length - 1];
  const r = (f.d - 3 + 4) % 4; // nombre de quarts de tour depuis le gabarit (cap G = 3)
  let ox = -250 - (-141); let oy = 450 - (-40);
  for (let k = 0; k < r; k++) [ox, oy] = [-oy, ox];
  cfg.fourmis.push({ x: f.x + ox, y: f.y + oy, d: (2 + r) % 4 });
  definirLecture(false); nouvelleSimulation(cfg);
  $('messageAtelier').textContent = 'Branché : nouvelle puissance en (' + (f.x + ox) + ', ' + (f.y + oy) + '), cap ' + 'HDBG'[(2 + r) % 4] +
    '. Elle continue tout droit seulement si la sortie lue est absente (NON). Gabarit R-56 : vérifie en simulant.';
}

// =============================================================================
// 7. Démarrage de la v7
// =============================================================================
(function demarrer() {
  $('versionV7').textContent = 'v7 — bibliothèque ' + BIB.version + ', ' + BIB.germes.length + ' éléments, ' + (BIB.circuits || []).length + ' circuits';
  construireArbreGermes('');
  $('calculerCircuit').addEventListener('click', calculer);
  $('tableCircuitBtn').addEventListener('click', touteLaTable);
  $('pasLectureCircuit').addEventListener('click', () => { if (circuit.spec) allerAuPas(Math.max(...circuit.spec.sorties.map((s) => s.pas)), () => { circuit.lecture = true; }); });
  $('couleursCircuit').addEventListener('change', () => { aRedessiner = true; });
  $('allerBtn').addEventListener('click', () => allerAuPas(Number($('allerPas').value)));
  $('stopAller').addEventListener('click', () => { allerTravail++; $('etatAller').textContent = 'arrêté au pas ' + fr(sim.pas); });
  $('vueTournee').checked = !!lireLocal('fourmi-v7-vue-tournee', false);
  $('vueTournee').addEventListener('change', appliquerRotation);
  window.addEventListener('resize', () => { if ($('vueTournee').checked) appliquerRotation(); });
  appliquerRotation();
  remplirPalette();
  $('poserPorte').addEventListener('click', commencerPose);
  $('brancherPorte').addEventListener('click', brancher);
  $('viderAtelier').addEventListener('click', () => { atelier.portes = []; afficherPortes(); $('messageAtelier').textContent = 'Liste vidée (la grille garde ce qui est posé).'; });
  $('enregistrerGerme').addEventListener('click', () => {
    const nom = prompt('Nom du germe à ajouter à « Mes germes » ?', 'Mon circuit');
    if (nom) { enregistrerMonGerme(nom, 'Portes posées : ' + atelier.portes.map((p) => p.nom).join(', ')); $('messageAtelier').textContent = 'Ajouté à « Mes germes » (et téléchargé en JSON).'; }
  });
  afficherPortes();
  // lien direct vers un germe : #germe=ID
  const suivreAdresse = () => {
    const m = location.hash.match(/germe=([^&]+)/);
    if (m) { const g = PAR_ID.get(decodeURIComponent(m[1])); if (g) chargerGerme(g); }
  };
  window.addEventListener('hashchange', suivreAdresse);
  suivreAdresse();
})();

'use strict';
// =============================================================================
//  test.js — tests du moteur.   Lancer avec :   node test.js
//  Aucune dépendance : seulement le module « assert » fourni avec Node.
// =============================================================================
const assert = require('assert');
const Langton = require('./engine.js');
const { Simulation } = Langton;

let reussis = 0;
let rates = 0;
function test(nom, fonction) {
  try {
    fonction();
    reussis++;
    console.log('  ok    ' + nom);
  } catch (erreur) {
    rates++;
    console.log('  ÉCHEC ' + nom + '\n        ' + erreur.message);
  }
}

// Une configuration « compliquée » pour les tests généraux :
// plusieurs fourmis, fond aléatoire, règle à 4 couleurs, une case dessinée.
const CONFIG_RICHE = {
  regle: 'LRNU',
  fourmis: [{ x: 0, y: 0, d: 0 }, { x: 5, y: -3, d: 1 }, { x: -4, y: 2, d: 2 }, { x: 0, y: 0, d: 3 }],
  initial: { type: 'aleatoire', densite: 0.3, graine: 42 },
  dessin: [[1, 0, 2]],
};

console.log('Étape 1 — règles de base');

test('"RL" : les 4 premiers pas à la main', () => {
  // Case blanche (couleur 0) => R. Départ en (0,0) vers le haut, y vers le bas.
  const s = new Simulation({ regle: 'RL' });
  const attendu = [[1, 0, 1], [1, 1, 2], [0, 1, 3], [0, 0, 0]]; // x, y, direction
  for (const [x, y, d] of attendu) {
    s.avancer(1);
    assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y, s.fourmis[0].d], [x, y, d]);
  }
  // 5e pas : la case (0,0) est maintenant de couleur 1 => L (gauche).
  s.avancer(1);
  assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y, s.fourmis[0].d], [-1, 0, 3]);
  assert.strictEqual(s.visites.size, 4);
  assert.strictEqual(s.visitesEn(0, 0), 2);
  assert.strictEqual(s.couleur(0, 0), 0); // N = 2, donc N mod 2 = 0
});

test('"RL" : 11 000 pas => chaque case visitée compte bien ses passages', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(11000);
  let noires = 0;
  for (const v of s.visites.values()) if (v % 2 === 1) noires++;
  console.log('        (cases visitées : ' + s.visites.size + ', cases noires : ' + noires + ')');
  assert.ok(noires > 0 && noires <= s.visites.size);
  // Une fourmi, un passage par pas : la somme des compteurs vaut le nombre de pas.
  let somme = 0;
  for (const v of s.visites.values()) somme += v;
  assert.strictEqual(somme, 11000);
});

test('lettres N et U', () => {
  const tout_droit = new Simulation({ regle: 'N' });
  tout_droit.avancer(10);
  assert.deepStrictEqual([tout_droit.fourmis[0].x, tout_droit.fourmis[0].y], [0, -10]);
  const demi_tour = new Simulation({ regle: 'U' });
  demi_tour.avancer(2); // descend, puis remonte
  assert.deepStrictEqual([demi_tour.fourmis[0].x, demi_tour.fourmis[0].y], [0, 0]);
});

test('motifs initiaux (damier, rayures, carré, aléatoire reproductible)', () => {
  const damier = new Simulation({ initial: { type: 'damier', taille: 1 } });
  assert.strictEqual(damier.couleur(0, 0), 0);
  assert.strictEqual(damier.couleur(1, 0), 1);
  assert.strictEqual(damier.couleur(-1, 0), 1);
  assert.strictEqual(damier.couleur(-1, -1), 0);
  const rayures = new Simulation({ initial: { type: 'rayures', taille: 2 } });
  assert.deepStrictEqual([-2, -1, 0, 1, 2, 3].map((x) => rayures.couleur(x, 7)), [1, 1, 0, 0, 1, 1]);
  const carre = new Simulation({ initial: { type: 'carre', taille: 4 } });
  assert.strictEqual(carre.couleur(-2, -2), 1);
  assert.strictEqual(carre.couleur(1, 1), 1);
  assert.strictEqual(carre.couleur(2, 0), 0);
  // Aléatoire : même graine => mêmes cases ; densité à peu près respectée.
  const a = new Simulation({ initial: { type: 'aleatoire', densite: 0.3, graine: 7 } });
  const b = new Simulation({ initial: { type: 'aleatoire', densite: 0.3, graine: 7 } });
  const c = new Simulation({ initial: { type: 'aleatoire', densite: 0.3, graine: 8 } });
  let pleines = 0;
  let differences = 0;
  for (let x = -50; x < 50; x++) {
    for (let y = -50; y < 50; y++) {
      assert.strictEqual(a.couleur(x, y), b.couleur(x, y));
      pleines += a.couleur(x, y);
      if (a.couleur(x, y) !== c.couleur(x, y)) differences++;
    }
  }
  assert.ok(Math.abs(pleines / 10000 - 0.3) < 0.03, 'densité mesurée : ' + pleines / 10000);
  assert.ok(differences > 1000, 'une autre graine doit donner un autre tirage');
});

test('dessin à la main : le clic fait défiler les couleurs', () => {
  const s = new Simulation({ regle: 'RLR' }); // 3 couleurs
  s.changerCouleur(2, 3);
  assert.strictEqual(s.couleur(2, 3), 1);
  s.changerCouleur(2, 3);
  assert.strictEqual(s.couleur(2, 3), 2);
  assert.deepStrictEqual(s.exporterConfig().dessin, [[2, 3, 2]]);
  s.changerCouleur(2, 3);
  assert.strictEqual(s.couleur(2, 3), 0);
  assert.strictEqual(s.dessin.size, 0);
});

console.log('Étape 1 — déterminisme');

test('même configuration => même résultat', () => {
  const a = new Simulation(CONFIG_RICHE);
  const b = new Simulation(JSON.parse(JSON.stringify(CONFIG_RICHE)));
  a.avancer(5000);
  b.avancer(5000);
  assert.strictEqual(a.etat(), b.etat());
});

test('avancer(5000) = 5000 fois avancer(1)', () => {
  const a = new Simulation(CONFIG_RICHE);
  const b = new Simulation(CONFIG_RICHE);
  a.avancer(5000);
  for (let i = 0; i < 5000; i++) b.avancer(1);
  assert.strictEqual(a.etat(), b.etat());
});

test('export JSON puis import => même simulation', () => {
  const a = new Simulation(CONFIG_RICHE);
  a.changerCouleur(3, 3);
  const b = new Simulation(JSON.parse(JSON.stringify(a.exporterConfig())));
  a.avancer(3000);
  b.avancer(3000);
  assert.strictEqual(a.etat(), b.etat());
});

test('une configuration abîmée est réparée, pas plantée', () => {
  const s = new Simulation({ regle: 'r l x 9', tore: -5, fourmis: 'oups', initial: { type: '???' } });
  assert.strictEqual(s.regle, 'RL');
  assert.strictEqual(s.L, 0);
  assert.strictEqual(s.fourmis.length, 1);
  s.avancer(10);
});

test('champ texte des fourmis : lecture et écriture', () => {
  const fourmis = Langton.lireFourmis('0,0,H ; 10, -2 ,b; 3,4');
  assert.deepStrictEqual(fourmis, [{ x: 0, y: 0, d: 0 }, { x: 10, y: -2, d: 2 }, { x: 3, y: 4, d: 0 }]);
  assert.strictEqual(Langton.ecrireFourmis(fourmis), '0,0,H ; 10,-2,B ; 3,4,H');
});

console.log('Étape 1 — réversibilité');

test('avancer 3000 pas puis reculer 3000 pas => état de départ', () => {
  const s = new Simulation(CONFIG_RICHE);
  const depart = s.etat();
  s.avancer(3000);
  assert.notStrictEqual(s.etat(), depart);
  s.reculer(3000);
  assert.strictEqual(s.etat(), depart);
  assert.strictEqual(s.visites.size, 0);
  assert.strictEqual(s.boite, null);
});

test('reculer pas à pas repasse exactement par les mêmes états', () => {
  const s = new Simulation(CONFIG_RICHE);
  const film = [s.etat()];
  for (let i = 0; i < 300; i++) {
    s.avancer(1);
    film.push(s.etat());
  }
  for (let i = 299; i >= 0; i--) {
    s.reculer(1);
    assert.strictEqual(s.etat(), film[i]);
  }
});

test('reculer ne descend pas sous le pas 0', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(5);
  s.reculer(50);
  assert.strictEqual(s.pas, 0);
});

test('la boîte englobante suit les allers-retours', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(500);
  const boite = JSON.stringify(s.boite);
  s.avancer(2000);
  s.reculer(2000);
  assert.strictEqual(JSON.stringify(s.boite), boite);
});

console.log('Étape 1 — tore');

test('tore : les fourmis restent dans 0..L-1 et la dynamique reste réversible', () => {
  const s = new Simulation({ regle: 'RL', tore: 16, fourmis: [{ x: -1, y: 20, d: 0 }, { x: 3, y: 3, d: 1 }] });
  assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y], [15, 4]);
  const depart = s.etat();
  for (let i = 0; i < 4000; i++) {
    s.avancer(1);
    for (const f of s.fourmis) assert.ok(f.x >= 0 && f.x < 16 && f.y >= 0 && f.y < 16);
  }
  assert.ok(s.visites.size <= 256);
  s.reculer(4000);
  assert.strictEqual(s.etat(), depart);
});

console.log('Étape 2 — détecteur d\'autoroute');

test('"RL" sur grille vide : période 104, déplacement (±2, ±2), début vers 10 000', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(9000);
  assert.strictEqual(s.fourmis[0].autoroute, null, 'pas d\'autoroute à 9000 pas');
  s.avancer(3000);
  const a = s.fourmis[0].autoroute;
  assert.ok(a, 'autoroute détectée à 12 000 pas');
  console.log('        (détecté : période ' + a.periode + ', déplacement (' + a.dx + ', ' + a.dy +
    '), début au pas ' + a.debut + ')');
  assert.strictEqual(a.periode, 104);
  assert.strictEqual(Math.abs(a.dx), 2);
  assert.strictEqual(Math.abs(a.dy), 2);
  assert.ok(a.debut > 9000 && a.debut < 11000, 'début = ' + a.debut);
  assert.ok(a.debutExact);
  // L'autoroute tient toujours beaucoup plus tard, avec le même début.
  s.avancer(500000);
  assert.strictEqual(s.fourmis[0].autoroute.periode, 104);
  assert.strictEqual(s.fourmis[0].autoroute.debut, a.debut);
});

test('"RL" pas à pas : aucune fausse alerte avant, même résultat après', () => {
  const reference = new Simulation({ regle: 'RL' });
  reference.avancer(12000);
  const s = new Simulation({ regle: 'RL' });
  const vues = new Set();
  for (let i = 0; i < 12000; i++) {
    s.avancer(1);
    if (s.fourmis[0].autoroute) vues.add(s.fourmis[0].autoroute.periode);
  }
  assert.deepStrictEqual(Array.from(vues), [104]);
  assert.deepStrictEqual(s.fourmis[0].autoroute, reference.fourmis[0].autoroute);
});

test('reculer avant le début de l\'autoroute => la détection disparaît, puis revient', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(12000);
  const a = Object.assign({}, s.fourmis[0].autoroute);
  s.reculer(100);
  assert.ok(s.fourmis[0].autoroute, 'toujours sur l\'autoroute à 11 900');
  s.reculer(2400);
  assert.strictEqual(s.fourmis[0].autoroute, null, 'plus d\'autoroute à 9 500');
  s.avancer(2500);
  assert.deepStrictEqual(s.fourmis[0].autoroute, a);
});

test('un obstacle sur l\'autoroute fait tomber la détection', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(12000);
  const { dx, dy } = s.fourmis[0].autoroute;
  // On noircit un pavé de cases un peu plus loin sur le chemin de la fourmi.
  const f = s.fourmis[0];
  for (let i = -6; i <= 6; i++) {
    for (let j = -6; j <= 6; j++) s.changerCouleur(f.x + 10 * dx + i, f.y + 10 * dy + j);
  }
  let perdue = false;
  for (let i = 0; i < 3000 && !perdue; i++) {
    s.avancer(1);
    perdue = s.fourmis[0].autoroute === null;
  }
  assert.ok(perdue, 'la détection aurait dû être abandonnée');
});

test('règle "N" : « autoroute » de période 1 ; règle "R" : cycle borné (déplacement nul)', () => {
  const n = new Simulation({ regle: 'N' });
  n.avancer(200);
  assert.deepStrictEqual(n.fourmis[0].autoroute, { periode: 1, dx: 0, dy: -1, debut: 0, debutExact: true });
  const r = new Simulation({ regle: 'R' });
  r.avancer(200);
  assert.strictEqual(r.fourmis[0].autoroute.periode, 4);
  assert.deepStrictEqual([r.fourmis[0].autoroute.dx, r.fourmis[0].autoroute.dy], [0, 0]);
});

test('"RL" : l\'autoroute commence exactement au pas 9 977 (non-régression)', () => {
  const s = new Simulation({ regle: 'RL', fourmis: [{ x: 0, y: 0, d: 'H' }] });
  s.avancer(20000);
  const a = s.fourmis[0].autoroute;
  assert.strictEqual(a.periode, 104);
  assert.strictEqual(a.debut, 9977);
  assert.ok(a.debutExact);
});

test('une autoroute détectée déplace vraiment la fourmi de (dx, dy) à chaque période', () => {
  for (const [regle, pas] of [['RL', 20000], ['H:L1L2NUL2L1R2', 200000]]) {
    const s = new Simulation({ regle });
    s.avancer(pas);
    const a = s.fourmis[0].autoroute;
    assert.ok(a, regle + ' : autoroute attendue');
    const f = s.fourmis[0];
    const [x, y] = [f.x, f.y];
    s.avancer(a.periode);
    assert.deepStrictEqual([f.x - x, f.y - y], [a.dx, a.dy], regle);
  }
});

console.log('Étape 3 — grille hexagonale');

test('lecture des règles : préfixe « H: », jetons, règle carrée inchangée', () => {
  assert.deepStrictEqual(Langton.analyserRegle('H:L2NNL1L2L1'),
    { M: 6, jetons: ['L2', 'N', 'N', 'L1', 'L2', 'L1'], texte: 'H:L2NNL1L2L1' });
  assert.strictEqual(Langton.nettoyerRegle(' h: l1 R2 x u '), 'H:L1R2U');
  assert.strictEqual(Langton.nettoyerRegle('H:RL'), 'H:R1L1'); // R et L seuls = R1 et L1
  assert.strictEqual(Langton.nettoyerRegle('H:'), 'H:R1L1');   // vide : règle par défaut
  assert.deepStrictEqual(Langton.analyserRegle('LLRR'), { M: 4, jetons: ['L', 'L', 'R', 'R'], texte: 'LLRR' });
  assert.strictEqual(Langton.nettoyerRegle('HRL'), 'RL');      // sans « : », H est ignoré comme avant
  const s = new Simulation({ regle: 'H:L1L2NUL2L1R2' });
  assert.strictEqual(s.M, 6);
  assert.strictEqual(s.q, 7);
  assert.deepStrictEqual(Array.from(s.virages), [5, 4, 0, 3, 4, 5, 2]);
});

test('caps hexagonaux : E SE SO O NO NE ou 0..5, lecture et écriture', () => {
  const fourmis = Langton.lireFourmis('0,0,E ; 1,2,so ; -3,4,NE ; 5,5,3 ; 7,7', 6);
  assert.deepStrictEqual(fourmis.map((f) => f.d), [0, 2, 5, 3, 0]);
  assert.strictEqual(Langton.ecrireFourmis(fourmis, 6), '0,0,E ; 1,2,SO ; -3,4,NE ; 5,5,O ; 7,7,E');
  const s = new Simulation({ regle: 'H:N', fourmis: [{ x: 0, y: 0, d: 'NO' }, { x: 0, y: 0, d: 9 }] });
  assert.deepStrictEqual(s.fourmis.map((f) => f.d), [4, 3]);
});

test('directions hexagonales : 0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1)', () => {
  const attendu = [[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]];
  for (let d = 0; d < 6; d++) {
    const s = new Simulation({ regle: 'H:N', fourmis: [{ x: 0, y: 0, d }] });
    s.avancer(3);
    assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y], [3 * attendu[d][0], 3 * attendu[d][1]]);
  }
  // Sens horaire à l'écran : la direction d+1 est à 60° à droite de d.
  for (let d = 0; d < 6; d++) {
    const [X0, Y0] = Langton.centreCase(6, ...attendu[d]);
    const [X1, Y1] = Langton.centreCase(6, ...attendu[(d + 1) % 6]);
    const angle = Math.atan2(X0 * Y1 - Y0 * X1, X0 * X1 + Y0 * Y1); // > 0 = sens horaire (y vers le bas)
    assert.ok(Math.abs(angle - Math.PI / 3) < 1e-9, 'd = ' + d);
    assert.ok(Math.abs(Math.hypot(X0, Y0) - 1) < 1e-9, 'voisins à distance 1');
  }
});

test('un pas hexagonal à la main : lire, tourner, compter, avancer', () => {
  // H:R1L1 : case blanche => R1 (+1), case de couleur 1 => L1 (-1).
  const s = new Simulation({ regle: 'H:R1L1', fourmis: [{ x: 0, y: 0, d: 'E' }] });
  s.avancer(1);
  assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y, s.fourmis[0].d], [0, 1, 1]); // cap SE
  assert.strictEqual(s.couleur(0, 0), 1);
  // H:R1 seule : 6 virages à droite = un petit hexagone, retour au départ.
  const r = new Simulation({ regle: 'H:R1' });
  r.avancer(6);
  assert.deepStrictEqual([r.fourmis[0].x, r.fourmis[0].y, r.fourmis[0].d], [0, 0, 0]);
  assert.strictEqual(r.visites.size, 6);
});

test('H:L2NNL1L2L1, 200 000 pas : 25 574 cases, fourmi en (62, 74), cap 3', () => {
  const s = new Simulation({ regle: 'H:L2NNL1L2L1', fourmis: [{ x: 0, y: 0, d: 'E' }] });
  s.avancer(200000);
  const f = s.fourmis[0];
  assert.strictEqual(s.visites.size, 25574);
  assert.deepStrictEqual([f.x, f.y, f.d], [62, 74, 3]);
});

test('H:L1L2NUL2L1R2, 200 000 pas : 62 472 cases, fourmi en (180, 4), cap 2', () => {
  const s = new Simulation({ regle: 'H:L1L2NUL2L1R2', fourmis: [{ x: 0, y: 0, d: 'E' }] });
  s.avancer(200000);
  const f = s.fourmis[0];
  assert.strictEqual(s.visites.size, 62472);
  assert.deepStrictEqual([f.x, f.y, f.d], [180, 4, 2]);
  const a = f.autoroute;
  console.log('        (détecté : période ' + a.periode + ', déplacement axial (' + a.dx + ', ' + a.dy +
    '), début au pas ' + a.debut + ')');
});

test('200 000 pas en avant puis 200 000 en arrière => grille blanche, fourmi au départ', () => {
  for (const config of [
    { regle: 'RL', fourmis: [{ x: 0, y: 0, d: 'H' }] },
    { regle: 'H:L2NNL1L2L1', fourmis: [{ x: 0, y: 0, d: 'E' }] },
    { regle: 'H:L1L2NUL2L1R2', fourmis: [{ x: 0, y: 0, d: 'E' }] },
  ]) {
    const s = new Simulation(config);
    const depart = s.etat();
    s.avancer(200000);
    s.reculer(200000);
    assert.strictEqual(s.pas, 0);
    assert.strictEqual(s.visites.size, 0, config.regle + ' : grille blanche');
    assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y, s.fourmis[0].d], [0, 0, 0], config.regle);
    assert.strictEqual(s.etat(), depart, config.regle);
    assert.strictEqual(s.boite, null);
    assert.strictEqual(s.fourmis[0].autoroute, null);
  }
});

test('hexagonal : configuration riche, avancer puis reculer pas à pas', () => {
  const config = Object.assign({}, CONFIG_RICHE, { regle: 'H:L1R2NUL2R1' });
  const s = new Simulation(config);
  const film = [s.etat()];
  for (let i = 0; i < 300; i++) {
    s.avancer(1);
    film.push(s.etat());
  }
  for (let i = 299; i >= 0; i--) {
    s.reculer(1);
    assert.strictEqual(s.etat(), film[i]);
  }
});

test('tore hexagonal (parallélogramme L × L en axial) : fourmis dans 0..L-1, réversible', () => {
  const s = new Simulation({ regle: 'H:L2NNL1L2L1', tore: 12,
    fourmis: [{ x: -1, y: 13, d: 'SO' }, { x: 3, y: 3, d: 'NE' }] });
  assert.deepStrictEqual([s.fourmis[0].x, s.fourmis[0].y], [11, 1]);
  const depart = s.etat();
  for (let i = 0; i < 4000; i++) {
    s.avancer(1);
    for (const f of s.fourmis) assert.ok(f.x >= 0 && f.x < 12 && f.y >= 0 && f.y < 12);
  }
  assert.ok(s.visites.size <= 144);
  s.reculer(4000);
  assert.strictEqual(s.etat(), depart);
});

test('géométrie de l\'écran : centre d\'une case -> la même case (arrondi cubique)', () => {
  for (const M of [4, 6]) {
    for (let x = -7; x <= 7; x++) {
      for (let y = -7; y <= 7; y++) {
        const [X, Y] = Langton.centreCase(M, x, y);
        assert.deepStrictEqual(Langton.caseSousPoint(M, X, Y), [x, y]);
        // un point un peu décalé (moins d'un demi-voisin) reste dans la case
        for (let k = 0; k < 6; k++) {
          const a = k + 0.3;
          assert.deepStrictEqual(Langton.caseSousPoint(M, X + 0.4 * Math.cos(a), Y + 0.4 * Math.sin(a)), [x, y]);
        }
      }
    }
  }
  // Un point juste à côté du bord est-ouest de deux hexagones voisins.
  assert.deepStrictEqual(Langton.caseSousPoint(6, 0.49, 0), [0, 0]);
  assert.deepStrictEqual(Langton.caseSousPoint(6, 0.51, 0), [1, 0]);
});

console.log('Étape 3 — grille par blocs et cycle exact');

// Une simulation « de référence », écrite le plus simplement possible et
// indépendamment du moteur (dictionnaire "x,y" -> V), pour vérifier la grille
// par blocs : coordonnées négatives, bords de blocs, tore, plusieurs fourmis.
function referenceNaive(config, pas) {
  const s = new Simulation(config); // seulement pour lire la configuration normalisée
  const M = s.M;
  const dirs = Langton.GEOMETRIES[M].directions;
  const V = new Map();
  const fourmis = s.fourmis.map((f) => ({ x: f.x, y: f.y, d: f.d }));
  for (let t = 0; t < pas; t++) {
    for (const f of fourmis) {
      const cle = f.x + ',' + f.y;
      const v = V.get(cle) || 0;
      const c = (s.couleurInitiale(f.x, f.y) + v) % s.q;
      f.d = (f.d + s.virages[c]) % M;
      V.set(cle, v + 1);
      f.x += dirs[f.d][0];
      f.y += dirs[f.d][1];
      if (s.L) { f.x = Langton.mod(f.x, s.L); f.y = Langton.mod(f.y, s.L); }
    }
  }
  const cases = Array.from(V, ([cle, v]) => cle + ':' + v).sort();
  return 'pas=' + pas + ' | fourmis=' + fourmis.map((f) => f.x + ',' + f.y + ',' + f.d).join(';') +
    ' | cases=' + cases.join(' ');
}

test('le moteur donne exactement le même résultat qu\'une simulation naïve', () => {
  const configs = [
    CONFIG_RICHE,
    Object.assign({}, CONFIG_RICHE, { regle: 'H:L1R2NUL2R1' }),
    { regle: 'RL', fourmis: [{ x: -64, y: -1, d: 3 }, { x: 63, y: 64, d: 1 }] },
    { regle: 'H:L2NNL1L2L1', fourmis: [{ x: -1, y: -1, d: 'O' }] },
    { regle: 'RRL', tore: 70, fourmis: [{ x: 69, y: 0, d: 0 }, { x: 0, y: 69, d: 2 }] },
    { regle: 'H:R1R2L1', tore: 65, initial: { type: 'damier', taille: 3 } },
  ];
  for (const config of configs) {
    const s = new Simulation(config);
    s.avancer(20000);
    assert.strictEqual(s.etat(), referenceNaive(config, 20000), config.regle);
  }
});

test('la grille par blocs se comporte comme un dictionnaire "x,y" -> V', () => {
  const g = new Langton.Grille();
  assert.strictEqual(g.size, 0);
  assert.strictEqual(g.get('-1,-1'), undefined);
  const s = new Simulation({ regle: 'RL', fourmis: [{ x: -1, y: -65, d: 0 }] });
  s.avancer(3000);
  let somme = 0;
  let n = 0;
  for (const [cle, v] of s.visites) {
    assert.strictEqual(s.visites.get(cle), v);
    assert.ok(s.visites.has(cle));
    somme += v;
    n++;
  }
  assert.strictEqual(n, s.visites.size);
  assert.strictEqual(somme, 3000);
  assert.strictEqual(Array.from(s.visites.keys()).length, n);
});

test('cycle exact (retour à l\'état initial) : trouvé quand il existe, oublié en reculant', () => {
  const bonus = new Simulation({ regle: 'RL', fourmis: [{ x: 0, y: 0, d: 0 }, { x: 1, y: 0, d: 0 }] });
  bonus.avancer(1000);
  assert.deepStrictEqual(bonus.cycle, { periode: 28 });
  bonus.reculer(990);
  assert.strictEqual(bonus.cycle, null);
  bonus.avancer(990);
  assert.deepStrictEqual(bonus.cycle, { periode: 28 });
  // Sur un tore, l'espace des états est fini et la dynamique réversible :
  // on revient forcément à l'état initial.
  const tore = new Simulation({ regle: 'RL', tore: 4 });
  tore.avancer(100000);
  assert.ok(tore.cycle, 'cycle sur le tore 4 × 4');
  const p = tore.cycle.periode;
  const verif = new Simulation({ regle: 'RL', tore: 4 });
  const depart = verif.etat().replace(/cases=.*/, '');
  verif.avancer(p);
  for (const v of verif.visites.values()) assert.strictEqual(v % 2, 0, 'toutes les cases blanches');
  assert.strictEqual(verif.etat().replace(/cases=.*/, '').replace('pas=' + p, 'pas=0'), depart);
  // RL seule sur la grille infinie : pas de cycle.
  const rl = new Simulation({ regle: 'RL' });
  rl.avancer(20000);
  assert.strictEqual(rl.cycle, null);
  // Dessiner en cours de route invalide la recherche de cycle.
  const d = new Simulation({ regle: 'H:R1' });
  d.avancer(3);
  d.changerCouleur(5, 5);
  d.avancer(30);
  assert.strictEqual(d.cycle, null);
});

test('cadrage « centre » : la zone de la fourmi au moment où l\'autoroute est reconnue', () => {
  const s = new Simulation({ regle: 'RL' });
  s.avancer(200000);
  const n = s.fourmis[0].noyau;
  const b = s.boite;
  assert.ok(n, 'noyau connu');
  const largeur = (x) => x.xmax - x.xmin + 1;
  console.log('        (zone totale ' + largeur(b) + ' de large, centre ' + largeur(n) + ')');
  assert.ok(largeur(n) < 100 && largeur(b) > 3000);
  assert.ok(n.xmin >= b.xmin && n.xmax <= b.xmax && n.ymin >= b.ymin && n.ymax <= b.ymax);
});

console.log('Étape 4 — outil en ligne de commande');

test('lancer.js : RL, fourmis voisines (cycle exact), rosace hexagonale', () => {
  const { execFileSync } = require('child_process');
  const lancer = (args) => JSON.parse(execFileSync(process.execPath, [require('path').join(__dirname, 'lancer.js'), ...args], { encoding: 'utf8' }));
  const r = lancer(['--regle', 'RL', '--fourmis', '0,0,H', '--pas', '20000', '--compact']);
  assert.strictEqual(r.pas, 20000);
  assert.strictEqual(r.cycle.oui, false);
  assert.strictEqual(r.fourmis[0].autoroute.periode, 104);
  assert.strictEqual(r.fourmis[0].autoroute.debut, 9977);
  // Même résultat que le moteur appelé directement.
  const s = new Simulation({ regle: 'RL' });
  s.avancer(20000);
  assert.strictEqual(r.casesVisitees, s.visites.size);
  assert.deepStrictEqual(r.zone.largeur, s.boite.xmax - s.boite.xmin + 1);
  const c = lancer(['--regle', 'RL', '--fourmis', '0,0,H ; 1,0,H', '--pas', '1000']);
  assert.deepStrictEqual([c.cycle.oui, c.cycle.periode, c.casesVisitees], [true, 28, 16]);
  const h = lancer(['--regle', 'H:L2NNL1L2L1', '--fourmis', '0,0,E', '--pas', '200000']);
  assert.deepStrictEqual([h.casesVisitees, h.fourmis[0].x, h.fourmis[0].y, h.fourmis[0].cap], [25574, 62, 74, 3]);
});

console.log('Étape 5 — cases noires, germes, autoroutes de groupe');

test('lirePoints : formats « x,y » et « x,y,c », séparateurs, commentaires', () => {
  const { points, erreurs } = Langton.lirePoints('# un commentaire\n1,2 ; 3,4,2\n-5, 6   7,-8\r\n\n  # autre\n0,0,0;9,9');
  assert.deepStrictEqual(erreurs, []);
  assert.deepStrictEqual(points, [[1, 2, 1], [3, 4, 2], [-5, 6, 1], [7, -8, 1], [0, 0, 0], [9, 9, 1]]);
});

test('points relatifs à la fourmi 1 : décalés de sa case de départ, puis dans config.dessin', () => {
  const fourmi = { x: 10, y: -3, d: 0 };
  const { points } = Langton.lirePoints('0,0 ; 1,0 ; 0,1,2');
  const dessin = points.map(([x, y, c]) => [x + fourmi.x, y + fourmi.y, c]);
  assert.deepStrictEqual(dessin, [[10, -3, 1], [11, -3, 1], [10, -2, 2]]);
  const s = new Simulation({ regle: 'RLR', fourmis: [fourmi], dessin });
  assert.deepStrictEqual([s.couleur(10, -3), s.couleur(11, -3), s.couleur(10, -2), s.couleur(0, 0)], [1, 1, 2, 0]);
  // et la configuration exportée (lien #c=..., JSON) les garde
  const t = new Simulation(JSON.parse(JSON.stringify(s.exporterConfig())));
  assert.strictEqual(t.etat(), s.etat());
  assert.deepStrictEqual(t.exporterConfig().dessin.sort(), dessin.sort());
});

test('lirePoints : une erreur donne la ligne et le morceau fautifs, le reste est lu', () => {
  const { points, erreurs } = Langton.lirePoints('1,2\n3,4 ; 5\n# ignoré\n6,7,-1 ; a,b ; 8,9.5');
  assert.deepStrictEqual(points, [[1, 2, 1], [3, 4, 1]]);
  assert.deepStrictEqual(erreurs.map((e) => [e.ligne, e.texte]), [[2, '5'], [4, '6,7,-1'], [4, 'a,b'], [4, '8,9.5']]);
  assert.ok(erreurs.every((e) => e.message.length > 0));
});

test('ecrirePoints puis lirePoints : aller-retour exact (et cases noires de RL à 5 000 pas)', () => {
  const points = [[0, 0, 1], [-3, 7, 2], [12, -40, 1], [5, 5, 0]];
  assert.strictEqual(Langton.ecrirePoints(points), '0,0 ; -3,7,2 ; 12,-40 ; 5,5,0');
  assert.deepStrictEqual(Langton.lirePoints(Langton.ecrirePoints(points)), { points, erreurs: [] });
  // Les cases noires de RL à 5 000 pas, recopiées comme départ d'une nouvelle simulation.
  const s = new Simulation({ regle: 'RL' });
  s.avancer(5000);
  const noires = [];
  s.visites.parcourir((x, y) => { if (s.couleur(x, y) === 1) noires.push([x, y, 1]); });
  const relu = Langton.lirePoints(Langton.ecrirePoints(noires)).points;
  const t = new Simulation({ regle: 'RL', dessin: relu });
  s.visites.parcourir((x, y) => assert.strictEqual(t.couleur(x, y), s.couleur(x, y)));
});

test('autoroute de groupe : même période, même déplacement, à moins de 30 cases', () => {
  // Deux fourmis RL éloignées : chacune son autoroute, pas de groupe.
  const loin = new Simulation({ regle: 'RL', fourmis: [{ x: 0, y: 0, d: 0 }, { x: 1000, y: 0, d: 0 }] });
  loin.avancer(30000);
  assert.ok(loin.fourmis.every((f) => f.autoroute && f.autoroute.periode === 104));
  assert.deepStrictEqual(loin.groupesAutoroute(30), []);
  // Fourmis « N » côte à côte (période 1, même déplacement) : un groupe de 3, la 4e trop loin.
  const n = new Simulation({ regle: 'N', fourmis: [{ x: 0, y: 0, d: 1 }, { x: 0, y: 5, d: 1 }, { x: 0, y: 30, d: 1 }, { x: 0, y: 100, d: 1 }] });
  n.avancer(200);
  assert.deepStrictEqual(n.groupesAutoroute(30), [{ fourmis: [0, 1, 2], periode: 1, dx: 1, dy: 0 }]);
  assert.strictEqual(n.bilan().autoroutesDeGroupe.length, 1);
});

// Germes : lus dans germes.js (produit par outils/germes_vers_js.js à partir de germes.json).
require('./germes.js');
function germe(nom) {
  // nom exact, ou suivi d'un complément entre parenthèses : « Autoroute 104 nue (11 cases) »
  return (globalThis.GERMES || []).find((g) => g.nom === nom || g.nom.startsWith(nom + " ("));
}
function simulerGerme(g) {
  const M = Langton.analyserRegle(g.regle).M;
  return new Simulation({ regle: g.regle, fourmis: Langton.lireFourmis(g.fourmis, M), dessin: Langton.lirePoints(g.points).points });
}
for (const [nom, verifier] of [
  ['Germe 3 cases', (a) => assert.ok(Math.abs(a.debut - 126) <= 10, 'début au pas ' + a.debut + ' (attendu vers 126)')],
  ['Autoroute 104 nue', (a) => assert.strictEqual(a.debut, 0, 'début au pas ' + a.debut + ' (attendu dès le début)')],
]) {
  if (!germe(nom)) {
    console.log('  (en attente) germe « ' + nom + ' » absent de germes.js : poser germes.json puis node outils/germes_vers_js.js');
    continue;
  }
  test('germe « ' + nom + ' » : autoroute de période 104', () => {
    const s = simulerGerme(germe(nom));
    s.avancer(5000);
    const a = s.fourmis[0].autoroute;
    assert.ok(a, 'pas d\'autoroute');
    console.log('        (période ' + a.periode + ', déplacement (' + a.dx + ', ' + a.dy + '), début au pas ' + a.debut + ')');
    assert.strictEqual(a.periode, 104);
    verifier(a);
  });
}

console.log('\n' + reussis + ' test(s) réussi(s), ' + rates + ' échec(s).');
process.exit(rates === 0 ? 0 : 1);

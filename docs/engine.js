'use strict';
// =============================================================================
//  engine.js — moteur de la fourmi de Langton (généralisée), SANS aucun DOM.
//
//  Ce fichier marche tel quel dans le navigateur (<script src="engine.js">)
//  et dans Node (const Langton = require('./engine.js')).
//  La page (ui.js), les tests (test.js) et l'outil en ligne de commande
//  (lancer.js) utilisent tous ce même fichier.
//
//  LE MODÈLE
//  ---------
//  * Deux grilles possibles :
//      - carrée (M = 4 directions), coordonnées (x, y) habituelles ;
//      - hexagonale (M = 6 directions), coordonnées AXIALES (x, y).
//    Dans les deux cas une case est un couple d'entiers (x, y), et une
//    direction est un numéro d (entier modulo M) : le reste du moteur ne
//    fait pas la différence.
//  * Chaque case (x, y) porte un compteur entier N.
//    Sa couleur est  c = N mod q,  où q = nombre de lettres de la règle.
//  * On écrit  N = N0 + V  avec
//        N0 = couleur initiale de la case (motif de départ ou dessin à la main),
//        V  = nombre de passages d'une fourmi sur la case.
//    On ne stocke que V, dans une « grille par blocs » (classe Grille) :
//    un bloc de 64 × 64 compteurs n'est créé que lorsqu'une fourmi y entre.
//    La grille est donc infinie, et une case jamais visitée a V = 0.
//  * À chaque pas, pour chaque fourmi dans l'ordre :
//        1. lire la couleur c de sa case ;
//        2. tourner : cap <- (cap + virage[c]) mod M ;
//        3. incrémenter le compteur de la case ;
//        4. avancer d'une case dans la direction du cap.
//
//  CONVENTION D'AXES : comme à l'écran, x vers la droite et y vers le BAS.
// =============================================================================

// ----------------------------------------------------------------------------
// 1. Géométries : directions et virages
// ----------------------------------------------------------------------------
// Les M directions sont rangées dans le sens horaire (à l'écran, y vers le bas).
// Un virage = de combien on ajoute au numéro de direction (toujours entre
// 0 et M-1, pour que le modulo M reste simple).
const GEOMETRIES = {
  // Grille carrée : règle écrite avec R L N U, par ex. « RL ».
  4: {
    M: 4,
    nom: 'carrée',
    directions: [
      [0, -1], // 0 : haut
      [1, 0],  // 1 : droite
      [0, 1],  // 2 : bas
      [-1, 0], // 3 : gauche
    ],
    noms: ['H', 'D', 'B', 'G'], // Haut, Droite, Bas, Gauche
    virages: {
      R: 1, // à droite  : +1 cran (sens horaire)
      L: 3, // à gauche  : -1 cran, c'est-à-dire +3 modulo 4
      N: 0, // tout droit
      U: 2, // demi-tour
    },
  },
  // Grille hexagonale, coordonnées axiales (x, y). Mêmes conventions que
  // l'outil de vérification bestiaire2.c. Règle écrite « H:... », par ex.
  // « H:L2NNL1L2L1 ».
  6: {
    M: 6,
    nom: 'hexagonale',
    directions: [
      [1, 0],  // 0 : E   (est)
      [0, 1],  // 1 : SE  (sud-est)
      [-1, 1], // 2 : SO  (sud-ouest)
      [-1, 0], // 3 : O   (ouest)
      [0, -1], // 4 : NO  (nord-ouest)
      [1, -1], // 5 : NE  (nord-est)
    ],
    noms: ['E', 'SE', 'SO', 'O', 'NO', 'NE'],
    virages: {
      N: 0,  // tout droit
      R1: 1, // à droite de 60°
      R2: 2, // à droite de 120°
      U: 3,  // demi-tour
      L2: 4, // à gauche de 120° (-2 modulo 6)
      L1: 5, // à gauche de 60°  (-1 modulo 6)
    },
  },
};
const PREFIXE_HEXAGONAL = 'H:';
// Autres noms acceptés à la saisie pour les directions hexagonales.
const ALIAS_HEXAGONAUX = { SW: 2, W: 3, NW: 4 };

// Noms historiques (grille carrée), gardés pour compatibilité.
const DIRECTIONS = GEOMETRIES[4].directions;
const NOMS_DIRECTIONS = GEOMETRIES[4].noms;
const TOURS = GEOMETRIES[4].virages;

// ----------------------------------------------------------------------------
// 2. Constantes du détecteur d'autoroute et de la grille
// ----------------------------------------------------------------------------
const TAILLE_HISTO = 65536;        // mémoire par fourmi (puissance de 2)
const FOURMIS_MAX = 1000;          // v7 : 1000 fourmis au plus (v6 : 100) ; 128 Ko d’historique par fourmi
const MASQUE_HISTO = TAILLE_HISTO - 1;
const PERIODE_MAX = 20000;         // plus grande période cherchée
const INTERVALLE_RECHERCHE = 4096; // on cherche au moins tous les 4096 pas
                                   // (et à la fin de chaque appel à avancer)
const NB_PERIODES = 3;             // répétition exigée : 3 périodes...
const LONGUEUR_MIN = 100;          // ...et au moins 100 pas (évite les fausses
                                   // alertes sur de toutes petites périodes)
// Il faut  NB_PERIODES * PERIODE_MAX + INTERVALLE_RECHERCHE <= TAILLE_HISTO
// pour que le début de l'autoroute soit encore en mémoire quand on la détecte.

const LONGUEUR_REGLE_MAX = 64;     // q <= 64
const TYPES_INITIAUX = ['vide', 'damier', 'rayures', 'aleatoire', 'carre'];

// Grille par blocs : un bloc = 64 × 64 cases.
const BITS_BLOC = 6;
const COTE_BLOC = 1 << BITS_BLOC;  // 64
const MASQUE_BLOC = COTE_BLOC - 1; // 63
// Les numéros de bloc vont de -2^24 à 2^24 : les coordonnées des cases
// restent donc dans ± 2^30 (environ un milliard), ce qui permet d'utiliser
// les opérations sur 32 bits (>> et &), bien plus rapides.
const BLOC_MAX = 1 << 24;
const COORD_MAX = 1e9;             // borne des coordonnées saisies

// ----------------------------------------------------------------------------
// 3. Petits outils
// ----------------------------------------------------------------------------
// Modulo toujours positif : mod(-1, 5) = 4 (alors que -1 % 5 = -1 en JavaScript).
function mod(a, n) {
  return ((a % n) + n) % n;
}

function entier(v, defaut) {
  const n = Math.round(Number(v));
  return Number.isFinite(n) ? n : defaut;
}

function borner(v, min, max) {
  return Math.min(max, Math.max(min, v));
}

// Nombre pseudo-aléatoire dans [0, 1[ qui ne dépend QUE de (x, y, graine).
// C'est une « fonction de hachage » : pas d'état caché, donc on peut demander
// la couleur de n'importe quelle case d'une grille infinie, dans n'importe
// quel ordre, et retrouver exactement le même tirage avec la même graine.
function hasard(x, y, graine) {
  let h = Math.imul(x, 0x27d4eb2d) ^ Math.imul(y, 0x165667b1) ^ Math.imul(graine, 0x9e3779b1);
  h = Math.imul(h ^ (h >>> 15), 0x85ebca6b);
  h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}

// ----------------------------------------------------------------------------
// 4. Géométrie de l'écran (utilisée par l'interface, testée par test.js)
// ----------------------------------------------------------------------------
// Le « plan » est l'écran sans le zoom ni le décalage : 1 unité = 1 case.
//  * carré : la case (x, y) est le carré [x, x+1[ × [y, y+1[ ;
//  * hexagone (pointe en haut) : la case axiale (x, y) a pour centre
//        X = x + y/2,   Y = y · √3/2
//    deux cases voisines ont leurs centres à distance 1.
const RACINE3_SUR_2 = Math.sqrt(3) / 2;

// Centre de la case (x, y) dans le plan.
function centreCase(M, x, y) {
  if (M === 6) return [x + y / 2, y * RACINE3_SUR_2];
  return [x + 0.5, y + 0.5];
}

// Case qui contient le point (X, Y) du plan.
// Hexagone : on repasse en coordonnées axiales (non entières), puis on arrondit
// en coordonnées « cubiques » (x, y, z) avec x + y + z = 0 : on arrondit les
// trois, et on recalcule celle qui a été le plus modifiée par l'arrondi.
function caseSousPoint(M, X, Y) {
  if (M !== 6) return [Math.floor(X), Math.floor(Y)];
  const fy = Y / RACINE3_SUR_2;
  const fx = X - fy / 2;
  const fz = -fx - fy;
  let rx = Math.round(fx);
  let ry = Math.round(fy);
  const rz = Math.round(fz);
  const ex = Math.abs(rx - fx);
  const ey = Math.abs(ry - fy);
  const ez = Math.abs(rz - fz);
  if (ex > ey && ex > ez) rx = -ry - rz;
  else if (ey > ez) ry = -rx - rz;
  return [rx + 0, ry + 0]; // « + 0 » transforme un éventuel -0 en 0
}

// ----------------------------------------------------------------------------
// 5. Règles et configuration
// ----------------------------------------------------------------------------
// Lit un mot-règle et renvoie { M, jetons, texte } :
//   « RL »          -> { M: 4, jetons: ['R', 'L'], texte: 'RL' }
//   « H:L2NNL1L2L1 » -> { M: 6, jetons: ['L2', 'N', 'N', 'L1', 'L2', 'L1'], ... }
// Les caractères inconnus sont ignorés. En hexagonal, « R » et « L » seuls
// valent R1 et L1.
function analyserRegle(texte) {
  const brut = String(texte == null ? '' : texte).toUpperCase().replace(/\s+/g, '');
  if (brut.startsWith(PREFIXE_HEXAGONAL)) {
    let jetons = (brut.slice(PREFIXE_HEXAGONAL.length).match(/[RL][12]?|N|U/g) || [])
      .map((j) => (j === 'R' || j === 'L' ? j + '1' : j))
      .slice(0, LONGUEUR_REGLE_MAX);
    if (jetons.length === 0) jetons = ['R1', 'L1'];
    return { M: 6, jetons, texte: PREFIXE_HEXAGONAL + jetons.join('') };
  }
  const mot = brut.replace(/[^RLNU]/g, '').slice(0, LONGUEUR_REGLE_MAX) || 'RL';
  return { M: 4, jetons: Array.from(mot), texte: mot };
}

// Nettoie un mot-règle (voir analyserRegle) et le renvoie sous forme de texte.
function nettoyerRegle(texte) {
  return analyserRegle(texte).texte;
}

// Une configuration est un objet simple (sérialisable en JSON) qui décrit
// entièrement une expérience. Même configuration => même simulation.
function configParDefaut() {
  return {
    regle: 'RL',                     // le mot-règle (« H:... » = grille hexagonale)
    tore: 0,                         // 0 = grille infinie ; sinon taille L du tore
    fourmis: [{ x: 0, y: 0, d: 0 }], // position et direction de départ
    initial: {
      type: 'vide',                  // 'vide', 'damier', 'rayures', 'aleatoire', 'carre'
      taille: 8,                     // taille des carreaux / largeur des rayures / côté du carré
      densite: 0.5,                  // pour 'aleatoire' : fraction de cases colorées
      graine: 1,                     // pour 'aleatoire' : graine du tirage
    },
    dessin: [],                      // cases dessinées à la main : [[x, y, couleur], ...]
  };
}

// Accepte une direction donnée par numéro (0..M-1) ou par nom
// (H, D, B, G en carré ; E, SE, SO, O, NO, NE en hexagonal).
function lireDirection(d, M = 4) {
  if (typeof d === 'string') {
    const nom = d.trim().toUpperCase();
    const i = GEOMETRIES[M].noms.indexOf(nom);
    if (i >= 0) return i;
    if (M === 6 && ALIAS_HEXAGONAUX[nom] !== undefined) return ALIAS_HEXAGONAUX[nom];
  }
  return mod(entier(d, 0), M);
}

// Rend une configuration complète et valide à partir d'un objet quelconque
// (par exemple lu dans une URL ou un fichier : on ne lui fait pas confiance).
function normaliserConfig(c) {
  c = c || {};
  const defaut = configParDefaut();
  const ini = c.initial || {};
  const regle = analyserRegle(c.regle);

  let tore = entier(c.tore, 0);
  tore = tore >= 2 ? borner(tore, 2, 1000) : 0;

  const coordonnee = (v) => borner(entier(v, 0), -COORD_MAX, COORD_MAX);
  let fourmis = Array.isArray(c.fourmis) ? c.fourmis.slice(0, FOURMIS_MAX) : [];
  fourmis = fourmis.map((f) => ({
    x: coordonnee(f && f.x),
    y: coordonnee(f && f.y),
    d: lireDirection(f && f.d, regle.M),
  }));
  if (fourmis.length === 0) fourmis = defaut.fourmis;

  const dessin = (Array.isArray(c.dessin) ? c.dessin : [])
    .filter((t) => Array.isArray(t) && t.length >= 3)
    .map((t) => [coordonnee(t[0]), coordonnee(t[1]), Math.max(0, entier(t[2], 0))]);

  const densite = Number(ini.densite);
  return {
    regle: regle.texte,
    tore,
    fourmis,
    initial: {
      type: TYPES_INITIAUX.includes(ini.type) ? ini.type : 'vide',
      taille: borner(entier(ini.taille, defaut.initial.taille), 1, 1000),
      densite: Number.isFinite(densite) ? borner(densite, 0, 1) : defaut.initial.densite,
      graine: entier(ini.graine, defaut.initial.graine),
    },
    dessin,
  };
}

// Fourmis <-> texte, pour le champ de l'interface et l'outil en ligne de commande.
// Format : "x,y,d ; x,y,d ; ..."
//   carré     : d parmi H, D, B, G          ex. "0,0,H ; 10,0,B"
//   hexagonal : d parmi E, SE, SO, O, NO, NE ex. "0,0,E ; 5,-2,NO"
function ecrireFourmis(fourmis, M = 4) {
  const noms = GEOMETRIES[M].noms;
  return fourmis.map((f) => f.x + ',' + f.y + ',' + noms[mod(f.d, M)]).join(' ; ');
}

function lireFourmis(texte, M = 4) {
  const fourmis = [];
  for (const morceau of String(texte).split(';')) {
    const champs = morceau.split(',').map((s) => s.trim());
    if (champs.length < 2 || champs[0] === '' || champs[1] === '') continue;
    const x = Number(champs[0]);
    const y = Number(champs[1]);
    if (!Number.isFinite(x) || !Number.isFinite(y)) continue;
    fourmis.push({ x: Math.round(x), y: Math.round(y), d: lireDirection(champs[2] || '0', M) });
  }
  return fourmis;
}

// Liste de cases colorées <-> texte (panneau « Cases noires », germes).
// Format : "x,y" (couleur 1) ou "x,y,c", séparés par ; ou un retour à la ligne
// ou des espaces. Les lignes qui commencent par # sont des commentaires.
// Renvoie { points: [[x, y, c], ...], erreurs: [{ ligne, texte, message }, ...] }.
function lirePoints(texte) {
  const points = [];
  const erreurs = [];
  String(texte == null ? '' : texte).split(/\r?\n/).forEach((brute, i) => {
    const ligne = brute.trim();
    if (ligne === '' || ligne.startsWith('#')) return;
    // « 3, 4 » = « 3,4 » : les espaces autour des virgules ne séparent pas.
    for (const morceau of ligne.replace(/\s*,\s*/g, ',').split(/[;\s]+/)) {
      if (morceau === '') continue;
      const champs = morceau.split(',');
      const nombres = champs.map(Number);
      let message = null;
      if (champs.length < 2 || champs.length > 3) message = 'il faut « x,y » ou « x,y,c »';
      else if (!nombres.every(Number.isInteger)) message = 'nombres entiers attendus';
      else if (champs.length === 3 && nombres[2] < 0) message = 'la couleur doit être positive';
      if (message) erreurs.push({ ligne: i + 1, texte: morceau, message });
      else points.push([nombres[0], nombres[1], champs.length === 3 ? nombres[2] : 1]);
    }
  });
  return { points, erreurs };
}

function ecrirePoints(points) {
  return points.map(([x, y, c]) => (c === 1 || c === undefined ? x + ',' + y : x + ',' + y + ',' + c)).join(' ; ');
}

// Fabrique la fonction fond(x, y) -> couleur initiale (avant modulo q)
// correspondant au motif choisi. Tous les motifs sont définis par une formule,
// donc valables sur toute la grille infinie. En hexagonal, les formules
// s'appliquent aux coordonnées axiales (un « carré » y devient un losange).
function fabriquerFond(initial) {
  const t = initial.taille;
  switch (initial.type) {
    case 'damier': // carreaux de côté t
      return (x, y) => mod(Math.floor(x / t) + Math.floor(y / t), 2);
    case 'rayures': // bandes de largeur t (verticales en carré)
      return (x, y) => mod(Math.floor(x / t), 2);
    case 'carre': { // carré plein de côté t, centré sur l'origine
      const a = -Math.floor(t / 2); // premier indice du carré
      return (x, y) => (x >= a && x < a + t && y >= a && y < a + t ? 1 : 0);
    }
    case 'aleatoire': // la couleur est tirée plus bas
      return null;
    default: // 'vide'
      return () => 0;
  }
}

// ----------------------------------------------------------------------------
// 6. La grille par blocs
// ----------------------------------------------------------------------------
// Un bloc : { bx, by, v, n }
//   (bx, by) = numéro du bloc : il contient les cases x = 64·bx .. 64·bx + 63
//              (idem en y) ;
//   v        = les 64 × 64 compteurs V, ligne par ligne (Uint32Array) ;
//   n        = nombre de cases du bloc avec V > 0 ;
//   version  = augmente à chaque changement d'un compteur du bloc (l'interface
//              s'en sert pour savoir si son résumé du bloc est encore bon).
// Indice d'une case dans son bloc : ((y & 63) << 6) | (x & 63).
//
// Pour que le reste du code (et les tests) puisse s'en servir comme d'un
// dictionnaire "x,y" -> V, la classe offre aussi size, get, has, keys,
// values, entries et for...of, comme un Map.
function cleBloc(bx, by) {
  return (bx + BLOC_MAX) * (2 * BLOC_MAX + 1) + (by + BLOC_MAX);
}

class Grille {
  constructor() {
    this.blocs = new Map(); // cleBloc -> bloc
    this.size = 0;          // nombre de cases avec V > 0
  }

  // Le bloc qui contient la case (x, y), ou undefined.
  blocDe(x, y) {
    return this.blocs.get(cleBloc(x >> BITS_BLOC, y >> BITS_BLOC));
  }

  // Le bloc n° (bx, by), créé s'il n'existe pas encore.
  blocCree(bx, by) {
    const cle = cleBloc(bx, by);
    let b = this.blocs.get(cle);
    if (!b) {
      if (Math.abs(bx) >= BLOC_MAX || Math.abs(by) >= BLOC_MAX) {
        throw new RangeError('Une fourmi est allée trop loin (coordonnée au-delà de ' + BLOC_MAX * COTE_BLOC + ').');
      }
      b = { bx, by, v: new Uint32Array(COTE_BLOC * COTE_BLOC), n: 0, version: 0 };
      this.blocs.set(cle, b);
    }
    return b;
  }

  // Nombre de passages V sur la case (x, y).
  lire(x, y) {
    const b = this.blocDe(x, y);
    return b ? b.v[((y & MASQUE_BLOC) << BITS_BLOC) | (x & MASQUE_BLOC)] : 0;
  }

  // Appelle fonction(x, y, V) pour chaque case avec V > 0.
  parcourir(fonction) {
    for (const b of this.blocs.values()) {
      if (b.n === 0) continue;
      const x0 = b.bx << BITS_BLOC;
      const y0 = b.by << BITS_BLOC;
      const v = b.v;
      for (let i = 0; i < v.length; i++) {
        if (v[i] !== 0) fonction(x0 + (i & MASQUE_BLOC), y0 + (i >> BITS_BLOC), v[i]);
      }
    }
  }

  // --- interface « comme un Map » ---
  get(cle) {
    const k = String(cle).indexOf(',');
    const v = this.lire(Number(cle.slice(0, k)), Number(cle.slice(k + 1)));
    return v === 0 ? undefined : v;
  }

  has(cle) {
    return this.get(cle) !== undefined;
  }

  *entries() {
    for (const b of this.blocs.values()) {
      if (b.n === 0) continue;
      const x0 = b.bx << BITS_BLOC;
      const y0 = b.by << BITS_BLOC;
      for (let i = 0; i < b.v.length; i++) {
        if (b.v[i] !== 0) yield [(x0 + (i & MASQUE_BLOC)) + ',' + (y0 + (i >> BITS_BLOC)), b.v[i]];
      }
    }
  }

  *keys() {
    for (const [cle] of this.entries()) yield cle;
  }

  *values() {
    for (const b of this.blocs.values()) {
      if (b.n === 0) continue;
      for (let i = 0; i < b.v.length; i++) if (b.v[i] !== 0) yield b.v[i];
    }
  }

  [Symbol.iterator]() {
    return this.entries();
  }
}

// ----------------------------------------------------------------------------
// 7. Boîtes englobantes
// ----------------------------------------------------------------------------
// Une boîte : { xmin, xmax, ymin, ymax, zmin, zmax } avec z = 2x + y.
// En hexagonal, z/2 est l'abscisse à l'écran du centre de la case : la boîte
// en z sert à cadrer exactement la forme (inutile, mais inoffensif, en carré).
function boitePoint(x, y) {
  const z = 2 * x + y;
  return { xmin: x, xmax: x, ymin: y, ymax: y, zmin: z, zmax: z };
}

function etendreBoite(b, x, y) {
  if (x < b.xmin) b.xmin = x;
  if (x > b.xmax) b.xmax = x;
  if (y < b.ymin) b.ymin = y;
  if (y > b.ymax) b.ymax = y;
  const z = 2 * x + y;
  if (z < b.zmin) b.zmin = z;
  if (z > b.zmax) b.zmax = z;
}

function copierBoite(b) {
  return b ? Object.assign({}, b) : null;
}

// ----------------------------------------------------------------------------
// 8. La simulation
// ----------------------------------------------------------------------------
class Simulation {
  constructor(config) {
    this.config = normaliserConfig(config);

    // Le dessin à la main : dictionnaire "x,y" -> couleur initiale imposée.
    // Il survit au « retour au départ » (il fait partie de la situation initiale).
    this.dessin = new Map();
    for (const [x, y, c] of this.config.dessin) this.dessin.set(x + ',' + y, c);

    this.reinitialiser();
  }

  // Remet la simulation au pas 0 (sans toucher à la configuration).
  reinitialiser() {
    const cfg = this.config;
    const regle = analyserRegle(cfg.regle);
    this.regle = regle.texte;
    this.jetons = regle.jetons;      // une « lettre » par couleur : 'R', 'L2', ...
    this.q = regle.jetons.length;    // nombre de couleurs
    this.M = regle.M;                // 4 (carré) ou 6 (hexagone)
    this.geometrie = GEOMETRIES[this.M];
    this.L = cfg.tore;               // 0 = infini, sinon taille du tore
    // Pour aller vite : déplacements et virages dans des tableaux d'entiers.
    this._dx = Int32Array.from(this.geometrie.directions, (d) => d[0]);
    this._dy = Int32Array.from(this.geometrie.directions, (d) => d[1]);
    // virages[c] = rotation à appliquer quand on lit la couleur c
    this.virages = Int32Array.from(regle.jetons, (j) => this.geometrie.virages[j]);

    // Fonction couleur de fond (voir fabriquerFond).
    const fond = fabriquerFond(cfg.initial);
    const q = this.q;
    const { densite, graine } = cfg.initial;
    const fondBrut = fond
      ? (x, y) => fond(x, y) % q
      : (x, y) => {
          // 'aleatoire' : avec la probabilité « densite », la case reçoit une
          // couleur non nulle tirée uniformément parmi 1 .. q-1.
          const u = hasard(x, y, graine);
          if (u >= densite) return 0;
          return (1 + Math.floor((u / densite) * (q - 1))) % q;
        };
    // Sur le tore, les coordonnées vivent dans 0 .. L-1. Pour que les motifs
    // restent centrés sur l'origine, on évalue le fond sur le représentant
    // de la case situé dans [-L/2, L/2[.
    const L = this.L;
    this.fond = L
      ? (x, y) => fondBrut(x >= L / 2 ? x - L : x, y >= L / 2 ? y - L : y)
      : fondBrut;
    this.fondVide = cfg.initial.type === 'vide';

    this.visites = new Grille(); // V de chaque case
    this.pas = 0;                // nombre de pas effectués
    this.maxVisites = 0;         // plus grand V rencontré (pour l'échelle de la carte)
    this._boite = null;          // boîte englobante des cases visitées (voir « get boite »)
    this._boiteFausse = false;   // true = à recalculer avant usage

    // Cycle exact : on compte les cases dont la couleur diffère de la couleur
    // initiale (V non multiple de q). Quand ce nombre vaut 0 ET que toutes les
    // fourmis sont revenues à leur position et à leur cap de départ, l'état
    // complet est redevenu l'état initial : c'est un cycle, et c'est une
    // PREUVE (le mouvement se répétera à l'identique pour toujours).
    this.casesChangees = 0;
    this.cycle = null;           // null, ou { periode } (premier retour à l'état initial)
    this._cycleImpossible = false; // devient true si on dessine en cours de route

    this.fourmis = cfg.fourmis.map((f) => {
      const x = this.replier(f.x);
      const y = this.replier(f.y);
      return {
        x, y,
        d: f.d,
        depart: { x, y, d: f.d },
        bloc: null,                          // dernier bloc utilisé (accélère avancer)
        boite: null,                         // boîte des cases visitées par CETTE fourmi
        noyau: null,                         // sa boîte quand son autoroute a été détectée
        // --- pour le détecteur d'autoroute ---
        histo: new Uint16Array(TAILLE_HISTO), // derniers « symboles » (voir avancer)
        dispo: 0,                             // combien de symboles récents sont valides
        autoroute: null,                      // résultat de la détection, ou null
      };
    });
  }

  // Ramène une coordonnée dans 0 .. L-1 sur le tore (ne fait rien si infini).
  replier(a) {
    return this.L ? mod(a, this.L) : a;
  }

  // Couleur initiale N0 de la case : le dessin à la main s'il y en a un,
  // sinon le motif de fond.
  couleurInitiale(x, y) {
    if (this.dessin.size > 0) {
      const c = this.dessin.get(x + ',' + y);
      if (c !== undefined) return c % this.q;
    }
    return this.fond(x, y);
  }

  // Nombre de passages V sur la case.
  visitesEn(x, y) {
    return this.visites.lire(x, y);
  }

  // Couleur actuelle de la case : (N0 + V) mod q.
  couleur(x, y) {
    return (this.couleurInitiale(x, y) + this.visitesEn(x, y)) % this.q;
  }

  // Boîte englobante des cases visitées : { xmin, xmax, ymin, ymax, zmin, zmax }
  // (z = 2x + y), ou null s'il n'y en a aucune. Recalculée seulement si besoin.
  get boite() {
    if (this._boiteFausse) {
      this._boiteFausse = false;
      this._boite = null;
      this.visites.parcourir((x, y) => {
        if (this._boite) etendreBoite(this._boite, x, y);
        else this._boite = boitePoint(x, y);
      });
    }
    return this._boite;
  }

  // ---------------------------------------------------------------- avancer
  avancer(n = 1) {
    const { q, L, M, virages, fourmis } = this;
    const DX = this._dx;
    const DY = this._dy;
    const grille = this.visites;
    const nf = fourmis.length;
    for (let k = 0; k < n; k++) {
      const t = this.pas; // numéro du pas qu'on est en train de faire
      for (let i = 0; i < nf; i++) {
        const f = fourmis[i];
        const x = f.x;
        const y = f.y;
        // Le bloc de la case (souvent le même qu'au pas précédent).
        const bx = x >> BITS_BLOC;
        const by = y >> BITS_BLOC;
        let b = f.bloc;
        if (b === null || b.bx !== bx || b.by !== by) {
          b = grille.blocCree(bx, by);
          f.bloc = b;
        }
        const indice = ((y & MASQUE_BLOC) << BITS_BLOC) | (x & MASQUE_BLOC);
        const v = b.v[indice];
        const n0 = this.fondVide && this.dessin.size === 0 ? 0 : this.couleurInitiale(x, y);

        // 1. lire la couleur
        const c = (n0 + v) % q;
        // 2. tourner
        const d = (f.d + virages[c]) % M;
        f.d = d;
        // 3. incrémenter le compteur de la case
        b.v[indice] = v + 1;
        b.version++;
        if (v === 0) {
          b.n++;
          grille.size++;
          if (!this._boiteFausse) {
            if (this._boite) etendreBoite(this._boite, x, y);
            else this._boite = boitePoint(x, y);
          }
        }
        if (v >= this.maxVisites) this.maxVisites = v + 1;
        if (v % q === 0) this.casesChangees++;       // la case quitte sa couleur initiale...
        if ((v + 1) % q === 0) this.casesChangees--; // ...ou y revient
        if (f.boite) etendreBoite(f.boite, x, y);
        else if (t > 0 && this.boite) f.boite = copierBoite(this.boite); // après un recul
        else f.boite = boitePoint(x, y);
        // 4. avancer (sur le tore, on ne sort que d'une case : un test suffit)
        let nx = x + DX[d];
        let ny = y + DY[d];
        if (L) {
          if (nx < 0) nx += L; else if (nx >= L) nx -= L;
          if (ny < 0) ny += L; else if (ny >= L) ny -= L;
        }
        f.x = nx;
        f.y = ny;

        // Mémoire pour le détecteur : un « symbole » par pas, qui résume
        // (couleur lue, direction prise). Si la suite des symboles est
        // périodique, alors la suite des couleurs lues ET le déplacement
        // par période se répètent tous les deux.
        const symbole = c * M + d;
        f.histo[t & MASQUE_HISTO] = symbole;
        if (f.dispo < TAILLE_HISTO) f.dispo++;
        // Si une autoroute était détectée, on vérifie à chaque pas qu'elle
        // continue. Sinon on l'oublie : une détection n'est pas une preuve !
        if (f.autoroute && symbole !== f.histo[(t - f.autoroute.periode) & MASQUE_HISTO]) {
          f.autoroute = null;
          f.noyau = null;
        }
      }
      this.pas = t + 1;
      if (this.casesChangees === 0 && this.cycle === null && !this._cycleImpossible && this._fourmisAuDepart()) {
        this.cycle = { periode: this.pas };
      }
      if (this.pas % INTERVALLE_RECHERCHE === 0) this.chercherAutoroutes();
    }
    this.chercherAutoroutes();
  }

  _fourmisAuDepart() {
    for (const f of this.fourmis) {
      if (f.x !== f.depart.x || f.y !== f.depart.y || f.d !== f.depart.d) return false;
    }
    return true;
  }

  // ---------------------------------------------------------------- reculer
  // La dynamique est réversible : on défait exactement les 4 opérations,
  // dans l'ordre inverse, en parcourant les fourmis dans l'ordre inverse.
  reculer(n = 1) {
    const { q, L, M, virages, fourmis } = this;
    const DX = this._dx;
    const DY = this._dy;
    const grille = this.visites;
    for (let k = 0; k < n && this.pas > 0; k++) {
      this.pas--;
      const t = this.pas;
      if (this.cycle && t < this.cycle.periode) this.cycle = null;
      for (let i = fourmis.length - 1; i >= 0; i--) {
        const f = fourmis[i];
        // 4. reculer d'une case (on connaît la direction : c'est celle d'arrivée)
        let x = f.x - DX[f.d];
        let y = f.y - DY[f.d];
        if (L) {
          if (x < 0) x += L; else if (x >= L) x -= L;
          if (y < 0) y += L; else if (y >= L) y -= L;
        }
        f.x = x;
        f.y = y;
        // 3. décrémenter le compteur
        const b = grille.blocCree(x >> BITS_BLOC, y >> BITS_BLOC);
        f.bloc = b;
        const indice = ((y & MASQUE_BLOC) << BITS_BLOC) | (x & MASQUE_BLOC);
        const v = b.v[indice] - 1;
        b.v[indice] = v;
        b.version++;
        if (v === 0) {
          b.n--;
          grille.size--;
          // Si la case était au bord de la boîte, la boîte devra être recalculée.
          const bo = this._boite;
          const z = 2 * x + y;
          if (!bo || x === bo.xmin || x === bo.xmax || y === bo.ymin || y === bo.ymax ||
              z === bo.zmin || z === bo.zmax) this._boiteFausse = true;
        }
        if ((v + 1) % q === 0) this.casesChangees++;
        if (v % q === 0) this.casesChangees--;
        // 1-2. la couleur est redevenue celle qui avait été lue : on dé-tourne
        const n0 = this.fondVide && this.dessin.size === 0 ? 0 : this.couleurInitiale(x, y);
        const c = (n0 + v) % q;
        f.d = (f.d - virages[c] + M) % M;
        // La boîte propre à chaque fourmi ne sait pas rétrécir : après un
        // retour en arrière, on repartira de la boîte de toutes les cases.
        f.boite = null;

        // Détecteur : on oublie le dernier symbole ; et si on est remonté
        // avant le moment où l'autoroute était établie, on l'oublie aussi.
        if (f.dispo > 0) f.dispo--;
        const a = f.autoroute;
        if (a && (t < a.debut + longueurExigee(a.periode) || f.dispo < a.periode)) {
          f.autoroute = null;
          f.noyau = null;
        }
      }
    }
  }

  // ------------------------------------------------------ détecteur d'autoroute
  chercherAutoroutes() {
    for (const f of this.fourmis) {
      if (f.autoroute) continue;
      f.autoroute = this._chercherAutoroute(f);
      // Pour le cadrage « centre » : la zone de la fourmi au moment où son
      // autoroute est reconnue (l'autoroute n'y fait encore que quelques cases).
      if (f.autoroute && (f.autoroute.dx !== 0 || f.autoroute.dy !== 0)) {
        f.noyau = copierBoite(f.boite || this.boite);
      }
    }
  }

  // Cherche la plus petite période P telle que les symboles (couleur lue,
  // direction) des derniers pas se répètent avec la période P sur au moins
  // NB_PERIODES périodes. Renvoie null ou un objet :
  //   { periode, dx, dy, debut, debutExact }
  //   - (dx, dy) : déplacement par période (coordonnées axiales en hexagonal) ;
  //     (0, 0) = cycle borné, pas une autoroute
  //   - debut : premier pas du régime périodique
  //   - debutExact : false si le début est sorti de la mémoire (debut = majorant)
  // ATTENTION : c'est une observation sur un temps fini, PAS une preuve que
  // le mouvement restera périodique pour toujours.
  _chercherAutoroute(f) {
    const h = f.histo;
    const t = this.pas;   // les symboles valides sont aux indices t - f.dispo .. t - 1
    const n = f.dispo;
    const M = this.M;
    if (n < LONGUEUR_MIN) return null; // pas assez d'historique
    // Plus grande période possible : il faut NB_PERIODES * P <= n.
    const Pmax = Math.min(PERIODE_MAX, Math.floor(n / NB_PERIODES));
    // Filtre rapide : les deux derniers symboles doivent déjà se répéter.
    const s1 = h[(t - 1) & MASQUE_HISTO];
    const s2 = h[(t - 2) & MASQUE_HISTO];
    for (let P = 1; P <= Pmax; P++) {
      if (h[(t - 1 - P) & MASQUE_HISTO] !== s1 || h[(t - 2 - P) & MASQUE_HISTO] !== s2) continue;
      const longueur = longueurExigee(P);

      // Vérifie h[i] == h[i - P] sur toute la fenêtre des « longueur » derniers pas.
      const iMin = t - longueur + P;
      let i = t - 1;
      while (i >= iMin && h[i & MASQUE_HISTO] === h[(i - P) & MASQUE_HISTO]) i--;
      if (i >= iMin) continue; // une différence : P n'est pas une période

      // Trouvé. On remonte le temps tant que la périodicité tient, pour dater le début.
      const limite = t - n + P; // en dessous, l'historique n'est plus en mémoire
      i = iMin;
      while (i > limite && h[(i - 1) & MASQUE_HISTO] === h[(i - 1 - P) & MASQUE_HISTO]) i--;

      // Déplacement par période = somme des P derniers déplacements élémentaires.
      let dx = 0;
      let dy = 0;
      for (let j = t - P; j < t; j++) {
        const d = h[j & MASQUE_HISTO] % M;
        dx += this._dx[d];
        dy += this._dy[d];
      }
      // Le début est sûr si on s'est arrêté sur une vraie différence, ou si
      // tout l'historique depuis le pas 0 est encore en mémoire.
      return { periode: P, dx, dy, debut: i - P, debutExact: i > limite || n === t };
    }
    return null;
  }

  // -------------------------------------------------------------- dessin à la main
  // Fait passer la case à la couleur suivante (clic dans l'interface).
  // On modifie N0, donc l'effet est conservé au « retour au départ ».
  changerCouleur(x, y) {
    x = this.replier(x);
    y = this.replier(y);
    const cle = x + ',' + y;
    const nouvelle = (this.couleurInitiale(x, y) + 1) % this.q;
    if (nouvelle === this.fond(x, y)) this.dessin.delete(cle); // revenu au motif de fond
    else this.dessin.set(cle, nouvelle);
    // Dessiner en cours de route change l'histoire : le test de cycle exact
    // n'a plus de sens jusqu'au prochain retour au départ.
    if (this.pas > 0) {
      this._cycleImpossible = true;
      this.cycle = null;
    }
  }

  effacerDessin() {
    this.dessin.clear();
    if (this.pas > 0) {
      this._cycleImpossible = true;
      this.cycle = null;
    }
  }

  // ------------------------------------------------------------- export / contrôle
  // Configuration complète actuelle (avec le dessin), prête pour JSON.stringify.
  exporterConfig() {
    const cfg = normaliserConfig(this.config);
    cfg.dessin = [];
    for (const [cle, c] of this.dessin) {
      const k = cle.indexOf(',');
      cfg.dessin.push([Number(cle.slice(0, k)), Number(cle.slice(k + 1)), c]);
    }
    return cfg;
  }

  // Résumé complet de l'état sous forme de texte : deux simulations sont dans
  // le même état si et seulement si leurs résumés sont égaux (utile aux tests).
  etat() {
    const cases = Array.from(this.visites, ([cle, v]) => cle + ':' + v).sort();
    const fourmis = this.fourmis.map((f) => f.x + ',' + f.y + ',' + f.d);
    return 'pas=' + this.pas + ' | fourmis=' + fourmis.join(';') + ' | cases=' + cases.join(' ');
  }

  // Autoroutes de groupe : fourmis sur une autoroute (déplacement non nul) de
  // même période et même déplacement, reliées de proche en proche par des
  // distances < distanceMax cases. Renvoie [{ fourmis: [i, j, ...], periode, dx, dy }]
  // (seulement les groupes d'au moins 2 fourmis).
  groupesAutoroute(distanceMax = 30) {
    const distance = (a, b) => {
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      return this.M === 6 ? (Math.abs(dx) + Math.abs(dy) + Math.abs(dx + dy)) / 2 : Math.max(Math.abs(dx), Math.abs(dy));
    };
    const parent = this.fourmis.map((f, i) => i);
    const racine = (i) => (parent[i] === i ? i : (parent[i] = racine(parent[i])));
    const sur = this.fourmis.map((f) => f.autoroute && (f.autoroute.dx !== 0 || f.autoroute.dy !== 0));
    for (let i = 0; i < this.fourmis.length; i++) {
      for (let j = i + 1; j < this.fourmis.length; j++) {
        const a = this.fourmis[i];
        const b = this.fourmis[j];
        if (sur[i] && sur[j] && a.autoroute.periode === b.autoroute.periode && a.autoroute.dx === b.autoroute.dx &&
            a.autoroute.dy === b.autoroute.dy && distance(a, b) < distanceMax) parent[racine(j)] = racine(i);
      }
    }
    const groupes = new Map();
    this.fourmis.forEach((f, i) => {
      if (!sur[i]) return;
      const r = racine(i);
      if (!groupes.has(r)) groupes.set(r, { fourmis: [], periode: f.autoroute.periode, dx: f.autoroute.dx, dy: f.autoroute.dy });
      groupes.get(r).fourmis.push(i);
    });
    return Array.from(groupes.values()).filter((g) => g.fourmis.length >= 2);
  }

  // Bilan des mesures, sous forme d'objet simple (pour lancer.js et l'interface).
  bilan() {
    const b = this.boite;
    const noms = this.geometrie.noms;
    return {
      regle: this.regle,
      grille: this.geometrie.nom + (this.L ? ' (tore ' + this.L + ' × ' + this.L + ')' : ''),
      pas: this.pas,
      cycle: this.cycle
        ? { oui: true, periode: this.cycle.periode, preuve: 'retour exact à l\'état initial' }
        : { oui: false },
      casesVisitees: this.visites.size,
      zone: b
        ? { xmin: b.xmin, xmax: b.xmax, ymin: b.ymin, ymax: b.ymax,
            largeur: b.xmax - b.xmin + 1, hauteur: b.ymax - b.ymin + 1 }
        : null,
      fourmis: this.fourmis.map((f) => ({
        x: f.x,
        y: f.y,
        cap: f.d,
        nomCap: noms[f.d],
        autoroute: f.autoroute
          ? {
              periode: f.autoroute.periode,
              deplacement: [f.autoroute.dx, f.autoroute.dy],
              bornee: f.autoroute.dx === 0 && f.autoroute.dy === 0,
              debut: f.autoroute.debut,
              debutExact: f.autoroute.debutExact,
            }
          : null,
      })),
      autoroutesDeGroupe: this.groupesAutoroute(),
    };
  }
}

// Longueur de la fenêtre sur laquelle on exige la périodicité.
function longueurExigee(P) {
  return Math.max(NB_PERIODES * P, LONGUEUR_MIN);
}

// ----------------------------------------------------------------------------
// 9. Ce que le fichier expose
// ----------------------------------------------------------------------------
const Langton = {
  GEOMETRIES,
  PREFIXE_HEXAGONAL,
  DIRECTIONS,
  NOMS_DIRECTIONS,
  TOURS,
  TYPES_INITIAUX,
  PERIODE_MAX,
  NB_PERIODES,
  LONGUEUR_MIN,
  BITS_BLOC,
  COTE_BLOC,
  RACINE3_SUR_2,
  mod,
  hasard,
  centreCase,
  caseSousPoint,
  analyserRegle,
  configParDefaut,
  normaliserConfig,
  nettoyerRegle,
  lireDirection,
  ecrireFourmis,
  lireFourmis,
  lirePoints,
  ecrirePoints,
  Grille,
  Simulation,
};

// Dans Node : module.exports. Dans le navigateur : la constante globale Langton.
if (typeof module !== 'undefined' && module.exports) module.exports = Langton;

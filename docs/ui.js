'use strict';
// =============================================================================
//  ui.js — l'interface : dessin sur <canvas>, souris, formulaires, mesures.
//
//  Toute la « physique » est dans engine.js (objet global Langton).
//  Ici on ne fait que : lire les formulaires -> fabriquer une configuration
//  -> créer une Langton.Simulation -> l'afficher et la faire avancer.
//
//  Plan du fichier :
//    1. constantes (vitesses, couleurs, expériences)
//    2. état de l'interface
//    3. création / modification de la simulation
//    4. cadrage (tout voir, centre, suivi de la forme)
//    5. dessin de la grille
//    6. mesures et graphe
//    7. boucle d'animation
//    8. souris et clavier
//    9. formulaires
//   10. partage (URL, JSON)
//   11. démarrage
// =============================================================================

const $ = (id) => document.getElementById(id);
const fr = (n) => n.toLocaleString('fr-FR'); // 10000 -> "10 000"
const HAUTEUR_RANG = Langton.RACINE3_SUR_2; // √3/2 : écart vertical entre deux rangées d'hexagones

// ----------------------------------------------------------------------------
// 1. Constantes
// ----------------------------------------------------------------------------
// Les crans du curseur de vitesse : d'abord en pas par seconde, puis en pas
// par image (le navigateur affiche environ 60 images par seconde).
const VITESSES = [];
for (const v of [1, 2, 5, 10, 30]) VITESSES.push({ parSeconde: v });
for (const v of [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000,
  200000, 500000, 1000000]) {
  VITESSES.push({ parImage: v });
}
const VITESSE_PAR_DEFAUT = 11; // 100 pas/image

// Couleurs des cases : 0 = clair, 1 = sombre (la fourmi classique), puis des teintes vives.
const PALETTE_HEX = ['#f4f2ec', '#23262d', '#e4572e', '#2e86de', '#17a36b', '#f2b705',
  '#8e44ad', '#00a8b5', '#d6336c', '#7a8b00', '#a0522d', '#5c6bc0'];
// Au-delà de 12 couleurs, on reboucle sur les teintes vives (indices 2 à 11).
function couleurHex(c) {
  return PALETTE_HEX[c < 12 ? c : 2 + ((c - 2) % 10)];
}

// Un pixel de canvas est un entier 32 bits rangé dans l'ordre A B G R.
function pixel(r, g, b) {
  return ((255 << 24) | (b << 16) | (g << 8) | r) >>> 0;
}
function pixelHex(hex) {
  const n = parseInt(hex.slice(1), 16);
  return pixel(n >> 16, (n >> 8) & 255, n & 255);
}
// Le même pixel écrit pour ctx.fillStyle (avec un petit cache).
const cacheCss = new Map();
function cssPixel(p) {
  let s = cacheCss.get(p);
  if (!s) {
    s = 'rgb(' + (p & 255) + ',' + ((p >>> 8) & 255) + ',' + ((p >>> 16) & 255) + ')';
    cacheCss.set(p, s);
  }
  return s;
}

// Carte des visites : dégradé du jaune clair (peu visité) au violet sombre (très visité).
// (Le même dégradé est écrit en CSS dans index.html pour la légende.)
const ETAPES_DEGRADE = ['#ffe9a8', '#f59e42', '#d1345b', '#5b1a6e', '#1b0b3a'];
const DEGRADE = new Uint32Array(256);
for (let i = 0; i < 256; i++) {
  const u = (i / 255) * (ETAPES_DEGRADE.length - 1);
  const k = Math.min(ETAPES_DEGRADE.length - 2, Math.floor(u));
  const a = parseInt(ETAPES_DEGRADE[k].slice(1), 16);
  const b = parseInt(ETAPES_DEGRADE[k + 1].slice(1), 16);
  const melange = (decalage) => {
    const va = (a >> decalage) & 255;
    const vb = (b >> decalage) & 255;
    return Math.round(va + (vb - va) * (u - k));
  };
  DEGRADE[i] = pixel(melange(16), melange(8), melange(0));
}
const PIXEL_NON_VISITE = pixelHex('#f4f2ec');

// Flèches des caps, par géométrie (même ordre que Langton.GEOMETRIES[M].directions).
const FLECHES = { 4: ['↑', '→', '↓', '←'], 6: ['→', '↘', '↙', '←', '↖', '↗'] };
const COULEUR_FOURMI = '#e11d48';

// Ce que fait chaque « lettre » de la règle (pour la légende).
const SENS_JETONS = {
  R: 'tourner à droite', L: 'tourner à gauche', N: 'tout droit', U: 'demi-tour',
  R1: 'tourner à droite de 60°', R2: 'tourner à droite de 120°',
  L1: 'tourner à gauche de 60°', L2: 'tourner à gauche de 120°',
};

// Les expériences du README (plus une en prime).
const EXPERIENCES = [
  { nom: '1. « RL » seule (chaos puis autoroute)', config: { regle: 'RL' }, echelle: 6 },
  { nom: '2. « RL » sur damier', config: { regle: 'RL', initial: { type: 'damier', taille: 1 } }, echelle: 12, vitesse: 3 },
  { nom: '3. Deux fourmis qui se croisent', config: { regle: 'RL', fourmis: [{ x: 0, y: 0, d: 0 }, { x: 40, y: 0, d: 3 }] }, echelle: 5 },
  { nom: '4. « LLRR » (motif symétrique)', config: { regle: 'LLRR' }, echelle: 7, vitesse: 15 },
  { nom: '5. « RLR » (croissance d\'allure chaotique)', config: { regle: 'RLR' }, echelle: 4, vitesse: 15 },
  { nom: '6. Rosace hexagonale (H:L2NNL1L2L1)', config: { regle: 'H:L2NNL1L2L1', fourmis: [{ x: 0, y: 0, d: 0 }] }, echelle: 4, vitesse: 14 },
  { nom: '7. Spirale hexagonale (H:L1L2NUL2L1R2)', config: { regle: 'H:L1L2NUL2L1R2', fourmis: [{ x: 0, y: 0, d: 0 }] }, echelle: 3, vitesse: 14 },
  { nom: 'Bonus. Deux fourmis voisines (cycle borné)', config: { regle: 'RL', fourmis: [{ x: 0, y: 0, d: 0 }, { x: 1, y: 0, d: 0 }] }, echelle: 40, vitesse: 2 },
];

// ----------------------------------------------------------------------------
// 2. État de l'interface
// ----------------------------------------------------------------------------
let sim = null;           // la simulation en cours (Langton.Simulation)
let enMarche = false;     // lecture ou pause
let indiceVitesse = VITESSE_PAR_DEFAUT;
let accumulateur = 0;     // fraction de pas en attente (vitesses en pas/s)
let dernierTemps = 0;
let aRedessiner = true;   // mettre à true dès que quelque chose a changé

// La vue : quel point du plan est au centre de l'écran, et combien de pixels
// (CSS) par unité du plan. Une unité du plan = une case (voir
// Langton.centreCase : en hexagonal, deux centres voisins sont à distance 1).
const vue = { cx: 0.5, cy: 0.5, echelle: 8 };
const ECHELLE_MIN = 1 / 1024;  // une case = 1/1024 de pixel : des millions de cases à l'écran
const ECHELLE_MAX = 80;
const ECHELLE_AUTO_MAX = 16;   // le cadrage automatique ne zoome pas plus que ça
const SEUIL_HEXAGONES = 5;     // en dessous (pixels par case), hexagones dessinés en losanges

// Points (pas, cases visitées) du petit graphe.
let courbe = [];

// Pour régler le rythme du dessin (voir boucle) et afficher les images/s.
let dureeDessin = 0;
let dernierDessin = -Infinity;
const datesDessins = [];

const canvas = $('vue');
const ctx = canvas.getContext('2d');
// Image intermédiaire : 1 pixel par case (ou par bloc de k × k cases),
// qu'on agrandit ensuite d'un coup.
const tampon = document.createElement('canvas');
const tamponCtx = tampon.getContext('2d');
let image = null;   // ImageData de la taille (nx, ny) courante
let pixels = null;  // la même mémoire vue comme un tableau d'entiers 32 bits
let sommes = null;  // pour les blocs de k × k cases : { r, g, b, n } (voir remplirReduit)
let tuile = null;   // pour le tore : les couleurs des L×L cases

// ----------------------------------------------------------------------------
// 3. Création / modification de la simulation
// ----------------------------------------------------------------------------
// Remplace la simulation par une nouvelle, construite sur « config ».
function nouvelleSimulation(config) {
  sim = new Langton.Simulation(config);
  courbe = [];
  accumulateur = 0;
  remplirFormulaire();
  aRedessiner = true;
}

// Modifie quelques champs de la configuration et repart du pas 0.
// Exemple : appliquer({ regle: 'LLRR' })
function appliquer(modifications) {
  const config = sim.exporterConfig();
  if (modifications.initial) {
    modifications = Object.assign({}, modifications, {
      initial: Object.assign(config.initial, modifications.initial),
    });
  }
  nouvelleSimulation(Object.assign(config, modifications));
}

function retourAuDepart() {
  sim.reinitialiser();
  courbe = [];
  accumulateur = 0;
  aRedessiner = true;
}

function definirLecture(marche) {
  enMarche = marche;
  $('lecture').textContent = marche ? '⏸ Pause' : '▶ Lecture';
}

// ----------------------------------------------------------------------------
// 4. Cadrage
// ----------------------------------------------------------------------------
// Rectangle du plan occupé par les cases d'une boîte { xmin, ..., zmin, zmax }.
function rectanglePlan(b) {
  if (sim.M === 6) {
    // Abscisse d'un centre = x + y/2 = z/2 ; un hexagone fait 1 de large et 2/√3 de haut.
    const demiHauteur = 1 / Math.sqrt(3);
    return { X0: b.zmin / 2 - 0.5, X1: b.zmax / 2 + 0.5,
      Y0: b.ymin * HAUTEUR_RANG - demiHauteur, Y1: b.ymax * HAUTEUR_RANG + demiHauteur };
  }
  return { X0: b.xmin, X1: b.xmax + 1, Y0: b.ymin, Y1: b.ymax + 1 };
}

function unionBoites(a, b) {
  if (!a) return b ? Object.assign({}, b) : null;
  if (!b) return a;
  for (const k of ['xmin', 'ymin', 'zmin']) a[k] = Math.min(a[k], b[k]);
  for (const k of ['xmax', 'ymax', 'zmax']) a[k] = Math.max(a[k], b[k]);
  return a;
}

function boiteDuPoint(x, y) {
  return { xmin: x, xmax: x, ymin: y, ymax: y, zmin: 2 * x + y, zmax: 2 * x + y };
}

// La zone à cadrer, en cases :
//   'tout'   : toutes les cases visitées et toutes les fourmis ;
//   'centre' : pareil, mais une fourmi qui est sur une autoroute ne compte que
//              pour la zone qu'elle occupait quand l'autoroute a été reconnue.
// Sur le tore, c'est toujours le tore entier.
function zoneACadrer(mode) {
  if (sim.L) {
    const n = sim.L - 1;
    return { xmin: 0, xmax: n, ymin: 0, ymax: n, zmin: 0, zmax: 3 * n };
  }
  let zone = null;
  const centre = mode === 'centre' && sim.fourmis.some((f) => f.autoroute && f.noyau);
  if (!centre) {
    zone = unionBoites(zone, sim.boite);
    for (const f of sim.fourmis) zone = unionBoites(zone, boiteDuPoint(f.x, f.y));
    return zone;
  }
  for (const f of sim.fourmis) {
    if (f.autoroute && f.noyau) {
      zone = unionBoites(zone, f.noyau);
    } else {
      zone = unionBoites(zone, f.boite || sim.boite);
      zone = unionBoites(zone, boiteDuPoint(f.x, f.y));
    }
  }
  return zone;
}

// Cadre la vue sur la zone choisie ('tout' ou 'centre').
function cadrer(mode) {
  const zone = zoneACadrer(mode);
  if (!zone) return;
  const r = rectanglePlan(zone);
  vue.cx = (r.X0 + r.X1) / 2;
  vue.cy = (r.Y0 + r.Y1) / 2;
  const marge = 1.1;
  const e = Math.min(canvas.clientWidth / ((r.X1 - r.X0) * marge), canvas.clientHeight / ((r.Y1 - r.Y0) * marge));
  vue.echelle = Math.min(ECHELLE_AUTO_MAX, Math.max(ECHELLE_MIN, e));
  aRedessiner = true;
}

// Boutons « Tout voir » et « Centre » : cadrent une fois, et règlent aussi le
// mode du suivi de la forme.
function boutonCadrer(mode) {
  $('cadrage').value = mode;
  $('suivre').checked = false;
  cadrer(mode);
}

// Toute action de l'utilisateur sur la vue arrête les suivis automatiques.
function arreterSuivis() {
  $('suivre').checked = false;
  $('suiviForme').checked = false;
}

// ----------------------------------------------------------------------------
// 5. Dessin de la grille
// ----------------------------------------------------------------------------
// Couleur du pixel d'une case qui a été visitée v fois.
// (palette, q, etc. sont recalculés au début de chaque image, voir dessiner.)
let palette = [];
let modeVisites = false;
let invLogMax = 0;
let teinteRapide = false; // true : la couleur ne dépend que de v (fond vide, pas de dessin)

function teinte(x, y, v) {
  if (modeVisites) {
    if (v === 0) return PIXEL_NON_VISITE;
    // Échelle logarithmique : 1 visite -> 0, maxVisites -> 255.
    return DEGRADE[Math.min(255, Math.floor(255 * Math.log(v) * invLogMax))];
  }
  return palette[(sim.couleurInitiale(x, y) + v) % sim.q];
}

// Couleur de n'importe quelle case (lent : sert pour les hexagones, peu nombreux).
function couleurCase(x, y) {
  if (sim.L) return tuile[Langton.mod(y, sim.L) * sim.L + Langton.mod(x, sim.L)];
  return teinte(x, y, sim.visites.lire(x, y));
}

function dessiner() {
  const dpr = window.devicePixelRatio || 1;
  const W = canvas.width;
  const H = canvas.height;
  const e = vue.echelle * dpr; // pixels réels par unité du plan
  const M = sim.M;

  // Conversion « point du plan » -> « pixel de l'écran ».
  const ecranX = (X) => (X - vue.cx) * e + W / 2;
  const ecranY = (Y) => (Y - vue.cy) * e + H / 2;
  const versEcran = (x, y) => {
    const [X, Y] = Langton.centreCase(M, x, y);
    return [ecranX(X), ecranY(Y)];
  };

  // Rectangle du plan visible, puis rectangle de cases qui le couvre
  // (en hexagonal : coordonnées axiales, d'où un rectangle un peu plus grand).
  const Xa = vue.cx - W / 2 / e;
  const Xb = vue.cx + W / 2 / e;
  const Ya = vue.cy - H / 2 / e;
  const Yb = vue.cy + H / 2 / e;
  let xa, xb, ya, yb;
  if (M === 6) {
    ya = Math.floor(Ya / HAUTEUR_RANG) - 1;
    yb = Math.ceil(Yb / HAUTEUR_RANG) + 1;
    xa = Math.floor(Xa - yb / 2) - 1;
    xb = Math.ceil(Xb - ya / 2) + 1;
  } else {
    xa = Math.floor(Xa); xb = Math.floor(Xb);
    ya = Math.floor(Ya); yb = Math.floor(Yb);
  }

  // Préparatifs pour teinte().
  palette = [];
  for (let c = 0; c < sim.q; c++) palette.push(pixelHex(couleurHex(c)));
  modeVisites = $('mode').value === 'visites';
  invLogMax = sim.maxVisites > 1 ? 1 / Math.log(sim.maxVisites) : 0;
  teinteRapide = !modeVisites && sim.fondVide && sim.dessin.size === 0;
  if (sim.L) calculerTuile();

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (M === 6 && vue.echelle >= SEUIL_HEXAGONES) {
    // --- a1) de près, en hexagonal : de vrais hexagones ---
    dessinerHexagones(xa, xb, ya, yb, e, versEcran, W, H);
  } else {
    // --- a2) sinon : une image d'un pixel par case (ou par bloc de k × k cases) ---
    dessinerImage(xa, xb, ya, yb, e, W, H);
  }

  // --- b) le quadrillage (seulement si les cases sont assez grosses) ---
  if ($('quadrillage').checked && vue.echelle >= 7) {
    ctx.strokeStyle = 'rgba(120, 120, 120, 0.28)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (M === 6) {
      pourChaqueHexagoneVisible(xa, xb, ya, yb, e, versEcran, W, H, (x, y, X, Y) => ajouterHexagone(ctx, X, Y, e));
    } else {
      for (let x = xa; x <= xb + 1; x++) {
        const X = Math.round(ecranX(x)) + 0.5;
        ctx.moveTo(X, 0);
        ctx.lineTo(X, H);
      }
      for (let y = ya; y <= yb + 1; y++) {
        const Y = Math.round(ecranY(y)) + 0.5;
        ctx.moveTo(0, Y);
        ctx.lineTo(W, Y);
      }
    }
    ctx.stroke();
  }

  // --- c) le contour du tore (les copies autour sont des images périodiques) ---
  if (sim.L) {
    const L = sim.L;
    // carré [0, L]² ; en hexagonal, parallélogramme des cases 0..L-1 en axial
    const coins = M === 6
      ? [[-0.5, -0.5], [L - 0.5, -0.5], [L - 0.5, L - 0.5], [-0.5, L - 0.5]].map(([x, y]) => [x + y / 2, y * HAUTEUR_RANG])
      : [[0, 0], [L, 0], [L, L], [0, L]];
    ctx.strokeStyle = COULEUR_FOURMI;
    ctx.lineWidth = 2 * dpr;
    ctx.setLineDash([6 * dpr, 4 * dpr]);
    ctx.beginPath();
    coins.forEach(([X, Y], i) => (i ? ctx.lineTo(ecranX(X), ecranY(Y)) : ctx.moveTo(ecranX(X), ecranY(Y))));
    ctx.closePath();
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // --- d) les fourmis ---
  sim.fourmis.forEach((f, numero) => {
    if (!sim.L) {
      const [X, Y] = versEcran(f.x, f.y);
      dessinerFourmi(X, Y, f.d, numero, e, dpr);
      return;
    }
    // Sur le tore : on dessine aussi les images périodiques visibles
    // (mais pas des milliers : si le tore est minuscule à l'écran, une seule).
    const L = sim.L;
    const copies = ((xb - xa) / L + 1) * ((yb - ya) / L + 1);
    if (copies > 400) {
      const [X, Y] = versEcran(f.x, f.y);
      dessinerFourmi(X, Y, f.d, numero, e, dpr);
      return;
    }
    for (let x = f.x + L * Math.ceil((xa - f.x) / L); x <= xb; x += L) {
      for (let y = f.y + L * Math.ceil((ya - f.y) / L); y <= yb; y += L) {
        const [X, Y] = versEcran(x, y);
        if (X > -50 && X < W + 50 && Y > -50 && Y < H + 50) dessinerFourmi(X, Y, f.d, numero, e, dpr);
      }
    }
  });
}

// Image d'un pixel par case, ou par bloc de k × k cases quand une case fait
// moins d'un pixel (k = puissance de 2). En carré, l'image est simplement
// agrandie ; en hexagonal, elle est posée avec une transformation oblique :
// chaque case devient un losange de même centre et de même aire que son
// hexagone (à moins de SEUIL_HEXAGONES pixels par case, ça ne se voit pas).
function dessinerImage(xa, xb, ya, yb, e, W, H) {
  let s = 0; // k = 2^s cases par pixel de l'image, en largeur comme en hauteur
  while (e * (1 << s) < 1 && s < 20) s++;
  const k = 1 << s;
  const x0 = Math.floor(xa / k) * k;
  const y0 = Math.floor(ya / k) * k;
  const nx = Math.floor((xb - x0) / k) + 1;
  const ny = Math.floor((yb - y0) / k) + 1;

  if (!image || image.width !== nx || image.height !== ny) {
    image = ctx.createImageData(nx, ny);
    pixels = new Uint32Array(image.data.buffer);
    tampon.width = nx;
    tampon.height = ny;
  }
  if (sim.L) remplirImageTore(x0, y0, nx, ny, k);
  else if (k === 1) remplirImageInfinie(x0, y0, nx, ny);
  else remplirReduit(x0, y0, nx, ny, s);
  tamponCtx.putImageData(image, 0, 0);

  ctx.imageSmoothingEnabled = false; // de gros pixels nets, pas de flou
  const ek = e * k;
  if (sim.M === 6) {
    // Coin du pixel (0, 0) de l'image = coin (x0 - 1/2, y0 - 1/2) en axial.
    const ax = x0 - 0.5;
    const ay = y0 - 0.5;
    ctx.setTransform(ek, 0, ek / 2, ek * HAUTEUR_RANG,
      (ax + ay / 2 - vue.cx) * e + W / 2, (ay * HAUTEUR_RANG - vue.cy) * e + H / 2);
  } else {
    ctx.setTransform(ek, 0, 0, ek, (x0 - vue.cx) * e + W / 2, (y0 - vue.cy) * e + H / 2);
  }
  ctx.drawImage(tampon, 0, 0);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
}

// Grille infinie, 1 pixel par case : fond, puis dessin à la main, puis cases visitées.
function remplirImageInfinie(x0, y0, nx, ny) {
  // 1. le fond
  if (modeVisites) {
    pixels.fill(PIXEL_NON_VISITE);
  } else if (sim.fondVide) {
    pixels.fill(palette[0]);
  } else {
    for (let j = 0; j < ny; j++) {
      for (let i = 0; i < nx; i++) pixels[j * nx + i] = palette[sim.fond(x0 + i, y0 + j)];
    }
  }
  // 2. les cases dessinées à la main
  if (!modeVisites) {
    for (const cle of sim.dessin.keys()) {
      const k = cle.indexOf(',');
      const i = Number(cle.slice(0, k)) - x0;
      const j = Number(cle.slice(k + 1)) - y0;
      if (i >= 0 && i < nx && j >= 0 && j < ny) pixels[j * nx + i] = teinte(i + x0, j + y0, 0);
    }
  }
  // 3. les cases visitées : on parcourt les blocs de 64 × 64 cases qui touchent l'image
  const q = sim.q;
  pourChaqueBlocVisible(x0, y0, x0 + nx, y0 + ny, (b, bx0, by0, xa, xb, ya, yb) => {
    const v = b.v;
    for (let y = ya; y < yb; y++) {
      const base = ((y - by0) << Langton.BITS_BLOC) - bx0;
      const ligne = (y - y0) * nx - x0;
      for (let x = xa; x < xb; x++) {
        const n = v[base + x];
        if (n !== 0) pixels[ligne + x] = teinteRapide ? palette[n % q] : teinte(x, y, n);
      }
    }
  });
}

// Appelle fonction(bloc, bx0, by0, xa, xb, ya, yb) pour chaque bloc non vide
// qui touche le rectangle de cases [x0, x1[ × [y0, y1[ ; (xa..xb, ya..yb) est
// la partie commune (bornes hautes exclues).
function pourChaqueBlocVisible(x0, y0, x1, y1, fonction) {
  const C = Langton.COTE_BLOC;
  for (const b of sim.visites.blocs.values()) {
    if (b.n === 0) continue;
    const bx0 = b.bx * C;
    const by0 = b.by * C;
    const xa = Math.max(bx0, x0);
    const xb = Math.min(bx0 + C, x1);
    if (xa >= xb) continue;
    const ya = Math.max(by0, y0);
    const yb = Math.min(by0 + C, y1);
    if (ya >= yb) continue;
    fonction(b, bx0, by0, xa, xb, ya, yb);
  }
}

// Grille infinie, très dézoomée : 1 pixel = un bloc de k × k cases (k = 2^s).
// Le pixel prend la couleur moyenne des cases visitées du bloc, mélangée au fond
// selon la proportion p de cases visitées. Le mélange suit √p plutôt que p,
// pour qu'un trait fin (une autoroute) reste visible de très loin.
//
// Pour aller vite quand des millions de cases sont à l'écran, chaque bloc de
// 64 × 64 cases du moteur garde un « résumé » : les sommes des couleurs de ses
// cases visitées par carrés de 4 × 4 cases, et pour le bloc entier. Le résumé
// n'est recalculé que si le bloc a changé (b.version) ou si l'affichage a
// changé (cleResume) : en pleine lecture, seuls un ou deux blocs bougent.
// Pour le zoom courant (carrés de 2^t × 2^t cases, 2 < t < 6), on en tire un
// résumé plus grossier, gardé lui aussi tant que t ne change pas.
const BITS_CARRE = 2;                                  // carrés de 4 × 4 cases
const CARRES = Langton.COTE_BLOC >> BITS_CARRE;        // 16 carrés par côté de bloc
let cleResume = '';
let versionDessin = 0; // augmente à chaque modification du dessin à la main

function resumerBloc(b, q) {
  const C = Langton.COTE_BLOC;
  const somme = new Uint32Array(4 * CARRES * CARRES); // r, g, b, nombre de cases, par carré
  const total = new Uint32Array(4);                    // pareil pour le bloc entier
  const v = b.v;
  const bx0 = b.bx * C;
  const by0 = b.by * C;
  for (let i = 0; i < v.length; i++) {
    const n = v[i];
    if (n === 0) continue;
    const xl = i & (C - 1);
    const yl = i >> Langton.BITS_BLOC;
    const c = teinteRapide ? palette[n % q] : teinte(bx0 + xl, by0 + yl, n);
    const p = 4 * ((yl >> BITS_CARRE) * CARRES + (xl >> BITS_CARRE));
    somme[p] += c & 255;
    somme[p + 1] += (c >>> 8) & 255;
    somme[p + 2] += (c >>> 16) & 255;
    somme[p + 3]++;
  }
  for (let p = 0; p < somme.length; p += 4) {
    total[0] += somme[p]; total[1] += somme[p + 1]; total[2] += somme[p + 2]; total[3] += somme[p + 3];
  }
  return { version: b.version, cle: cleResume, somme, total, t: BITS_CARRE, grossier: somme };
}

// Résumé par carrés de 2^t × 2^t cases, tiré des carrés de 4 × 4 du résumé.
function regrouperResume(res, t) {
  const m = Langton.COTE_BLOC >> t;
  const g = new Uint32Array(4 * m * m);
  const d = t - BITS_CARRE;
  for (let j = 0; j < CARRES; j++) {
    for (let i = 0; i < CARRES; i++) {
      const o = 4 * (j * CARRES + i);
      if (res.somme[o + 3] === 0) continue;
      const p = 4 * ((j >> d) * m + (i >> d));
      g[p] += res.somme[o]; g[p + 1] += res.somme[o + 1]; g[p + 2] += res.somme[o + 2]; g[p + 3] += res.somme[o + 3];
    }
  }
  res.t = t;
  res.grossier = g;
}

function remplirReduit(x0, y0, nx, ny, s) {
  const k = 1 << s;
  const n = nx * ny;
  if (!sommes || sommes.r.length !== n) {
    sommes = { r: new Uint32Array(n), g: new Uint32Array(n), b: new Uint32Array(n), n: new Uint32Array(n) };
  } else {
    sommes.r.fill(0); sommes.g.fill(0); sommes.b.fill(0); sommes.n.fill(0);
  }
  const { r: R, g: G, b: B, n: N } = sommes;
  const q = sim.q;
  // (l'échelle des visites ne compte que dans la carte des visites)
  cleResume = modeVisites ? 'visites|' + invLogMax : 'couleurs|' + q + '|' + versionDessin;
  pourChaqueBlocVisible(x0, y0, x0 + nx * k, y0 + ny * k, (b, bx0, by0, xa, xb, ya, yb) => {
    if (s < BITS_CARRE) {
      // k = 2 : plus fin que les carrés du résumé, on lit les cases une à une.
      const v = b.v;
      for (let y = ya; y < yb; y++) {
        const base = ((y - by0) << Langton.BITS_BLOC) - bx0;
        const ligne = ((y - y0) >> s) * nx;
        for (let x = xa; x < xb; x++) {
          const nv = v[base + x];
          if (nv === 0) continue;
          const c = teinteRapide ? palette[nv % q] : teinte(x, y, nv);
          const p = ligne + ((x - x0) >> s);
          R[p] += c & 255; G[p] += (c >>> 8) & 255; B[p] += (c >>> 16) & 255; N[p]++;
        }
      }
      return;
    }
    let res = b.resume;
    if (!res || res.version !== b.version || res.cle !== cleResume) res = b.resume = resumerBloc(b, q);
    if (s >= Langton.BITS_BLOC) {
      // Le bloc entier tombe dans un seul pixel.
      const px = (bx0 - x0) >> s;
      const py = (by0 - y0) >> s;
      if (px < 0 || px >= nx || py < 0 || py >= ny) return;
      const p = py * nx + px;
      const t = res.total;
      R[p] += t[0]; G[p] += t[1]; B[p] += t[2]; N[p] += t[3];
      return;
    }
    if (res.t !== s) regrouperResume(res, s);
    const somme = res.grossier;
    const m = Langton.COTE_BLOC >> s;
    for (let j = 0; j < m; j++) {
      const py = (by0 + (j << s) - y0) >> s;
      if (py < 0 || py >= ny) continue;
      for (let i = 0; i < m; i++) {
        const o = 4 * (j * m + i);
        if (somme[o + 3] === 0) continue;
        const px = (bx0 + (i << s) - x0) >> s;
        if (px < 0 || px >= nx) continue;
        const p = py * nx + px;
        R[p] += somme[o]; G[p] += somme[o + 1]; B[p] += somme[o + 2]; N[p] += somme[o + 3];
      }
    }
  });
  // Les cases dessinées à la main et jamais visitées comptent aussi.
  if (!modeVisites) {
    for (const cle of sim.dessin.keys()) {
      const i = cle.indexOf(',');
      const x = Number(cle.slice(0, i));
      const y = Number(cle.slice(i + 1));
      const px = (x - x0) >> s;
      const py = (y - y0) >> s;
      if (px < 0 || px >= nx || py < 0 || py >= ny || sim.visites.lire(x, y) !== 0) continue;
      const c = teinte(x, y, 0);
      const p = py * nx + px;
      R[p] += c & 255; G[p] += (c >>> 8) & 255; B[p] += (c >>> 16) & 255; N[p]++;
    }
  }
  // Mélange avec le fond (constant, ou pris au centre du bloc pour les motifs).
  const fondConstant = modeVisites ? PIXEL_NON_VISITE : sim.fondVide ? palette[0] : -1;
  const k2 = k * k;
  for (let j = 0; j < ny; j++) {
    for (let i = 0; i < nx; i++) {
      const p = j * nx + i;
      const fond = fondConstant >= 0 ? fondConstant : palette[sim.fond(x0 + i * k + (k >> 1), y0 + j * k + (k >> 1))];
      const c = N[p];
      if (c === 0) { pixels[p] = fond; continue; }
      // a = part de la couleur moyenne des cases visitées, 1 - a = part du fond
      const a = c >= k2 ? 1 : Math.sqrt(c / k2);
      const sur = a / c;
      const r = R[p] * sur + (fond & 255) * (1 - a);
      const g = G[p] * sur + ((fond >>> 8) & 255) * (1 - a);
      const b = B[p] * sur + ((fond >>> 16) & 255) * (1 - a);
      pixels[p] = ((255 << 24) | (b << 16) | (g << 8) | r) >>> 0; // = pixel(r, g, b) ; « | » arrondit
    }
  }
}

// Tore : la couleur des L×L cases (calculée une fois par image).
function calculerTuile() {
  const L = sim.L;
  if (!tuile || tuile.length !== L * L) tuile = new Uint32Array(L * L);
  for (let y = 0; y < L; y++) {
    for (let x = 0; x < L; x++) tuile[y * L + x] = teinte(x, y, 0);
  }
  for (const [cle, v] of sim.visites) {
    const k = cle.indexOf(',');
    const x = Number(cle.slice(0, k));
    const y = Number(cle.slice(k + 1));
    tuile[y * L + x] = teinte(x, y, v);
  }
}

// Tore : on pave l'image avec la tuile (une case sur k si k > 1).
function remplirImageTore(x0, y0, nx, ny, k) {
  const L = sim.L;
  const centre = k > 1 ? k >> 1 : 0;
  const colonne = new Int32Array(nx);
  for (let i = 0; i < nx; i++) colonne[i] = Langton.mod(x0 + i * k + centre, L);
  for (let j = 0; j < ny; j++) {
    const ligne = Langton.mod(y0 + j * k + centre, L) * L;
    for (let i = 0; i < nx; i++) pixels[j * nx + i] = tuile[ligne + colonne[i]];
  }
}

// Appelle fonction(x, y, X, Y) pour chaque case hexagonale dont le centre
// (X, Y), en pixels, est à l'écran (ou presque).
function pourChaqueHexagoneVisible(xa, xb, ya, yb, e, versEcran, W, H, fonction) {
  for (let y = ya; y <= yb; y++) {
    for (let x = xa; x <= xb; x++) {
      const [X, Y] = versEcran(x, y);
      if (X < -e || X > W + e || Y < -e || Y > H + e) continue;
      fonction(x, y, X, Y);
    }
  }
}

// Ajoute à « chemin » le contour de l'hexagone (pointe en haut) de centre
// (X, Y) et de largeur e pixels (rayon centre -> sommet : e/√3).
function ajouterHexagone(chemin, X, Y, e) {
  const R = e / Math.sqrt(3);
  const demi = e / 2;
  chemin.moveTo(X, Y - R);
  chemin.lineTo(X + demi, Y - R / 2);
  chemin.lineTo(X + demi, Y + R / 2);
  chemin.lineTo(X, Y + R);
  chemin.lineTo(X - demi, Y + R / 2);
  chemin.lineTo(X - demi, Y - R / 2);
  chemin.closePath();
}

// De près, en hexagonal : on peint le fond, puis chaque case d'une autre
// couleur, regroupées par couleur (un seul chemin par couleur : c'est rapide).
// Le contour est repassé dans la même couleur pour ne pas laisser de fines
// lignes claires entre deux hexagones voisins.
function dessinerHexagones(xa, xb, ya, yb, e, versEcran, W, H) {
  const fond = modeVisites ? PIXEL_NON_VISITE : palette[0];
  ctx.fillStyle = cssPixel(fond);
  ctx.fillRect(0, 0, W, H);
  const chemins = new Map(); // pixel -> Path2D
  pourChaqueHexagoneVisible(xa, xb, ya, yb, e, versEcran, W, H, (x, y, X, Y) => {
    const c = couleurCase(x, y);
    if (c === fond) return;
    let chemin = chemins.get(c);
    if (!chemin) { chemin = new Path2D(); chemins.set(c, chemin); }
    ajouterHexagone(chemin, X, Y, e);
  });
  ctx.lineWidth = 1;
  ctx.lineJoin = 'round';
  for (const [c, chemin] of chemins) {
    ctx.fillStyle = ctx.strokeStyle = cssPixel(c);
    ctx.fill(chemin);
    ctx.stroke(chemin);
  }
}

// Une fourmi : un triangle qui pointe dans sa direction (ou un point si on est très dézoomé).
function dessinerFourmi(X, Y, d, numero, e, dpr) {
  ctx.fillStyle = COULEUR_FOURMI;
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1.5 * dpr;
  ctx.beginPath();
  if (e < 7 * dpr) {
    ctx.arc(X, Y, 3.5 * dpr, 0, 2 * Math.PI);
  } else {
    // direction dans le plan (vecteur de longueur 1)
    const [ax, ay] = sim.geometrie.directions[d];
    const [dx, dy] = sim.M === 6 ? [ax + ay / 2, ay * HAUTEUR_RANG] : [ax, ay];
    const r = 0.42 * e;
    // pointe vers l'avant, deux coins à l'arrière ((-dy, dx) = perpendiculaire)
    ctx.moveTo(X + dx * r, Y + dy * r);
    ctx.lineTo(X - dx * r - dy * r * 0.75, Y - dy * r + dx * r * 0.75);
    ctx.lineTo(X - dx * r + dy * r * 0.75, Y - dy * r - dx * r * 0.75);
    ctx.closePath();
  }
  ctx.fill();
  ctx.stroke();
  // numéro de la fourmi, s'il y en a plusieurs
  if (sim.fourmis.length > 1) {
    ctx.font = 'bold ' + 11 * dpr + 'px system-ui, sans-serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'bottom';
    const texte = String(numero + 1);
    const decalage = Math.max(5 * dpr, 0.45 * e);
    ctx.strokeText(texte, X + decalage, Y - decalage);
    ctx.fillText(texte, X + decalage, Y - decalage);
  }
}

// ----------------------------------------------------------------------------
// 6. Mesures et graphe
// ----------------------------------------------------------------------------
function afficherMesures() {
  $('mPas').textContent = fr(sim.pas);
  $('mCases').textContent = fr(sim.visites.size);
  const b = sim.boite;
  $('mBoite').textContent = b
    ? 'x ∈ [' + b.xmin + ' ; ' + b.xmax + '], y ∈ [' + b.ymin + ' ; ' + b.ymax + ']  (' +
      fr(b.xmax - b.xmin + 1) + ' × ' + fr(b.ymax - b.ymin + 1) + (sim.M === 6 ? ', axial)' : ')')
    : '—';
  $('mCycle').textContent = sim.cycle
    ? 'oui : état initial retrouvé au pas ' + fr(sim.cycle.periode) + ' (période ' + fr(sim.cycle.periode) + ')'
    : 'non (pas de retour à l\'état initial)';
  // images par seconde, sur la dernière seconde
  const maintenant = performance.now();
  while (datesDessins.length && datesDessins[0] < maintenant - 1000) datesDessins.shift();
  $('mImages').textContent = enMarche ? String(datesDessins.length) : '—';

  const signe = (n) => (n > 0 ? '+' + n : String(n).replace('-', '−'));
  const noms = sim.geometrie.noms;
  let html = '';
  sim.fourmis.forEach((f, i) => {
    html += '<div class="fourmi"><b>n°' + (i + 1) + '</b> : case (' + f.x + ' ; ' + f.y + '), cap ' +
      FLECHES[sim.M][f.d] + ' ' + noms[f.d] + '<br>';
    const a = f.autoroute;
    if (!a) {
      html += '<small>Pas de répétition détectée (périodes essayées : 1 à ' + fr(Langton.PERIODE_MAX) + ').</small>';
    } else {
      const debut = (a.debutExact ? 'début au pas ' : 'début au plus tard au pas ') + fr(a.debut);
      if (a.dx === 0 && a.dy === 0) {
        html += '<span class="detecte">Cycle borné détecté</span><br>période P = ' + fr(a.periode) +
          ', déplacement nul, ' + debut;
      } else {
        html += '<span class="detecte">Autoroute détectée</span><br>période P = ' + fr(a.periode) +
          ', déplacement (' + signe(a.dx) + ' ; ' + signe(a.dy) + ') par période' +
          (sim.M === 6 ? ' (axial)' : '') + ', ' + debut;
      }
    }
    html += '</div>';
  });
  // Autoroutes de groupe : même période, même déplacement, fourmis à moins de 30 cases.
  for (const g of sim.groupesAutoroute(30)) {
    html = '<div class="fourmi"><span class="detecte">Autoroute de groupe (' + g.fourmis.length + ' fourmis)</span><br>' +
      'n°' + g.fourmis.map((i) => i + 1).join(', n°') + ' : période P = ' + fr(g.periode) +
      ', déplacement (' + signe(g.dx) + ' ; ' + signe(g.dy) + ') par période</div>' + html;
  }
  $('mFourmis').innerHTML = html;

  $('echelleVisites').hidden = $('mode').value !== 'visites';
  $('maxVisites').textContent = fr(Math.max(1, sim.maxVisites)) + ' visites';
}

// Ajoute le point (pas, cases visitées) à la courbe.
function enregistrerCourbe() {
  // Si on a reculé dans le temps, on efface le « futur ».
  while (courbe.length && courbe[courbe.length - 1][0] > sim.pas) courbe.pop();
  if (courbe.length && courbe[courbe.length - 1][0] === sim.pas) return;
  courbe.push([sim.pas, sim.visites.size]);
  // Trop de points : on n'en garde qu'un sur deux.
  if (courbe.length > 800) courbe = courbe.filter((p, i) => i % 2 === 0 || i === courbe.length - 1);
}

function dessinerGraphe() {
  const c = $('graphe');
  const dpr = window.devicePixelRatio || 1;
  const W = Math.round(c.clientWidth * dpr);
  const H = Math.round(c.clientHeight * dpr);
  if (c.width !== W || c.height !== H) { c.width = W; c.height = H; }
  const g = c.getContext('2d');
  const style = getComputedStyle(document.documentElement);
  const discret = style.getPropertyValue('--discret');
  g.clearRect(0, 0, W, H);

  const gauche = 6 * dpr, droite = W - 6 * dpr, haut = 18 * dpr, bas = H - 18 * dpr;
  const tMax = Math.max(1, sim.pas);
  let nMax = Math.max(1, sim.visites.size);
  for (const p of courbe) if (p[1] > nMax) nMax = p[1];

  // axes
  g.strokeStyle = style.getPropertyValue('--trait');
  g.lineWidth = dpr;
  g.beginPath();
  g.moveTo(gauche, haut); g.lineTo(gauche, bas); g.lineTo(droite, bas);
  g.stroke();
  // courbe
  g.strokeStyle = style.getPropertyValue('--accent');
  g.lineWidth = 2 * dpr;
  g.lineJoin = 'round';
  g.beginPath();
  g.moveTo(gauche, bas);
  for (const [t, n] of courbe) {
    g.lineTo(gauche + (droite - gauche) * (t / tMax), bas - (bas - haut) * (n / nMax));
  }
  g.stroke();
  // graduations : seulement les valeurs extrêmes
  g.fillStyle = discret;
  g.font = 11 * dpr + 'px system-ui, sans-serif';
  g.textBaseline = 'top';
  g.textAlign = 'left';
  g.fillText(fr(nMax) + (nMax > 1 ? ' cases' : ' case'), gauche, 2 * dpr);
  g.fillText('0', gauche, bas + 4 * dpr);
  g.textAlign = 'right';
  g.fillText(fr(tMax) + ' pas', droite, bas + 4 * dpr);
}

// ----------------------------------------------------------------------------
// 7. Boucle d'animation (appelée par le navigateur à chaque image)
// ----------------------------------------------------------------------------
function boucle(temps) {
  const dt = Math.min(0.1, (temps - dernierTemps) / 1000); // secondes depuis l'image précédente
  dernierTemps = temps;

  if (enMarche) {
    const vitesse = VITESSES[indiceVitesse];
    let n;
    if (vitesse.parImage) {
      n = vitesse.parImage;
    } else {
      // vitesses lentes : on accumule le temps jusqu'à avoir un pas entier à faire
      accumulateur += dt * vitesse.parSeconde;
      n = Math.floor(accumulateur);
      accumulateur -= n;
    }
    if (n > 0) {
      sim.avancer(n);
      aRedessiner = true;
    }
  }

  // On dessine au plus une fois par image. Si le dessin coûte cher (beaucoup
  // de cases à l'écran), on ne le refait pas à chaque image pendant la
  // lecture : il ne doit pas prendre plus de la moitié du temps, le reste
  // allant à la simulation.
  const maintenant = performance.now();
  const dessinPermis = !enMarche || dureeDessin < 8 || maintenant - dernierDessin >= 2 * dureeDessin;
  if (aRedessiner && dessinPermis) {
    aRedessiner = false;
    if ($('suiviForme').checked) {
      cadrer($('cadrage').value);
    } else if ($('suivre').checked) {
      [vue.cx, vue.cy] = Langton.centreCase(sim.M, sim.fourmis[0].x, sim.fourmis[0].y);
    }
    enregistrerCourbe();
    dessiner();
    dureeDessin = performance.now() - maintenant;
    dernierDessin = maintenant;
    datesDessins.push(maintenant);
    afficherMesures();
    dessinerGraphe();
  }
  requestAnimationFrame(boucle);
}

// Le canvas doit avoir autant de pixels que sa taille réelle à l'écran.
function ajusterTailleCanvas() {
  const dpr = window.devicePixelRatio || 1;
  const W = Math.max(1, Math.round(canvas.clientWidth * dpr));
  const H = Math.max(1, Math.round(canvas.clientHeight * dpr));
  if (canvas.width !== W || canvas.height !== H) {
    canvas.width = W;
    canvas.height = H;
    aRedessiner = true;
  }
}

// ----------------------------------------------------------------------------
// 8. Souris et clavier
// ----------------------------------------------------------------------------
// Case située sous le pointeur de la souris.
function caseSousPointeur(evenement) {
  const r = canvas.getBoundingClientRect();
  const X = vue.cx + (evenement.clientX - r.left - r.width / 2) / vue.echelle;
  const Y = vue.cy + (evenement.clientY - r.top - r.height / 2) / vue.echelle;
  const [x, y] = Langton.caseSousPoint(sim.M, X, Y);
  return { x: sim.replier(x), y: sim.replier(y) };
}

function outilCourant() {
  return document.querySelector('input[name=outil]:checked').value;
}

// Zoom d'un certain facteur en gardant fixe le point (px, py) de l'écran
// (coordonnées en pixels CSS, mesurées depuis le centre du canvas).
function zoomer(facteur, px = 0, py = 0) {
  const ancienne = vue.echelle;
  vue.echelle = Math.min(ECHELLE_MAX, Math.max(ECHELLE_MIN, ancienne * facteur));
  vue.cx += px / ancienne - px / vue.echelle;
  vue.cy += py / ancienne - py / vue.echelle;
  $('suiviForme').checked = false;
  aRedessiner = true;
}

let glisse = null; // geste en cours : { x, y, cx, cy, bouge }

canvas.addEventListener('pointerdown', (ev) => {
  glisse = { x: ev.clientX, y: ev.clientY, cx: vue.cx, cy: vue.cy, bouge: false };
  canvas.setPointerCapture(ev.pointerId);
});

canvas.addEventListener('pointermove', (ev) => {
  if (glisse) {
    const dx = ev.clientX - glisse.x;
    const dy = ev.clientY - glisse.y;
    // On ne considère que c'est un « glisser » qu'au-delà de 4 pixels :
    // en dessous, c'est un clic un peu tremblant.
    if (Math.abs(dx) + Math.abs(dy) > 4) glisse.bouge = true;
    if (glisse.bouge) {
      vue.cx = glisse.cx - dx / vue.echelle;
      vue.cy = glisse.cy - dy / vue.echelle;
      arreterSuivis();
      aRedessiner = true;
    }
  }
  const { x, y } = caseSousPointeur(ev);
  const v = sim.visitesEn(x, y);
  const n0 = sim.couleurInitiale(x, y);
  const c = sim.couleur(x, y);
  $('infoCase').textContent = 'Case (' + x + ' ; ' + y + ')' + (sim.M === 6 ? ' axiale' : '') + ' — couleur ' + c +
    ' → ' + sim.jetons[c] + ' — N = N₀ + visites = ' + n0 + ' + ' + fr(v) + ' = ' + fr(n0 + v);
});

canvas.addEventListener('pointerup', (ev) => {
  const geste = glisse;
  glisse = null;
  if (!geste || geste.bouge) return; // c'était un déplacement de la vue
  const { x, y } = caseSousPointeur(ev);
  if (outilCourant() === 'dessin') {
    sim.changerCouleur(x, y);
    versionDessin++;
    aRedessiner = true;
  } else {
    clicFourmi(x, y, ev.button === 2 || ev.shiftKey);
  }
});

canvas.addEventListener('pointercancel', () => { glisse = null; });
canvas.addEventListener('contextmenu', (ev) => ev.preventDefault()); // pas de menu au clic droit

canvas.addEventListener('wheel', (ev) => {
  ev.preventDefault();
  const r = canvas.getBoundingClientRect();
  // Firefox compte souvent la molette en lignes (deltaMode 1, environ 3 par cran)
  // ou en pages (deltaMode 2), Chrome en pixels (environ 100 par cran) : on ramène tout en pixels.
  const pixelsDefiles = ev.deltaY * (ev.deltaMode === 1 ? 33 : ev.deltaMode === 2 ? r.height : 1);
  zoomer(Math.exp(-pixelsDefiles * 0.0015), ev.clientX - r.left - r.width / 2, ev.clientY - r.top - r.height / 2);
}, { passive: false });

// Outil « placer les fourmis » : on modifie les positions de DÉPART.
function clicFourmi(x, y, enlever) {
  const fourmis = sim.config.fourmis.map((f) => ({ x: sim.replier(f.x), y: sim.replier(f.y), d: f.d }));
  const i = fourmis.findIndex((f) => f.x === x && f.y === y);
  if (enlever) {
    if (i < 0 || fourmis.length <= 1) return; // il faut garder au moins une fourmi
    fourmis.splice(i, 1);
  } else if (i >= 0) {
    fourmis[i].d = (fourmis[i].d + 1) % sim.M; // tourner d'un cran
  } else {
    fourmis.push({ x, y, d: 0 });
  }
  appliquer({ fourmis });
}

document.addEventListener('keydown', (ev) => {
  // On ne vole pas les touches quand on écrit dans un champ. Sur un bouton,
  // l'espace appartient au bouton (il le « clique »), mais les flèches sont à nous.
  const balise = ev.target.tagName;
  if (/^(INPUT|SELECT|TEXTAREA)$/.test(balise)) return;
  if (ev.key === ' ' && balise !== 'BUTTON') { ev.preventDefault(); definirLecture(!enMarche); }
  if (ev.key === 'ArrowRight') { ev.preventDefault(); unPas(+1); }
  if (ev.key === 'ArrowLeft') { ev.preventDefault(); unPas(-1); }
});

function unPas(sens) {
  definirLecture(false);
  if (sens > 0) sim.avancer(1);
  else sim.reculer(1);
  aRedessiner = true;
}

// ----------------------------------------------------------------------------
// 9. Formulaires
// ----------------------------------------------------------------------------
// Recopie la configuration de la simulation dans les champs.
function remplirFormulaire() {
  const cfg = sim.config;
  $('regle').value = cfg.regle;
  $('exemplesRegle').value = '';
  $('geometrie').value = String(sim.M);
  $('tore').checked = cfg.tore > 0;
  if (cfg.tore > 0) $('tailleTore').value = cfg.tore;
  $('ligneTailleTore').hidden = cfg.tore === 0;
  $('motif').value = cfg.initial.type;
  $('taille').value = cfg.initial.taille;
  $('densite').value = cfg.initial.densite;
  $('graine').value = cfg.initial.graine;
  $('nbFourmis').value = cfg.fourmis.length;
  $('texteFourmis').value = Langton.ecrireFourmis(cfg.fourmis, sim.M);
  $('messagePoints').textContent = fr(sim.dessin.size) + ' case(s) dessinée(s) dans la situation de départ.';
  $('messagePoints').classList.remove('erreur');
  $('aideFourmis').textContent = sim.M === 6
    ? 'Cap : E, SE, SO, O, NO, NE (ou 0 à 5). Coordonnées axiales : x vers la droite (E), y vers le bas à droite (SE).'
    : 'Direction : H haut, D droite, B bas, G gauche. L\'axe y pointe vers le bas, comme à l\'écran.';

  // On ne montre que les réglages utiles au motif choisi.
  const type = cfg.initial.type;
  $('ligneTaille').hidden = !['damier', 'rayures', 'carre'].includes(type);
  $('nomTaille').textContent = { damier: 'Côté carreau', rayures: 'Largeur', carre: 'Côté' }[type] || 'Taille';
  $('ligneDensite').hidden = $('ligneGraine').hidden = type !== 'aleatoire';

  // Légende de la règle : une pastille « couleur → lettre » par couleur.
  const legende = $('legendeRegle');
  legende.textContent = '';
  sim.jetons.forEach((jeton, c) => {
    const pastille = document.createElement('span');
    pastille.className = 'pastille';
    pastille.title = 'couleur ' + c + ' : ' + SENS_JETONS[jeton];
    const rond = document.createElement('i');
    rond.style.background = couleurHex(c);
    pastille.append(rond, c + '→' + jeton);
    legende.append(pastille);
  });
}

function afficherVitesse() {
  const v = VITESSES[indiceVitesse];
  $('vitesse').value = indiceVitesse;
  $('texteVitesse').textContent = v.parSeconde ? fr(v.parSeconde) + ' pas/s' : fr(v.parImage) + ' pas/image';
}

// Passe la règle d'une grille à l'autre, au plus près :
// carré -> hexagone : R -> R1, L -> L1 ; hexagone -> carré : R1, R2 -> R ; L1, L2 -> L.
function convertirRegle(M) {
  if (M === sim.M) return sim.regle;
  if (M === 6) return Langton.PREFIXE_HEXAGONAL + sim.jetons.map((j) => ({ R: 'R1', L: 'L1' }[j] || j)).join('');
  return sim.jetons.map((j) => j[0]).join('');
}

// --- Panneau « Cases noires » : tout passe par config.dessin ([[x, y, c], ...]) ---
// Décalage à appliquer si les coordonnées sont relatives à la fourmi n°1 (sa case de départ).
function decalagePoints() {
  const f = sim.config.fourmis[0];
  return $('pointsRelatifs').checked ? [f.x, f.y] : [0, 0];
}

function direPoints(texte, erreur) {
  $('messagePoints').textContent = texte;
  $('messagePoints').classList.toggle('erreur', !!erreur);
}

// Lit la zone de texte ; en cas d'erreur, affiche la première ligne fautive et renvoie null.
function lireZonePoints() {
  const { points, erreurs } = Langton.lirePoints($('textePoints').value);
  if (erreurs.length) {
    const e = erreurs[0];
    direPoints('Ligne ' + e.ligne + ' : « ' + e.texte + ' » — ' + e.message +
      (erreurs.length > 1 ? ' (et ' + (erreurs.length - 1) + ' autre(s) erreur(s))' : '') + '. Rien n\'a été changé.', true);
    return null;
  }
  const [dx, dy] = decalagePoints();
  return points.map(([x, y, c]) => [sim.replier(x + dx), sim.replier(y + dy), c]);
}

// Ajoute (remplacer = false) ou remplace (true) le dessin de départ, puis repart du pas 0.
function poserPoints(remplacer) {
  const points = lireZonePoints();
  if (!points) return;
  const dessin = new Map();
  if (!remplacer) for (const [x, y, c] of sim.exporterConfig().dessin) dessin.set(x + ',' + y, [x, y, c]);
  for (const p of points) dessin.set(p[0] + ',' + p[1], p); // la dernière valeur l'emporte
  definirLecture(false);
  appliquer({ dessin: Array.from(dessin.values()) });
  direPoints(fr(points.length) + ' case(s) lue(s) ; ' + fr(sim.dessin.size) + ' case(s) dessinée(s) dans la situation de départ.');
}

// Écrit des points dans la zone de texte (relatifs à la fourmi n°1 si la case est cochée).
function ecrireZonePoints(points, quoi) {
  const [dx, dy] = decalagePoints();
  points.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
  $('textePoints').value = Langton.ecrirePoints(points.map(([x, y, c]) => [x - dx, y - dy, c]));
  direPoints(fr(points.length) + ' case(s) ' + quoi + '.' +
    (sim.fondVide ? '' : ' (Les cases du motif de fond ne sont pas comptées.)'));
}

// Les cases non blanches de l'instant présent (cases visitées ou dessinées).
function casesNoiresActuelles() {
  const points = [];
  sim.visites.parcourir((x, y) => {
    const c = sim.couleur(x, y);
    if (c !== 0) points.push([x, y, c]);
  });
  for (const cle of sim.dessin.keys()) {
    const [x, y] = cle.split(',').map(Number);
    const c = sim.couleur(x, y);
    if (sim.visitesEn(x, y) === 0 && c !== 0) points.push([x, y, c]);
  }
  return points;
}

function copierPoints() {
  const texte = $('textePoints').value;
  const repli = () => { $('textePoints').select(); direPoints('Texte sélectionné : Ctrl+C (ou Cmd+C) pour le copier.'); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(texte).then(() => direPoints('Copié dans le presse-papiers.'), repli);
  } else {
    repli();
  }
}

// --- Germes : window.GERMES vient de germes.js (fetch ne marche pas en file://) ---
function listeGermes() {
  return Array.isArray(window.GERMES) ? window.GERMES : [];
}

// Construit l'arbre des germes. Avec un filtre : seuls les germes dont le nom, la règle ou le dossier
// contient le texte sont gardés, et les dossiers qui les contiennent sont ouverts.
let germeChoisi = -1;
function construireArbreGermes(filtre) {
  const arbre = $('arbreGermes');
  arbre.textContent = '';
  const f = String(filtre || '').trim().toLowerCase();
  const racine = { enfants: new Map(), germes: [], total: 0 };
  listeGermes().forEach((g, i) => {
    const dossier = g.dossier ? String(g.dossier) : 'Divers';
    if (f && !(g.nom + ' ' + g.regle + ' ' + dossier).toLowerCase().includes(f)) return;
    let noeud = racine;
    noeud.total++;
    for (const morceau of dossier.split('/').map((m) => m.trim()).filter(Boolean)) {
      if (!noeud.enfants.has(morceau)) noeud.enfants.set(morceau, { enfants: new Map(), germes: [], total: 0 });
      noeud = noeud.enfants.get(morceau);
      noeud.total++;
    }
    noeud.germes.push(i);
  });
  if (racine.enfants.has('Divers')) { const d = racine.enfants.get('Divers'); racine.enfants.delete('Divers'); racine.enfants.set('Divers', d); }
  const remplir = (parent, noeud) => {
    for (const [nom, enfant] of noeud.enfants) {
      const details = document.createElement('details');
      if (f) details.open = true;
      const resume = document.createElement('summary');
      resume.textContent = nom + ' ';
      const nb = document.createElement('span');
      nb.className = 'nb';
      nb.textContent = '(' + enfant.total + ')';
      resume.append(nb);
      details.append(resume);
      remplir(details, enfant);
      parent.append(details);
    }
    for (const i of noeud.germes) {
      const bouton = document.createElement('button');
      bouton.type = 'button';
      bouton.className = 'germe' + (i === germeChoisi ? ' choisi' : '');
      bouton.textContent = listeGermes()[i].nom;
      bouton.title = listeGermes()[i].note || '';
      bouton.addEventListener('click', () => {
        germeChoisi = i;
        for (const b of arbre.querySelectorAll('button.germe.choisi')) b.classList.remove('choisi');
        bouton.classList.add('choisi');
        chargerGerme(listeGermes()[i]);
      });
      parent.append(bouton);
    }
  };
  remplir(arbre, racine);
  if (f && racine.total === 0) arbre.textContent = 'Aucun germe ne correspond.';
}

function chargerGerme(g) {
  definirLecture(false);
  const M = Langton.analyserRegle(g.regle).M;
  const fourmis = Langton.lireFourmis(g.fourmis || '0,0,0', M);
  const { points, erreurs } = Langton.lirePoints(g.points || '');
  nouvelleSimulation({ regle: g.regle, fourmis: fourmis.length ? fourmis : undefined, dessin: points });
  $('noteGerme').textContent = (g.note || '') +
    (erreurs.length ? ' (Attention : ' + erreurs.length + ' coordonnée(s) illisible(s) ignorée(s) dans ce germe.)' : '');
  $('textePoints').value = Langton.ecrirePoints(points);
  $('pointsRelatifs').checked = false;
  cadrer($('cadrage').value);
}

function brancherFormulaire() {
  // --- commandes de temps ---
  $('lecture').addEventListener('click', () => definirLecture(!enMarche));
  $('avancer').addEventListener('click', () => unPas(+1));
  $('reculer').addEventListener('click', () => unPas(-1));
  $('retour').addEventListener('click', () => { definirLecture(false); retourAuDepart(); });
  $('vitesse').max = VITESSES.length - 1;
  $('vitesse').addEventListener('input', () => { indiceVitesse = Number($('vitesse').value); afficherVitesse(); });

  // --- vue ---
  $('zoomPlus').addEventListener('click', () => zoomer(1.5));
  $('zoomMoins').addEventListener('click', () => zoomer(1 / 1.5));
  $('toutVoir').addEventListener('click', () => boutonCadrer('tout'));
  $('centre').addEventListener('click', () => boutonCadrer('centre'));
  for (const id of ['mode', 'quadrillage', 'cadrage']) $(id).addEventListener('change', () => { aRedessiner = true; });
  // Les deux suivis s'excluent.
  $('suivre').addEventListener('change', () => {
    if ($('suivre').checked) $('suiviForme').checked = false;
    aRedessiner = true;
  });
  $('suiviForme').addEventListener('change', () => {
    if ($('suiviForme').checked) $('suivre').checked = false;
    aRedessiner = true;
  });

  // --- règle ---
  $('regle').addEventListener('change', () => appliquer({ regle: $('regle').value }));
  $('exemplesRegle').addEventListener('change', () => {
    if ($('exemplesRegle').value) appliquer({ regle: $('exemplesRegle').value });
  });

  // --- grille ---
  $('geometrie').addEventListener('change', () => {
    appliquer({ regle: convertirRegle(Number($('geometrie').value)) });
    cadrer($('cadrage').value);
  });
  const lireTore = () => {
    appliquer({ tore: $('tore').checked ? Number($('tailleTore').value) || 64 : 0 });
    cadrer('tout');
  };
  $('tore').addEventListener('change', lireTore);
  $('tailleTore').addEventListener('change', lireTore);

  // --- situation initiale ---
  $('motif').addEventListener('change', () => appliquer({ initial: { type: $('motif').value } }));
  $('taille').addEventListener('change', () => appliquer({ initial: { taille: Number($('taille').value) } }));
  $('densite').addEventListener('change', () => appliquer({ initial: { densite: Number($('densite').value) } }));
  $('graine').addEventListener('change', () => appliquer({ initial: { graine: Number($('graine').value) } }));
  $('effacerDessin').addEventListener('click', () => { sim.effacerDessin(); versionDessin++; aRedessiner = true; });

  // --- fourmis ---
  $('texteFourmis').addEventListener('change', () => {
    const fourmis = Langton.lireFourmis($('texteFourmis').value, sim.M);
    if (fourmis.length > 0) appliquer({ fourmis });
    else remplirFormulaire(); // texte illisible : on remet l'ancien
  });
  $('nbFourmis').addEventListener('change', () => {
    const voulu = Math.min(100, Math.max(1, Math.round(Number($('nbFourmis').value)) || 1));
    const fourmis = sim.config.fourmis.slice(0, voulu);
    // Les nouvelles fourmis sont posées sur l'axe x, de 4 cases en 4 cases, sur des cases libres.
    for (let x = 0; fourmis.length < voulu; x += 4) {
      if (!fourmis.some((f) => f.x === x && f.y === 0)) fourmis.push({ x, y: 0, d: 0 });
    }
    appliquer({ fourmis });
  });
  // L'outil « fourmis » agit sur les positions de départ : on y retourne pour les voir.
  for (const radio of document.querySelectorAll('input[name=outil]')) {
    radio.addEventListener('change', () => {
      if (outilCourant() === 'fourmi' && sim.pas > 0) { definirLecture(false); retourAuDepart(); }
    });
  }

  // --- cases noires ---
  $('ajouterPoints').addEventListener('click', () => poserPoints(false));
  $('remplacerPoints').addEventListener('click', () => poserPoints(true));
  $('exporterPoints').addEventListener('click', () => ecrireZonePoints(casesNoiresActuelles(), 'non blanche(s) au pas ' + fr(sim.pas)));
  $('exporterDepart').addEventListener('click', () => ecrireZonePoints(sim.exporterConfig().dessin, 'dessinée(s) au départ'));
  $('copierPoints').addEventListener('click', copierPoints);

  // --- germes ---
  // Arbre de dossiers repliables (<details>) : « Passagers/Trace 104 » = dossier Passagers, sous-dossier Trace 104.
  // Dossiers dans l'ordre où ils apparaissent ; germes sans dossier dans « Divers », à la fin. Tout est fermé au départ.
  construireArbreGermes('');
  $('filtreGermes').addEventListener('input', () => construireArbreGermes($('filtreGermes').value));
  if (listeGermes().length === 0) $('noteGerme').textContent = 'Aucun germe : germes.js est vide (voir README).';

  // --- expériences ---
  EXPERIENCES.forEach((experience, i) => {
    const option = document.createElement('option');
    option.value = i;
    option.textContent = experience.nom;
    $('experience').append(option);
  });
  $('experience').addEventListener('change', () => {
    const experience = EXPERIENCES[$('experience').value];
    if (!experience) return;
    definirLecture(false);
    nouvelleSimulation(experience.config);
    indiceVitesse = experience.vitesse === undefined ? VITESSE_PAR_DEFAUT : experience.vitesse;
    afficherVitesse();
    // Point de vue de départ (le suivi de la forme, s'il est coché, le remplacera).
    [vue.cx, vue.cy] = Langton.centreCase(sim.M, 0, 0);
    vue.echelle = experience.echelle;
    $('suivre').checked = false;
  });

  // --- partage ---
  $('copierLien').addEventListener('click', partagerLien);
  $('exporter').addEventListener('click', exporterJSON);
  $('importer').addEventListener('click', () => $('fichier').click());
  $('fichier').addEventListener('change', importerJSON);
}

// ----------------------------------------------------------------------------
// 10. Partage : URL et fichier JSON
// ----------------------------------------------------------------------------
// La configuration complète = celle du moteur + quelques réglages d'affichage.
function configComplete() {
  const config = sim.exporterConfig();
  config.vitesse = indiceVitesse;
  config.affichage = { mode: $('mode').value };
  return config;
}

// Charge une configuration complète (venue d'une URL ou d'un fichier).
// (Les anciens fichiers peuvent contenir affichage.damierHV : on l'ignore.)
function chargerConfig(config) {
  definirLecture(false);
  if (config && config.affichage) {
    $('mode').value = config.affichage.mode === 'visites' ? 'visites' : 'couleurs';
  }
  nouvelleSimulation(config); // le moteur vérifie et répare la configuration
  const v = Math.round(Number(config && config.vitesse));
  indiceVitesse = v >= 0 && v < VITESSES.length ? v : VITESSE_PAR_DEFAUT;
  afficherVitesse();
  cadrer('tout');
  if (!sim.L) vue.echelle = 8;
}

// Le lien contient toute la configuration après le « # » :  page.html#c=<JSON encodé>
function partagerLien() {
  const lien = location.href.split('#')[0] + '#c=' + encodeURIComponent(JSON.stringify(configComplete()));
  history.replaceState(null, '', lien);
  $('lien').hidden = false;
  $('lien').value = lien;
  $('lien').select();
  const dire = (texte) => { $('messagePartage').textContent = texte; };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(lien).then(
      () => dire('Lien copié dans le presse-papiers (et dans la barre d\'adresse).'),
      () => dire('Copie le lien ci-dessus (il est aussi dans la barre d\'adresse).'));
  } else {
    dire('Copie le lien ci-dessus (il est aussi dans la barre d\'adresse).');
  }
}

function lireLien() {
  if (!location.hash.startsWith('#c=')) return false;
  try {
    chargerConfig(JSON.parse(decodeURIComponent(location.hash.slice(3))));
    return true;
  } catch (erreur) {
    $('messagePartage').textContent = 'Lien illisible : configuration par défaut chargée.';
    return false;
  }
}

function exporterJSON() {
  const texte = JSON.stringify(configComplete(), null, 2);
  const lien = document.createElement('a');
  lien.href = URL.createObjectURL(new Blob([texte], { type: 'application/json' }));
  lien.download = 'fourmi-langton.json';
  lien.click();
  URL.revokeObjectURL(lien.href);
}

function importerJSON() {
  const fichier = $('fichier').files[0];
  if (!fichier) return;
  const lecteur = new FileReader();
  lecteur.onload = () => {
    try {
      chargerConfig(JSON.parse(lecteur.result));
      $('messagePartage').textContent = 'Configuration importée : ' + fichier.name;
    } catch (erreur) {
      $('messagePartage').textContent = 'Fichier illisible : ce n\'est pas du JSON valide.';
    }
    $('fichier').value = ''; // pour pouvoir réimporter le même fichier
  };
  lecteur.readAsText(fichier);
}

// ----------------------------------------------------------------------------
// 11. Démarrage
// ----------------------------------------------------------------------------
brancherFormulaire();
ajusterTailleCanvas();
new ResizeObserver(ajusterTailleCanvas).observe(canvas);
if (!lireLien()) {
  nouvelleSimulation(Langton.configParDefaut());
  afficherVitesse();
}
window.addEventListener('hashchange', lireLien);
requestAnimationFrame(boucle);

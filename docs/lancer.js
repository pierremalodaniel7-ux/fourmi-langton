#!/usr/bin/env node
'use strict';
// =============================================================================
//  lancer.js — lancer une expérience en ligne de commande, résultat en JSON.
//
//  Utilise EXACTEMENT le même moteur que la page (engine.js) : aucune copie.
//
//  Exemples :
//    node lancer.js --regle RL --fourmis "0,0,H ; 0,1,H" --pas 1000000
//    node lancer.js --regle H:L2NNL1L2L1 --fourmis "0,0,E" --pas 200000
//    node lancer.js --regle RL --tore 32 --pas 10000000 --arret-cycle
//    node lancer.js --config experience.json --pas 500000
//    node lancer.js --aide
// =============================================================================
const fs = require('fs');
const path = require('path');
const Langton = require(path.join(__dirname, 'engine.js'));

const AIDE = `Usage : node lancer.js [options]

  --regle R          mot-règle : « RL », « LLRR »… (carré) ou « H:L2NNL1L2L1 » (hexagonal)
  --fourmis "x,y,d ; …"
                     positions et caps de départ (carré : H D B G ; hexagonal : E SE SO O NO NE)
                     défaut : une fourmi en 0,0 cap 0 (H en carré, E en hexagonal)
  --pas N            nombre de pas (défaut 100000 ; « 1e6 » accepté)
  --tore L           grille repliée en tore L × L (en hexagonal : parallélogramme L × L en axial)
  --motif T          vide, damier, rayures, aleatoire, carre (défaut vide)
  --taille t         taille du motif (carreaux, rayures, carré)
  --densite p        densité du motif aléatoire (0 à 1)
  --graine g         graine du motif aléatoire
  --config F         lit la configuration dans le fichier JSON F (celui exporté par la page) ;
                     les autres options la modifient
  --arret-cycle      s'arrête dès qu'un cycle exact (retour à l'état initial) est trouvé
  --compact          JSON sur une seule ligne
  --aide             cette aide

Résultat (JSON) : cycle exact (oui/non, période), autoroute détectée pour chaque fourmi
(période, déplacement par période, pas de début), cases visitées, taille de la zone visitée.
Une « autoroute » est une DÉTECTION sur un temps fini, pas une preuve ; un « cycle » est un
retour exact à l'état initial, donc une preuve que tout se répète.`;

// Lit les options « --nom valeur » et « --drapeau ».
function lireOptions(args) {
  const drapeaux = new Set(['arret-cycle', 'compact', 'aide', 'help', 'h']);
  const options = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (!a.startsWith('-')) throw new Error('argument inattendu : ' + a);
    const nom = a.replace(/^-+/, '');
    if (drapeaux.has(nom)) { options[nom] = true; continue; }
    if (i + 1 >= args.length) throw new Error('il manque une valeur après ' + a);
    options[nom] = args[++i];
  }
  return options;
}

function nombre(texte, nom) {
  const n = Number(texte);
  if (!Number.isFinite(n)) throw new Error('--' + nom + ' : nombre attendu, reçu « ' + texte + ' »');
  return n;
}

function principal() {
  const options = lireOptions(process.argv.slice(2));
  if (options.aide || options.help || options.h) {
    console.log(AIDE);
    return 0;
  }

  // 1. La configuration : fichier, puis options par-dessus.
  let config = Langton.configParDefaut();
  if (options.config) config = JSON.parse(fs.readFileSync(options.config, 'utf8'));
  if (options.regle !== undefined) config.regle = options.regle;
  const M = Langton.analyserRegle(config.regle).M;
  if (options.fourmis !== undefined) {
    config.fourmis = Langton.lireFourmis(options.fourmis, M);
    if (config.fourmis.length === 0) throw new Error('--fourmis : aucune fourmi lisible dans « ' + options.fourmis + ' »');
  }
  if (options.tore !== undefined) config.tore = nombre(options.tore, 'tore');
  config.initial = Object.assign({}, config.initial);
  if (options.motif !== undefined) {
    if (!Langton.TYPES_INITIAUX.includes(options.motif)) {
      throw new Error('--motif : un parmi ' + Langton.TYPES_INITIAUX.join(', '));
    }
    config.initial.type = options.motif;
  }
  if (options.taille !== undefined) config.initial.taille = nombre(options.taille, 'taille');
  if (options.densite !== undefined) config.initial.densite = nombre(options.densite, 'densite');
  if (options.graine !== undefined) config.initial.graine = nombre(options.graine, 'graine');
  const pas = Math.max(0, Math.round(nombre(options.pas === undefined ? 100000 : options.pas, 'pas')));

  // 2. La simulation, par tranches (pour pouvoir s'arrêter sur un cycle).
  const sim = new Langton.Simulation(config);
  const debut = process.hrtime.bigint();
  const TRANCHE = 1 << 16;
  while (sim.pas < pas) {
    sim.avancer(Math.min(TRANCHE, pas - sim.pas));
    if (options['arret-cycle'] && sim.cycle) break;
  }
  const ms = Number(process.hrtime.bigint() - debut) / 1e6;

  // 3. Le bilan.
  const resultat = Object.assign({ pasDemandes: pas }, sim.bilan(), {
    fourmisDepart: Langton.ecrireFourmis(sim.config.fourmis, sim.M),
    dureeMs: Math.round(ms),
  });
  console.log(options.compact ? JSON.stringify(resultat) : JSON.stringify(resultat, null, 2));
  return 0;
}

try {
  process.exitCode = principal();
} catch (erreur) {
  console.error('Erreur : ' + erreur.message + '\n(node lancer.js --aide pour l\'aide)');
  process.exitCode = 2;
}

'use strict';
// =============================================================================
//  outils/germes_vers_js.js — convertit germes.json en germes.js.
//  Usage (depuis le dossier fourmi-langton) :  node outils/germes_vers_js.js
//
//  Pourquoi : la page s'ouvre par double-clic (file://), où fetch('germes.json')
//  est refusé par le navigateur. Une balise <script src="germes.js"> marche.
//  Chaque germe : { nom, regle, fourmis: "x,y,D ; ...", points: "x,y ; ...", note, dossier }
//  (dossier facultatif, ex. "Passagers/Trace 104" ; sans dossier : « Divers » dans le menu).
//  germes.json peut être une liste de germes ou un objet { germes: [...] }.
// =============================================================================
const fs = require('fs');
const path = require('path');
const Langton = require(path.join(__dirname, '..', 'engine.js'));

const racine = path.join(__dirname, '..');
const donnees = JSON.parse(fs.readFileSync(path.join(racine, 'germes.json'), 'utf8'));
const germes = Array.isArray(donnees) ? donnees : donnees.germes;
if (!Array.isArray(germes)) throw new Error('germes.json : une liste de germes est attendue');

let problemes = 0;
const propres = germes.map((g, i) => {
  const nom = String(g.nom || 'Germe ' + (i + 1));
  const regle = Langton.nettoyerRegle(g.regle);
  const M = Langton.analyserRegle(regle).M;
  // fourmis et points peuvent aussi être donnés sous forme de listes
  const fourmis = Array.isArray(g.fourmis) ? Langton.ecrireFourmis(g.fourmis.map((f) => ({ x: f.x, y: f.y, d: Langton.lireDirection(f.d, M) })), M) : String(g.fourmis || '0,0,0');
  const points = Array.isArray(g.points) ? Langton.ecrirePoints(g.points) : String(g.points || '');
  const { erreurs } = Langton.lirePoints(points);
  for (const e of erreurs) { problemes++; console.log('« ' + nom + ' », points : « ' + e.texte + ' » — ' + e.message); }
  if (Langton.lireFourmis(fourmis, M).length === 0) { problemes++; console.log('« ' + nom + ' » : aucune fourmi lisible'); }
  if (regle !== String(g.regle).toUpperCase().replace(/\s+/g, '')) console.log('« ' + nom + ' » : règle « ' + g.regle + ' » lue comme « ' + regle + ' »');
  const germe = { nom, regle, fourmis, points, note: String(g.note || '') };
  if (g.dossier) germe.dossier = String(g.dossier); // « A/B » : rangé dans le dossier A/B du menu
  return germe;
});

const texte = '// germes.js — généré par outils/germes_vers_js.js à partir de germes.json.\n' +
  '// Ne pas modifier à la main : modifier germes.json puis relancer le script.\n' +
  '// (globalThis = window dans le navigateur ; ainsi le fichier se lit aussi dans Node.)\n' +
  'globalThis.GERMES = ' + JSON.stringify(propres, null, 2) + ';\n';
fs.writeFileSync(path.join(racine, 'germes.js'), texte);
console.log(propres.length + ' germe(s) écrit(s) dans germes.js' + (problemes ? ', ' + problemes + ' problème(s) signalé(s) ci-dessus.' : '.'));

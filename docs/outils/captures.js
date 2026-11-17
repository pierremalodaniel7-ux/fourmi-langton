// =============================================================================
//  outils/captures.js — vérifie la page dans un vrai navigateur (Chromium sans
//  fenêtre, via Playwright) et prend des captures d'écran.
//  Usage : node outils/captures.js . captures   (depuis le dossier fourmi-langton ; nécessite Playwright)
//
//  Vérifications automatiques (chacune affiche « ok » ou « ÉCHEC ») :
//    - aucune erreur JavaScript ;
//    - le pixel au centre de cases visitées a exactement la couleur que donne
//      le moteur (carré, hexagones de près, losanges de loin) ;
//    - un clic au centre d'une case hexagonale dessine bien CETTE case ;
//    - le suivi de la forme fait tenir toute la zone dans l'image ;
//    - le cadrage « centre » zoome sur la forme centrale ;
//    - le damier H/V a disparu.
// =============================================================================
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const dossier = path.resolve(process.argv[2]);
const sortie = path.resolve(process.argv[3] || 'captures');
fs.mkdirSync(sortie, { recursive: true });

let echecs = 0;
function verifier(condition, message, detail) {
  if (!condition) echecs++;
  console.log((condition ? '  ok    ' : '  ÉCHEC ') + message + (detail ? '  (' + detail + ')' : ''));
}

(async () => {
  const navigateur = await chromium.launch();
  const page = await navigateur.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
  const erreurs = [];
  page.on('pageerror', (e) => erreurs.push(e.message));
  await page.goto('file://' + dossier + '/index.html');
  await page.waitForTimeout(300);

  // Petites commandes exécutées dans la page.
  const dans = (f, ...a) => page.evaluate(f, ...a);
  const image = async () => { await page.waitForTimeout(150); };
  const capture = async (nom, toutePage) => {
    const fichier = path.join(sortie, nom);
    if (toutePage) await page.screenshot({ path: fichier });
    else await page.locator('#cadre').screenshot({ path: fichier });
    console.log('        capture : ' + path.relative(process.cwd(), fichier));
  };
  const experience = async (texte) => {
    const valeur = await dans((t) => [...document.querySelectorAll('#experience option')].find((o) => o.textContent.includes(t)).value, texte);
    await page.selectOption('#experience', valeur);
  };
  const avancer = async (n) => { await dans((n) => { sim.avancer(n); aRedessiner = true; }, n); await image(); };

  // Compare, pour quelques cases visitées loin des fourmis, le pixel au centre
  // de la case et la couleur donnée par le moteur.
  const comparerPixels = () => dans(() => {
    dessiner();
    const dpr = window.devicePixelRatio || 1;
    const e = vue.echelle * dpr;
    // les cases visitées visibles à l'écran, loin des fourmis
    const cases = [];
    sim.visites.parcourir((x, y) => {
      if (sim.fourmis.some((f) => Math.abs(f.x - x) + Math.abs(f.y - y) < 3)) return;
      const [X, Y] = Langton.centreCase(sim.M, x, y);
      const px = Math.round((X - vue.cx) * e + canvas.width / 2);
      const py = Math.round((Y - vue.cy) * e + canvas.height / 2);
      if (px >= 2 && py >= 2 && px <= canvas.width - 3 && py <= canvas.height - 3) cases.push([x, y, px, py]);
    });
    let essais = 0, justes = 0;
    const exemples = [];
    for (let i = 0; i < cases.length && essais < 25; i += Math.max(1, Math.floor(cases.length / 25))) {
      const [x, y, px, py] = cases[i];
      const d = ctx.getImageData(px, py, 1, 1).data;
      const attendu = pixelHex(couleurHex(sim.couleur(x, y)));
      const lu = pixel(d[0], d[1], d[2]);
      essais++;
      if (lu === attendu) justes++;
      else if (exemples.length < 3) exemples.push('(' + x + ',' + y + ') lu ' + lu.toString(16) + ' attendu ' + attendu.toString(16));
    }
    return { essais, justes, exemples };
  });

  // Le rectangle d'écran (pixels CSS) occupé par la zone visitée.
  const zoneEcran = () => dans(() => {
    const r = rectanglePlan(zoneACadrer('tout'));
    const sx = (X) => (X - vue.cx) * vue.echelle + canvas.clientWidth / 2;
    const sy = (Y) => (Y - vue.cy) * vue.echelle + canvas.clientHeight / 2;
    return { gauche: sx(r.X0), droite: sx(r.X1), haut: sy(r.Y0), bas: sy(r.Y1), W: canvas.clientWidth, H: canvas.clientHeight, echelle: vue.echelle };
  });
  const dedans = (z) => z.gauche >= -1 && z.haut >= -1 && z.droite <= z.W + 1 && z.bas <= z.H + 1;

  console.log('Page');
  verifier(await page.$('#damierHV') === null && !(await page.content()).includes('Cohen'), 'le damier H/V a disparu');
  verifier(await page.isChecked('#suiviForme'), 'suivi de la forme activé par défaut');

  // 1. RL, 20 000 pas.
  console.log('1. RL à 20 000 pas (suivi de la forme)');
  await experience('« RL » seule');
  await page.check('#suiviForme');
  await avancer(20000);
  let z = await zoneEcran();
  verifier(dedans(z), 'toute la zone visitée tient dans l\'image', 'échelle ' + z.echelle.toFixed(2) + ' px/case');
  await capture('01-rl-20000-pas.png');
  await capture('00-page-entiere.png', true);
  await dans(() => { $('suiviForme').checked = false; vue.echelle = 12; [vue.cx, vue.cy] = [0.5, 0.5]; aRedessiner = true; });
  let r = await comparerPixels();
  verifier(r.essais >= 15 && r.justes === r.essais, 'carré : couleur au centre des cases = couleur du moteur', r.justes + '/' + r.essais + ' ' + r.exemples.join(' '));

  // 2. Rosace hexagonale.
  console.log('2. Rosace hexagonale, 200 000 pas');
  await experience('Rosace');
  await page.check('#suiviForme');
  await avancer(200000);
  const etat = await dans(() => [sim.visites.size, sim.fourmis[0].x, sim.fourmis[0].y, sim.fourmis[0].d]);
  verifier(JSON.stringify(etat) === '[25574,62,74,3]', 'mêmes chiffres que le moteur seul', etat.join(', '));
  z = await zoneEcran();
  verifier(dedans(z), 'toute la rosace tient dans l\'image', 'échelle ' + z.echelle.toFixed(2) + ' px/case');
  await capture('02-rosace-hexagonale.png');
  r = await comparerPixels();
  verifier(r.essais >= 15 && r.justes === r.essais, 'losanges (de loin) : couleur au centre = couleur du moteur', r.justes + '/' + r.essais + ' ' + r.exemples.join(' '));

  // 3. De près : vrais hexagones, quadrillage, clic.
  console.log('3. Hexagones de près');
  await dans(() => { $('suiviForme').checked = false; vue.echelle = 26; [vue.cx, vue.cy] = Langton.centreCase(6, 0, 0); aRedessiner = true; });
  await image();
  r = await comparerPixels();
  verifier(r.essais >= 15 && r.justes === r.essais, 'hexagones : couleur au centre = couleur du moteur', r.justes + '/' + r.essais + ' ' + r.exemples.join(' '));
  await capture('03-hexagones-de-pres.png');
  // Clic au centre de la case (3, -2), puis à 0,4 case de son centre.
  for (const [dX, dY, nom] of [[0, 0, 'au centre'], [0.4, 0.1, 'près du bord est'], [-0.1, -0.45, 'près de la pointe']]) {
    const avant = await dans(() => sim.couleur(3, -2));
    const pos = await dans(([dX, dY]) => {
      const [X, Y] = Langton.centreCase(6, 3, -2);
      const r = canvas.getBoundingClientRect();
      return { x: r.left + (X + dX - vue.cx) * vue.echelle + r.width / 2, y: r.top + (Y + dY - vue.cy) * vue.echelle + r.height / 2 };
    }, [dX, dY]);
    await page.mouse.click(pos.x, pos.y);
    const apres = await dans(() => sim.couleur(3, -2));
    const info = await page.textContent('#infoCase');
    verifier(apres === (avant + 1) % 6 && info.includes('Case (3 ; -2)'), 'clic ' + nom + ' d\'un hexagone → case axiale (3, -2)', info.slice(0, 30));
  }

  // 4. Spirale hexagonale.
  console.log('4. Spirale hexagonale, 200 000 pas');
  await experience('Spirale');
  await page.check('#suiviForme');
  await avancer(200000);
  z = await zoneEcran();
  verifier(dedans(z), 'toute la spirale tient dans l\'image', 'échelle ' + z.echelle.toFixed(2) + ' px/case');
  await capture('04-spirale-hexagonale.png');

  // 5. Autoroute : cadrage « tout » puis « centre ».
  console.log('5. RL à 300 000 pas : autoroute, cadrage tout / centre');
  await experience('« RL » seule');
  await page.check('#suiviForme');
  await page.selectOption('#cadrage', 'tout');
  await avancer(300000);
  z = await zoneEcran();
  verifier(dedans(z), 'cadrage « tout » : la diagonale entière tient dans l\'image', 'échelle ' + z.echelle.toFixed(3) + ' px/case');
  await capture('05-autoroute-cadrage-tout.png');
  const echelleTout = z.echelle;
  await page.click('#centre');
  await image();
  const echelleCentre = await dans(() => vue.echelle);
  verifier(echelleCentre > 10 * echelleTout && await page.isChecked('#suiviForme') && await page.inputValue('#cadrage') === 'centre',
    'bouton « Centre » : zoom ' + (echelleCentre / echelleTout).toFixed(0) + ' fois plus fort, le suivi continue en mode centre');
  await capture('06-autoroute-cadrage-centre.png');
  r = await comparerPixels();
  verifier(r.essais >= 15 && r.justes === r.essais, 'cadrage centre : couleurs justes', r.justes + '/' + r.essais);

  // 6. Des millions de cases, puis dézoom maximal.
  console.log('6. Des millions de cases (case < 1 pixel)');
  await dans(() => { nouvelleSimulation({ regle: 'RL', fourmis: [{ x: 0, y: 0, d: 0 }, { x: 0, y: 1, d: 0 }] }); });
  await page.check('#suiviForme');
  await page.selectOption('#cadrage', 'tout');
  await avancer(4000000);
  const millions = await dans(() => sim.visites.size);
  z = await zoneEcran();
  verifier(millions > 2e6 && dedans(z), millions.toLocaleString('fr-FR') + ' cases visitées, toutes dans l\'image', 'échelle ' + z.echelle.toFixed(4) + ' px/case');
  await capture('07-millions-de-cases.png');
  // L'intérieur du losange est visité un nombre pair de fois : il est blanc.
  // La carte des visites le montre.
  await dans(() => { $('mode').value = 'visites'; aRedessiner = true; });
  await image();
  await capture('07b-millions-de-cases-carte-des-visites.png');
  await dans(() => { $('mode').value = 'couleurs'; aRedessiner = true; });
  await page.click('#zoomMoins'); // arrête le suivi
  for (let i = 0; i < 30; i++) await page.click('#zoomMoins');
  const emin = await dans(() => vue.echelle);
  verifier(Math.abs(emin - 1 / 1024) < 1e-9 && !(await page.isChecked('#suiviForme')), 'dézoom maximal : 1/1024 px par case, le zoom manuel coupe le suivi');
  await capture('08-dezoom-maximal.png');

  // 7. Tore hexagonal.
  console.log('7. Tore hexagonal (parallélogramme 40 × 40)');
  await dans(() => { nouvelleSimulation({ regle: 'H:L2NNL1L2L1', tore: 40 }); $('suiviForme').checked = true; });
  await avancer(30000);
  const toreOk = await dans(() => sim.fourmis.every((f) => f.x >= 0 && f.x < 40 && f.y >= 0 && f.y < 40));
  verifier(toreOk, 'la fourmi reste dans le parallélogramme');
  await capture('09-tore-hexagonal.png');

  // 8. Carte des visites en hexagonal.
  await dans(() => { nouvelleSimulation({ regle: 'H:L1L2NUL2L1R2' }); $('mode').value = 'visites'; $('suiviForme').checked = true; });
  await avancer(200000);
  await capture('10-spirale-carte-des-visites.png');
  await dans(() => { $('mode').value = 'couleurs'; });

  verifier(erreurs.length === 0, 'aucune erreur JavaScript', erreurs.join(' | '));
  await navigateur.close();
  console.log('\n' + (echecs === 0 ? 'Toutes les vérifications sont passées.' : echecs + ' vérification(s) en échec.'));
  process.exit(echecs ? 1 : 0);
})();

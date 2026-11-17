// Mesure le nombre d'images par seconde de la page, à vitesse maximale.
// Usage : node outils/mesurer_fps.js <dossier de la page> [secondes]
const { chromium } = require('playwright');
const path = require('path');
const dossier = path.resolve(process.argv[2]);
const duree = Number(process.argv[3] || 5) * 1000;

const SCENARIOS = [
  { nom: 'RL, 8 px/case', regle: 'RL', echelle: 8 },
  { nom: 'RL, 0,5 px/case', regle: 'RL', echelle: 0.5 },
  { nom: 'RLR, 0,5 px/case', regle: 'RLR', echelle: 0.5 },
  // seulement dans la nouvelle version :
  { nom: 'RL, 1/1024 px/case', regle: 'RL', echelle: 1 / 1024, nouveau: true },
  { nom: 'RL, suivi de la forme', regle: 'RL', suivi: true, nouveau: true },
  { nom: 'Spirale hex., suivi', regle: 'H:L1L2NUL2L1R2', suivi: true, nouveau: true },
];

(async () => {
  const navigateur = await chromium.launch();
  for (const sc of SCENARIOS) {
    if (sc.nouveau && !require('fs').existsSync(dossier + '/lancer.js')) continue;
    const page = await navigateur.newPage({ viewport: { width: 1400, height: 900 } });
    await page.goto('file://' + dossier + '/index.html');
    await page.evaluate(() => {
      // Chronométrage des deux postes : simulation et dessin.
      window.__t = { sim: 0, dessin: 0, nSim: 0, nDessin: 0 };
      const av = Langton.Simulation.prototype.avancer;
      Langton.Simulation.prototype.avancer = function (n) {
        const t = performance.now(); av.call(this, n); window.__t.sim += performance.now() - t; window.__t.nSim++;
      };
      const d = window.dessiner;
      window.dessiner = function () {
        const t = performance.now(); d(); window.__t.dessin += performance.now() - t; window.__t.nDessin++;
      };
    });
    await page.fill('#regle', sc.regle);
    await page.dispatchEvent('#regle', 'change');
    if (await page.$('#suiviForme')) {
      if (sc.suivi) await page.check('#suiviForme'); else await page.uncheck('#suiviForme');
    }
    if (sc.echelle) await page.evaluate((e) => { vue.cx = vue.cy = 0.5; vue.echelle = e; }, sc.echelle);
    await page.evaluate(() => {
      const v = document.getElementById('vitesse');
      v.value = 20; v.dispatchEvent(new Event('input')); // 100 000 pas/image dans les deux versions
    });
    await page.click('#lecture');
    const res = await page.evaluate((duree) => new Promise((ok) => {
      let images = 0;
      const debut = performance.now();
      Object.assign(window.__t, { sim: 0, dessin: 0, nSim: 0, nDessin: 0 });
      const pas0 = Number(document.getElementById('mPas').textContent.replace(/\D/g, ''));
      function compter() {
        images++;
        if (performance.now() - debut < duree) requestAnimationFrame(compter);
        else {
          const s = (performance.now() - debut) / 1000;
          const pas1 = Number(document.getElementById('mPas').textContent.replace(/\D/g, ''));
          ok({ fps: images / s, pasParSeconde: (pas1 - pas0) / s, cases: document.getElementById('mCases').textContent,
               msSim: window.__t.sim / Math.max(1, window.__t.nSim), msDessin: window.__t.dessin / Math.max(1, window.__t.nDessin),
               dessinsParSeconde: window.__t.nDessin / s });
        }
      }
      requestAnimationFrame(compter);
    }), duree);
    console.log(sc.nom.padEnd(22), 'images/s', res.fps.toFixed(1).padStart(5), '| dessins/s', res.dessinsParSeconde.toFixed(1).padStart(5),
      '| pas/s', Math.round(res.pasParSeconde).toLocaleString('fr-FR').padStart(11),
      '| ms simu/image', res.msSim.toFixed(1).padStart(5), '| ms dessin', res.msDessin.toFixed(1).padStart(5), '| cases à la fin', res.cases);
    await page.close();
  }
  await navigateur.close();
})();

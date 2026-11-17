// Ouvre la page et affiche les erreurs JavaScript.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  p.on('pageerror', (e) => console.log('ERREUR PAGE :', e.message, e.stack.split('\n')[1]));
  p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('CONSOLE', m.type(), m.text()); });
  await p.goto('file://' + path.resolve(process.argv[2]) + '/index.html');
  await p.waitForTimeout(800);
  console.log('pas affichés :', await p.textContent('#mPas'));
  await b.close();
})();

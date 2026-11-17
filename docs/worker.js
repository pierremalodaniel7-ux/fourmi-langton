// worker.js — calcul des circuits dans un Web Worker (la page reste fluide pendant les grands calculs).
// Messages reçus : { id, spec, lignes:[valeurs...] }   envoyés : { id, type:'progres', ligne, pas, total } | { id, type:'ligne', i, res } | { id, type:'fin' }
importScripts('engine.js', 'circuit.js');
self.onmessage = (ev) => {
  const { id, spec, lignes } = ev.data;
  try {
    lignes.forEach((valeurs, i) => {
      let dernier = 0;
      const res = Circuit.verifier(Langton, spec, valeurs, (pas, total) => {
        const t = Date.now();
        if (t - dernier > 150) { dernier = t; self.postMessage({ id, type: 'progres', ligne: i, pas, total }); }
      });
      self.postMessage({ id, type: 'ligne', i, res: { sorties: res.sorties, affichage: res.affichage, valeurs } });
    });
    self.postMessage({ id, type: 'fin' });
  } catch (err) {
    self.postMessage({ id, type: 'erreur', message: String(err && err.message || err) });
  }
};

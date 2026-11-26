#!/usr/bin/env python3
"""R-304 FIL (a) : part des petites configurations qui donnent une autoroute.
Fourmi en (0,0) cap 0, 0 à 3 cases de couleur 1 dans [-2,2]² (coordonnées de la grille : carré, axiales hexa, triangle),
2 626 configurations par règle, T = 2^20. Sortie : data/fil_<règle>.txt (une ligne par config) + résumé sur stdout."""
import sys, itertools, collections
from outils_r import lot, parse
T = 1 << 20
def configs():
    C = [(x, y) for y in range(-2, 3) for x in range(-2, 3)]
    for k in range(4):
        for s in itertools.combinations(C, k): yield s
for rule in sys.argv[1:]:
    cf = list(configs())
    lines = [f"{rule}|0,0,0|" + ';'.join(f"{x},{y}" for x, y in s) for s in cf]
    out = lot(lines, T)
    cnt = collections.Counter(); per = collections.Counter(); debs = []
    fn = 'data/fil_' + rule.replace(':', '_') + '.txt'
    with open(fn, 'w') as f:
        for s, l in zip(cf, out):
            d = parse(l); f.write(l + '\n')
            cnt[d['issue']] += 1
            if d['issue'] == 'AUTOROUTES':
                per[d['sig']] += 1; debs.append(d['ants'][0][3])
    debs.sort()
    med = debs[len(debs) // 2] if debs else '-'
    top = ' '.join(f"{k}:{v}" for k, v in per.most_common(4))
    print(f"{rule}\t{len(cf)}\tAUTO {cnt['AUTOROUTES']}\tCYCLE {cnt['CYCLE']}\tINDEC {cnt['INDECIS']}\tdeb_med {med}\tdeb_min {debs[0] if debs else '-'}\t{top}", flush=True)

"""T2 — cherche dans des machines cycliques une droite de porte à passages RÉGULIERS (écarts égaux, en cyclique sur la période)
dont l'issue (T/D) n'est pas constante : candidat « diviseur » (horloge régulière en entrée, issue qui dépend de l'histoire).
Usage : python3 s2_horloge/t2_regulier.py fichier.json [tol]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from t2_portes import analyse
L = json.load(open(sys.argv[1])); tol = int(sys.argv[2]) if len(sys.argv) > 2 else 0
cnt = collections.Counter(); out = []
for n, m in enumerate(L):
    P = m['P']; gates, res = analyse(m['sit'], P)
    for r in res:
        t = [x[0] for x in r['seq']]; s = ''.join(x[2] for x in r['seq'])
        if len(t) < 2: continue
        dt = [b - a for a, b in zip(t, t[1:])] + [t[0] + P - t[-1]]
        reg = max(dt) - min(dt) <= tol
        var = 'T' in s and 'D' in s
        cnt[(reg, var)] += 1
        if reg and var:
            print('machine', n, 'P', P, 'porte', r['gate'], r['p'], 'droite', r['lane'], s, 'écart', dt[0], flush=True)
            out.append({'n': n, 'P': P, 'porte': r['p'], 'droite': r['lane'], 'seq': s, 'ecart': dt[0], 'sit': m['sit']})
print('(régulier, variable) :', dict(cnt))
json.dump(out, open(sys.argv[1].replace('.json', '_regulier.json'), 'w'))

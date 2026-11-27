#!/usr/bin/env python3
"""S1 / R-411 étape E : montages de k2full.json : sortie commune O sans ombre (aucune sortie des autres cas parallèle à ≤ 6 voies) ;
puis 2 usages (N couples au hasard, superposition exacte). Écrit s1_fusion/k2reuse.json. Usage : python3 s1_fusion/k2reuse.py T3 N"""
import sys, os, json, collections, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from sup2 import superpose
from circuit import Circuit
T3, N = int(sys.argv[1]), int(sys.argv[2])
R = json.load(open(os.path.join(HERE, 'k2full.json')))
V = lambda k: (k[0] == '1' and k[1] == '1' and k[2] == '1' and k[3] == '0') or (k[0:2] != '11' and k[2:] == '11')
good = []; st = collections.Counter()
for r in R:
    others = [tuple(o) for k, s in r['out'].items() if not V(k) for o in s]
    Os = [tuple(o) for o in r['O'] if not any(p[0] == o[0] and abs(p[1] - o[1]) <= 6 for p in others)]
    if not Os: st['ombre'] += 1; continue
    st['sans ombre'] += 1; r['Os'] = Os; good.append(r)
print(dict(st), flush=True)
random.seed(1); PAIRS = [(random.randrange(16), random.randrange(16)) for _ in range(N)]
Cs = [Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in r['pieces']]) for r in good]
sc = superpose(Cs, T3, pairs=PAIRS)
for r, s in zip(good, sc): r['deux'] = s
json.dump([dict((k, v) for k, v in r.items() if k != 'out') for r in good], open(os.path.join(HERE, 'k2reuse.json'), 'w'))
print('2 usages (%d couples) :' % N, sorted(collections.Counter(sc).items(), reverse=True)[:8])

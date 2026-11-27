#!/usr/bin/env python3
"""S1 / R-410 : les montages propres 16/16 de add3_k07.json passent-ils 2 usages (256 couples, superposition exacte) ? Écrit k07_reuse.json.
Usage : python3 s1_fusion/k07_reuse.py T3 [nb de couples au hasard, 1 rang par fusion]"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from sup2 import superpose
from add2_perm import build
from circuit import Circuit
from fa_lib import back
T3 = int(sys.argv[1]); ST1 = build('A', 0, 20)
F = json.load(open(os.path.join(HERE, 'fus07.json'))); R = json.load(open(os.path.join(HERE, 'add3_k07.json')))
ok = [l for l in R if not l['sales']]
if len(sys.argv) > 2:
    seen = set(); ok = [l for l in ok if not (l['f'] in seen or seen.add(l['f']))]
import random; random.seed(0); PAIRS = [(random.randrange(16), random.randrange(16)) for _ in range(int(sys.argv[2]))] if len(sys.argv) > 2 else None
Cs = []
for l in ok:
    f = F[l['f']]; Kp = back((tuple(f['K'][0]), [tuple(c) for c in f['K'][1]]), 1095)
    Cs.append(Circuit(ST1.pieces[:l['rank']] + [('K7', Kp, None)] + ST1.pieces[l['rank']:]))
sc = superpose(Cs, T3, pairs=PAIRS)
out = [dict(f=l['f'], rank=l['rank'], deux_usages=s) for l, s in zip(ok, sc)]
json.dump(out, open(os.path.join(HERE, 'k07_reuse.json'), 'w'))
print(len(ok), 'montages ; scores 2 usages :', sorted(collections.Counter(sc).items(), reverse=True)[:10])

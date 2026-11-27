#!/usr/bin/env python3
"""S1 / R-411 étape B : pour chaque K1 de côté (k1side.json : V0 + K1 → {p0, q0}, V7 + K1 → {p7, q7}), cherche une fusion du catalogue posée
EXACTEMENT sur (p0, p7) (4 choix de paires, 2 ordres). Écrit s1_fusion/k1match.json. Usage : python3 s1_fusion/k1match.py"""
import sys, os, json, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from matchlib import matches
R = json.load(open(os.path.join(HERE, 'k1side.json'))); T = 9600
res = []
for i, r in enumerate(R):
    for p, q in itertools.product(r['s0'], r['s7']):
        for X, Y in ((p, q), (q, p)):
            for m in matches(tuple(X), tuple(Y), T):
                res.append(dict(i=i, X=X, Y=Y, **m))
json.dump(res, open(os.path.join(HERE, 'k1match.json'), 'w'))
print(len(R), 'K1 ;', len(res), 'appariements exacts ;', len({x['i'] for x in res}), 'K1 distincts')

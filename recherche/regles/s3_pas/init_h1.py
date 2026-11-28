#!/usr/bin/env python3
"""R-620 Départ « en arbre en H » pour l'arbre h1'' (207 puissances) : longueurs croissantes avec la taille du sous-arbre,
D[n] = a + b·taille(n)^e (périodes), G[n] = g0 + g1·(taille du plus gros enfant)^e ; les modules h1' gardent les longueurs vérifiées.
Usage : python3 init_h1.py a b e g0 g1  -> nombre de conflits (chain_h1b), écrit data/init_<a>_<b>_<e>_<g0>_<g1>.json"""
import sys, json
from chain_h1b import build_state, full_conflicts, names, SUB, R
from modules import nodes
a, b, e, g0, g1 = map(float, sys.argv[1:6])
size = {n: len(SUB[n]) for n in names}
kids = {n.name: [it.name for _, it in n.inputs if not isinstance(it, str)] for n in nodes(R)}
h1p = json.load(open('h1_param_simple.json'))
D = {n: int(a + b * size[n] ** e) for n in names}
G = {n: int(g0 + g1 * max([size[k] for k in kids[n]] or [0]) ** e) for n in names}
for q in ('gN1h', 'gN2h', 'gP1h', 'gP2h'):
    for k in h1p['D']: D[q + k] = h1p['D'][k]; G[q + k] = h1p['G'][k]
st = build_state(D, G); c = full_conflicts(st)
print(sys.argv[1:6], 'conflits', len(c), 'tmax', st[0].tmax, flush=True)
json.dump(dict(D=D, G=G, conflits=len(c)), open('data/init_' + '_'.join(sys.argv[1:6]) + '.json', 'w'))

#!/usr/bin/env python3
"""R-323 Miroir fixe : N autoroutes identiques sur la même voie, espacées de m périodes, contre le même obstacle.
Sortie de chacune (direction, voie). Usage : multi_passage.py REGLE "x,y;x,y;…" N m"""
import sys, json
from banc import launcher, sit, outcome, K
from outils_r import lot, parse
rule = sys.argv[1]; obst = [tuple(map(int, p.split(','))) for p in sys.argv[2].split(';')]; N = int(sys.argv[3]); m = int(sys.argv[4])
g = json.load(open('data/germes_regles.json'))[rule]; P, D = g['P'], tuple(g['D'])
ants = []; cells = {}
for u in range(N):                       # la fourmi u part u·m périodes DERRIÈRE la première (ordre : la plus avancée d'abord)
    a, c = launcher(g, 0, (-u * m * D[0], -u * m * D[1])); ants.append(a); cells.update(c)
for o in obst: cells[o] = 1
l = lot([sit(rule, ants, cells)], max(1 << 21, 4 * N * m * P), ncpu=1)[0]
outs = [outcome(rule, l, i, P, D)[:3] for i in range(N)]
for i, o in enumerate(outs): print(f"autoroute {i+1} : {o}")
print('même sortie pour toutes :', len(set(outs)) == 1, '|', parse(l)['sig'])

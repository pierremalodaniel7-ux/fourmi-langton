#!/usr/bin/env python3
"""R-340 (tri) : parmi les bascules R → R' → R (bascule_hexa.py), celles où le MÊME vaisseau (direction, voie absolue, ordre de jeu)
fait les deux changements (bascule « T »), routes dans un demi-plan, sortie différente selon l'état."""
import json, collections, sys
from hx import rot, ship_dir
F = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'data/bascules_osc2.json'))
def kv(s): return dict(x.split('=') for x in s.split()[1:] if '=' in x)
def lane(x, y, r): X, Y = rot((x, y), -r % 6); return X + Y
def absl(info):
    f = kv(info); r = int(f['r']); l = int(f['l']); cx, cy = map(int, f['centre'].split(','))
    e = rot((1, 0), r); return r, lane(cx + l * e[0], cy + l * e[1], r), int(f['ord']), int(f['sortie_r']), f['qui'], int(f['ph']), int(f['p'])
H = [frozenset({d, (d + 1) % 6, (d + 2) % 6}) for d in range(6)]
T = []; seen = set()
for x in F:
    a, b = absl(x['s1']), absl(x['s2'])
    if a[:3] != b[:3]: continue
    dirs = {a[0], a[3], b[3]}
    half = any(dirs <= h for h in H)
    key = (x['R'], a[:4], b[3])
    if key in seen: continue
    seen.add(key); T.append({'R': x['R'], 'R2': x['R2'], 's1': x['s1'], 's2': x['s2'], 'entree': a[:3], 'sortie1': a[3], 'sortie2': b[3], 'demi_plan': half,
              'lecture': a[3] != b[3]})
print('bascules T (même vaisseau pour les 2 changements) :', len(T), '; routes dans un demi-plan :', sum(t['demi_plan'] for t in T),
      '; + sortie différente selon l\'état :', sum(t['demi_plan'] and t['lecture'] for t in T))
for t in [t for t in T if t['demi_plan'] and t['lecture']][:8]: print(' ', t['R'], 'entrée', t['entree'], 'sorties', t['sortie1'], t['sortie2'], '|', t['s1'][:60], '||', t['s2'][:60])
json.dump(T, open('data/bascules_T.json', 'w'))

#!/usr/bin/env python3
"""R-708 (suite) Pour les sondes « transparentes dans un état, X dans l'autre » : sortie lisible (≠ entrée) ? et existe-t-il UN vaisseau
qui remet X dans l'état de départ (M ou R'), au même endroit ? (balayage dir × voie −8..8 × phase de X, hx.py) -> sondes_retour.json"""
import json
from traj import *
import pixel
from exp_osc import setup
import sonde_scan as S
CAND = [("R'", 0, 2), ('M', 0, -3), ('M', 1, -3), ("R'", 3, -3), ('M', 3, 2), ('M', 4, 2)]
def run(osc, r, l, ph, extra=400):
    E = setup(osc, r, l, ph, 0); B = [list(a) for a in E['ants']]; g = dict(E['g'])
    for _ in range(E['T'] + extra): step(B, g)
    near = [tuple(b) for b in B if hd(b[0], b[1]) <= 8]; nc = sorted(c for c in g if hd(*c) <= 8)
    return near, nc
def osc_str(a, c): return 'H:R2L2|' + ';'.join(f'{x},{y},{h}' for x, y, h in a) + '|' + ';'.join(f'{x},{y}' for x, y in c)
out = []
for st, r, l in CAND:
    src = pixel.M if st == 'M' else pixel.R2; P = len(pixel.ORB[0 if st == 'M' else 1])
    for ph in range(P):
        x = S.probe(src, r, l, ph)
        if not x or not x.get('propre') or x['objet'] != 'X': continue
        lisible = x['sorties'] != [x['entree']]
        a, c = run(src, r, l, ph); X = osc_str(a, c); KX = S.orbit_key(a, c); PX = len(KX)
        target = S.KM if st == 'M' else S.KR
        fix = []
        for r2 in range(6):
            for l2 in range(-8, 9):
                for p2 in range(PX):
                    try: E = setup(X, r2, l2, p2, 0)
                    except Exception: continue
                    B = [list(z) for z in E['ants']]; g = dict(E['g'])
                    for _ in range(E['T'] + 400): step(B, g)
                    near = [tuple(b) for b in B if hd(b[0], b[1]) <= 8]; nc = [cc for cc in g if hd(*cc) <= 8]
                    if near and S.orbit_key(near, nc) == target: fix.append((r2, l2, p2))
        print(st, r, l, ph, 'X période', PX, 'lisible', lisible, 'retours', fix[:5], len(fix), flush=True)
        out.append({'etat': st, 'r': r, 'l': l, 'ph': ph, 'X': X, 'PX': PX, 'lisible': lisible, 'sorties': x['sorties'], 'entree': x['entree'], 'retours': fix})
json.dump(out, open(HERE + '/sondes_retour.json', 'w'), default=list)

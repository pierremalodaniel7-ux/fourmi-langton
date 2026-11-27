#!/usr/bin/env python3
"""R-712 Après une lecture « OFF » (sonde utile de R-708 : M devient X), peut-on remettre le pixel en état AVEC LES PORTS D'ÉCRITURE
déjà en place ? Pour chaque sonde utile, M (phase de la sonde) + sonde à t = 0, puis UN vaisseau sur une voie de kit (SET0, SET5, RST2,
RST3 : mêmes droites que les sorties des démux de l'écran) retardé de Δ (toutes les phases de X : Δ = 0..PX·3 après le passage).
Issue exacte (hx.py) : objet = M, R', autre ; reste = vaisseaux libres ? -> lecture_kits.json"""
import json, sys
from traj import *
import pixel
from exp_osc import setup
import sonde_scan as SS
sys.argv = [sys.argv[0], '1', '1']
import ecran3_geo as E3
SONDES = [(0, -3, 6), (3, 2, 8), (4, 2, 15)]
def run(ants, cells, T):
    A = [list(a) for a in ants]; g = {c: 1 for c in cells}
    for _ in range(T): step(A, g)
    return A, g
res = []
for r, l, ph in SONDES:
    E = setup(pixel.M, r, l, ph, 0); sh = tuple(E['ants'][-1]); sc = sorted(c for c in E['g'] if c not in E['states'][ph][1])
    Tp = of_label(lab_piece((sh, sc), 0))           # trajectoire de la sonde, M en phase ph à t = 0 (repère absolu du pixel)
    oa, og = E['states'][ph]
    for kn, K in E3.KS.items():
        for De in range(20, 150):
            # retard de la pièce kit : sa trajectoire de référence (objet en phase K['ph'] à t = 0) décalée de De
            Tk = movT(K['S'], (0, 0), De)
            P1 = piece_at(Tp, 0); P2 = piece_at(Tk, 0)
            ants = [tuple(a) for a in oa] + [P1[0], P2[0]]; cells = list(og) + P1[1] + P2[1]
            if len(set(cells)) < len(cells): continue
            Tend = De + E['T'] + 400
            A, g = run(ants, cells, Tend)
            near = [tuple(b) for b in A if hd(b[0], b[1]) <= 8]; far = [tuple(b) for b in A if hd(b[0], b[1]) > 8]
            nc = [c for c in g if hd(*c) <= 8]; fc = [c for c in g if hd(*c) > 8]
            d = decode(far, fc)
            if d is None: continue
            k = SS.orbit_key(near, nc) if near else None
            name = 'M' if k == SS.KM else "R'" if k == SS.KR else None
            if name:
                res.append({'sonde': (r, l, ph), 'kit': kn, 'De': De, 'objet': name, 'n_vaisseaux': len(d)})
                print((r, l, ph), kn, De, name, len(d), flush=True)
json.dump(res, open(HERE + '/lecture_kits.json', 'w'), default=list)
print(len(res), 'issues propres M / R\'')

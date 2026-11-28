#!/usr/bin/env python3
"""T4 (27/11) : vaisseau de REMPLISSAGE. Les 2 droites de mise à 1 (dir 0 voie 1, dir 5 voie 1) jouées sur R' (ON) à toutes les phases :
R' reste-t-il R' ? (hx.py). Sortie t4/remplir_scan.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pixel import M, R2, ORB, kit
from traj import *
out = []
for (r, l) in [(0, 1), (5, 1)]:
    for osc, s in [(R2, 1), (M, 0)]:
        for ph in range(len(ORB[s])):
            try: K = kit(osc, r, l, ph)
            except Exception: out.append(dict(r=r, l=l, etat=s, ph=ph, res='?')); continue
            fin = None
            for s2 in (0, 1):
                if K['obj'] in ORB[s2]: fin = (s2, ORB[s2].index(K['obj']))
            out.append(dict(r=r, l=l, etat=s, ph=ph, T=K['T'], fin=fin, traverse=same(K['S'], K['out'])))
json.dump(out, open(HERE + '/t4/remplir_scan.json', 'w'))
for o in out: print(o['r'], o['l'], o['etat'], o['ph'], o.get('fin', o.get('res')), o.get('traverse'))

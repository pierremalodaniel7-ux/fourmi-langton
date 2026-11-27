#!/usr/bin/env python3
"""T4 (27/11) : vaisseau d'EFFACEMENT. Pour les 2 droites de mise à 0 (RST : dir 2 voie -2, dir 3 voie -2), on joue le même vaisseau sur
M (OFF) à toutes les phases : M reste-t-il M (et en quelle phase), le vaisseau ressort-il sur sa route ? (hx.py, comme kits_scan.py)
Sortie : t4/effacer_scan.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pixel
from pixel import M, R2, ORB, kit
from traj import *
out = []
for (r, l) in [(2, -2), (3, -2)]:
    for osc, s in [(M, 0), (R2, 1)]:
        for ph in range(len(ORB[s])):
            try: K = kit(osc, r, l, ph)
            except Exception as ex: out.append(dict(r=r, l=l, etat=s, ph=ph, res='?')); continue
            fin = None
            for s2 in (0, 1):
                if K['obj'] in ORB[s2]: fin = (s2, ORB[s2].index(K['obj']))
            tr = same(K['S'], K['out'])
            out.append(dict(r=r, l=l, etat=s, ph=ph, T=K['T'], fin=fin, traverse=tr))
json.dump(out, open(HERE + '/t4/effacer_scan.json', 'w'))
for o in out:
    if o.get('fin'): print(o)

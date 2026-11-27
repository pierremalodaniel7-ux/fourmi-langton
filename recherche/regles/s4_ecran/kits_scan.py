#!/usr/bin/env python3
"""R-705 Toutes les écritures à UN vaisseau (joué après l'objet) entre M (OFF) et R' (ON) au même endroit (la paire de R-341) :
pour chaque direction r, voie l, phase ph : le vaisseau change-t-il M en une phase de R' (mise à 1) / R' en une phase de M (mise à 0),
en ressortant seul et propre ? Moteur hx.py (Python) ; contrôle fourmi_r sur les retenus. -> kits.json
But : trouver des couples (mise à 1, mise à 0) dont les directions font 0° ou 60° (R-341 : 120°, ce qui bloque l'écran, R-703/R-704)."""
import json
from traj import *
import pixel
from exp_osc import setup
def try_kit(src, dst, r, l, ph):
    try:
        E = setup(src, r, l, ph, 0)
    except Exception:
        return None
    A = E['ants']; B = [list(a) for a in A]; g = dict(E['g'])
    for _ in range(E['T']): step(B, g)
    obj = (sorted(tuple(b) for b in B[:-1]), sorted(c for c in g if hd(*c) <= 6))
    far = sorted(c for c in g if hd(*c) > 6)
    if hd(B[-1][0], B[-1][1]) <= 6: return None
    try: fin = pixel.ORB[dst].index(obj)
    except ValueError: return None
    if decode([tuple(B[-1])], far) is None: return None
    return {'r': r, 'l': l, 'ph': ph, 'T': E['T'], 'fin': fin}
if __name__ == '__main__':
    res = {}
    for name, src, dst in (('SET', pixel.M, 1), ('RST', pixel.R2, 0)):
        res[name] = [k for r in range(6) for l in range(-8, 9) for ph in range(len(pixel.ORB[1 - dst]))
                     for k in [try_kit(src, dst, r, l, ph)] if k]
        print(name, len(res[name]), sorted({(k['r'], k['l']) for k in res[name]}))
    json.dump(res, open(HERE + '/kits.json', 'w'))

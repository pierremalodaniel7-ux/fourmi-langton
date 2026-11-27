#!/usr/bin/env python3
"""T4 : place un pixel M/R' (kit SET0, R-705) sur chacune des 4 sorties c00' c10' c01' c11' du pas complet R-617, au premier endroit
après le germe qui est à ≥ MARGE (distance hex) de toutes les autres routes (t4/rayons.json). Sortie : t4/placement.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
MARGE = int(os.environ.get('MARGE', 20)); SEG = json.load(open(os.path.join(T4, 'rayons.json')))
def libre(c, own):
    for r, l, a0, a1 in SEG:
        if (r, l) == own: continue
        lc, ac = lat_ab(c, r)
        if abs(l - lc) < MARGE and a0 - MARGE <= ac and (a1 is None or ac <= a1 + MARGE): return False
    return True
PL = {}
for nm in CASES:
    O = wl_to_T(STEP.out[nm]); r = O[0]; p = T_pos(O, TDEC); own = (r, lat_ab(p, r)[0])
    others = [s for s in SEG if (s[0], s[1]) == own]
    t = TDEC + 8 * MARGE
    while True:
        rho, c, dl = kit_on('SET0a', O, t)
        if libre(c, own): break
        t += 8
    PL[nm] = dict(kit='SET0a', rho=rho, c=list(c), arrivee=dl, phase0=(kit('SET0a')['ph'] - dl) % PER[0], distance_germe=(t - TDEC) // 8,
                  meme_route=others)
    print(nm, PL[nm])
json.dump(PL, open(os.path.join(T4, 'placement.json'), 'w'), indent=1)

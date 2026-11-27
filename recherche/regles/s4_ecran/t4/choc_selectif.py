#!/usr/bin/env python3
"""R-721 (T4) : chocs SÉLECTIFS EN TEMPS pour la lecture. La sonde R-708 (dir 0, voie −3) ressort 3 pas EN AVANCE si le pixel est OFF
(M -> X), à l'heure s'il est ON (R' intact). On cherche les chocs propres du catalogue R-700 (data/chocs.json) tels que, si l'entrée
« signal » (B ou A) arrive 3 pas PLUS TARD, les 2 vaisseaux se croisent sans rien changer (transparent exact). Moteur fourmi_r (lot),
puis hx.py sur les retenus. Sortie : t4/choc_selectif.json = [{k, signal (0 = B, 1 = A), retard}]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
from lib4 import situation, lotdump, decode, lab_of, transform, pyrun
cat = json.load(open(os.path.join(S4, 'data', 'chocs.json')))
lines, meta = [], []
for k, c in enumerate(cat):
    LB, LA = tuple(c['LB']), tuple(c['LA'])
    for sig in (0, 1):
        for dl in (3,):
            L2 = [transform(LB, 0, (0, 0), dl), LA] if sig == 0 else [LB, transform(LA, 0, (0, 0), dl)]
            labs = L2 if c['ordre'] == 0 else L2[::-1]
            lines.append(situation(labs)); meta.append((k, sig, dl, tuple(sorted(L2))))
T = 16 * 25 + 480 + 8
R = lotdump(lines, T); out = []
for (k, sig, dl, L2), (a, cc), s in zip(meta, R, lines):
    d = decode(a, cc)
    if d is None or len(d) != 2: continue
    if tuple(sorted(lab_of(x, T) for x in d)) == L2:
        pa, pc = pyrun(s, T); ok2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, cc))
        out.append(dict(k=k, signal=sig, retard=dl, deux_moteurs=ok2))
json.dump(out, open(os.path.join(T4, 'choc_selectif.json'), 'w'))
print(len(cat), 'chocs propres ;', len(out), 'deviennent transparents si le signal a 3 pas de retard ; 2 moteurs :', sum(o['deux_moteurs'] for o in out))

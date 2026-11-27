#!/usr/bin/env python3
"""R-701 (tri) Parmi les démultiplexeurs justes 4/4 : (a) aucune paire (sortie, entrée) de face sur le même axe (condition de
réutilisation, R-338) ; (b) pour chaque sortie O_j, un point P_j de sa route, au-delà du dernier choc, à distance ≥ DMIN de TOUS
les autres rayons (entrées et sorties des 4 cas) : c'est là qu'on pourra poser le pixel j. Classement : durée totale, distance.
Usage : python3 demux_filtre.py data/demux_*.json -> data/demux_tries.json"""
import sys, json, glob, itertools, numpy as np
from rayons import *
DMIN = 16
def arr(T, t0, t1):
    L = to_label(T); return np.array([antpos(L, t) for t in range(t0, t1, 2)])
def hdn(D): return (np.abs(D[:, 0]) + np.abs(D[:, 1]) + np.abs(D[:, 0] + D[:, 1])) // 2
def T_(t): return tuple(t)
def analyse(B):
    ins = [T_(v) for v in B['T'].values()]
    exp = {k: [T_(t) for t in v] for k, v in B['exp'].items()}
    outs_all = sorted({t for v in exp.values() for t in v})
    if head_on(outs_all, ins): return None
    t0, t1 = min(B['times'].values()), max(B['times'].values())
    rays = {}
    for t in outs_all: rays[t] = arr(t, t0, t1 + 4000)
    for t in ins: rays.setdefault(t, arr(t, -4000, t1))
    opts = {'(0, 0)': [T_(B['T']['W'])], '(0, 1)': [T_(t) for t in B['outs']['(0, 1)']], '(1, 0)': [T_(t) for t in B['outs']['(1, 0)']], '(1, 1)': [T_(t) for t in B['outs']['(1, 1)']]}
    best = None
    for choice in itertools.product(*opts.values()):
        res = []
        for O in choice:
            found = None
            for Lp in range(10, 200, 3):
                P = np.array(antpos(to_label(O), t1 + 8 * Lp))
                dm = min(int(hdn(r - P).min()) for t, r in rays.items() if t != O)
                if dm >= DMIN: found = (Lp, dm); break
            if not found: break
            res.append(found)
        if len(res) == 4:
            sc = sum(r[0] for r in res)
            if best is None or sc < best[0]: best = (sc, choice, res)
    if not best: return None
    return {'outs4': best[1], 'pix': best[2], 'duree': t1 - t0, 'score': best[0] + (t1 - t0) / 8}
if __name__ == '__main__':
    allB = []
    for f in sys.argv[1:]: allB += json.load(open(os.path.join(HERE, f)))
    good = []
    for B in allB:
        a = analyse(B)
        if a: B.update(a); good.append(B)
    good.sort(key=lambda B: B['score'])
    print(len(allB), 'démultiplexeurs ;', len(good), 'sans paire de face et avec 4 places de pixel')
    for B in good[:8]: print(B['duree'], B['pix'], B['order'], B['choix'])
    json.dump(good, open(HERE + '/data/demux_tries.json', 'w'))

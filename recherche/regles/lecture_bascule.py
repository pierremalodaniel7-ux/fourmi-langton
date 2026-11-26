#!/usr/bin/env python3
"""R-346 Lecture NON destructive de la bascule R-341 : un vaisseau-sonde qui traverse M (bit 0) sans rien changer, et qui est DÉCALÉ
(ou dévié) par R' (bit 1) en laissant R' intact. Pour chaque direction r, voie l, ordre de jeu et phase de l'objet : issue exacte.
Usage : python3 lecture_bascule.py"""
import json, collections
from fa_lib import lotdump, decode
from relais import orbit, parse, split
from hx import ship, ship_dir, rot
from demi_add_k import fmt
M = 'H:R2L2|0,0,1;1,-1,0|-1,1'; RP = 'H:R2L2|-1,0,3;1,1,0|-1,0;-1,1;0,-1;1,0;1,1'
D = 30; TT = 8 * (2 * D + 12)
OM = orbit(*parse(M)); ORP = orbit(*parse(RP))
def key(L): return frozenset((frozenset(a), c) for a, c in L)
KM, KR = key(OM), key(ORP)
def tirs(L):
    jobs = []; meta = []
    for r in range(6):
        d = ship_dir(r); e = rot((1, 0), r)
        for l in range(-6, 7):
            st = (-D * d[0] + l * e[0], -D * d[1] + l * e[1]); sa, sc = ship(r, st)
            for ph in range(len(L)):
                for o in (0, 1):
                    A = ([sa] if o else []) + list(L[ph][0]) + ([] if o else [sa])
                    jobs.append(fmt(A, list(L[ph][1]) + [sc])); meta.append((r, l, ph, o))
    out = {}
    free = {}
    for m, res in zip(meta, lotdump(jobs, TT)):
        s = split(res[0], res[1], (0, 0))
        if s is None: continue
        obj, oc, sh = s
        if len(sh) != 1 or len(obj) != 2: continue
        Lo = orbit(list(obj), list(oc))
        if not Lo: continue
        out[m] = (key(Lo), tuple(sh[0]))
    return out
if __name__ == '__main__':
    TM, TR = tirs(OM), tirs(ORP)
    # vaisseau seul (référence) : même (r, l, o) sans objet → position finale
    ref = {}
    for r in range(6):
        d = ship_dir(r); e = rot((1, 0), r); st = (-D * d[0] + l * e[0], -D * d[1] + l * e[1]) if False else None
    res = []
    for (r, l, ph, o), (k, s) in TM.items():
        if k != KM: continue                                  # M intact
        for (r2, l2, ph2, o2), (k2, s2) in TR.items():
            if (r2, l2, o2) != (r, l, o) or k2 != KR: continue  # R' intact
            if s2 != s: res.append({'r': r, 'l': l, 'o': o, 'phM': ph, 'phR': ph2, 'sortie_M': s, 'sortie_R': s2})
    print('sondes (M intact, R\' intact, sorties différentes) :', len(res))
    c = collections.Counter((x['r'], x['l'], x['o']) for x in res); print(c.most_common(10))
    json.dump(res, open('data/lecture_bascule.json', 'w'))
    for x in res[:5]: print(x)

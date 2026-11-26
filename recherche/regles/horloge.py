#!/usr/bin/env python3
"""R-349 Horloges R2L2 « en orbite » : m vaisseaux placés avec une symétrie de rotation d'ordre m (m = 2, 3, 6) autour de l'origine ;
on cherche les configurations qui reviennent EXACTEMENT à leur état de départ (CYCLE de fourmi_r = preuve par réversibilité) avec de
longs vols libres (grande boîte). Un tel objet est une horloge : un signal (un vaisseau) fait le tour et revient, indéfiniment, sans miroir.
Usage : python3 horloge.py [rayon] [T]"""
import sys, json, collections
from fa_lib import kship
from hx import ship, rot
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
Rr = int(sys.argv[1]) if len(sys.argv) > 1 else 10; T = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
jobs = []; meta = []
for m, step_r in ((2, 3), (3, 2), (6, 1)):
    for x in range(-Rr, Rr + 1):
        for y in range(-Rr, Rr + 1):
            if hd(x, y) > Rr or (x, y) == (0, 0): continue
            for r in range(6):
                for tau in range(8):
                    K = kship(r, (x, y), tau); ants = []; cells = []
                    for k in range(m):
                        a, cs = K; rr = k * step_r
                        X, Y = rot(a[:2], rr); ants.append((X, Y, (a[2] + rr) % 6)); cells += [rot(c, rr) for c in cs]
                    if len(set(cells)) < len(cells) or len({a[:2] for a in ants}) < m: continue
                    if min(hd(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(ants) for b in ants[i + 1:]) < 3: continue
                    jobs.append(fmt(ants, cells)); meta.append((m, x, y, r, tau))
print('configurations :', len(jobs), flush=True)
out = lot(jobs, T)
res = []
cnt = collections.Counter()
for mt, l in zip(meta, out):
    f = l.split('|'); issue = f[3] if len(f) > 3 else '?'; cnt[(mt[0], issue)] += 1
    if issue == 'CYCLE':
        P = int(f[5]); box = f[-1]
        res.append({'m': mt[0], 'gen': mt[1:], 'P': P, 'boite': box, 'sit': jobs[meta.index(mt)] if False else l.split('|CYCLE')[0]})
print(sorted(cnt.items()))
def bsize(b):
    try: w, h = b.split()[-1].split('x'); return int(w) * int(h)
    except Exception: return 0
res.sort(key=lambda z: -bsize(z['boite']))
json.dump(res, open('data/horloges_%d.json' % Rr, 'w'))
print('cycles :', len(res))
for z in res[:15]: print(z['m'], z['gen'], 'P =', z['P'], z['boite'], z['sit'][:110])

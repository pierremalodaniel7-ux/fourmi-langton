import sys, os, random
os.environ.setdefault('SEQ', '4,5,5')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle_long as BL, boucle3 as B3, conflits as CF, numpy as np
rnd = random.Random(1); D = 384888; nm = 'c00'; G = CF.germ_segments(D)
for _ in range(40):
    tri = [rnd.choice(s) for s in B3.SEQ]; s = BL.search(nm, tri, D)
    if not s: continue
    ns, g0, co, Kr, O = BL.affine(nm, tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])])
    pres, absn = CF.loop_segments(nm, BL.PL, tri, chocs, s['e'], BL.PL[nm]['arrivee'])
    K0 = pres[1][1]; d, t = CF.dmin(K0, G); j = int(np.argmin(d)); print('K0', K0, '\n G', G[j], d[j], t[j], 'O', CF.seg_T(O, 0, 0))
    print(' choc0', chocs[0].te, chocs[0].p, 'ins', chocs[0].ins, 'tri', tri[0])

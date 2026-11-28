import sys, os, random
os.environ.setdefault('SEQ', '4,5,5')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle_long as BL, boucle3 as B3, boucle_choix as BC, ecran_deux_pas as E2
from lib4 import closest
rnd = random.Random(1); D = 384888; nm = 'c00'; skip = int(sys.argv[1])
while True:
    tri = [rnd.choice(s) for s in B3.SEQ]; s = BL.search(nm, tri, D)
    if s:
        if skip == 0: break
        skip -= 1
ns, g0, co, Kr, O = BL.affine(nm, tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])])
print('tri', tri, 'te', [C.te for C in chocs], 'lieux', [C.p for C in chocs])
cand = dict(chocs=chocs, e=s['e'], u=s['u'], toks=BC.order(chocs, tri))
envs = STEP.cases(); e0 = [e for e in envs if spec(nm, e) == 0][0]; e1 = E2.rl(e0)
p = BL.PL[nm]; T = int(sys.argv[2]); A, G = [], []
a, g = place_ordered(0, p['phase0'], p['rho'], tuple(p['c'])); A += a; G += g
for tok in cand['toks']:
    if tok == 'GERM':
        for u, ee in ((0, e0), (D, e1)):
            for w in STEP.present(ee): pa, cs = render3(S3L.tshift(w, u), 0); A.append(pa); G += cs
    else: (x, y, h), cs = TR.piece_at(tok[1], 0); A.append((x, y, h)); G += cs
a, c = run_py(S3L.sit(A, G), T)
cs = set(c); bad = []
for x, y, h in a:
    near = frozenset((q[0] - x, q[1] - y) for q in cs if hd(q[0] - x, q[1] - y) <= 2)
    if (h, near) not in S3L.REC: bad.append((x, y, h))
print('T', T, 'fourmis', len(a), 'non-vaisseaux :', len(bad), bad[:12])
K = [C.ins[1 - i] for C, (k, i, o) in zip(chocs, tri)]
for j, k in enumerate(K): print('K%d' % (j + 1), 'à T :', T_pos(k, T))
ra = [x for x in a if hd(x[0] - p['c'][0], x[1] - p['c'][1]) > 6]; rc = [q for q in c if hd(q[0] - p['c'][0], q[1] - p['c'][1]) > 6]
d = decode3(ra, rc, T); print('decode', d is not None, 'pixel', pixel.read_state(a, c, p['rho'], tuple(p['c'])))
used = set()
for x, y, h in ra:
    used |= {q for q in cs if hd(q[0] - x, q[1] - y) <= 2}
left = [q for q in rc if q not in used]; print('cases orphelines', len(left), left[:10])
if d: print({k: int(S3L.tshift(STEP.out[k], D) in d) for k in STEP.names}, {k: spec(k, e1) for k in STEP.names})

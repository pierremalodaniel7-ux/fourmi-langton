import sys, os, random
os.environ.setdefault('SEQ', '4,5,5'); os.environ['DIAG'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle_long as BL, boucle3 as B3, boucle_choix as BC, ecran_deux_pas as E2
rnd = random.Random(1); D = 384888; nm = sys.argv[1]; skip = int(sys.argv[2])
while True:
    tri = [rnd.choice(s) for s in B3.SEQ]; s = BL.search(nm, tri, D)
    if s:
        if skip == 0: break
        skip -= 1
ns, g0, co, Kr, O = BL.affine(nm, tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])])
cand = dict(chocs=chocs, e=s['e'], u=s['u'], toks=BC.order(chocs, tri))
envs = STEP.cases(); test = []
for want in ((1, 1), (1, 0), (0, 1), (0, 0)):
    test += [e for e in envs if (spec(nm, e), spec(nm, E2.rl(e))) == want][:1]
for e in test: print(e)
print(BL.test2(nm, cand, D, test))

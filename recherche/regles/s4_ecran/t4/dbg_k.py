import sys, os, random
os.environ.setdefault('SEQ', '4,5,5')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle_long as BL, boucle3 as B3
rnd = random.Random(1); D = 384888
while True:
    tri = [rnd.choice(s) for s in B3.SEQ]; s = BL.search('c00', tri, D)
    if s: break
ns, g0, co, Kr, O = BL.affine('c00', tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])])
K = [C.ins[1 - i] for C, (k, i, o) in zip(chocs, tri)]
print('chocs te', [C.te for C in chocs], 'lieux', [C.p for C in chocs])
from lib4 import closest
L = [TR.to_label(k) for k in K] + [TR.to_label(O)]
names = ['K1', 'K2', 'K3', 'signal']
for i in range(4):
    for j in range(i + 1, 4):
        print(names[i], names[j], closest(L[i], L[j], 0, 400000, 8))

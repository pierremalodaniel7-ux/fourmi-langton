"""R-608 Recherche des longueurs (D, G par nœud) par descente : objectif = nb de couples de segments à < THR (diag.py, hors chocs voulus)
+ nb de couples de routes opposées à < THR voies ; puis vérification par simulation (tous les cas)."""
import random
from nor import *
from diag import conflicts
THR = 4
def score(root, Dm, Gm, a=0):
    L = Layout(root, a=a, Dmap=Dm, Gmap=Gm)
    c = conflicts(L, thr=THR); w, bad = L.opposed()
    nb = sum(1 for o, i in bad if True)
    badop = [x for x in bad]
    opp = 0
    for o, i in bad:
        lo = [lane_of2(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of2(antpos(i, t), o[0]) for t in range(8)]
        if min(abs(x - y) for x in lo for y in li) < THR: opp += 1
    return len(c) + opp, L, c
def descend(root, seed=0, iters=3000, a=0, log=print, Dr=(8, 60), Gr=(8, 20)):
    rnd = random.Random(seed); names = [n.name for n in nodes(root)]
    Dm = {n: rnd.randint(*Dr) for n in names}; Gm = {n: rnd.randint(*Gr) for n in names}
    s, L, c = score(root, Dm, Gm, a); best = s
    for it in range(iters):
        D2, G2 = dict(Dm), dict(Gm)
        for _ in range(rnd.choice((1, 1, 2, 3))):
            n = rnd.choice(names)
            if rnd.random() < 0.6: D2[n] = max(Dr[0], min(Dr[1], D2[n] + rnd.randint(-6, 6)))
            else: G2[n] = max(Gr[0], min(Gr[1], G2[n] + rnd.randint(-3, 3)))
        s2, L2, c2 = score(root, D2, G2, a)
        if s2 <= s:
            Dm, Gm, s, L, c = D2, G2, s2, L2, c2
            if s < best: best = s; log(f'  itération {it} : {s} conflits')
        if s == 0: break
    return s, L, dict(D=Dm, G=Gm, a=a), c
def nodes(n):
    yield n
    for _, it in n.inputs:
        if not isinstance(it, str): yield from nodes(it)

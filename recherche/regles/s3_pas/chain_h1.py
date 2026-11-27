#!/usr/bin/env python3
"""R-620 h1'' enchaîné : h1'' = g' ⊕ c' où g' = h1' ⊕ h0' et c' = case lue après le pas 1 (case (x', y') de c'_ij).
Arbre du pas 2 (sur les sorties du pas 1) :  h1'' = NOR(A, B), A = NOR(¬g', ¬c'), B = NOR(g', c')   (comme h1_tree)
  g' = NOR(NOR(¬h1', ¬h0'), NOR(h1', h0')) ; ¬g' = NOR(NOR(¬h1', h0'), NOR(h1', ¬h0'))
  c' = MUX(x', MUX(y', c'11, c'10), MUX(y', c'01, c'00)),  MUX(s, a, b) = NOR(NOR(¬s, a), NOR(s, b))  (¬c' : mêmes MUX sur les ¬c'_ij)
Chaque littéral du pas 1 = un module du pas 1 (chain2.S ; h1' = arbre h1_tree de R-614, ¬h1' = le même avec h0 inversé, donc même
géométrie que le module vérifié h1_param_simple.json quand il est branché en face). 4 copies de h1', ≈ 200 puissances.
Placement : descente guidée par les conflits (diag2.segments2, couples élagués par boîtes, intervalle [0, T] : 1 usage).
Usage : python3 chain_h1.py graine secondes [départ.json]   (formule : python3 chain_h1.py 0 0)"""
import sys, json, random, time, itertools, os
from htree import build, h1_tree
from chain2 import S, spec2
from modules import VARS, nodes
from nor import Layout
from diag2 import segments2
from diag import pmin, INF
from s3lib import antpos
def ren(t, p, flip=False):
    name, ins = t; out = []
    for it in ins:
        if isinstance(it, str): out.append({'h0': '~h0', '~h0': 'h0'}.get(it, it) if flip else it)
        else: out.append(ren(it, p, flip))
    return (p + name, out)
def H1(p, pol): return ren(h1_tree(), p, flip=(pol == 0))
def lit(v, p, pol): return H1(p, pol) if v == 'h1' else S(v, p, pol)
def MUX(p, s, a, b):
    """a, b : (variable, pol) ou sous-arbre déjà construit ; s : variable de sélection"""
    def f(z, q): return z if not isinstance(z, tuple) or isinstance(z[0], str) and isinstance(z[1], list) else lit(z[0], q, z[1])
    return (p, [(p + 'a', [lit(s, p + 'as', 0), f(a, p + 'aa')]), (p + 'b', [lit(s, p + 'bs', 1), f(b, p + 'bb')])])
def tree():
    def C(pol, p):
        return MUX(p, 'x', MUX(p + 'X1', 'y', ('c11', pol), ('c10', pol)), MUX(p + 'X0', 'y', ('c01', pol), ('c00', pol)))
    def G(pol, p):   # pol = 1 : g' ; 0 : ¬g'   (sous-nœuds : h1' en 1er -> branché en face sous un nœud de côté)
        if pol: return (p, [(p + '1', [lit('h1', p + '1h', 0), lit('h0', p + '1o', 0)]), (p + '2', [lit('h1', p + '2h', 1), lit('h0', p + '2o', 1)])])
        return (p, [(p + '1', [lit('h1', p + '1h', 0), lit('h0', p + '1o', 1)]), (p + '2', [lit('h1', p + '2h', 1), lit('h0', p + '2o', 0)])])
    return ('Z', [('ZA', [G(0, 'gN'), C(0, 'cN')]), ('ZB', [G(1, 'gP'), C(1, 'cP')])])
R = build(tree())
def conflicts3(L, T, thr=7, guard=80):
    """comme diag2.conflicts2, mais segments coupés à [0, T] (1 usage : l'état part de t = 0 et est lu à T) et couples élagués par boîtes"""
    segs = []
    for s in segments2(L):
        a, b = max(s[2], 0), min(s[3], T)
        if a > b: continue
        p, q = antpos(s[1], a), antpos(s[1], b)
        segs.append((s, a, b, min(p[0], q[0]) - thr - 4, max(p[0], q[0]) + thr + 4, min(p[1], q[1]) - thr - 4, max(p[1], q[1]) + thr + 4))
    segs.sort(key=lambda z: z[3]); gt = {frozenset((g[0], g[5])): g[2] for g in L.gates}; out = []
    for i in range(len(segs)):
        A = segs[i]
        for j in range(i + 1, len(segs)):
            B = segs[j]
            if B[3] > A[4]: break
            if B[5] > A[6] or A[5] > B[6] or B[1] > A[2] or A[1] > B[2]: continue
            a, b = A[0], B[0]
            if a[0] == b[0] or not (a[4] & b[4]): continue
            m, t = pmin(a[1], A[1], A[2], b[1], B[1], B[2], thr)
            if m < thr:
                tg = gt.get(frozenset((a[0], b[0])))
                if tg is not None and abs(t - tg) <= guard: continue
                out.append((a[0], b[0], m, t))
    return out
names = [n.name for n in nodes(R)]
PARENT = {}
for n in nodes(R):
    for _, it in n.inputs:
        if not isinstance(it, str): PARENT[it.name] = n.name
def owner(x, L): return x if x in PARENT or x == R.name else next(g[0] for g in L.gates if g[5] == x)
if __name__ == '__main__':
    seed, secs = int(sys.argv[1]), float(sys.argv[2]); rnd = random.Random(seed); SIM = int(os.environ.get('SIM', 6))
    full = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
    ok = all(R.value(e) == spec2('h1', e) for e in full)
    nl = sum(1 for n in nodes(R) for _, it in n.inputs if isinstance(it, str))
    print(f"h1'' : formule {'JUSTE' if ok else 'FAUSSE'} sur les 256 états ; {len(names)} puissances, {nl} littéraux", flush=True)
    if secs <= 0: sys.exit()
    h1p = json.load(open('h1_param_simple.json'))
    if len(sys.argv) > 3: p = json.load(open(sys.argv[3])); Dm, Gm = p['D'], p['G']
    else:
        Dm = {n: rnd.randint(30, 300) for n in names}; Gm = {n: rnd.randint(8, 60) for n in names}
        for q in ('gN1h', 'gN2h', 'gP1h', 'gP2h'):   # modules h1' : longueurs du module vérifié (R-614)
            for k in h1p['D']: assert q + k in Dm; Dm[q + k] = h1p['D'][k]; Gm[q + k] = h1p['G'][k]
    def evaluate(Dm, Gm):
        L = Layout(R, Dmap=Dm, Gmap=Gm); T = L.tmax + 1200; c = conflicts3(L, T); return len(c), c, L
    s, cl, L = evaluate(Dm, Gm); t0 = time.time(); it = 0; tested = set()
    log = open(f'data/chainh1_{seed}.log', 'a'); print('départ', s, f'tmax {L.tmax}', file=log, flush=True)
    while time.time() - t0 < secs:
        it += 1; D2, G2 = dict(Dm), dict(Gm)
        for _ in range(rnd.choice((1, 1, 2))):
            if cl and rnd.random() < 0.8:   # guidé : un nœud en conflit, ou un de ses ancêtres
                n = owner(rnd.choice(rnd.choice(cl)[:2]), L)
                while n in PARENT and rnd.random() < 0.4: n = PARENT[n]
            else: n = rnd.choice(names)
            big = rnd.random() < 0.3
            if rnd.random() < 0.6: D2[n] = max(8, min(300, D2[n] + (rnd.randint(-60, 60) if big else rnd.randint(-8, 8))))
            else: G2[n] = max(8, min(60, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
        s2, c2, L2 = evaluate(D2, G2)
        if s2 <= s:
            if s2 < s: print(f'{it} {time.time()-t0:.0f}s conflits {s2}', file=log, flush=True)
            Dm, Gm, s, cl, L = D2, G2, s2, c2, L2
            json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1_{seed}.json', 'w'))
            key = json.dumps([Dm, Gm], sort_keys=True)
            if s <= SIM and key not in tested:
                tested.add(key); r = L.check(); z = {v: 0 for v in VARS}
                bad = sum(1 for e, c_, got, val, _ in r if got != spec2('h1', {**z, **e})); dirty = sum(1 for x in r if not x[1])
                print(f'   simulation : {bad} faux, {dirty} sales / {len(r)} (tmax {L.tmax})', file=log, flush=True)
                if bad == 0 and dirty == 0:
                    json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1_OK_{seed}.json', 'w')); break
    print('fin', it, 'itérations', s, f'{time.time()-t0:.0f}s', file=log, flush=True)

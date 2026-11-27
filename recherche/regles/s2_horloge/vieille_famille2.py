"""S2 R-504 — famille R-349b : alignement de deux termes (rotation globale × relabellisation cyclique dans chaque groupe de 3 ×
début de chacun des chocs à 2 vaisseaux), extrapolation affine, test CYCLE. Usage : vieille_famille2.py n1 n2 [nmax]"""
import sys, json, itertools
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import certif_tri as C
from fa_lib import parts_of
from hx import step, rot
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
H = json.load(open('resumes/horloges_6_fourmis.json'))
ALL = False
def states_at_events(h):
    C.terme = lambda j, h=h: (0, 0, h['situation']); C.P_attendu = lambda j, h=h: h['P']
    P, segs, evs, hist = C.structure(0)
    times = sorted({e['ws'] for e in evs if len(e['parts']) == 2}) if not ALL else list(range(P))
    a, c = parts_of(h['situation']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    out = {}; t = 0
    for T in times:
        while t < T: step(A, G); t += 1
        out[T] = ([tuple(x) for x in A], dict(G))
    return out
def attach(A, G):
    out = []
    for k, an in enumerate(A):
        out.append(tuple(sorted((q[0] - an[0], q[1] - an[1]) for q in G if min(range(len(A)), key=lambda l: (hd(q[0] - A[l][0], q[1] - A[l][1]), l)) == k)))
    return out
def transform(A, G, k, perm):
    A2 = [(*rot(a[:2], k), (a[2] + k) % 6) for a in A]; G2 = {rot(q, k): 1 for q in G}
    return [A2[perm[i]] for i in range(6)], G2
perms = []
for s1 in range(3):
    for s2 in range(3):
        perms.append([(i + s1) % 3 for i in range(3)] + [3 + (i + s2) % 3 for i in range(3)])
n1, n2 = int(sys.argv[1]), int(sys.argv[2]); nmax = int(sys.argv[3]) if len(sys.argv) > 3 else n2 + 6
S1 = states_at_events(H[n1]); ALL = True; S2 = states_at_events(H[n2])
t1 = min(S1); A1, G1 = S1[t1]; pat1 = attach(A1, G1)
P = lambda n: 2322 + 2736 * n
cands = []
for t2, (A, G) in S2.items():
    for k in range(6):
        for perm in perms:
            B, GB = transform(A, G, k, perm)
            if [b[2] for b in B] != [a[2] for a in A1]: continue
            if attach(B, GB) != pat1: continue
            cands.append((t2, k, perm, B))
print('alignements candidats :', len(cands))
dn = n2 - n1
for t2, k, perm, B in cands:
    ns = [n for n in range(n2 + dn, nmax + 1, dn)]
    sits = []
    for n in ns:
        m = (n - n1) // dn
        A = [(a[0] + m * (b[0] - a[0]), a[1] + m * (b[1] - a[1]), a[2]) for a, b in zip(A1, B)]
        sits.append(fmt(A, [(an[0] + dx, an[1] + dy) for an, pat in zip(A, pat1) for dx, dy in pat]))
    out = lot(sits, P(max(ns)) + 10)
    res = [(n, l.split('|')[3], l.split('|')[5]) for n, l in zip(ns, out)]
    print('t2', t2, 'rot', k, 'perm', perm, res)
    if all(r[1] == 'CYCLE' for r in res): print('  FAMILLE :', sits[0])

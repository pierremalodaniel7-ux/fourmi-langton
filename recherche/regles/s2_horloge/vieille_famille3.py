"""S2 R-504 — alignement libre (toute rotation, toute permutation des fourmis, tout temps) entre deux termes de R-349b.
Usage : vieille_famille3.py n1 n2"""
import sys, json, itertools, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from fa_lib import parts_of
from hx import step, rot
from exp_osc import hd
H = json.load(open('resumes/horloges_6_fourmis.json'))
def attach(A, G):
    out = []
    for k, an in enumerate(A):
        out.append(tuple(sorted((q[0] - an[0], q[1] - an[1]) for q in G if min(range(len(A)), key=lambda l: (hd(q[0] - A[l][0], q[1] - A[l][1]), l)) == k)))
    return out
def sig(A, G, k):
    """signature (cap, motif) par fourmi après rotation k"""
    B = [(*rot(a[:2], k), (a[2] + k) % 6) for a in A]; GB = {rot(q, k): 1 for q in G}
    return [(b[2], p) for b, p in zip(B, attach(B, GB))], B
n1, n2 = int(sys.argv[1]), int(sys.argv[2])
a, c = parts_of(H[n1]['situation']); A1 = [tuple(t) for t in a]; G1 = {tuple(t): 1 for t in c}
s1, _ = sig(A1, G1, 0); ms1 = collections.Counter(s1)
a, c = parts_of(H[n2]['situation']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
hits = []
for t in range(H[n2]['P']):
    At = [tuple(x) for x in A]
    for k in range(6):
        s2, B = sig(At, G, k)
        if collections.Counter(s2) == ms1: hits.append((t, k))
    step(A, G)
print('temps × rotations dont les signatures coïncident avec le terme', n1, 'au temps 0 :', len(hits), hits[:10])

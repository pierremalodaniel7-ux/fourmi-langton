"""S2 R-504 — famille R-349b (P = 2 322 + 2 736 n) : alignement de deux termes au début du 1er choc à 2 vaisseaux, extrapolation affine
(fourmi par fourmi ; cases rattachées à la fourmi la plus proche, motif relatif identique exigé), test CYCLE. Usage : vieille_famille.py n1 n2"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import certif_tri as C
from fa_lib import parts_of
from hx import step
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
H = json.load(open('resumes/horloges_6_fourmis.json'))
def aligned(h):
    C.terme = lambda j, h=h: (0, 0, h['situation']); C.P_attendu = lambda j, h=h: h['P']
    P, segs, evs, hist = C.structure(0)
    e = next(e for e in evs if len(e['parts']) == 2)
    a, c = parts_of(h['situation']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(e['ws']): step(A, G)
    return A, G, e
def attach(A, G):
    out = []
    for k, an in enumerate(A):
        out.append(sorted((q[0] - an[0], q[1] - an[1]) for q in G if min(range(len(A)), key=lambda l: (hd(q[0] - A[l][0], q[1] - A[l][1]), l)) == k))
    return out
n1, n2 = int(sys.argv[1]), int(sys.argv[2])
A1, G1, e1 = aligned(H[n1]); A2, G2, e2 = aligned(H[n2])
print('événements', e1['parts'], e2['parts'])
p1, p2 = attach(A1, G1), attach(A2, G2)
print('motifs identiques :', p1 == p2, ' caps identiques :', [a[2] for a in A1] == [a[2] for a in A2])
sits = []; ns = list(range(n2 + 1, n2 + 12)); dn = n2 - n1
for n in ns:
    k = (n - n1) / dn
    if k != int(k): sits.append(None); continue
    k = int(k)
    A = [(a[0] + k * (b[0] - a[0]), a[1] + k * (b[1] - a[1]), a[2]) for a, b in zip(A1, A2)]
    cells = [(an[0] + dx, an[1] + dy) for an, pat in zip(A, p1) for dx, dy in pat]
    sits.append(fmt(A, cells))
P = lambda n: 2322 + 2736 * n
todo = [(n, s) for n, s in zip(ns, sits) if s]
out = lot([s for n, s in todo], P(max(n for n, s in todo)) + 10)
for (n, s), l in zip(todo, out): print(n, 'attendu', P(n), '→', l.split('|')[3], l.split('|')[5])

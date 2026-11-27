"""T2 — PIXEL EN AVAL D'UNE PORTE : dans une machine cyclique à portes d'interaction (étoile décalée R-516, hexagramme R-512), on pose une
bascule R-341 (pixel) « relative au vaisseau » (compteur4.place : copie de (vaisseau qui allume + pixel) de R-502, 160 pas avant l'allumage)
devant chaque vaisseau libre ; critère : CYCLE exact (fourmi_r, T = 8 P). Ensuite (t2_pixel_tri.py) on garde les pixels dont un écrivain
passe par une porte à issue variable : le pixel est alors piloté par la sortie de la porte (objectif 2, version « causale »).
Usage : python3 s2_horloge/t2_pixel_aval.py machines.json i0 i1 sortie.json"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step
from fa_lib import parts_of
from demi_add_k import fmt
from exp_osc import hd
import anti_pixel as ap
LEAD, DS, DP = 48, 6, 5      # pixel posé LEAD pas avant l'allumage ; isolement du vaisseau (DS) et du pixel (DP)
def reference(lead=LEAD):
    # comme compteur4.reference, mais LEAD pas avant l'allumage (machines plus serrées que les horloges seules)
    a, c = parts_of(ap.W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    O_M = ap.orbit(*ap.local(A, G, (0, 1)))
    hist = []
    for t in range(600):
        hist.append(([tuple(q) for q in A], dict(G)))
        if t > 10 and ap.norm(*ap.local(A, G, (0, 1))) not in O_M: break
        step(A, G)
    ton = t; As, Gs = hist[ton]
    i_s = min(range(2, len(As)), key=lambda i: hd(As[i][0] - As[0][0], As[i][1] - As[0][1]))
    As, Gs = hist[ton - lead]
    sx, sy, sh = As[i_s]
    ship = (sh, frozenset((q[0] - sx, q[1] - sy) for q in Gs if hd(q[0] - sx, q[1] - sy) <= 2))
    pa, pc = ap.local([list(q) for q in As], dict(Gs), (0, 1))
    return ship, ([(x - sx, y - sy, h) for x, y, h in pa], [(x - sx, y - sy) for x, y in pc])
def place(sit, P, ship, pix):
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    refs = [((ship[0] + k) % 6, frozenset(rot(q, k) for q in ship[1]), k) for k in range(6)]
    jobs = []; info = []
    for t in range(P):
        for i, (x, y, h) in enumerate(A):
            if min(hd(x - b[0], y - b[1]) for j, b in enumerate(A) if j != i) < DS: continue
            loc = frozenset((q[0] - x, q[1] - y) for q in G if hd(q[0] - x, q[1] - y) <= 2)
            for hh, cc, k in refs:
                if h != hh or loc != cc: continue
                Pa = [(*(lambda v: (v[0] + x, v[1] + y))(rot((px, py), k)), (ph + k) % 6) for px, py, ph in pix[0]]
                Pc = [(lambda v: (v[0] + x, v[1] + y))(rot(q, k)) for q in pix[1]]
                if min(hd(p[0] - b[0], p[1] - b[1]) for p in Pa for j, b in enumerate(A) if j != i) < DP: continue
                if any(q in G or hd(q[0] - b[0], q[1] - b[1]) <= 1 for q in Pc for b in G): continue
                jobs.append(fmt(Pa + [tuple(q) for q in A], list(G) + Pc)); info.append({'t': t, 'ship': i, 'k': k})
        step(A, G)
    return jobs, info
from outils_r import lot
M = json.load(open(sys.argv[1])); i0, i1 = int(sys.argv[2]), int(sys.argv[3]); outn = sys.argv[4]
ship, pix = reference()
hits = []; tot = collections.Counter()
for n in range(i0, min(i1, len(M))):
    m = M[n]; P = m['P']
    jobs, info = place(m['sit'], P, ship, pix)
    res = lot(jobs, 8 * P + 10)
    for j, inf, o in zip(jobs, info, res):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE': hits.append({'n': n, 'P0': P, 'P': int(f[5]), **inf, 'sit': j})
    json.dump(hits, open(outn, 'w'))
    print(n, 'P', P, 'poses', len(jobs), dict(tot), 'CYCLE', len(hits), flush=True)
print('fin', dict(tot), 'CYCLE', len(hits), collections.Counter((h['P0'], h['P']) for h in hits).most_common(8))

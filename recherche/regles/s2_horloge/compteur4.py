"""S2 R-507 — COMPTEUR 2 BITS par deux horloges de périodes P et 2P, chacune avec un pixel (bascule R-341).
1) familles d'horloges triangle (tri_cycles_rB5.json) prolongées linéairement (T, centre c, P) ; paires P1, P2 = 2 P1.
2) pose du pixel « relative au vaisseau » : on copie, depuis la machine R-502 n° 0, la configuration (vaisseau qui allume + pixel) 160 pas
   avant l'allumage ; sur la nouvelle horloge, à chaque instant où un vaisseau libre est dans le même état (à rotation k près), on pose le
   pixel tourné de k au même endroit relatif. Critère : CYCLE exact de période P (fourmi_r).
Usage : python3 s2_horloge/compteur4.py P1min P1max npaires"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
from tri_test import build
import anti_pixel as ap

def families():
    d = json.load(open('s2_horloge/tri_cycles_rB5.json')); F = collections.defaultdict(list)
    for w in d:
        F[(w['B'][0], tuple(w['B'][1]), w['B'][2], w['order'], tuple(w['A2'][1]), w['A2'][2])].append((w['T'], tuple(w['c']), w['P']))
    ext = {}
    for k, v in F.items():
        v.sort()
        if len(v) < 4: continue
        dT = {v[i + 1][0] - v[i][0] for i in range(len(v) - 1)}; dc = {(v[i + 1][1][0] - v[i][1][0], v[i + 1][1][1] - v[i][1][1]) for i in range(len(v) - 1)}
        if len(dT) != 1 or len(dc) != 1: continue
        s = dT.pop(); e = dc.pop(); P0, P1 = v[0][2], v[1][2]; dd = v[2][2] - P0
        if not all(v[i][2] == (P0 if i % 2 == 0 else P1) + dd * (i // 2) for i in range(len(v))): continue
        ext[k] = [(v[0][0] + s * i, (v[0][1][0] + e[0] * i, v[0][1][1] + e[1] * i), (P0 if i % 2 == 0 else P1) + dd * (i // 2)) for i in range(400)]
    return ext

def clock_sit(k, c):
    return build((0, (0, 0), 0), (k[0], k[1], k[2]), c, k[3])

def reference():
    a, c = parts_of(ap.W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    O_M = ap.orbit(*ap.local(A, G, (0, 1)))
    hist = []
    for t in range(600):
        hist.append(([tuple(q) for q in A], dict(G)))
        if t > 10 and ap.norm(*ap.local(A, G, (0, 1))) not in O_M: break
        step(A, G)
    ton = t; As, Gs = hist[ton]
    i_s = min(range(2, len(As)), key=lambda i: hd(As[i][0] - As[0][0], As[i][1] - As[0][1]))
    tr = ton - 160; As, Gs = hist[tr]
    sx, sy, sh = As[i_s]
    ship = (sh, frozenset((q[0] - sx, q[1] - sy) for q in Gs if hd(q[0] - sx, q[1] - sy) <= 2))
    pa, pc = ap.local([list(q) for q in As], dict(Gs), (0, 1))
    pix = ([(x - sx, y - sy, h) for x, y, h in pa], [(x - sx, y - sy) for x, y in pc])
    return ship, pix

def place(sit, P, ship, pix):
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    refs = []
    for k in range(6):
        refs.append(((ship[0] + k) % 6, frozenset(rot(q, k) for q in ship[1]), k))
    jobs = []; info = []
    for t in range(P):
        for i, (x, y, h) in enumerate(A):
            if min(hd(x - b[0], y - b[1]) for j, b in enumerate(A) if j != i) < 12: continue
            loc = frozenset((q[0] - x, q[1] - y) for q in G if hd(q[0] - x, q[1] - y) <= 2)
            for hh, cc, k in refs:
                if h != hh or loc != cc: continue
                Pa = [(*(lambda v: (v[0] + x, v[1] + y))(rot((px, py), k)), (ph + k) % 6) for px, py, ph in pix[0]]
                Pc = [(lambda v: (v[0] + x, v[1] + y))(rot(q, k)) for q in pix[1]]
                if min(hd(p[0] - b[0], p[1] - b[1]) for p in Pa for j, b in enumerate(A) if j != i) < 10: continue
                if any(q in G for q in Pc): continue
                jobs.append(fmt(Pa + [tuple(q) for q in A], list(G) + Pc)); info.append({'t': t, 'ship': i, 'k': k})
        step(A, G)
    return jobs, info

if __name__ == '__main__':
    lo, hi, npairs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ext = families(); allP = collections.defaultdict(list)
    for k, L in ext.items():
        for T, c, P in L: allP[P].append((k, T, c))
    pairs = [(p, 2 * p) for p in sorted(allP) if lo <= p <= hi and 2 * p in allP][:npairs]
    print('paires P/2P :', pairs, flush=True)
    ship, pix = reference(); print('référence vaisseau', ship, 'pixel', pix, flush=True)
    res = []
    for P1, P2 in pairs:
        ent = {}
        for P in (P1, P2):
            for k, T, c in allP[P][:3]:
                s = clock_sit(k, c)
                if not s: continue
                l = lot([s], P + 10)[0].split('|')
                if l[3] != 'CYCLE' or int(l[5]) != P: continue
                jobs, info = place(s, P, ship, pix)
                out = lot(jobs, P + 10) if jobs else []
                win = [dict(i, sit=j, P=P, fam=list(map(str, k)), T=T) for i, j, o in zip(info, jobs, out) if o.split('|')[3] == 'CYCLE' and int(o.split('|')[5]) == P]
                print(P, 'horloge', k, T, 'poses', len(jobs), 'CYCLE', len(win), flush=True)
                if win: ent[P] = win; break
        if len(ent) == 2: res.append({'P1': P1, 'P2': P2, 'm1': ent[P1][:40], 'm2': ent[P2][:40]}); json.dump(res, open('s2_horloge/compteur4_paires.json', 'w'))
    print('paires avec pixel sur les deux horloges :', len(res))

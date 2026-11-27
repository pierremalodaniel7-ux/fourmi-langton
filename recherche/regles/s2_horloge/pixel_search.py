"""S2 R-502 — PIXEL QUI CLIGNOTE : horloge triangle (tri.py) + UNE bascule « exacte » (le vaisseau qui écrit ressort non perturbé,
data/bascules_exactes.json) posée sur l'arête C0C1 : un vaisseau anti-horaire (dir 5) et un horaire (dir 2) la traversent à chaque tiers
de période ; l'un met l'objet R → R', l'autre R' → R. Critère : CYCLE exact (fourmi_r) de toute la machine.
Usage : python3 s2_horloge/pixel_search.py jmin jmax"""
import sys, json, re, itertools, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step, ship_dir
from fa_lib import parts_of, kship
from demi_add_k import fmt, lane
from tri import collide, adv, R as Rmap, at
from tri_test import build
from outils_r import lot
from exp_osc import hd
from anal import segs as segs_old
D = 40; TT = 720
def kv(s): return dict(re.findall(r'(\w+)=(\S+)', s))
def ctrunc(a, b): return int(a / b)
def rotsit(ants, cells, k):
    return [(*rot(a[:2], k), (a[2] + k) % 6) for a in ants], [rot(c, k) for c in cells]
def bascule_frame(f, k):
    """bascule f tournée de k crans : (R ants, R cells, info1, S1 (départ du vaisseau s1 tourné), r1), idem pour s2 et R'"""
    out = []
    for Rs, s in ((f['R'], f['s1']), (f['R2'], f['s2'])):
        a, c = parts_of(Rs); info = kv(s)
        oc = (ctrunc(sum(t[0] for t in a), len(a)), ctrunc(sum(t[1] for t in a), len(a)))
        r = int(info['r']); d = ship_dir(r); e = rot((1, 0), r)
        S = (oc[0] - D * d[0] + int(info['l']) * e[0], oc[1] - D * d[1] + int(info['l']) * e[1])
        A2, C2 = rotsit(a, c, k)
        out.append({'ants': A2, 'cells': C2, 'p': int(info['p']), 'ph': int(info['ph']), 'ord': int(info['ord']),
                    'r': (r + k) % 6, 'S': rot(S, k)})
    return out
def clock_virtuals(sit, P):
    """vaisseaux libres de l'horloge sur une période : liste (fourmi, virtuel, début, fin)"""
    from certif_tri import FREE
    from tri import virt
    a, cs = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in cs}
    cur = {}; res = []
    for t in range(P + 1):
        for k, (x, y, h) in enumerate(A):
            dmin = min(hd(x - b[0], y - b[1]) for l, b in enumerate(A) if l != k)
            v = virt((x, y, h), G, t)[0] if dmin > 6 else None
            if v is not None and not (dmin > 10 or (k in cur and cur[k][1] == v and cur[k][3] == t - 1)): v = None
            if v is not None and k in cur and cur[k][1] == v and cur[k][3] == t - 1: cur[k][3] = t
            elif v is not None: cur[k] = [k, v, t, t]; res.append(cur[k])
        if t < P: step(A, G)
    return res
def orbit_phase(ants, cells, Rants, Rcells, p):
    """phase ψ de l'état (ants, cells) dans l'orbite de R (positions absolues), ou None"""
    A = [list(t) for t in Rants]; G = {tuple(c): 1 for c in Rcells}
    tgt = (sorted(map(tuple, ants)), sorted(map(tuple, cells)))
    for ps in range(p):
        if (sorted(map(tuple, A)), sorted(G)) == tgt: return ps
        step(A, G)
    return None
if __name__ == '__main__':
    j0, j1 = int(sys.argv[1]), int(sys.argv[2])
    Bs = json.load(open('data/bascules_exactes.json'))
    good = json.load(open('s2_horloge/tri_cycles_rB5.json'))
    fam = {}
    for g in good:
        if 3 * g['T'] - g['P'] in (18, 36): fam.setdefault((tuple(g['B'][1]), g['B'][2], g['order']), []).append(g['T'])
    print('familles d\'horloges :', len(fam), ' bascules exactes :', len(Bs), flush=True)
    jobs = []; meta = []
    for (bpos, btau, order), Ts in fam.items():
        A = (0, (0, 0), 0); B = (5, bpos, btau)
        A2, B2 = collide(A, B, order)
        offc = lane(*A2[1], 2) - lane(*B[1], 2)
        import os
        BF = set(map(int, os.environ['BASC'].split(','))) if os.environ.get('BASC') else None
        for bi, f in enumerate(Bs):
            if BF is not None and bi not in BF: continue
            r1 = int(kv(f['s1'])['r'])
            for k in range(6):
                if (r1 + k) % 6 not in (2, 5): continue
                b1, b2 = bascule_frame(f, k)
                Sd2, Sd5 = (b1['S'], b2['S']) if b1['r'] == 2 else (b2['S'], b1['S'])
                if lane(*Sd2, 2) - lane(*Sd5, 2) != offc: continue
                # ordre : groupe B (dir 5) puis groupe A (dir 2) si order == 1, sinon l'inverse
                ordB = b1['ord'] if b1['r'] == 5 else b2['ord']; ordA = b1['ord'] if b1['r'] == 2 else b2['ord']
                first = 'B' if order == 1 else 'A'
                # position du pixel dans la liste : 0 (avant tout), 3 (entre les groupes), 6 (après)
                pos = None
                for cand in (0, 3, 6):
                    def ok(grp, o):   # o = 1 : vaisseau joué avant l'objet
                        idx = 0 if grp == first else 3
                        return (idx < cand) == (o == 1)
                    if ok('B', ordB) and ok('A', ordA): pos = cand
                if pos is None: continue
                for T in Ts:
                    j = (T - 133) // 8 if False else None
                for T in sorted(Ts):
                    pass
                for jj in range(j0, j1 + 1):
                    T = min(Ts) + 8 * jj
                    a2 = adv(A2, T)
                    q = rot(A[1], 2); c = (a2[1][0] - q[0], a2[1][1] - q[1])
                    if Rmap(adv(B2, T), c) != B: continue
                    sit = build(A, B, c, order)
                    if sit is None: continue
                    jobs.append(None); meta.append(((bpos, btau, order), T, c, sit, bi, k, b1, b2, pos))
    print('combinaisons (horloge, bascule, taille) :', len(meta), flush=True)
    # placements : temps t du départ « tir » du vaisseau s1 (tau 0, position S1 + o)
    jobs = []; info = []
    cache = {}
    for (fk, T, c, sit, bi, k, b1, b2, pos) in meta:
        P = 3 * T - (36 if ((T - 133) // 8) % 2 == 0 else 18)   # approximatif : on contrôle par CYCLE
        key = (fk, T)
        if key not in cache:
            # P réel de l'horloge seule
            l = lot([sit], 3 * T + 10)[0].split('|'); Pr = int(l[5]) if l[3] == 'CYCLE' else None
            cache[key] = (Pr, clock_virtuals(sit, Pr) if Pr else [])
        Pr, V = cache[key]
        if not Pr: continue
        for seg in V:
            kk, v, ts, te = seg
            if v[0] != b1['r'] or lane(*v[1], b1['r']) != lane(*b1['S'], b1['r']) + 0 and False: pass
            if v[0] != b1['r']: continue
            # le vaisseau v doit être sur la route s1 à une translation o près : on choisit t (tir) dans le segment
            for t in range(ts - 8 * D + 60, te - 8 * D - 60):
                av = adv(v, t)
                if av[2] != 0: continue
                pass
                o = (av[1][0] - b1['S'][0], av[1][1] - b1['S'][1])
                # le pixel (R tourné, translaté de o) à la phase (ph − t) mod p au temps 0
                Ra = [[x + o[0], y + o[1], h] for x, y, h in b1['ants']]; RG = {(x + o[0], y + o[1]): 1 for x, y in b1['cells']}
                for _ in range((b1['ph'] - t) % b1['p']): step(Ra, RG)
                a0, cs0 = parts_of(sit)
                if min(hd(a[0] - x[0], a[1] - x[1]) for a in a0 for x in Ra) < 20: continue
                ants = [tuple(x) for x in a0]; ants[pos:pos] = [tuple(x) for x in Ra]
                s = fmt(ants, list(cs0) + list(RG))
                jobs.append(s); info.append({'horloge': fk, 'T': T, 'P_horloge': Pr, 'bascule': bi, 'rot': k, 't_tir': t, 'o': o, 'pos': pos, 'sit': s})
    print('machines à tester :', len(jobs), flush=True)
    out = lot(jobs, max(i['P_horloge'] for i in info) + 10) if jobs else []   # période de la machine = période de l'horloge (constaté sur les 310 premières)
    cnt = collections.Counter(); win = []
    for i, l in zip(info, out):
        f = l.split('|'); cnt[f[3]] += 1
        if f[3] == 'CYCLE': i['P'] = int(f[5]); win.append(i)
    print(sorted(cnt.items()))
    json.dump(win, open('s2_horloge/pixel_cycles_%d_%d.json' % (j0, j1), 'w'))
    for w in sorted(win, key=lambda w: w['P'])[:10]: print(w['P'], w['P_horloge'], w['horloge'], w['T'], w['bascule'], w['rot'], w['t_tir'])

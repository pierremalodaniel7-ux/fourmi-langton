#!/usr/bin/env python3
"""R-620 (suite) descente INCRÉMENTALE pour l'arbre h1'' enchaîné (chain_h1.tree, 207 puissances).
Changer D ou G d'un nœud n ne déplace que les segments de n et de ses descendants : on ne recalcule que les couples (segments déplacés,
tous les segments), avec un pré-filtre numpy par boîtes espace-temps. Même définition des conflits que chain_h1.conflicts3 (contrôlée
au départ). Échelles : D ≤ DMAX (défaut 600), G ≤ 60.
Usage : python3 chain_h1b.py graine secondes [départ.json]"""
import sys, json, random, time, os
import numpy as np
from chain_h1 import R, names, PARENT, conflicts3, spec2
from modules import VARS, nodes
from nor import Layout
from diag2 import segments2
from diag import pmin
from s3lib import antpos
THR, GUARD = 7, 80
DMAX = int(os.environ.get('DMAX', 600)); SIM = int(os.environ.get('SIM', 6)); TFIX = int(os.environ.get('TFIX', 36000))
GMAX = int(os.environ.get('GMAX', 60)); MULT = int(os.environ.get('MULT', 0)); REALSIM = int(os.environ.get('REALSIM', 0)); REALOBJ = int(os.environ.get('REALOBJ', 0))
SUB = {}
for n in nodes(R): SUB[n.name] = {m.name for m in nodes(n)}
def build_state(Dm, Gm):
    L = Layout(R, Dmap=Dm, Gmap=Gm); T = max(TFIX, L.tmax + 1200)   # T fixe : l'incrémental reste exact
    own = {g[5]: g[0] for g in L.gates}; segs = []
    for s in segments2(L):
        a, b = max(s[2], 0), min(s[3], T)
        if a > b: continue
        p, q = antpos(s[1], a), antpos(s[1], b)
        o = s[0] if s[0] in SUB else own[s[0]]
        segs.append((s, a, b, o, min(p[0], q[0]) - THR - 4, max(p[0], q[0]) + THR + 4, min(p[1], q[1]) - THR - 4, max(p[1], q[1]) + THR + 4))
    box = np.array([[z[1], z[2], z[4], z[5], z[6], z[7]] for z in segs], dtype=np.int64)
    mask = [z[0][4] for z in segs]
    gt = {frozenset((g[0], g[5])): g[2] for g in L.gates}
    return L, T, segs, box, mask, gt
def pairs_for(idx, segs, box, mask, gt, only_lower=None):
    """conflits entre les segments idx et tous les autres (chaque couple compté une fois)"""
    out = []; idxset = set(idx)
    for i in idx:
        A = segs[i]
        cand = np.nonzero((box[:, 2] <= A[5]) & (box[:, 3] >= A[4]) & (box[:, 4] <= A[7]) & (box[:, 5] >= A[6]) & (box[:, 0] <= A[2]) & (box[:, 1] >= A[1]))[0]
        for j in cand:
            if j == i or (j in idxset and j < i): continue
            B = segs[j]; a, b = A[0], B[0]
            if a[0] == b[0] or not (mask[i] & mask[j]): continue
            m, t = pmin(a[1], A[1], A[2], b[1], B[1], B[2], THR)
            if m < THR:
                tg = gt.get(frozenset((a[0], b[0])))
                if tg is not None and abs(t - tg) <= GUARD: continue
                out.append((a[0], b[0], m, t, A[3], B[3], a[1], b[1]))
    return out
def full_conflicts(st):
    L, T, segs, box, mask, gt = st; return pairs_for(range(len(segs)), segs, box, mask, gt)
def incr(st_old, confl_old, st_new, moved):
    """conflits du nouvel état : ceux de l'ancien qui ne touchent pas « moved », plus les couples recalculés"""
    keep = [c for c in confl_old if c[4] not in moved and c[5] not in moved]
    L, T, segs, box, mask, gt = st_new
    idx = [i for i, z in enumerate(segs) if z[3] in moved]
    return keep + pairs_for(idx, segs, box, mask, gt)
if __name__ == '__main__':
    seed, secs = int(sys.argv[1]), float(sys.argv[2]); rnd = random.Random(seed)
    if len(sys.argv) > 3: p = json.load(open(sys.argv[3])); Dm, Gm = p['D'], p['G']
    else:
        h1p = json.load(open('h1_param_simple.json'))
        Dm = {n: rnd.randint(30, DMAX) for n in names}; Gm = {n: rnd.randint(8, 60) for n in names}
        for q in ('gN1h', 'gN2h', 'gP1h', 'gP2h'):
            for k in h1p['D']: Dm[q + k] = h1p['D'][k]; Gm[q + k] = h1p['G'][k]
    st = build_state(Dm, Gm); t0 = time.time(); cl = full_conflicts(st)
    if REALOBJ:
        from circ import real_pairs
        rr = real_pairs([(c[6], c[7], c[3]) for c in cl]); cl = [c for c, x in zip(cl, rr) if x]
    log = open(f'data/chainh1b_{seed}.log', 'a')
    ref = len(conflicts3(st[0], st[1]))
    print(f'départ {len(cl)} conflits (contrôle conflicts3 : {ref}), tmax {st[0].tmax}, {time.time()-t0:.0f}s', file=log, flush=True)
    it = 0; tested = set(); s = len(cl); last = time.time()
    while time.time() - t0 < secs:
        it += 1; D2, G2 = dict(Dm), dict(Gm); moved = set()
        if cl and rnd.random() < 0.85:
            c = rnd.choice(cl); n = rnd.choice(c[4:6])
            while n in PARENT and rnd.random() < 0.3: n = PARENT[n]
        else: n = rnd.choice(names)
        big = rnd.random() < 0.3
        if MULT:   # R-620 (27/11 T1) : pas proportionnels à la valeur (départ « arbre en H » à grandes longueurs, init_h1.py)
            if rnd.random() < 0.6: v = D2[n]; D2[n] = max(8, min(DMAX, v + rnd.randint(-1, 1) * rnd.randint(1, max(1, int(v * (0.3 if big else 0.04))))))
            else: v = G2[n]; G2[n] = max(8, min(GMAX, v + rnd.randint(-1, 1) * rnd.randint(1, max(1, int(v * (0.3 if big else 0.06))))))
        elif rnd.random() < 0.6: D2[n] = max(8, min(DMAX, D2[n] + (rnd.randint(-80, 80) if big else rnd.randint(-8, 8))))
        else: G2[n] = max(8, min(60, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
        moved = SUB[n]
        if n in PARENT and Dm[n] != D2[n]: pass   # D de n : n garde sa ligne d'univers, ses portes et ses descendants bougent
        st2 = build_state(D2, G2)
        if st2[1] != st[1]: cl2 = full_conflicts(st2)
        else: cl2 = incr(st, cl, st2, moved)
        if REALOBJ:   # objectif = conflits RÉELS seulement (couples simulés seuls, mémo par géométrie)
            from circ import real_pairs
            rr = real_pairs([(c[6], c[7], c[3]) for c in cl2]); cl2 = [c for c, x in zip(cl2, rr) if x]
        if len(cl2) <= s:
            if len(cl2) < s: print(f'{it} {time.time()-t0:.0f}s conflits {len(cl2)}', file=log, flush=True)
            Dm, Gm, st, cl, s = D2, G2, st2, cl2, len(cl2)
            json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1b_{seed}.json', 'w'))
            if REALSIM and s <= REALSIM:   # R-620 (T1) : conflits réels (couples simulés seuls) ; 0 réel -> simulation complète
                from circ import real_pairs
                nr = sum(real_pairs([(c[6], c[7], c[3]) for c in cl]))
                print(f'   {s} conflits du modèle, {nr} réels', file=log, flush=True)
                if nr == 0:
                    key = json.dumps([Dm, Gm], sort_keys=True)
                    if key not in tested:
                        tested.add(key); json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1b_{seed}_r0.json', 'w'))
                        r = st[0].check(); z = {v: 0 for v in VARS}
                        bad = sum(1 for e, c_, got, val, _ in r if got != spec2('h1', {**z, **e})); dirty = sum(1 for x in r if not x[1])
                        print(f'   simulation : {bad} faux, {dirty} sales / {len(r)} (tmax {st[0].tmax})', file=log, flush=True)
                        if bad == 0 and dirty == 0:
                            json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1b_OK_{seed}.json', 'w')); break
                continue
            if s <= SIM:
                chk = len(conflicts3(st[0], st[1])) if not REALOBJ else s
                if chk != s: print(f'   contrôle : incrémental {s} ≠ complet {chk} -> recalcul', file=log, flush=True); cl = full_conflicts(st); s = len(cl); continue
                key = json.dumps([Dm, Gm], sort_keys=True)
                if key in tested: continue
                tested.add(key); r = st[0].check(); z = {v: 0 for v in VARS}
                bad = sum(1 for e, c_, got, val, _ in r if got != spec2('h1', {**z, **e})); dirty = sum(1 for x in r if not x[1])
                print(f'   simulation : {bad} faux, {dirty} sales / {len(r)} (tmax {st[0].tmax})', file=log, flush=True)
                if bad == 0 and dirty == 0:
                    json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/chainh1b_OK_{seed}.json', 'w')); break
    print('fin', it, 'itérations', s, f'{time.time()-t0:.0f}s', file=log, flush=True)

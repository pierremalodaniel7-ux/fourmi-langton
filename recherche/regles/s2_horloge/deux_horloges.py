"""S2 R-508 — DEUX HORLOGES QUI SE CROISENT (objectif 3, version « porte = choc de 2 vaisseaux »).
Horloge A = terme j1 de R-500 (formule.py) ; horloge B = terme j2 tourné de k crans, translaté de v, avancé de s pas.
On tire au hasard une rencontre (instant t, fourmi de A, fourmi de B, petit écart w) : v est choisi pour que les deux fourmis soient
à l'écart w à l'instant t. Pré-filtre (trajectoires seules, entiers) : les deux horloges se voient (distance ≤ 6) mais ne se recouvrent pas.
Critère : CYCLE exact de TOUTE la machine (12 fourmis) dans fourmi_r, puis interaction réelle (trajectoire jointe ≠ superposition, hx.py).
Usage : python3 s2_horloge/deux_horloges.py j1 j2 N graine   (écrit s2_horloge/deux_<j1>_<j2>_<graine>.json)"""
import sys, json, random
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import rot, step
from fa_lib import parts_of
from formule import horloge, periode
from outils_r import lot
from math import gcd

def traj(sit, T):
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    X = np.zeros((T, len(A), 2), dtype=np.int64)
    for t in range(T):
        X[t] = [(q[0], q[1]) for q in A]; step(A, G)
    return X

def hexd(d): return (np.abs(d[..., 0]) + np.abs(d[..., 1]) + np.abs(d[..., 0] + d[..., 1])) // 2

def rotarr(X, k):
    x, y = X[..., 0].copy(), X[..., 1].copy()
    for _ in range(k % 6): x, y = -y, x + y
    return np.stack([x, y], -1)

def machine(j2, k, v, s):
    a, c = parts_of(horloge(j2)); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    for _ in range(s): step(A, G)
    A2 = [(*(np.add(rot((x, y), k), v)), (h + k) % 6) for x, y, h in A]
    C2 = [tuple(np.add(rot(p, k), v)) for p in G]
    return [tuple(int(z) for z in q) for q in A2], [tuple(int(z) for z in p) for p in C2]

if __name__ == '__main__':
    j1, j2, N, seed = map(int, sys.argv[1:5]); random.seed(seed)
    P1, P2 = periode(j1), periode(j2); L = P1 * P2 // gcd(P1, P2)
    XA = traj(horloge(j1), L); XB0 = traj(horloge(j2), 2 * P2)   # B seule sur 2 périodes (indices t+s mod P2)
    aA, cA = parts_of(horloge(j1))
    cand = []; tries = 0
    while len(cand) < N and tries < 40 * N:
        tries += 1
        k = random.randrange(6); s = random.randrange(P2); t = random.randrange(L)
        ia, ib = random.randrange(6), random.randrange(6)
        w = (random.randint(-3, 3), random.randint(-3, 3))
        XB = rotarr(XB0[(np.arange(L) + s) % P2], k)
        v = tuple(XA[t, ia] - XB[t, ib] + np.array(w))
        D = hexd(XA[:, :, None, :] - (XB + np.array(v))[:, None, :, :])   # L x 6 x 6
        m = D.min(axis=(1, 2))
        if m.min() > 3 or m.min() < 1: continue
        if (m <= 6).sum() > L // 4: continue          # recouvrement trop fort : on veut une rencontre, pas une fusion
        a2, c2 = machine(j2, k, v, s)
        sit = 'H:R2L2|' + ';'.join('%d,%d,%d' % q for q in list(aA) + a2) + '|' + ';'.join('%d,%d' % p for p in list(cA) + c2)
        cand.append({'k': k, 's': s, 'v': [int(v[0]), int(v[1])], 'dmin': int(m.min()), 'tvoit': int((m <= 6).sum()), 'sit': sit})
    out = lot([c['sit'] for c in cand], 4 * L + 10)
    hits = []
    for c, l in zip(cand, out):
        f = l.split('|')
        if f[3] == 'CYCLE':
            c['P'] = int(f[5]); X = traj(c['sit'], L)
            XB = rotarr(XB0[(np.arange(L) + c['s']) % P2], c['k']) + np.array(c['v'])
            c['diff'] = int((X != np.concatenate([XA, XB], 1)).any(-1).any(-1).sum())
            if c['diff']: hits.append(c)
    print('issues :', __import__('collections').Counter(l.split('|')[3] for l in out))
    print('j1', j1, 'j2', j2, 'P', P1, P2, 'machines', len(cand), 'CYCLE', len(hits), flush=True)
    json.dump(hits, open('s2_horloge/deux_%d_%d_%d.json' % (j1, j2, seed), 'w'))

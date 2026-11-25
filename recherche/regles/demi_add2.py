#!/usr/bin/env python3
"""R-325 Demi-additionneur R2L2 sans case fixe, version 2 : porte d'interaction (A, B) ; U = « A seule » (a∧¬b), V = « B seule » (¬a∧b).
Deux vaisseaux CONSTANTS K1 (sur V) et K2 (sur U) les tournent vers la même 3e direction d3, et on cale les voies (la voie de sortie
d'un virage avance d'une voie par période de décalage du point de virage). S = a⊕b sur la voie (d3, λ) ; C = a∧b = A déviée."""
import json, subprocess, itertools, sys
from banc import launcher, sit, outcome, rotv
from outils_r import lot, parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
gate = sys.argv[1] if len(sys.argv) > 1 else 'H:R2L2|0,0,4;29,-56,0|1,0,1;28,-55,1'
a_, c_ = gate.split('|')[1:]
ants = [tuple(map(int, t.split(','))) for t in a_.split(';')]
B = (ants[0], {(1, 0): 1}); A = (ants[1], {tuple(map(int, t.split(',')[:2])): 1 for t in c_.split(';') if t and t.split(',')[:2] != ['1', '0']})
def tracks(l, n):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'][:n])]
def pos(src, n):
    out = subprocess.run(['./fourmi_r', '-T', str(n * P), '-x', '-dump', '-lot'], input=sit(R, [src[0]], src[1]) + '\n', capture_output=True, text=True).stdout
    return tuple(map(int, [l for l in out.splitlines() if l.startswith('DUMP')][0].split('|')[1].split(',')[:2]))
dU = tracks(lot([sit(R, [A[0]], A[1])], 1 << 16)[0], 1)[0][0]; dV = tracks(lot([sit(R, [B[0]], B[1])], 1 << 16)[0], 1)[0][0]
dirs = [rotv(R, D, r) for r in range(6)]
iU, iV = dirs.index(dU), dirs.index(dV)
d3 = [dirs[k] for k in range(6) if k not in (iU, iV) and (k - iU) % 6 in (2, 4) and (k - iV) % 6 in (2, 4)][0]
print('U', dU, 'V', dV, 'd3', d3)
def kpos(src, dsrc, r, n, m, i, j):
    Y = pos(src, n); DK = rotv(R, D, r)
    return (Y[0] + m * dsrc[0] - (n + m) * DK[0] + i, Y[1] + m * dsrc[1] - (n + m) * DK[1] + j)
def fam(src, dsrc):
    """familles (r,i,j) qui tournent src vers d3 proprement ; voie de sortie en n = 60 et 61"""
    F = []
    for r in range(6):
        DK = rotv(R, D, r)
        if DK in (dsrc, (-dsrc[0], -dsrc[1])): continue
        L = []; meta = []
        for n in (60, 61):
            for i in range(-3, 4):
                for j in range(-3, 4):
                    K = launcher(G, r, kpos(src, dsrc, r, n, 20, i, j)); L.append(sit(R, [src[0], K[0]], {**src[1], **K[1]})); meta.append((n, i, j))
        out = dict(zip(meta, lot(L, 1 << 17)))
        for i in range(-3, 4):
            for j in range(-3, 4):
                t0, t1 = tracks(out[(60, i, j)], 2), tracks(out[(61, i, j)], 2)
                if t0[0] and t1[0] and t0[1] and t1[1] and t0[0][0] == d3 and t1[0][0] == d3:
                    F.append((r, i, j, t0[0][1], t1[0][1] - t0[0][1]))
    return F
FV = fam(B, dV); FU = fam(A, dU)
print('familles V :', len(FV), ' familles U :', len(FU), flush=True)
print('V', sorted(set((f[3], f[4]) for f in FV))[:12]); print('U', sorted(set((f[3], f[4]) for f in FU))[:12])
found = []
for (r1, i1, j1, l1, s1), (r2, i2, j2, l2, s2) in itertools.product(FV, FU):
    if s1 == 0 or s2 == 0: continue
    for n1 in range(35, 140):
        lam = l1 + s1 * (n1 - 60)
        if (lam - l2) % s2: continue
        n2 = 60 + (lam - l2) // s2
        if not 35 <= n2 <= 140: continue
        K1 = launcher(G, r1, kpos(B, dV, r1, n1, 20, i1, j1)); K2 = launcher(G, r2, kpos(A, dU, r2, n2, 20, i2, j2))
        L = []
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            al = []; ce = {}
            for on, (x, cc) in ((b, B), (a, A), (1, K1), (1, K2)):
                if on: al.append(x); ce.update(cc)
            L.append(sit(R, al, ce))
        tr = [tracks(l, 4) for l in lot(L, 1 << 18)]
        if any(t is None for x in tr for t in x): continue
        onS = [sum(1 for t in x if t == (d3, lam)) for x in tr]
        if onS == [0, 1, 1, 0]:
            found.append({'porte': gate, 'K1': [r1, list(kpos(B, dV, r1, n1, 20, i1, j1))], 'K2': [r2, list(kpos(A, dU, r2, n2, 20, i2, j2))],
                          'S': [list(d3), lam], 'sorties': [[list(map(list, [t[0]])) + [t[1]] for t in x] for x in tr], 'situations': L})
            print('TROUVÉ', found[-1]['K1'], found[-1]['K2'], 'S =', d3, lam, flush=True)
            if len(found) >= 10: break
    if len(found) >= 10: break
json.dump(found, open('data/demi_add2.json', 'w'))
print('total', len(found))

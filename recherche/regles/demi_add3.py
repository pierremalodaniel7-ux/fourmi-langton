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
d3_ = [dirs[k] for k in range(6) if k not in (iU, iV) and (k - iU) % 6 in (2, 4) and (k - iV) % 6 in (2, 4)][0]

def kpos(src, dsrc, r, n, m, i, j):
    Y = pos(src, n); DK = rotv(R, D, r)
    return (Y[0] + m * dsrc[0] - (n + m) * DK[0] + i, Y[1] + m * dsrc[1] - (n + m) * DK[1] + j)
def fam(src, dsrc, TGT):
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
                if t0[0] and t1[0] and t0[1] and t1[1] and t0[0][0] == TGT and t1[0][0] == TGT:
                    F.append((r, i, j, t0[0][1], t1[0][1] - t0[0][1]))
    return F

for mode in ('U->V', 'V->U'):
    src, dsrc, other, dother = (A, dU, B, dV) if mode == 'U->V' else (B, dV, A, dU)
    lam = tracks(lot([sit(R, [other[0]], other[1])], 1 << 16)[0], 1)[0][1]
    F = fam(src, dsrc, dother)
    print(mode, 'familles', len(F), 'voie cible', lam, 'voies en n=60 :', sorted(set((f[3], f[4]) for f in F))[:6], flush=True)
    found = []
    for (r, i, j, l0, s0) in F:
        if s0 == 0 or (lam - l0) % s0: continue
        n = 60 + (lam - l0) // s0
        if not 33 <= n <= 400: continue
        K = launcher(G, r, kpos(src, dsrc, r, n, 20, i, j))
        L = []
        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
            al = []; ce = {}
            for on, (x, cc) in ((b, B), (a, A), (1, K)):
                if on: al.append(x); ce.update(cc)
            L.append(sit(R, al, ce))
        tr = [tracks(l, 3) for l in lot(L, 1 << 18)]
        if any(t is None for x in tr for t in x): continue
        onS = [sum(1 for t in x if t == (dother, lam)) for x in tr]
        print('  essai', r, i, j, 'n', n, onS, flush=True)
        if onS == [0, 1, 1, 0]:
            found.append({'mode': mode, 'porte': gate, 'K': [r, list(kpos(src, dsrc, r, n, 20, i, j))], 'S': [list(dother), lam], 'situations': L})
    print(mode, 'TROUVÉS', len(found))
    json.dump(found, open(f"data/demi_add3_{mode.replace('->','_')}.json", 'w'))

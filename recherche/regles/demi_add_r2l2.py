#!/usr/bin/env python3
"""R-325 Demi-additionneur R2L2 sans case fixe : porte d'interaction (A, B) + 1 vaisseau CONSTANT K qui renvoie la sortie
« B seule » (¬a∧b) sur la voie de « A seule » (a∧¬b) ⇒ S = a⊕b sur UNE voie ; C = a∧b = A déviée. Recherche de K, puis test.
Usage : demi_add_r2l2.py [nb_portes]"""
import json, sys, subprocess
from banc import launcher, sit, outcome, rotv
from outils_r import lot, parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
EX = json.load(open('data/porte_reuse_H_R2L2_k100.json'))['exemples']
NG = int(sys.argv[1]) if len(sys.argv) > 1 else 5
def ps(s):
    r, a, c = s.split('|')
    return [tuple(map(int, t.split(','))) for t in a.split(';')], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
def state(s, T):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input=s + '\n', capture_output=True, text=True).stdout.splitlines()
    return [tuple(map(int, t.split(','))) for t in [l for l in out if l.startswith('DUMP')][0].split('|')[1].split(';')]
def tracks(l, n):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'][:n])]
found = []
for gate in EX[:NG]:
    ants, cells = ps(gate)
    B = (ants[0], {(1, 0): 1}); A = (ants[1], {c: 1 for c in cells if c != (1, 0)})
    sA = tracks(lot([sit(R, [A[0]], A[1])], 1 << 16)[0], 1)[0]           # voie de « A seule »
    sB = tracks(lot([sit(R, [B[0]], B[1])], 1 << 16)[0], 1)[0]
    lc = lot([sit(R, [B[0], A[0]], {**B[1], **A[1]})], 1 << 16)[0]; cB, cA = tracks(lc, 2)  # sorties a∧b
    cands = []
    for n in [60]:
        Y = state(sit(R, [B[0]], B[1]), n * P)[0][:2]
        for r in range(6):
            DK = rotv(R, D, r)
            if DK in (D, (-D[0], -D[1])): continue
            for m in (20, 40):
                L = []; meta = []
                for i in range(-3, 4):
                    for j in range(-3, 4):
                        st = (Y[0] + m * D[0] - (n + m) * DK[0] + i, Y[1] + m * D[1] - (n + m) * DK[1] + j)
                        K = launcher(G, r, st); L.append(sit(R, [B[0], K[0]], {**B[1], **K[1]})); meta.append((r, m, i, j))
                for l, mt in zip(lot(L, 1 << 17, ncpu=2), meta):
                    t = tracks(l, 2)
                    if t[0] and t[1] and t[0][0] == sA[0]: cands.append(mt)
    print(gate, 'candidats K (V tourné vers la direction de U) :', len(cands), flush=True)
    for (r0, m0, i0, j0) in cands:
      for n in range(30, 200):
        Y = state(sit(R, [B[0]], B[1]), n * P)[0][:2]
        for r in [r0]:
            DK = rotv(R, D, r)
            if DK in (D, (-D[0], -D[1])): continue
            for m in [m0]:
                for i in [i0]:
                    for j in [j0]:
                        st = (Y[0] + m * D[0] - (n + m) * DK[0] + i, Y[1] + m * D[1] - (n + m) * DK[1] + j)
                        K = launcher(G, r, st)
                        L = []
                        for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
                            al = []; ce = {}
                            for on, (x, cc) in ((b, B), (a, A), (1, K)):
                                if on: al.append(x); ce.update(cc)
                            L.append(sit(R, al, ce))
                        res = lot(L, 1 << 17, ncpu=2)
                        tr = [tracks(l, 3) for l in res]
                        if any(t is None for x in tr for t in x): continue
                        on_S = [sum(1 for t in x if t == sA) for x in tr]
                        on_C = sum(1 for t in tr[3] if t == cA)
                        if on_S == [0, 1, 1, 0] and on_C == 1:
                            found.append({'porte': gate, 'K': [r, list(st)], 'S': sA, 'C': cA}); print('trouvé', gate, r, st, flush=True)
    print(gate, 'cumul', len(found), flush=True)
json.dump(found, open('data/demi_add_r2l2.json', 'w'))

#!/usr/bin/env python3
"""R-325 (tous les K2) Demi-additionneur R2L2 sans case fixe (version zigzag) : porte d'interaction (B, A) ; U = « A seule » (a∧¬b) est tournée
2 fois par 2 vaisseaux constants K2 (U → d3) puis K3 (d3 → direction de V), et la voie finale est calée sur celle de V = « B seule »
(¬a∧b) ⇒ S = a⊕b sur UNE voie. C = a∧b = A déviée par B. Usage : demi_add4.py"""
import json, subprocess
from banc import launcher, sit, rotv
from outils_r import lot, parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1)
gate = 'H:R2L2|0,0,4;29,-56,0|1,0,1;28,-55,1'
B = ((0, 0, 4), {(1, 0): 1}); A = ((29, -56, 0), {(28, -55): 1})
dirs = [rotv(R, D, r) for r in range(6)]
def tracks(l, n):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'][:n])]
def pos0(ants, cells, n):
    out = subprocess.run(['./fourmi_r', '-T', str(n * P), '-x', '-dump', '-lot'], input=sit(R, ants, cells) + '\n', capture_output=True, text=True).stdout
    return tuple(map(int, [l for l in out.splitlines() if l.startswith('DUMP')][0].split('|')[1].split(';')[0].split(',')[:2]))
def kp(Y, dsrc, r, n, m, i, j):
    DK = dirs[r]; return (Y[0] + m * dsrc[0] - (n + m) * DK[0] + i, Y[1] + m * dsrc[1] - (n + m) * DK[1] + j)
dU = tracks(lot([sit(R, [A[0]], A[1])], 1 << 16)[0], 1)[0][0]; tV = tracks(lot([sit(R, [B[0]], B[1])], 1 << 16)[0], 1)[0]; dV, lamV = tV
iU, iV = dirs.index(dU), dirs.index(dV)
d3 = [dirs[k] for k in range(6) if k not in (iU, iV) and (k - iU) % 6 in (2, 4) and (k - iV) % 6 in (2, 4)][0]
print('U', dU, 'V', dV, 'voie V', lamV, 'd3', d3, flush=True)
# 1er virage : K2 tourne U vers d3 au point n2 = 60 (familles propres)
n2 = 60; Y2 = pos0([A[0]], A[1], n2); F2 = []
L = []; meta = []
for r in range(6):
    if dirs[r] in (dU, (-dU[0], -dU[1])): continue
    for i in range(-3, 4):
        for j in range(-3, 4):
            K = launcher(G, r, kp(Y2, dU, r, n2, 20, i, j)); L.append(sit(R, [A[0], K[0]], {**A[1], **K[1]})); meta.append((r, i, j, K))
for l, mt in zip(lot(L, 1 << 17), meta):
    t = tracks(l, 2)
    if t[0] and t[1] and t[0][0] == d3: F2.append(mt)
print('K2 possibles :', len(F2), flush=True)
found = []
for (r2, i2, j2, K2) in F2:
    ants2 = [A[0], K2[0]]; cells2 = {**A[1], **K2[1]}
    # 2e virage : K3 tourne la fourmi (maintenant en d3) vers dV ; voie en fonction du point n3
    for r3 in range(6):
        if dirs[r3] in (d3, (-d3[0], -d3[1])): continue
        for i in range(-2, 3):
            for j in range(-2, 3):
                lanes = {}
                for n3 in (n2 + 40, n2 + 41):
                    Y3 = pos0(ants2, cells2, n3)
                    K3 = launcher(G, r3, kp(Y3, d3, r3, n3, 20, i, j))
                    t = tracks(lot([sit(R, ants2 + [K3[0]], {**cells2, **K3[1]})], 1 << 18, ncpu=1)[0], 3)
                    if t[0] and t[1] and t[2] and t[0][0] == dV: lanes[n3] = t[0][1]
                if len(lanes) < 2: continue
                s = lanes[n2 + 41] - lanes[n2 + 40]
                if s == 0 or (lamV - lanes[n2 + 40]) % s: continue
                n3 = n2 + 40 + (lamV - lanes[n2 + 40]) // s
                if not n2 + 15 <= n3 <= n2 + 400: continue
                Y3 = pos0(ants2, cells2, n3); K3 = launcher(G, r3, kp(Y3, d3, r3, n3, 20, i, j))
                Lt = []
                for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    al = []; ce = {}
                    for on, (x, cc) in ((b, B), (a, A), (1, K2), (1, K3)):
                        if on: al.append(x); ce.update(cc)
                    Lt.append(sit(R, al, ce))
                tr = [tracks(l, 4) for l in lot(Lt, 1 << 19)]
                if any(t is None for x in tr for t in x): continue
                onS = [sum(1 for t in x if t == (dV, lamV)) for x in tr]
                print('  essai K2', (r2, i2, j2), 'K3', (r3, i, j), 'n3', n3, 'S sur la voie :', onS, flush=True)
                if onS == [0, 1, 1, 0]:
                    found.append({'porte': gate, 'K2': [K2[0], sorted(K2[1])], 'K3': [K3[0], sorted(K3[1])], 'S': [list(dV), lamV],
                                  'situations': Lt, 'sorties': [[[list(t[0]), t[1]] for t in x] for x in tr]})
                    json.dump(found, open('data/demi_add5.json', 'w'), default=list)
                    print('TROUVÉ', len(found), flush=True)
print('total', len(found))

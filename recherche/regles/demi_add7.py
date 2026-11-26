#!/usr/bin/env python3
"""R-329 (virages sans débris) R-327 Demi-additionneur R2L2 RÉUTILISABLE : porte d'interaction SANS DÉBRIS (data/portes_propres.json) + zigzag (K2, K3) de R-325,
puis test de réutilisation (16 suites de 2 usages) ; on garde ceux qui font 16/16. Usage : demi_add6.py [nb_portes] [max_par_porte]"""
import json, subprocess, itertools, sys
from banc import launcher, sit, rotv
from outils_r import lot, parse
R = 'H:R2L2'; G = json.load(open('data/germes_regles.json'))[R]; P, D = 8, (1, -1); k = 200
NG = int(sys.argv[1]) if len(sys.argv) > 1 else 10; MX = int(sys.argv[2]) if len(sys.argv) > 2 else 40
dirs = [rotv(R, D, r) for r in range(6)]
def tracks(l):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'])]
def pos0(ants, cells, n):
    out = subprocess.run(['./fourmi_r', '-T', str(n * P), '-x', '-dump', '-lot'], input=sit(R, ants, cells) + '\n', capture_output=True, text=True).stdout
    return tuple(map(int, [l for l in out.splitlines() if l.startswith('DUMP')][0].split('|')[1].split(';')[0].split(',')[:2]))
def kp(Y, dsrc, r, n, m, i, j):
    DK = dirs[r]; return (Y[0] + m * dsrc[0] - (n + m) * DK[0] + i, Y[1] + m * dsrc[1] - (n + m) * DK[1] + j)
def debris(ants, cells, T=3000):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input=sit(R, ants, cells) + '\n', capture_output=True, text=True).stdout.splitlines()
    l = [x for x in out if not x.startswith('DUMP')][0]; dmp = [x for x in out if x.startswith('DUMP')][0]
    fins = parse(l)['fin']
    cs = [tuple(map(int, c.split(',')[:2])) for c in dmp.split('|')[2].split(';') if c]
    return sum(1 for c in cs if all(abs(c[0] - f[0]) + abs(c[1] - f[1]) > 6 for f in fins))
def one_dir(src): return tracks(lot([sit(R, [src[0]], src[1])], 1 << 16)[0])[0]
good_all = []
for gate in json.load(open('data/portes_propres.json'))[:NG]:
    a_, c_ = gate.split('|')[1:]
    an = [tuple(map(int, t.split(','))) for t in a_.split(';')]
    cl = [tuple(map(int, t.split(',')[:2])) for t in c_.split(';') if t]
    B = (an[0], {(1, 0): 1}); A = (an[1], {c: 1 for c in cl if c != (1, 0)})
    dU = one_dir(A)[0]; dV, lamV = one_dir(B)
    Ctrack = tracks(lot([sit(R, [B[0], A[0]], {**B[1], **A[1]})], 1 << 16)[0])[1]
    iU, iV = dirs.index(dU), dirs.index(dV)
    c3 = [dirs[q] for q in range(6) if q not in (iU, iV) and (q - iU) % 6 in (2, 4) and (q - iV) % 6 in (2, 4)]
    if not c3: print(gate, 'pas de 3e direction'); continue
    d3 = c3[0]; n2 = 60; Y2 = pos0([A[0]], A[1], n2)
    L = []; meta = []
    for r in range(6):
        if dirs[r] in (dU, (-dU[0], -dU[1])): continue
        for i in range(-3, 4):
            for j in range(-3, 4):
                K2 = launcher(G, r, kp(Y2, dU, r, n2, 20, i, j)); L.append(sit(R, [A[0], K2[0]], {**A[1], **K2[1]})); meta.append(K2)
    F2 = [K2 for l, K2 in zip(lot(L, 1 << 17), meta) if (lambda t: t[0] and t[1] and t[0][0] == d3)(tracks(l))]
    F2 = [K2 for K2 in F2 if debris([A[0], K2[0]], {**A[1], **K2[1]}) == 0]
    found = []
    for K2 in F2:
        ants2 = [A[0], K2[0]]; cells2 = {**A[1], **K2[1]}
        for r3 in range(6):
            if dirs[r3] in (d3, (-d3[0], -d3[1])): continue
            for i in range(-2, 3):
                for j in range(-2, 3):
                    lanes = {}
                    for n3 in (n2 + 40, n2 + 41):
                        Y3 = pos0(ants2, cells2, n3); K3 = launcher(G, r3, kp(Y3, d3, r3, n3, 20, i, j))
                        t = tracks(lot([sit(R, ants2 + [K3[0]], {**cells2, **K3[1]})], 1 << 18, ncpu=1)[0])
                        if all(t) and t[0][0] == dV: lanes[n3] = t[0][1]
                    if len(lanes) < 2: continue
                    s = lanes[n2 + 41] - lanes[n2 + 40]
                    if s == 0 or (lamV - lanes[n2 + 40]) % s: continue
                    n3 = n2 + 40 + (lamV - lanes[n2 + 40]) // s
                    if not n2 + 15 <= n3 <= n2 + 400: continue
                    Y3 = pos0(ants2, cells2, n3); K3 = launcher(G, r3, kp(Y3, d3, r3, n3, 20, i, j))
                    if debris(ants2 + [K3[0]], {**cells2, **K3[1]}, 6000) == 0: found.append((K2, K3))
            if len(found) >= MX: break
        if len(found) >= MX: break
    # test : table puis 16 suites de 2 usages
    srcs = {'B': B, 'A': A}
    def build(K2, K3, uses):
        S = dict(srcs); S['K2'] = K2; S['K3'] = K3; al = []; ce = {}
        for u, (a, b) in enumerate(uses):
            for nme, on in (('B', b), ('A', a), ('K2', 1), ('K3', 1)):
                if not on: continue
                x, cc = S[nme]; dd = one_dir(S[nme])[0]; v = (-u * k * dd[0], -u * k * dd[1])
                al.append((x[0] + v[0], x[1] + v[1], x[2])); [ce.__setitem__((c[0] + v[0], c[1] + v[1]), 1) for c in cc]
        return sit(R, al, ce)
    def SC(l):
        t = tracks(l)
        return None if any(x is None for x in t) else (sum(1 for x in t if x == (dV, lamV)), sum(1 for x in t if x == Ctrack))
    AB = ((0, 0), (1, 0), (0, 1), (1, 1)); ok_gate = 0; table_ok = 0
    for K2, K3 in found:
        one = dict(zip(AB, [SC(l) for l in lot([build(K2, K3, [ab]) for ab in AB], 1 << 19)]))
        if one != {(0, 0): (0, 0), (1, 0): (1, 0), (0, 1): (1, 0), (1, 1): (0, 1)}: continue
        table_ok += 1
        seqs = list(itertools.product(AB, repeat=2))
        res = [SC(l) for l in lot([build(K2, K3, list(s)) for s in seqs], 1 << 20)]
        good = sum(1 for s, t in zip(seqs, res) if t == tuple(x + y for x, y in zip(one[s[0]], one[s[1]])))
        if good == 16:
            ok_gate += 1
            good_all.append({'porte': gate, 'K2': [list(K2[0]), sorted(K2[1])], 'K3': [list(K3[0]), sorted(K3[1])], 'S': [list(dV), lamV], 'C': [list(Ctrack[0]), Ctrack[1]]})
            json.dump(good_all, open('data/demi_add_reutilisables7.json', 'w'))
    print(f"{gate} : zigzags {len(found)}, table juste {table_ok}, réutilisables 16/16 {ok_gate}", flush=True)
print('TOTAL réutilisables', len(good_all))

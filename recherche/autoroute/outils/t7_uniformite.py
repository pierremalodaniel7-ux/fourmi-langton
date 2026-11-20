#!/usr/bin/env python3
"""t7_uniformite.py [N] [graine] : test d'additivité du pas certifié en (k1, m, m3) sur N triplets T7 « NS0 + sans demi-tour » (R-126).
Lit data/t7/{triples,rec_k1,rec_m,directions}.txt. (S10)"""
import random, subprocess, re, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
F = 'src/fourmi'
T = [l.split() for l in open('data/t7/triples.txt') if not l.startswith('#')]
k1 = [l.split() for l in open('data/t7/rec_k1.txt')]; m = [l.split() for l in open('data/t7/rec_m.txt')]
D = [l.split() for l in open('data/t7/directions.txt')]
cand = [i for i in range(len(T)) if k1[i][-1] == 'NS0' and m[i][-3] == 'OK[0]' and 'X' not in D[i][2]]
S = random.sample(cand, min(N, len(cand))); cfg = []
for i in S:
    c = [tuple(map(int, p.split(','))) for p in T[i][1].split(';')]; d = (-2, 2)
    d2, d3 = [(int(a), int(b)) for a, b in re.findall(r'\((-?\d+), (-?\d+)\)', ' '.join(D[i][3:]))][:2]
    for a, b, cc in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (7, 5, 6)]:
        c1 = (c[0][0] + a*d[0], c[0][1] + a*d[1]); c2 = (c[1][0] + a*d[0] + b*d2[0], c[1][1] + a*d[1] + b*d2[1])
        c3 = (c[2][0] + a*d[0] + b*d2[0] + cc*d3[0], c[2][1] + a*d[1] + b*d2[1] + cc*d3[1])
        cfg.append(f'RL|0,0,H|{c1[0]},{c1[1]};{c2[0]},{c2[1]};{c3[0]},{c3[1]}\n')
o = subprocess.run([F, '-T', '400000000', '-cert', '-lot'], input=''.join(cfg), capture_output=True, text=True).stdout.splitlines()
ok = 0
for j, i in enumerate(S):
    v = [int(re.search(r'CERT (\d+)', l).group(1)) for l in o[5*j:5*j+5]]
    ok += v[0] + 7*(v[1]-v[0]) + 5*(v[2]-v[0]) + 6*(v[3]-v[0]) == v[4]
print(f'candidats {len(cand)} ; prédictions exactes {ok}/{len(S)}')

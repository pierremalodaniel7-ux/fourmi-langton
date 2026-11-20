#!/usr/bin/env python3
"""t7_triples.py : à partir des bases T7 finies (data/t7/b_<n>.txt), liste des triplets (c1 ; c2 ; c3) dans le repère d'origine
(fourmi 0,0,H), un par (base, classe de c3) ; contrôle : `fourmi -cert` sur le triplet redonne le pas certifié de relatif.py.
Sortie (stdout) : "n c1x,c1y;c2x,c2y;c3x,c3y CE NS [p…]". (S10)"""
import os, re, subprocess
here = os.path.dirname(os.path.abspath(__file__)); R = here + '/../../..'
F = R + '/src/fourmi'
bases = [l.split() for l in open(R + '/resultats/relatif/t7_bases.txt')]
def unrot(c, r):                       # inverse de r quarts de tour (x,y) -> (-y,x)
    x, y = c
    for _ in range(r): x, y = y, -x
    return x, y
out = []; cfg = []
for n, (B, T0, CAP, ORIG) in enumerate(bases):
    f = f'{R}/data/t7/b_{n}.txt'
    if not os.path.exists(f) or os.path.getsize(f) == 0: continue
    r = 'HDBG'.index(CAP)
    for l in open(f):
        w = l.split()
        if w[0] != 'OK': continue
        J, K, CE = int(w[1]), int(w[2]), int(w[3])
        c3 = unrot((J - K, K), r)
        out.append(f'{n} {ORIG};{c3[0]},{c3[1]} {CE} ' + ' '.join(w[4:]))
        cfg.append(f'RL|0,0,H|{ORIG};{c3[0]},{c3[1]}\n')
res = subprocess.run([F, '-T', '400000000', '-cert', '-lot'], input=''.join(cfg), capture_output=True, text=True).stdout.splitlines()
bad = 0
for o, r_ in zip(out, res):
    m = re.search(r'CERT (\d+)', r_)
    if not m or m.group(1) != o.split()[2]: bad += 1; print('# DESACCORD', o, r_[-80:])
    print(o)
import sys; print(f'# {len(out)} triplets, {bad} désaccord(s)', file=sys.stderr)

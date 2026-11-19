#!/usr/bin/env python3
"""t7_mprime.py REC_M_C3FIXE DIRECTIONS : lemme T' (b) pour les preuves (M) « c₃ fixe » (base blanc + c₁ + c₃ pivotée, îlot c₂, NS = 1) :
transport le long de m₃ (f = d₃) : règle non utilisée, c₃ touchée après s₁ + 104, et d₃ = −d₂ (p₂ diminue) ou d₃ ⟂ d₂ avec lectures
« hors Δ » après le contact avec c₃ et fenêtre finale qui s'éloignent de Δ₁. Sortie : data/t7/mprime.txt. (S11)"""
import re, subprocess, os, sys
from collections import Counter
A = 'recherche/autoroute/ant'
base = {}
for l in open('resultats/relatif/bases9.txt'): b, t = l.split(); base[b] = (b, 0)
for l in open('resultats/relatif/bases13.txt'): b, t, cap, o = l.split(); base[o] = (b, 'HDBG'.index(cap))
def rot(c, r):
    x, y = c
    for _ in range(r): x, y = -y, x
    return x, y
D = {}
for l in open(sys.argv[2]):
    w = l.split(); D[(w[0], w[1])] = [(int(a), int(b)) for a, b in re.findall(r'\((-?\d+), (-?\d+)\)', ' '.join(w[3:]))]
E = 1 << 30
def loin(x0, x1, y0, y1, f):
    if x0 >= E: return True
    s = f[0] + f[1]; return (s > 0 and x0 > y1) or (s < 0 and x1 < y0)
cnt = Counter(); out = open('data/t7/mprime.txt', 'w')
for l in open(sys.argv[1]):
    if 'deux:EXACT' not in l: continue
    w = l.split(); n, C, CE, T0 = w[0], w[1], w[2], w[3][3:]; P = re.search(r'OK\[([^\]]*)\]', l).group(1).split()
    c = [tuple(map(int, p.split(','))) for p in C.split(';')]; B, r = base[f'{c[0][0]},{c[0][1]}']
    c2, c3 = rot(c[1], r), rot(c[2], r); d3p = rot(D[(n, C)][1], r)
    env = dict(os.environ, BASE=f'{B};{c3[0]},{c3[1]}', T0=T0, H0=str(r))
    o = subprocess.run([A, 'multi', str(c2[0] + c2[1]), str(c2[1]), CE] + P, capture_output=True, text=True, env=env).stdout.splitlines()[-1]
    g = lambda rx: tuple(map(int, re.search(rx, o).groups()))
    s1 = int(re.search(r's1=(-?\d+)', o).group(1)) if 's1=' in o else -1
    zl, zd, tl, l0, l1 = g(r'zlow=(\d) zd=(\d) tlast=(-?\d+) horsD_apres_last=\[(-?\d+),(-?\d+)\]')
    D0, D1 = g(r'Delta1=\[(-?\d+),(-?\d+)\]'); Z0, Z1 = g(r'diagZ=\[(-?\d+),(-?\d+)\]'); rg = int(re.search(r'regle=(\d+)', o).group(1))
    dd = d3p[0] * (-2) + d3p[1] * 2
    crit = rg == 0 and P[0] == '1' and tl > s1 + 104 and (dd < 0 or (dd == 0 and loin(l0, l1, D0, D1, d3p) and (zl == 1 or loin(Z0, Z1, D0, D1, d3p))))
    why = '' if crit else ('regle' if rg else 'NS' if P[0] != '1' else 'tc3' if tl <= s1 + 104 else 'dir' if dd > 0 else 'diag')
    cnt[('MP:ok' if crit else 'MP:non', why)] += 1; out.write(f'{n} {C} {"MP:ok" if crit else "MP:non"} {why} s1={s1}\n')
for k, v in cnt.most_common(): print(k, v)

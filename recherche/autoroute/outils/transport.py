#!/usr/bin/env python3
"""transport.py : uniformité de la double récurrence (deux cases loin), voir E2_epars.md (S5).
Pour chaque paire (classe de c1, classe de c2) : d2 = direction de l'autoroute après c1 (repère d'origine, y vers le bas),
vérification (b) (récurrence en k1, îlot {c1,c2} déplacé en bloc) à la base m0 lue dans dbl22.res (NS) ;
si NS = 0, relance `ant multi … 0` pour lire la direction finale et les diagonales de la fenêtre finale.
Verdict DEMONTRE si : NS_b = 0 et [d2 = d] ou [d2 ⟂ d et (direction finale ≠ −d ou diagonales qui s'éloignent de D)]."""
import re, subprocess, os
here = os.path.dirname(os.path.abspath(__file__)); A = here + '/../ant'
dirs = {}
for l in open('gap.cert'):
    f = l.split('|'); x, y = map(int, f[2].split(','))
    m = re.search(r' 104,(-?\d+),(-?\d+),', l); dirs[(x, y)] = (int(m.group(1)), int(m.group(2)))
pairs = []
for line in open('bases9.txt'):
    b, t = line.split()
    for l in open(f'rel_{b}.txt'): pairs.append(tuple(map(int, b.split(','))))
for line in open('bases13.txt'):
    b, t, cap, orig = line.split()
    for l in open(f'rel13_{b}.txt'): pairs.append(tuple(map(int, orig.split(','))))
res = [l.split() for l in open('dbl22.res')]
assert len(res) == 2 * len(pairs), (len(res), len(pairs))
from collections import Counter
cnt = Counter(); out = open('transport.res', 'w')
for i, c1 in enumerate(pairs):
    J, K, CE, ex, ey = res[2 * i][:5]; v = ' '.join(res[2 * i][5:]); d2 = dirs[c1]
    perp = d2[0] * (-2) + d2[1] * 2 == 0; same = d2 == (-2, 2)
    if not v.startswith('NS0'):
        verdict = 'NON_TRAITE(' + v + ')'
    else:
        r = subprocess.run([A, 'multi', J, K, CE, '0', ex, ey], capture_output=True, text=True).stdout
        m = re.search(r'dir=\((-?\d+),(-?\d+)\) diagZ=\[(-?\d+),(-?\d+)\] diagD=\[(-?\d+),(-?\d+)\]', r)
        fx, fy, z0, z1, D0, D1 = map(int, m.groups())
        moinsd = (fx, fy) == (2, 2)          # repère y vers le haut : -d = (2,2)
        if same: verdict = 'DEMONTRE'
        elif perp:
            if not moinsd: verdict = 'DEMONTRE'
            else:
                s = 4 if (d2[0] + d2[1]) > 0 else -4   # variation de x+y (y bas) par pas de d2
                ok = (s > 0 and z0 > D1) or (s < 0 and z1 < D0)
                verdict = 'DEMONTRE' if ok else 'NON_TRAITE(diagonales vers D)'
        else: verdict = 'NON_TRAITE(d2=-d)'
    cnt[verdict] += 1; out.write(f'{c1} {J} {K} {CE} {ex} {ey} d2={d2} {verdict}\n')
print(dict(cnt))

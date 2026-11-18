#!/usr/bin/env python3
"""preuves_loin.py FICHIER.cert : classes lointaines (forme, j, parité de k) d'un îlot ; pentes du pas certifié ;
écrit sur la sortie les commandes ./ant (pmin pour pente 52, uturn pour pente 104) au plus petit k."""
import re, sys
from collections import defaultdict
cl = defaultdict(list)
for l in open(sys.argv[1]):
    f = l.split('|'); cs = [tuple(map(int, c.split(','))) for c in f[2].split(';')]
    x0, y0 = cs[0]; off = tuple((x - x0, y - y0) for x, y in cs[1:])
    c = int(re.search(r'CERT (\d+)', l).group(1)); d = re.search(r' 104,(-?\d+),(-?\d+),', l).groups()
    cl[(off, x0 + y0, y0 % 2)].append((y0, c, d))
stat = defaultdict(int)
for (off, j, par), L in sorted(cl.items()):
    L.sort(); k0, c0, _ = L[0]
    sl = {(c - c0) / (k - k0) for k, c, _ in L[1:]}; nd = len({r[2] for r in L})
    if len(sl) != 1 or nd != 1: print('# IRRÉGULIER', off, j, par, sl, nd, file=sys.stderr); stat['irr'] += 1; continue
    s = sl.pop(); stat[s] += 1; e = ' '.join(f'{a} {b}' for a, b in off)
    if s == 52: print(f'pmin {j} {k0} {c0 + 104} {e}')
    elif s == 104: print(f'uturn {j} {k0} 150 {c0} {e}')
    elif s != 0: print('# pente inattendue', off, j, par, s, file=sys.stderr)
print('# classes :', dict(stat), file=sys.stderr)

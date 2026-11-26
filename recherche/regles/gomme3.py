#!/usr/bin/env python3
"""R-301 : autre moyen d'effacer pour q >= 3 ? Après T pas d'une fourmi (départ blanc), on pose UNE fourmi effaceuse
(même règle) sur chaque case à distance <= 3 de la fin, chaque cap, et on regarde si la grille redevient TOUTE blanche
en <= 2·10^5 pas (-z). Puis « double gomme » : 2 effaceuses (toutes les paires de la liste précédente limitée)."""
import subprocess, itertools, sys
from gomme import run, geo
def lot(lines, T):
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-z', '-lot'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout
    return [l for l in out.splitlines()]
for rule in ['RL', 'LLR', 'LLLR', 'RLLR', 'LLRRRL', 'H:R1R2', 'H:R1L2', 'H:R1R2L1', 'T:RLL']:
    D, M = geo(rule)
    for T in (20, 100, 1000):
        _, ants, cells = run(f"{rule}|0,0,0|", T)
        x, y, d = ants[0]
        cs = ';'.join(f"{a},{b},{k}" for (a, b), k in cells.items())
        lines = [f"{rule}|{x+i},{y+j},{h}|{cs}" for i in range(-3, 4) for j in range(-3, 4) for h in range(M)]
        res = lot(lines, 200000)
        z = [l for l in res if l.startswith('ZERO')]
        # paires : effaceuse « gomme » + une 2e sur une case voisine (repasser 2 fois)
        px, py = x - D[d][0], y - D[d][1]
        g = f"{px},{py},{(d + M // 2) % M}"
        lines2 = [f"{rule}|{g};{x+i},{y+j},{h}|{cs}" for i in range(-2, 3) for j in range(-2, 3) for h in range(M)]
        z2 = [l for l in lot(lines2, 200000) if l.startswith('ZERO')]
        print(f"{rule:10s} T={T:5d} cases={len(cells):4d}  1 effaceuse : {len(z)}/{len(lines)}   gomme+1 : {len(z2)}/{len(lines2)}", flush=True)

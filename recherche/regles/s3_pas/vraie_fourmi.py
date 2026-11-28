#!/usr/bin/env python3
"""Fourmi RL sur le tore 2×2, écrite directement (indépendante des formules R-61 de modules.spec) — contrôle des trajectoires (T1).
Conventions du projet : caps 0=H 1=D 2=B 3=G, y vers le bas ; case blanche (0) -> tourne à droite, noire (1) -> à gauche ;
on retourne la couleur puis on avance d'une case (tore 2×2). État : c00 c10 c01 c11 x y h1 h0 (h = 2·h1 + h0)."""
import itertools
from modules import VARS, spec
DIRS = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
def pas(e):
    g = {(i, j): e[f'c{i}{j}'] for i in (0, 1) for j in (0, 1)}; x, y = e['x'], e['y']; h = 2 * e['h1'] + e['h0']
    h = (h + (1 if g[(x, y)] == 0 else -1)) % 4; g[(x, y)] ^= 1
    dx, dy = DIRS[h]; x, y = (x + dx) % 2, (y + dy) % 2
    return {**{f'c{i}{j}': g[(i, j)] for i in (0, 1) for j in (0, 1)}, 'x': x, 'y': y, 'h1': h >> 1, 'h0': h & 1}
def trajectoire(e, n):
    out = [e]
    for _ in range(n): out.append(pas(out[-1]))
    return out
if __name__ == '__main__':
    full = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
    bad = sum(1 for e in full for v in VARS if pas(e)[v] != spec(v, e))
    print(f'vraie fourmi RL (tore 2×2) contre formules R-61 : {bad} bits différents sur 256 × 8')

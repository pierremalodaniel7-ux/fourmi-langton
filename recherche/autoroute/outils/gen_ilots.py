#!/usr/bin/env python3
"""gen_ilots.py A|C fichier : îlots = toutes les formes contenues dans un carré 3×3 (400 formes à translation près).
A : translations où l'îlot touche la boîte [-24,32]x[-25,25] (positions du départ blanc avant 10 185 : [-21,29]x[-22,22])
    ou la bande x+y in [-28,-18] avec y <= 100 (début de la bande Z de l'autoroute).
C : classes lointaines, 1re case (y,x minimal) en (j-k, k), j in [-32,-14], k = 100..105."""
import sys
shapes = []
for m in range(1, 512):
    P = [(i % 3, i // 3) for i in range(9) if m >> i & 1]
    if min(a for a, b in P) == 0 and min(b for a, b in P) == 0:
        shapes.append(sorted(P, key=lambda c: (c[1], c[0])))
mode, out = sys.argv[1], open(sys.argv[2], 'w')
def line(cells): out.write('RL|0,0,H|' + ';'.join(f'{x},{y}' for x, y in cells) + '\n')
n = 0
for P in shapes:
    a0, b0 = P[0]
    if mode == 'A':
        for ty in range(-30, 103):
            for tx in range(-140, 40):
                C = [(a + tx, b + ty) for a, b in P]
                if any(-24 <= x <= 32 and -25 <= y <= 25 for x, y in C) or any(-28 <= x + y <= -18 and y <= 100 for x, y in C):
                    line(C); n += 1
    else:
        for j in range(-32, -13):
            for k in range(100, 106):
                x0, y0 = j - k, k
                line([(a - a0 + x0, b - b0 + y0) for a, b in P]); n += 1
print(len(shapes), 'formes,', n, 'situations', file=sys.stderr)

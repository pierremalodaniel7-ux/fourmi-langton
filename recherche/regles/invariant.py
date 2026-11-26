#!/usr/bin/env python3
"""R-331 Invariant mod 3 de H:R2L2 : Q = (nb de cases noires) − Σ_fourmis ⌊cap/2⌋ (mod 3) ne change JAMAIS.
Preuve (1 ligne) : sur blanc, cap +2 (⌊cap/2⌋ +1 mod 3) et 1 case noire de plus ; sur noir, cap +4 (⌊cap/2⌋ +2 ≡ −1) et 1 case noire
de moins. Ici : vérification sur des situations au hasard (2e moteur hx.py) + valeur de Q pour le vaisseau dans les 6 directions."""
import random
from hx import run, ship, step, HX
def Q(ants, g): return (sum(1 for v in g.values() if v) - sum(a[2] // 2 for a in ants)) % 3
random.seed(7); bad = 0
for _ in range(300):
    A = [[random.randint(-4, 4), random.randint(-4, 4), random.randint(0, 5)] for _ in range(random.randint(1, 6))]
    g = {(random.randint(-4, 4), random.randint(-4, 4)): 1 for _ in range(random.randint(0, 10))}
    q0 = Q(A, g)
    for t in range(500):
        step(A, g)
        if Q(A, g) != q0: bad += 1; break
print('situations au hasard (1 à 6 fourmis, 500 tours) : Q constant dans', 300 - bad, '/ 300')
for r in range(6):
    a, c = ship(r); print(f'  vaisseau r={r} direction {[(1,-1),(1,0),(0,1),(-1,1),(-1,0),(0,-1)][r]} : Q = {Q([list(a)], {c: 1})}')

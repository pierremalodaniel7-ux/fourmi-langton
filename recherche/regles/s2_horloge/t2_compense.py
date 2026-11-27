"""T2 — vérifie la règle de compensation (R-514) : δh + rot120(δa) = 0 ⇒ l'horloge triangle referme (pour les 596 chocs de tri_rB5.json).
δ est un décalage continu d'espace-temps : case (dx, dy) + retard dt (= −dt/8 case le long de la direction du vaisseau).
On prend δh = (dx, dy, dt) et on construit δa = −rot120⁻¹(δh) exprimé dans le repère du vaisseau anti-horaire (dir 3 → dir 1 après coin).
Usage : python3 s2_horloge/t2_compense.py"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from fractions import Fraction as Fr
from hx import rot, ship_dir
from tri import R, adv
F = json.load(open('s2_horloge/tri_rB5.json'))
ch = {}
for f in F: ch[(tuple(f['B'][1]), f['B'][0], f['B'][2], f['order'])] = f
def tup(v): return (v[0], tuple(v[1]), v[2])
def shift(v, dx, dy, dt):
    r, p, tau = adv(v, dt + 64); d = ship_dir(r)
    return (r, (p[0] + dx - 8 * d[0], p[1] + dy - 8 * d[1]), tau)
def cont(r, dx, dy, dt):
    d = ship_dir(r); return (Fr(dx) + Fr(dt * d[0], 8), Fr(dy) + Fr(dt * d[1], 8))
def sols(A2, B2, Bv, Tmax=1500):
    out = []
    for T in range((-A2[2]) % 8 + 16, Tmax, 8):
        a2 = adv(A2, T); q = (0, 0); c = (a2[1][0], a2[1][1])
        if R(adv(B2, T), c) == Bv: out.append(T)
    return out
# δa cherché parmi (dx, dy, dt) petits tels que cont(rB2, δa) = −rot120⁻¹(cont(rA2, δh))
def rotf(v, k):
    x, y = v
    for _ in range(k % 6): x, y = -y, x + y
    return (x, y)
cands = [(x, y, t) for x in range(-4, 5) for y in range(-4, 5) for t in range(-7, 8)]
tests = [(1, -2, 0), (-2, 0, 0), (1, 0, 0), (1, 2, 0), (0, 1, 0), (0, 0, 3), (1, -1, 5)]
ok = collections.Counter(); nb = collections.Counter()
for key, f in list(ch.items()):
    A2, B2, Bv = tup(f['A2']), tup(f['B2']), tup(f['B'])
    for dh in tests:
        vh = cont(A2[0], *dh); target = rotf((-vh[0], -vh[1]), -2)
        da = [c for c in cands if cont(B2[0], *c) == target]
        if not da: nb[dh] += 0; continue
        nb[dh] += 1
        if sols(shift(A2, *dh), shift(B2, *da[0]), Bv): ok[dh] += 1
for dh in tests: print('δh', dh, ': chocs testés', nb[dh], 'referment', ok[dh])

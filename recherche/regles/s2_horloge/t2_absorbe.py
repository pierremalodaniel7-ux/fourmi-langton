"""T2 — équations de fermeture de l'horloge triangle (tri.py) quand une « porte » décale, à chaque tiers, le vaisseau horaire de δh
et/ou l'anti-horaire de δa (δ = case (distance ≤ 2) + retard dt ∈ [−7, 7]). Calcul exact sur vaisseaux virtuels, sans simulation.
Question : quels décalages une horloge 3-symétrique peut-elle absorber (en changeant de taille) ?
Usage : python3 s2_horloge/t2_absorbe.py [Tmax]"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, ship_dir
from tri import R, adv
from exp_osc import hd
Tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
F = json.load(open('s2_horloge/tri_rB5.json'))
ch = {}
for f in F: ch[(tuple(map(tuple, [f['B'][1]])), f['B'][0], f['B'][2], f['order'])] = f
def tup(v): return (v[0], tuple(v[1]), v[2])
def shift(v, dx, dy, dt):
    r, p, tau = adv(v, dt + 64); d = ship_dir(r)
    return (r, (p[0] + dx - 8 * d[0], p[1] + dy - 8 * d[1]), tau)
D = [(x, y, t) for x in range(-2, 3) for y in range(-2, 3) if hd(x, y) <= 2 for t in range(-7, 8)]
A = (0, (0, 0), 0)
def sols(A2, B2):
    out = []
    for T in range((-A2[2]) % 8 + 16, Tmax, 8):
        a2 = adv(A2, T)
        q = rot(A[1], 2); c = (a2[1][0] - q[0], a2[1][1] - q[1])
        if R(adv(B2, T), c) == A_B[0]: out.append(T)
    return out
res = collections.Counter(); ex = {}
for key, f in ch.items():
    A2, B2 = tup(f['A2']), tup(f['B2']); A_B = [tup(f['B'])]
    for (dx, dy, dt) in D:
        for who in ('h', 'a'):
            if (dx, dy, dt) == (0, 0, 0) and who == 'a': continue
            a2 = shift(A2, dx, dy, dt) if who == 'h' else A2
            b2 = shift(B2, dx, dy, dt) if who == 'a' else B2
            s = sols(a2, b2)
            if s:
                res[(who, dx, dy, dt)] += 1
                ex.setdefault((who, dx, dy, dt), (key, s[:4]))
print(len(ch), 'chocs ; décalages absorbés (qui, dx, dy, dt) : nb de chocs')
for k, v in sorted(res.items(), key=lambda kv: -kv[1])[:40]: print(k, v, ex[k][1])
json.dump([[list(k), v] for k, v in res.items()], open('s2_horloge/t2_absorbe.json', 'w'))

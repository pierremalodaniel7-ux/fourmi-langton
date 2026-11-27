"""S2 — Horloge « triangle » : 3 vaisseaux horaires (classe paire) + 3 anti-horaires (classe impaire) ; à chaque coin un choc
de 2 vaisseaux qui les tourne de +120° et −120°. Recherche : choc (A dir rA, B dir rB) → (A' dir rA+2, B' dir rB−2) propre,
puis rotation R(x) = rot2(x) + c et temps T tels que A'(T) = R(A(0)) et R(B'(T)) = B(0) ⇒ état(T) = R(état(0)) ⇒ CYCLE de période 3T.
Positions entières, moteur hx.py (Python) pour l'énumération ; vérification finale fourmi_r (CYCLE) + hx.py.
Usage : python3 s2_horloge/tri.py rB [Tmax]"""
import sys, json
sys.path.insert(0, '.')
from hx import ship, ship_dir, rot, step, PHASES
from demi_add_k import OFFS, fmt
from fa_lib import kship
from exp_osc import hd
def virt(ant, cells, t):
    """vaisseau propre (fourmi + cases à ≤ 2) au temps t -> (r, pos0, tau0) virtuel au temps 0, ou None"""
    x, y, h = ant
    near = frozenset((p[0]-x, p[1]-y) for p in cells if hd(p[0]-x, p[1]-y) <= 2)
    k = PHASES.get((h, near))
    if not k: return None, near
    r, ph = k; gx, gy = x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1]
    tau0 = (ph - t) % 8; m = (tau0 + t - ph) // 8; d = ship_dir(r)
    return (r, (gx - m*d[0], gy - m*d[1]), tau0), near
def at(sh, t):
    """état (fourmi, cases) du vaisseau virtuel sh au temps t (t ≥ -8*K quelconque entier)"""
    r, p, tau = sh; d = ship_dir(r); s = tau + t; m = s // 8; ph = s % 8
    return kship(r, (p[0] + m*d[0], p[1] + m*d[1]), ph)
def collide(A, B, order, t0=-96, t1=160):
    """simule A, B (virtuels) de t0 à t1 ; renvoie les virtuels sortants (A', B') ou None"""
    a, ca = at(A, t0); b, cb = at(B, t0)
    ants = [list(a), list(b)] if order == 0 else [list(b), list(a)]
    G = {c: 1 for c in ca + cb}
    if len(G) < 2: return None
    mind = 99
    for t in range(t0, t1):
        step(ants, G); mind = min(mind, hd(ants[0][0]-ants[1][0], ants[0][1]-ants[1][1]))
    if mind > 6: return None
    if hd(ants[0][0]-ants[1][0], ants[0][1]-ants[1][1]) <= 6: return None
    res = []
    used = set()
    for an in ants:
        v, near = virt(an, G, t1)
        if v is None: return None
        used |= {(an[0]+u, an[1]+w) for u, w in near}
        res.append(v)
    if set(G) - used: return None
    return (res[0], res[1]) if order == 0 else (res[1], res[0])
def R(sh, c, k=1):
    r, p, tau = sh
    for _ in range(k):
        q = rot(p, 2); p = (q[0] + c[0], q[1] + c[1]); r = (r + 2) % 6
    return (r, p, tau)
def adv(sh, T):
    r, p, tau = sh; d = ship_dir(r); s = tau + T
    return (r, (p[0] + (s//8)*d[0], p[1] + (s//8)*d[1]), s % 8)
if __name__ == '__main__':
    rB = int(sys.argv[1]); Tmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    rA = 0; A = (0, (0, 0), 0)
    found = []; ncol = 0
    for vx in range(-9, 10):
        for vy in range(-9, 10):
            if hd(vx, vy) > 9: continue
            for tau in range(8):
                B = (rB, (vx, vy), tau)
                for order in (0, 1):
                    o = collide(A, B, order)
                    if not o: continue
                    A2, B2 = o
                    if A2[0] != (rA + 2) % 6 or B2[0] != (rB - 2) % 6: continue
                    ncol += 1
                    for T in range(16, Tmax):
                        a2 = adv(A2, T)
                        if a2[2] != A[2]: continue
                        q = rot(A[1], 2); c = (a2[1][0] - q[0], a2[1][1] - q[1])
                        if R(adv(B2, T), c) == B:
                            found.append({'B': B, 'order': order, 'A2': A2, 'B2': B2, 'T': T, 'c': c})
    print('chocs propres (+120, -120) :', ncol, ' solutions (choc, T) :', len(found))
    json.dump(found, open('s2_horloge/tri_rB%d.json' % rB, 'w'))
    import collections
    byc = collections.defaultdict(list)
    for f in found: byc[(f['B'], f['order'])].append(f['T'])
    for k, v in list(byc.items())[:20]: print(k, v[:12], len(v))

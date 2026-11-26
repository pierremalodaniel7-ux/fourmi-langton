"""R-608 Diagnostic géométrique d'un placement (sans simulation) : chaque vaisseau a au plus 3 segments possibles de ligne d'univers
(arrivée jusqu'à sa porte, puis tout droit OU dévié). On cherche les couples de segments qui passent à moins de `thr` l'un de l'autre,
hors des chocs voulus. Sert à guider la recherche des longueurs (D, G) ; la vérification reste la simulation complète (2 moteurs)."""
from s3lib import *
INF = 10 ** 7
def segments(L):
    W = {nm: w for nm, k, w in L.ships}
    seg = {nm: [] for nm in W}; ev = {}
    first = {}
    for node, side, tg, oA, oB, pn in L.gates:
        seg[pn].append((W[pn], -INF, tg, 'in')); seg[pn].append((W[pn], tg, INF, 'droit')); seg[pn].append((oA, tg, INF, 'dévié'))
        seg[node].append((oB, tg, INF, 'dévié'))
        ev.setdefault(node, []).append(tg); ev.setdefault(pn, []).append(tg)
    for nm in W:
        if nm not in {g[5] for g in L.gates}: seg[nm].append((W[nm], -INF, INF, 'puissance'))
        if not any(s[3] == 'in' for s in seg[nm]): pass
    # la puissance d'un nœud : arrivée jusqu'à sa dernière porte (au plus), tout droit ensuite (déjà couvert par sa porte chez le parent)
    return seg
def pmin(w1, a1, b1, w2, a2, b2, thr=7):
    lo, hi = max(a1, a2), min(b1, b2)
    if lo > hi: return INF, None
    d1, d2 = ship_dir(w1[0]), ship_dir(w2[0]); u = (d1[0] - d2[0], d1[1] - d2[1])
    p1, p2 = antpos(w1, 0), antpos(w2, 0); v = (p1[0] - p2[0], p1[1] - p2[1])
    if u == (0, 0):
        if hd(*v) > thr + 4: return INF, None
        t0 = lo if lo > -INF else (hi if hi < INF else 0); ts = range(t0, t0 + 8)
    else:
        ts = set()
        for a, b in ((v[0], u[0]), (v[1], u[1]), (v[0] + v[1], u[0] + u[1])):
            if b:
                c = int(-8 * a / b)
                vv = (v[0] + u[0] * c / 8, v[1] + u[1] * c / 8)
                if hd(int(vv[0]), int(vv[1])) > thr + 6: continue
                ts |= set(range(c - 10, c + 11))
        if lo > -INF: ts |= set(range(lo, lo + 8))
        if hi < INF: ts |= set(range(hi - 7, hi + 1))
    best, bt = INF, None
    for t in ts:
        if lo <= t <= hi:
            p, q = antpos(w1, t), antpos(w2, t); dd = hd(p[0] - q[0], p[1] - q[1])
            if dd < best: best, bt = dd, t
    return best, bt
def conflicts(L, thr=7, guard=80):
    seg = segments(L); names = list(seg); out = []
    gates = {}
    for node, side, tg, oA, oB, pn in L.gates: gates[frozenset((node, pn))] = tg
    for i in range(len(names)):
        for j in range(i):
            a, b = names[i], names[j]; tg = gates.get(frozenset((a, b)))
            for s1 in seg[a]:
                for s2 in seg[b]:
                    m, t = pmin(s1[0], s1[1], s1[2], s2[0], s2[1], s2[2], thr)
                    if m < thr and not (tg is not None and abs(t - tg) <= guard):
                        out.append((a, s1[3], b, s2[3], m, t))
    return out

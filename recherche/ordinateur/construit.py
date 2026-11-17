"""construit.py — briques de construction : approche, virage, recherche de case."""
import fourmis as F
P = F.P

def hw(cells, ants, w, T, tmin=0):
    n, dh, xs, ys, fr = F.simule(cells, ants, T, w)
    if n < 0: return None, (dh, xs, ys, fr)
    return F.autoroute(dh, xs, ys, tmin=tmin), (dh, xs, ys, fr)

def candidats(cells, ants, w, T, tmin, sp):
    """après stabilisation (t0>=tmin), avancer sp périodes, puis cases neuves visitées pendant 1 période"""
    h, (dh, xs, ys, fr) = hw(cells, ants, w, T, tmin)
    if h is None: return None, []
    t0 = h[0]; u0 = t0 + sp * P
    if u0 + P >= len(dh) - 21 * P: return h, None
    out = []
    for u in range(u0, u0 + P):
        if fr[u + 1]:          # case où arrive la fourmi au pas u+1 = (xs[u],ys[u]) : neuve
            out.append((int(xs[u]), int(ys[u]), u))
    return h, out

def place(cells, ants, w, T, tmin, sp, veut, filtre=None):
    """cherche une case qui fait passer la fourmi w dans la direction veut (ou un filtre(h)) ;
    renvoie (case, h_après, temps_de_chaos) ou None"""
    h, cand = candidats(cells, ants, w, T, tmin, sp)
    if not cand: return None
    best = None
    for (x, y, u) in cand:
        h2, _ = hw(cells + [(x, y)], ants, w, T, tmin=u + 2)
        if h2 is None: continue
        ok = (h2[1] == veut) if filtre is None else filtre(h, h2)
        if not ok: continue
        ch = h2[0] - u
        if best is None or ch < best[2]: best = ((x, y), h2, ch)
    return best

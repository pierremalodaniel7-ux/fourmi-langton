"""R-617 Certificat R-606 SANS MÉMOIRE (même lemme, mêmes conditions que reuse.certificate / cert2) pour les gros germes :
les positions ne sont pas stockées ; à chaque pas on calcule (numpy) « deux fourmis à < 7 » et la distance max à un centre fixé.
Le centre = celui du cas n° 0 (comme reuse.certificate) ; il est calculé d'abord. 2 processus. Trajectoires : hx.py."""
import numpy as np
from multiprocessing import Pool
from s3lib import *
from reuse import ray_min, lane_of
def _run(args):
    s, T, W, centre = args
    a, c = parse(s); A = [list(x) for x in a]; G = {tuple(x[:2]): 1 for x in c}; n = len(A)
    iu, ju = np.triu_indices(n, 1); close = np.zeros(T + 1, bool); dmax = np.zeros(T + 1, np.int64)
    sx = sy = cnt = 0; bad_t = []
    for t in range(T + 1):
        if t: step(A, G)
        X = np.array([[p[0], p[1]] for p in A], np.int64)
        if t % 97 == 0 and not close[:t].any() and sorted(antpos(w, t) for w in W) != sorted((p[0], p[1]) for p in A): bad_t.append(t)
        dx = X[iu, 0] - X[ju, 0]; dy = X[iu, 1] - X[ju, 1]
        close[t] = bool((((np.abs(dx) + np.abs(dy) + np.abs(dx + dy)) // 2) < 7).any())
        if centre is not None:
            ex = X[:, 0] - centre[0]; ey = X[:, 1] - centre[1]; dmax[t] = int(((np.abs(ex) + np.abs(ey) + np.abs(ex + ey)) // 2).max())
        else: sx += int(X[:, 0].sum()); sy += int(X[:, 1].sum()); cnt += n
    idx = np.nonzero(close)[0]; T0, T1 = (int(idx[0]), int(idx[-1])) if len(idx) else (0, 0); free_ok = not any(t <= T0 for t in bad_t)
    return T0, T1, [tuple(x) for x in A], sorted(G), int(dmax[T0:T1 + 1].max()) if centre is not None else None, free_ok, (sx, sy, cnt)
def certificate3(layout, envs=None, T=None, log=print, procs=2):
    envs = envs or layout.cases(); T = T or layout.tmax + 1200
    Ws = [layout.present(e) for e in envs]; S = [sit_wls(W) for W in Ws]
    # centre : moyenne des positions du cas 0 dans SA fenêtre (2 passes sur le cas 0)
    T0, T1, *_ = _run((S[0], T, Ws[0], None))
    r0 = _run((S[0], T1, Ws[0], None)); r0b = _run((S[0], T0 - 1, Ws[0], None)) if T0 > 0 else (0, 0, 0, 0, 0, 0, (0, 0, 0))
    sx, sy, cnt = (r0[6][0] - r0b[6][0], r0[6][1] - r0b[6][1], r0[6][2] - r0b[6][2]); centre = (sx // cnt, sy // cnt)
    with Pool(procs) as P: R = P.map(_run, [(s, T, W, centre) for s, W in zip(S, Ws)])
    ins, outs, span, Rg = [], [], 0, 0
    for e, W, (T0, T1, a, c, dm, free_ok, _) in zip(envs, Ws, R):
        d = decode(a, c, T); assert d is not None, ('état final non propre', e)
        assert free_ok, ('entrant non libre', e)
        ma = min([ray_min(W[i], W[j], T0 - 1, -1) for i in range(len(W)) for j in range(i)] or [99])
        mb = min([ray_min(d[i], d[j], T, +1) for i in range(len(d)) for j in range(i)] or [99])
        assert ma >= 7 and mb >= 7, ('rayons trop proches', e, ma, mb)
        assert T1 < T - 64
        span = max(span, T1 - T0); Rg = max(Rg, dm); ins += W; outs += d
    worst = 99
    for o in set(outs):
        for i in set(ins):
            if (o[0] - i[0]) % 6 == 3:
                lo = [lane_of(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of(antpos(i, t), o[0]) for t in range(8)]
                worst = min(worst, min(abs(x - y) for x in lo for y in li))
    delta = span + 16 * (2 * Rg + 11); ok = worst >= 7
    log(f'certificat : {len(envs)} cas, fenêtre active max {span} pas, rayon {Rg} autour de {centre}, voies opposées : écart min {worst} '
        f'⇒ {"OK" if ok else "ÉCHEC"} : tout nombre d’usages pour Δ ≥ {delta} pas ({-(-delta // 8)} périodes)')
    return ok, delta, dict(span=span, R=Rg, centre=centre, opposees=worst)

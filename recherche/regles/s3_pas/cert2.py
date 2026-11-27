"""R-616 Certificat R-606 ACCÉLÉRÉ (même lemme, mêmes conditions que reuse.certificate) : la fenêtre [T0, T1] (deux fourmis à < 7)
est calculée avec numpy (distances hexagonales de toutes les paires à chaque pas) au lieu d'une double boucle Python.
Trajectoires : hx.py (2e moteur), comme reuse.trajectory. Sorties identiques à reuse.certificate (contrôlé sur le module x')."""
import numpy as np
from s3lib import *
from reuse import trajectory, ray_min, lane_of
def window_np(P, n):
    A = np.array([p[:n] for p in P], dtype=np.int64)          # T × n × 2
    iu, ju = np.triu_indices(n, 1)
    close = np.zeros(len(A), bool)
    for k in range(0, len(iu), 400):
        a, b = iu[k:k + 400], ju[k:k + 400]
        dx = A[:, a, 0] - A[:, b, 0]; dy = A[:, a, 1] - A[:, b, 1]
        d = (np.abs(dx) + np.abs(dy) + np.abs(dx + dy)) // 2
        close |= (d < 7).any(axis=1)
    idx = np.nonzero(close)[0]
    return (int(idx[0]), int(idx[-1])) if len(idx) else (None, None)
def certificate2(layout, envs=None, T=None, log=print):
    envs = envs or layout.cases(); T = T or layout.tmax + 1200
    ins, outs, rep, trajs = [], [], [], []
    for e in envs:
        W = layout.present(e); s = sit_wls(W)
        P, a, c = trajectory(s, T); d = decode(a, c, T)
        assert d is not None, ('état final non propre', e)
        T0, T1 = window_np(P, len(W))
        if T0 is None: T0, T1 = 0, 0
        for t in range(0, T0 + 1, 97):
            assert sorted(antpos(w, t) for w in W) == sorted(P[t]), ('entrant non libre', e, t)
        ma = min([ray_min(W[i], W[j], T0 - 1, -1) for i in range(len(W)) for j in range(i)] or [99])
        mb = min([ray_min(d[i], d[j], T, +1) for i in range(len(d)) for j in range(i)] or [99])
        assert ma >= 7 and mb >= 7, ('rayons trop proches', e, ma, mb)
        assert T1 < T - 64
        ps = np.array([p for t in range(T0, T1 + 1) for p in P[t]] or [(0, 0)])
        cx, cy = int(ps[:, 0].sum() // len(ps)), int(ps[:, 1].sum() // len(ps))
        rep.append(dict(cas=e, T0=T0, T1=T1, centre=(cx, cy), min_entrants=ma, min_sortants=mb))
        trajs.append(np.array([P[t] for t in range(T0, T1 + 1)], dtype=np.int64))
        ins += W; outs += d
    cx, cy = rep[0]['centre']; Rg = 0
    for X in trajs:
        dx = X[..., 0] - cx; dy = X[..., 1] - cy; Rg = max(Rg, int(((np.abs(dx) + np.abs(dy) + np.abs(dx + dy)) // 2).max()))
    worst = 99
    for o in set(outs):
        for i in set(ins):
            if (o[0] - i[0]) % 6 == 3:
                lo = [lane_of(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of(antpos(i, t), o[0]) for t in range(8)]
                worst = min(worst, min(abs(x - y) for x in lo for y in li))
    span = max(x['T1'] - x['T0'] for x in rep); delta = span + 16 * (2 * Rg + 11); ok = worst >= 7
    log(f'certificat : {len(envs)} cas, fenêtre active max {span} pas, rayon {Rg} autour de {(cx, cy)}, voies opposées : écart min {worst} '
        f'⇒ {"OK" if ok else "ÉCHEC"} : tout nombre d’usages pour Δ ≥ {delta} pas ({-(-delta // 8)} périodes)')
    return ok, delta, dict(span=span, R=Rg, centre=(cx, cy), opposees=worst, cas=rep)

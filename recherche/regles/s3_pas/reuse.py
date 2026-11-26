"""R-606 Réutilisation au même endroit (S3) : usages multiples dans UNE simulation, et certificat « tout nombre d'usages ».
Usage u = le même circuit (cas e_u) retardé de u·Δ pas (chaque vaisseau reculé sur sa propre route : c'est la même chose).
LEMME (démontré dans le journal R-606) : soit, pour chaque cas, [T0, T1] la fenêtre où deux fourmis sont à moins de 7 l'une de l'autre,
R le rayon (distance hexagonale à un centre O) de toutes les fourmis pendant [T0, T1]. Si
  (a) avant T0 les vaisseaux sont libres (rayons entrants) et ne s'approchent jamais à moins de 7 entre eux (pour tout t ≤ T0),
  (b) après T1 tout est fait de vaisseaux libres qui ne s'approchent plus jamais à moins de 7 (pour tout t ≥ T1), aucune case orpheline,
  (c) aucune route sortante (d'un cas quelconque) n'est opposée à une route entrante (d'un cas quelconque) à moins de 7 voies,
alors pour Δ ≥ (T1 − T0)max + 16·(2R + 11), N usages = superposition exacte des usages seuls, pour tout N et toute suite de cas.
(Deux vaisseaux libres non opposés s'éloignent à vitesse ≥ 1/16 case par pas ; ±4 cases de marge pour la position de la fourmi dans sa période.)"""
from s3lib import *
import itertools
def ray_min(w1, w2, t0, sign):
    """distance minimale EXACTE entre les fourmis de 2 vaisseaux libres, pour t ≥ t0 (sign = +1) ou t ≤ t0 (sign = −1)"""
    best = 10 ** 9
    d1, d2 = ship_dir(w1[0]), ship_dir(w2[0]); u = (d1[0] - d2[0], d1[1] - d2[1])
    for rho in range(8):
        tt = t0 + sign * rho
        p1, p2 = antpos(w1, tt), antpos(w2, tt); v = (p1[0] - p2[0], p1[1] - p2[1])
        us = (sign * u[0], sign * u[1])          # v(m) = v + m·us, m ≥ 0
        cands = {0}
        for a, b in ((v[0], us[0]), (v[1], us[1]), (v[0] + v[1], us[0] + us[1])):
            if b:
                m = -a / b
                for mm in (int(m) - 1, int(m), int(m) + 1):
                    if mm >= 0: cands.add(mm)
        for m in cands: best = min(best, hd(v[0] + m * us[0], v[1] + m * us[1]))
    return best
def lane_of(p, r):
    X, Y = rot(p, -r % 6); return X + Y
def trajectory(s, T):
    """2e moteur (hx.py) pas à pas : positions des fourmis à chaque pas (pour T0, T1, R)"""
    a, c = parse(s); A = [list(x) for x in a]; G = {tuple(x[:2]): 1 for x in c}
    P = [[(x[0], x[1]) for x in A]]
    for _ in range(T):
        step(A, G); P.append([(x[0], x[1]) for x in A])
    return P, [tuple(x) for x in A], sorted(G)
def window(P, n):
    close = []
    for t, ps in enumerate(P):
        if any(hd(ps[i][0] - ps[j][0], ps[i][1] - ps[j][1]) < 7 for i in range(n) for j in range(i)): close.append(t)
    return (close[0], close[-1]) if close else (None, None)
def certificate(layout, envs=None, T=None, log=print):
    envs = envs or layout.cases(); T = T or layout.tmax + 1200
    ins, outs, rep = [], [], []
    for e in envs:
        W = layout.present(e); s = sit_wls(W)
        P, a, c = trajectory(s, T); d = decode(a, c, T)
        assert d is not None, ('état final non propre', e)
        T0, T1 = window(P, len(W))
        if T0 is None: T0, T1 = 0, 0
        # (a) entrants : libres jusqu'à T0 et deux à deux ≥ 7 pour tout t ≤ T0
        for t in range(0, T0 + 1, 97):
            assert sorted(antpos(w, t) for w in W) == sorted(P[t]), ('entrant non libre', e, t)
        ma = min([ray_min(W[i], W[j], T0 - 1, -1) for i in range(len(W)) for j in range(i)] or [99])
        mb = min([ray_min(d[i], d[j], T, +1) for i in range(len(d)) for j in range(i)] or [99])
        assert ma >= 7 and mb >= 7, ('rayons trop proches', e, ma, mb)
        assert T1 < T - 64
        ps = [p for t in range(T0, T1 + 1) for p in P[t]]
        cx = sum(p[0] for p in ps) // len(ps); cy = sum(p[1] for p in ps) // len(ps)
        R = max(hd(p[0] - cx, p[1] - cy) for p in ps)
        rep.append(dict(cas=e, T0=T0, T1=T1, R=R, centre=(cx, cy), min_entrants=ma, min_sortants=mb))
        ins += W; outs += d
    # centre commun : on prend le plus grand rayon autour d'UN centre (le 1er cas) pour tous les cas
    cx, cy = rep[0]['centre']
    Rg = 0
    for e, x in zip(envs, rep):
        P, _, _ = trajectory(layout.sit(e), x['T1'] + 1)
        Rg = max([Rg] + [hd(p[0] - cx, p[1] - cy) for t in range(x['T0'], x['T1'] + 1) for p in P[t]])
    # (c) routes opposées : différence de voie des fourmis (toutes phases) ≥ 7
    worst = 99
    for o in set(outs):
        for i in set(ins):
            if (o[0] - i[0]) % 6 == 3:
                lo = [lane_of(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of(antpos(i, t), o[0]) for t in range(8)]
                worst = min(worst, min(abs(x - y) for x in lo for y in li))
    span = max(x['T1'] - x['T0'] for x in rep)
    delta = span + 16 * (2 * Rg + 11)
    ok = worst >= 7
    log(f'certificat : {len(envs)} cas, fenêtre active max {span} pas, rayon {Rg} autour de {(cx, cy)}, voies opposées : écart min {worst} '
        f'⇒ {"OK" if ok else "ÉCHEC"} : tout nombre d’usages pour Δ ≥ {delta} pas ({-(-delta // 8)} périodes)')
    return ok, delta, dict(span=span, R=Rg, centre=(cx, cy), opposees=worst, cas=rep)
def multi(layout, seq, D):
    """situation de N usages (cas seq[u]) espacés de D pas, ordre de jeu : usage 0, puis 1, …"""
    W = []
    for u, e in enumerate(seq): W += [tshift(w, u * D) for w in layout.present(e)]
    return sit_wls(W)
def check_multi(layout, seq, D, engine2=False, T=None):
    T = T or layout.tmax + (len(seq) - 1) * D + 1200
    s = multi(layout, seq, D); a, c = run_c([s], T)[0]; d = decode(a, c, T)
    singles = run_c([layout.sit(e) for e in seq], T)
    union = []
    for u, (a1, c1) in enumerate(singles):
        d1 = decode(a1, c1, T); union += [tshift(w, u * D) for w in d1]
    sup = d is not None and sorted(d) == sorted(union)
    good = sum(int(tshift(layout.out, u * D) in (d or [])) == layout.root.value(e) for u, e in enumerate(seq))
    same = None
    if engine2:
        pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
    return sup, good, same, len(parse(s)[0])

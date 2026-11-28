"""T4 : distances minimales (exactes à ±2 près : mouvement pris continu, 1 case / 8 pas) entre trajectoires rectilignes sur des
intervalles de temps. Segment = (A, B, t0, t1) : position(t) = A + B·t, t ∈ [t0, t1]. Calcul vectorisé (numpy) : la norme hex
max(|x|, |y|, |x+y|) d'un vecteur affine en t est convexe par morceaux ; son minimum est en un bout ou en un point de cassure."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
INF = 10 ** 9
def seg_wl(w, t0, t1, shift=0):
    w = S3L.tshift(w, shift); r = w[0]; d = TR.D[r]; p = S3L.antpos(w, 0); return (p[0], p[1], d[0] / 8, d[1] / 8, t0, t1)
def seg_T(T, t0, t1):
    r = T[0]; d = TR.D[r]; p = T_pos(T, 0); return (p[0], p[1], d[0] / 8, d[1] / 8, t0, t1)
def seg_point(c, t0=0, t1=INF): return (c[0], c[1], 0.0, 0.0, t0, t1)
def germ_segments(D=None):
    f = os.path.join(S4, 'data', 't4_germe_segments.json')
    if os.path.exists(f): base = json.load(open(f))
    else:
        ins = set(); outs = set(); envs = STEP.cases()
        for e in envs: ins |= set(STEP.present(e))
        for (a, c) in run_c([STEP.sit(e) for e in envs], TDEC):
            outs |= set(decode3(a, c, TDEC))
        base = dict(ins=sorted(ins), outs=sorted(outs)); json.dump(base, open(f, 'w'))
    S = []
    for sh in ([0] if D is None else [0, D]):
        S += [seg_wl(tuple(w), sh, sh + STEP.tmax, sh) for w in base['ins']]
        S += [seg_wl(tuple(w), sh + TDEC - 1200, INF, sh) for w in base['outs']]
    return np.array(S, dtype=float)
def dmin(seg, G):
    """distance minimale de seg à chaque segment de G (tableau N×6) -> (dist, t) vecteurs"""
    ax, ay, bx, by, s0, s1 = seg
    X0 = ax - G[:, 0]; Y0 = ay - G[:, 1]; VX = bx - G[:, 2]; VY = by - G[:, 3]
    t0 = np.maximum(s0, G[:, 4]); t1 = np.minimum(s1, G[:, 5]); ok = t0 <= t1
    cands = [t0, t1]
    # cassures : x = 0, y = 0, x + y = 0, x = ±y, x = ±(x+y), y = ±(x+y)
    for fx, fy in ((1, 0), (0, 1), (1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (2, 1), (1, 2)):
        num = fx * X0 + fy * Y0; den = fx * VX + fy * VY
        with np.errstate(divide='ignore', invalid='ignore'): tc = np.where(den != 0, -num / den, t0)
        cands.append(np.clip(tc, t0, t1))
    best = np.full(len(G), np.inf); bt = np.zeros(len(G))
    for tc in cands:
        x = X0 + VX * tc; y = Y0 + VY * tc; h = np.maximum(np.maximum(np.abs(x), np.abs(y)), np.abs(x + y))
        m = h < best; best = np.where(m, h, best); bt = np.where(m, tc, bt)
    best = np.where(ok, best, np.inf)
    return best, bt
def loop_segments(nm, PL, tri, chocs, e, a1):
    """segments du cas « signal présent » et du cas « absent » ; chaque segment porte les instants de choc qui le bornent"""
    O = wl_to_T(STEP.out[nm]); pres = []; X = O; t = a1
    for j, (C, (k, i, o)) in enumerate(zip(chocs, tri)):
        pres.append(('sig%d' % j, seg_T(X, t, C.te), {j - 1, j}))
        pres.append(('K%d' % j, seg_T(C.ins[1 - i], 0, C.te), {j}))
        pres.append(('deb%d' % j, seg_T(C.outs[1 - o], C.te, INF), {j}))
        X = C.outs[o]; t = C.te
    pres.append(('retour', seg_T(X, t, INF), {len(chocs) - 1}))
    absn = [('K%d' % j, seg_T(C.ins[1 - i], 0, INF), set()) for j, (C, (k, i, o)) in enumerate(zip(chocs, tri))]
    return pres, absn
def loop_ok(nm, PL, tri, chocs, e, D, G, marge=6, log=None, cases=('présent', 'absent'), paires=False):
    a1 = PL[nm]['arrivee']; pres, absn = loop_segments(nm, PL, tri, chocs, e, a1)
    O = wl_to_T(STEP.out[nm]); own = np.array(seg_T(O, 0, 0)[:4])
    Gm = G[~((np.abs(G[:, :4] - own).max(axis=1) < 3) & (G[:, 4] < D))]       # sans la sortie c_nm de l'usage 1 (c'est le signal)
    pts = np.array([seg_point(PL[k]['c']) for k in CASES])
    worst = []
    for case, S in (('présent', pres), ('absent', absn)):
        if case not in cases: continue
        for name, s, ch in S:
            d, t = dmin(s, Gm); j = int(np.argmin(d)); worst.append((d[j], case, name, 'germe', float(t[j])))
            dp, tp = dmin(s, pts)
            for k, nmk in enumerate(CASES):
                if nmk == nm and name in ('sig0', 'retour'): continue
                worst.append((dp[k], case, name, 'pixel ' + nmk, float(tp[k])))
        for x in (range(len(S)) if paires else []):
            for y in range(x + 1, len(S)):
                if S[x][2] & S[y][2]: continue
                d, t = dmin(S[x][1], np.array([S[y][1]])); worst.append((d[0], case, S[x][0], S[y][0], float(t[0])))
    worst.sort(key=lambda w: w[0])
    return worst[0][0] >= marge, worst[:3]
def pair_transparent(T1, T2, tm, W=240):
    """deux vaisseaux libres (trajectoires traj) qui se frôlent vers l'instant tm : on joue la paire seule de tm − W à tm + W (hx.py),
    dans les 2 ordres ; True si dans les 2 cas ils ressortent exactement sur leurs trajectoires (croisement transparent)"""
    from lib4 import situation as sit4, labels_at
    t0 = max(0, int(tm) - W); L = [TR.to_label(T1), TR.to_label(T2)]
    for order in (L, L[::-1]):
        s = sit4(order, t0); a, c = run_py(s, 2 * W)
        got = labels_at(a, c, t0 + 2 * W)
        if got is None or sorted(got) != sorted(L): return False
    return True
def germ_traj(G, j):
    """trajectoire traj d'une ligne de G (on retrouve le vaisseau exact par sa position à l'instant t0 de son segment)"""
    return None

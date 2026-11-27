"""S1 / R-404 Certificat FIN « tout nombre d'usages » (raffine circuit.certificat de R-338/R-349).
Faits utilisés (calcul exhaustif, croisement.py et paralleles.py) : deux vaisseaux LIBRES ne s'influencent jamais si leurs fourmis
restent à distance ≥ 2 (directions différentes) ou ≥ 3 (même direction) ; et une fourmi ne lit jamais une case d'un autre usage si
elle en reste à distance ≥ 7 (cases d'un vaisseau à ≤ 2 de sa fourmi, R-338).
Une fourmi d'un usage est « libre » à l'instant t si elle est dans sa partie rectiligne (avant sa première ou après sa dernière
interaction : pos(t + 8) = pos(t) + v) ET qu'aucune autre fourmi de SON usage n'est à moins de 7.
Argument de superposition (parité) : la couleur d'une case = parité du nombre de passages ; si, pour chaque paire de fourmis
d'usages différents, la contribution de l'autre aux cases lues est paire (cas des paires libres sans influence, ou trop loin), alors
chaque fourmi lit la même couleur que dans son usage seul, et par récurrence sur les pas N usages = superposition exacte.
Condition vérifiée ici pour toute paire d'usages d'écart j (j = 1 … J) et tous les couples d'entrées, sur toute la droite des temps :
  distance ≥ 7, ou (les deux libres et distance ≥ 3 (parallèles) / ≥ 2 (sinon)).
Au-delà de J : fenêtres actives disjointes ; on exige en plus « aucune paire de routes à contresens dont la somme des voies est dans
[−3, 1] » (seules à pouvoir se rapprocher à ≤ 1) et que les distances minimales par écart croissent (constaté)."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from circuit import traj, posarr, hdist, DIRS
from hx import rot
def windows(T, W):
    """pour chaque fourmi : (dernier instant non rectiligne au début, premier instant non rectiligne à la fin) → libre si t < a ou t > b"""
    P, vin, vout = T; n = P.shape[1]; a = np.zeros(n, int); b = np.zeros(n, int)
    D = P[8:] - P[:-8]                                   # (W+1, n, 2)
    for i in range(n):
        okin = (D[:, i] == vin[i]).all(-1); okout = (D[:, i] == vout[i]).all(-1)
        bad_in = np.where(~okin)[0]; bad_out = np.where(~okout)[0]
        a[i] = bad_in[0] if len(bad_in) else W + 8          # libre (entrée) pour t < a[i]
        b[i] = bad_out[-1] + 8 if len(bad_out) else -1     # libre (sortie) pour t > b[i]
    return a, b, vin, vout
def freemask(T, W, ts):
    P, vin, vout = T; a, b, _, _ = windows(T, W)
    X = posarr(T, ts, W)                                 # (len, n, 2)
    straight = (ts[:, None] < a[None, :]) | (ts[:, None] > b[None, :])
    D = hdist(X[:, :, None, :] - X[:, None, :, :]); n = X.shape[1]
    D[:, np.arange(n), np.arange(n)] = 99
    iso = (D >= 7).all(-1)
    return X, straight & iso
def dirs_of(T, ts, W):
    """direction (indice de DIRS) de chaque fourmi à chaque instant (entrée ou sortie) ; −1 pendant l'activité"""
    P, vin, vout = T; a, b, _, _ = windows(T, W); n = P.shape[1]
    di = np.array([DIRS.index(tuple(vin[i])) for i in range(n)]); do = np.array([DIRS.index(tuple(vout[i])) for i in range(n)])
    out = np.where(ts[:, None] < a[None, :], di[None, :], np.where(ts[:, None] > b[None, :], do[None, :], -1))
    return out
def pair_ok(T1, T2, shift, W, far=1500):
    """vrai si la condition fine tient pour T1(t) et T2(t − shift), t ∈ [−8 far, W + shift + 8 far] ; renvoie aussi la plus petite
    distance « hors libre-libre » et la plus petite distance libre-libre"""
    lo = min(0, shift) - 8 * far; hi = max(W, W + shift) + 8 * far
    ts = np.arange(lo, hi); worst_strict = 10 ** 9; worst_free = 10 ** 9; ok = True
    for s0 in range(0, len(ts), 4000):
        tt = ts[s0:s0 + 4000]
        X1, F1 = freemask(T1, W, tt); X2, F2 = freemask(T2, W, tt - shift)
        d1 = dirs_of(T1, tt, W); d2 = dirs_of(T2, tt - shift, W)
        D = hdist(X1[:, :, None, :] - X2[:, None, :, :])
        FF = F1[:, :, None] & F2[:, None, :]
        par = (d1[:, :, None] == d2[:, None, :]) & (d1[:, :, None] >= 0)
        need = np.where(FF, np.where(par, 3, 2), 7)
        if (D < need).any(): ok = False
        if (~FF).any(): worst_strict = min(worst_strict, int(np.where(~FF, D, 10 ** 9).min()))
        if FF.any(): worst_free = min(worst_free, int(np.where(FF, D, 10 ** 9).min()))
    # bouts : les distances doivent être non décroissantes à chaque extrémité (sinon le minimum serait au-delà)
    for t0, sg in ((lo, -1), (hi - 1, 1)):
        for c in range(8):
            ta = np.array([t0 + sg * c, t0 + sg * (c + 8)])
            X1 = posarr(T1, ta, W); X2 = posarr(T2, ta - shift, W)
            D = hdist(X1[:, :, None, :] - X2[:, None, :, :])
            if (D[1] < D[0]).any(): ok = False
    return ok, worst_strict, worst_free
def certificat_fin(C, k, W, J=10, log=print):
    K8 = k * 8; TR = {}
    for inp in C.cases(): TR[tuple(sorted(inp.items()))] = traj(C, inp, W)
    keys = list(TR); per = []; allok = True
    for j in range(1, J + 1):
        oks, ws, wf = True, 10 ** 9, 10 ** 9
        for a in keys:
            for b in keys:
                ok, s_, f_ = pair_ok(TR[a], TR[b], j * K8, W); oks &= ok; ws = min(ws, s_); wf = min(wf, f_)
        per.append((oks, ws, wf)); allok &= oks; log(f'écart {j} : condition fine {oks}, distance min (non libres) {ws}, (libres) {wf}')
    def droite(T, i, out):
        P, vin, vout = T; v = tuple(vout[i] if out else vin[i]); p = P[W][i] if out else P[0][i]
        r = DIRS.index(v); X, Y = rot((int(p[0]), int(p[1])), -r % 6); return r, X + Y
    S = {droite(TR[a], i, True) for a in keys for i in range(TR[a][0].shape[1])}
    E = {droite(TR[a], i, False) for a in keys for i in range(TR[a][0].shape[1])}
    fronts = [(s, e) for s in S for e in E if (s[0] - e[0]) % 6 == 3 and -5 <= s[1] + e[1] <= 3]   # bande [−3, 1] élargie de 2 (voie mesurée sur la fourmi, pas sur le point de référence)
    return allok and not fronts, per, fronts

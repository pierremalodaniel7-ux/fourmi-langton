"""R-344+ Circuits R2L2 réutilisables : description générique, usages répétés, test de superposition, certificat « tout nombre d'usages ».
Un circuit = liste ordonnée (ordre de jeu) de pièces-vaisseaux (fourmi, cases), chacune constante ou attachée à une entrée.
Un usage u est la copie du circuit reculée de u·k périodes sur les routes (chaque pièce recule le long de SA route).
Superposition exacte : l'état final de N usages = réunion des états finaux des usages faits seuls (décalés) — critère de R-337.
Certificat (comme R-338) : distance minimale EXACTE, sur toute la droite des temps, entre fourmis de deux usages ; > 6 ⇒ aucun usage
ne voit jamais un autre ⇒ N usages = superposition, pour tout N (avec la condition « pas de paire de routes de face »)."""
import itertools, json, numpy as np
from fa_lib import lotdump, decode, sit, back, pyrun, parts_of
from hx import step, rot
from exp_osc import hd
class Circuit:
    def __init__(self, pieces, outputs=None):
        """pieces : liste de (nom, pièce, entrée ou None) dans l'ordre de jeu ; outputs : dict nom -> (fonction des entrées, positions)"""
        self.pieces = pieces; self.vars = sorted({v for _, _, v in pieces if v})
        self.outputs = outputs or {}
    def cases(self):
        return [dict(zip(self.vars, bits)) for bits in itertools.product((0, 1), repeat=len(self.vars))]
    def parts(self, inp, u=0, k=200):
        return [back(p, u * k) for _, p, v in self.pieces if v is None or inp.get(v)]
    def sit(self, inp, u=0, k=200): return sit(self.parts(inp, u, k))
    def multi(self, seq, k=200):
        P = []
        for u, inp in enumerate(seq): P += self.parts(inp, u, k)
        return sit(P)
def shiftsh(s, n):
    """un vaisseau décodé (r, voie, abscisse, phase) d'un usage reculé de n périodes : abscisse − 2n"""
    return (s[0], s[1], s[2] - 2 * n, s[3])
def read(C, ships, u=0, k=200, extra=0):
    """valeurs des sorties lues dans une liste de vaisseaux décodés, pour l'usage u ; positions de référence données au temps T0 = 4000
    pour l'usage 0 ; extra = nombre de périodes simulées en plus de T0"""
    S = set(map(tuple, ships))
    return {o: int(any(shiftsh(p, u * k - extra) in S for p in pos)) for o, (f, pos) in C.outputs.items()}
def check_cases(C, T, engine2=True):
    """tous les cas : propres ? sorties justes ? 2 moteurs identiques ?"""
    res = []
    L = [C.sit(inp) for inp in C.cases()]
    R = lotdump(L, T)
    for inp, s, r in zip(C.cases(), L, R):
        d = decode(*r); ok = d is not None
        got = read(C, d) if ok else None
        want = {o: f(inp) for o, (f, pos) in C.outputs.items()}
        same = None
        if engine2:
            pa, pc = pyrun(s, T); same = sorted(pa) == sorted(map(tuple, r[0])) and sorted(pc) == sorted(map(tuple, r[1]))
        res.append((inp, ok and got == want, got, same))
    return res
def check_multi(C, seq, k, T0=4000, engine2=False):
    """N usages dans UNE simulation : superposition exacte ? sorties justes ? (2e moteur en option)"""
    T = len(seq) * k * 8 + T0
    s = C.multi(seq, k); r = lotdump([s], T)[0]; d = decode(*r)
    singles = lotdump([C.sit(inp) for inp in seq], T)
    union = []
    for u, rr in enumerate(singles):
        dd = decode(*rr); union += [shiftsh(x, u * k) for x in dd] if dd else [None]
    sup = d is not None and sorted(map(tuple, d)) == sorted(union)
    good = 0
    for u, inp in enumerate(seq):
        want = {o: f(inp) for o, (f, pos) in C.outputs.items()}
        good += read(C, d or [], u, k, len(seq) * k) == want
    same = None
    if engine2:
        pa, pc = pyrun(s, T); same = sorted(pa) == sorted(map(tuple, r[0])) and sorted(pc) == sorted(map(tuple, r[1]))
    return sup, good, same, s
# ---------------- certificat ----------------
DIRS = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
def traj(C, inp, W):
    a, c = parts_of(C.sit(inp)); A = [list(x) for x in a]; G = {tuple(x[:2]): 1 for x in c}
    P = [[tuple(x[:2]) for x in A]]
    for t in range(W + 8):
        step(A, G); P.append([tuple(x[:2]) for x in A])
    P = np.array(P)                                    # (W+9, n, 2)
    vin = P[8] - P[0]; vout = P[W + 8] - P[W]
    for t in range(0, 64): assert (P[t + 8] - P[t] == vin).all(), ('entrée non rectiligne', inp)
    for t in range(W - 64, W): assert (P[t + 8] - P[t] == vout).all(), ('sortie non rectiligne', inp)
    return P, vin, vout
def posarr(T, ts, W):
    """positions (len(ts), n, 2) pour des temps quelconques (extrapolation exacte des bouts rectilignes)"""
    P, vin, vout = T; out = np.empty((len(ts), P.shape[1], 2), dtype=np.int64)
    for k, t in enumerate(ts):
        if t < 0:
            m = (-t + 7) // 8; out[k] = P[t + 8 * m] - m * vin
        elif t > W + 8:
            m = (t - W) // 8; tt = t - 8 * m
            if tt > W + 8: tt -= 8; m += 1
            out[k] = P[tt] + m * vout
        else: out[k] = P[t]
    return out
def hdist(D):
    return (np.abs(D[..., 0]) + np.abs(D[..., 1]) + np.abs(D[..., 0] + D[..., 1])) // 2
def mind(T1, T2, shift, W, far=6000):
    """distance minimale entre fourmis de T1(t) et T2(t − shift) pour tout t ∈ Z : fenêtre balayée, puis bouts rectilignes
    (sur chaque classe t mod 8, la différence est affine : on prolonge tant que la distance n'augmente pas)."""
    lo = min(0, shift) - 16; hi = max(W, W + shift) + 24
    ts = np.arange(lo, hi)
    A = posarr(T1, ts, W); B_ = posarr(T2, ts - shift, W)
    best = int(hdist(A[:, :, None, :] - B_[:, None, :, :]).min())
    for t0, sg in ((lo, -1), (hi, 1)):
        for c in range(8):
            ta = t0 + sg * c
            d0 = hdist(posarr(T1, [ta], W)[0][:, None, :] - posarr(T2, [ta - shift], W)[0][None, :, :])
            d1 = hdist(posarr(T1, [ta + sg * 8 * far], W)[0][:, None, :] - posarr(T2, [ta + sg * 8 * far - shift], W)[0][None, :, :])
            # affine par morceaux et convexe (norme) : si d1 >= d0 la distance sur la demi-droite est ≥ min(d0, minimum intérieur) ;
            # on balaie m = 0..far pour les paires qui ne s'éloignent pas
            bad = np.argwhere(d1 < d0 + 1)
            for i, j in bad:
                ms = np.arange(0, far + 1)
                tt = ta + sg * 8 * ms
                pa = posarr(T1, tt, W)[:, i]; pb = posarr(T2, tt - shift, W)[:, j]
                best = min(best, int(hdist(pa - pb).min()))
    return best
def certificat(C, k, W, J=10, log=print):
    K8 = k * 8; TR = {}
    for inp in C.cases(): TR[tuple(sorted(inp.items()))] = traj(C, inp, W)
    keys = list(TR); worst = 10 ** 9; per = []
    for j in range(1, J + 1):
        m = min(mind(TR[a], TR[b], j * K8, W) for a in keys for b in keys)
        per.append(m); worst = min(worst, m); log(f'écart {j} : distance min {m}')
    # paires de routes de face (sortie de l'usage u, entrée d'un usage ultérieur) : même axe, sens opposés, à ≤ 6 voies
    def droite(T, i, out):
        P, vin, vout = T; v = tuple(vout[i] if out else vin[i]); p = P[W][i] if out else P[0][i]
        r = DIRS.index(v); X, Y = rot((int(p[0]), int(p[1])), -r % 6); return r, X + Y
    S = {droite(TR[a], i, True) for a in keys for i in range(TR[a][0].shape[1])}
    E = {droite(TR[a], i, False) for a in keys for i in range(TR[a][0].shape[1])}
    fronts = [(s, e) for s in S for e in E if (s[0] - e[0]) % 6 == 3 and abs(s[1] + e[1]) <= 6]
    return worst, per, fronts

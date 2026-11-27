#!/usr/bin/env python3
"""R-622 CIRCUIT GÉNÉRAL de vaisseaux R2L2 (S3/T1, 27/11) : portes à 60° (nor.BASE) entre un vaisseau K (sur sa ligne) et un partenaire P
(sur la sienne) ; contrairement à nor.Layout (arbre), un vaisseau peut être le partenaire d'une porte APRÈS avoir été dévié (débris
réutilisé = copie, routage) : c'est un graphe, pas un arbre.
Modèle logique (le même que diag2, R-610) : à l'instant t de la porte, si K est sur sa ligne ET P sur la sienne, K part sur oB et P
sur oA ; sinon chacun continue tout droit. Chaque segment de ligne d'univers reçoit le MASQUE des cas où il existe.
Vérification : simulation complète (moteur C et hx.py) ; l'état final doit être EXACTEMENT l'ensemble des lignes prévues par le
modèle (donc aucun débris inattendu, et chaque valeur intermédiaire est lisible sur une ligne précise)."""
import itertools
import numpy as np
from s3lib import *
from diag import pmin, INF
from nor import BASE, TC
_PM = {}   # mémo des distances minimales entre segments (même couple de segments -> même résultat)
class Circ:
    def __init__(self, vars_):
        self.vars = list(vars_); self.cases = [dict(zip(self.vars, b)) for b in itertools.product((0, 1), repeat=len(self.vars))]
        self.full = (1 << len(self.cases)) - 1
        self.ships = []      # (id, ligne à t = 0, masque de présence à t = 0)
        self.gates = []      # (t, K id, K ligne, P id, P ligne, oA, oB, étiquette)
        self.n = 0
    def mask_of(self, f):
        m = 0
        for b, e in enumerate(self.cases):
            if f(e): m |= 1 << b
        return m
    def add_ship(self, line, mask=None, name=None):
        i = name or f's{self.n}'; self.n += 1
        self.ships.append((i, line, self.full if mask is None else mask)); return i
    def add_gate(self, t, K, Kl, P, Pl, oA, oB, tag=''):
        self.gates.append((t, K, Kl, P, Pl, oA, oB, tag))
    def compile(self, T):
        """segments (id, ligne, t0, t1, masque) jusqu'à T ; self.at_T = {(id, ligne): masque} à l'instant T"""
        cur = {}; segs = []
        for i, w, m in self.ships: cur[(i, w)] = (0, m)
        for t, K, Kl, P, Pl, oA, oB, tag in sorted(self.gates, key=lambda g: g[0]):
            tK, mK = cur.get((K, Kl), (t, 0)); tP, mP = cur.get((P, Pl), (t, 0)); both = mK & mP
            if mK: segs.append((K, Kl, tK, t, mK))
            if mP: segs.append((P, Pl, tP, t, mP))
            cur[(K, Kl)] = (t, mK & ~both); cur[(P, Pl)] = (t, mP & ~both)
            for key, mm in (((K, oB), both), ((P, oA), both)):
                if mm:
                    t0, m0 = cur.get(key, (t, 0)); assert m0 == 0, ('ligne déjà occupée', key)
                    cur[key] = (t, mm)
        self.at_T = {}
        for (i, w), (t0, m) in cur.items():
            if m: segs.append((i, w, t0, T, m)); self.at_T[(i, w)] = m
        self.segs = segs; self.T = T
        return segs
    def present(self, i, w, t):
        """masque des cas où le vaisseau i est sur la ligne w à l'instant t"""
        m = 0
        for j, ww, a, b, mm in self.segs:
            if j == i and ww == w and a <= t <= b: m |= mm
        return m
    def conflicts(self, thr=7, guard=80, only=None):
        """couples de segments (vaisseaux différents, cas communs) à < thr, hors chocs voulus (même couple K,P à ±guard de la porte)"""
        S = self.segs; gt = {}
        for g in self.gates: gt.setdefault(frozenset((g[1], g[3])), []).append(g[0])
        box = []
        for i, w, a, b, m in S:
            p, q = antpos(w, a), antpos(w, b)
            box.append((a, b, min(p[0], q[0]) - thr - 4, max(p[0], q[0]) + thr + 4, min(p[1], q[1]) - thr - 4, max(p[1], q[1]) + thr + 4))
        B = np.array(box, dtype=np.int64); out = []
        idx = range(len(S)) if only is None else only
        for x in idx:
            A = B[x]
            cand = np.nonzero((B[:, 0] <= A[1]) & (B[:, 1] >= A[0]) & (B[:, 2] <= A[3]) & (B[:, 3] >= A[2]) & (B[:, 4] <= A[5]) & (B[:, 5] >= A[4]))[0]
            for y in cand:
                if y <= x and (only is None or y in only): continue
                a, b = S[x], S[y]
                if a[0] == b[0] or not (a[4] & b[4]): continue
                key = (a[1], a[2], a[3], b[1], b[2], b[3])
                r = _PM.get(key)
                if r is None:
                    r = pmin(a[1], a[2], a[3], b[1], b[2], b[3], thr)
                    if len(_PM) > 2_000_000: _PM.clear()
                    _PM[key] = r
                m, t = r
                if m < thr:
                    tg = gt.get(frozenset((a[0], b[0])))
                    if tg is not None and any(abs(t - z) <= guard for z in tg): continue
                    out.append((a[0], b[0], m, t))
        return out
    def situation(self, b):
        """situation fourmi_r du cas b (ordre de jeu = ordre d'ajout)"""
        return sit_wls([w for i, w, m in self.ships if m >> b & 1])
    def expected(self, b):
        return sorted(w for (i, w), m in self.at_T.items() if m >> b & 1)
    def check(self, cases=None, engine2=False):
        """simule les cas (indices) jusqu'à self.T ; renvoie [(cas, état final = prévu ?, 2 moteurs identiques ?)]"""
        cases = range(len(self.cases)) if cases is None else cases
        S = [self.situation(b) for b in cases]; R = run_c(S, self.T); out = []
        for b, s, (a, c) in zip(cases, S, R):
            d = decode(a, c, self.T); ok = d is not None and sorted(d) == self.expected(b); same = None
            if engine2:
                pa, pc = run_py(s, self.T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
            out.append((b, ok, same))
        return out
def gate_geom(Kl, side, t):
    """comme nor.gate : la puissance K donnée, le partenaire heurte K vers l'instant t -> (P ligne, oA, oB, instant)"""
    from nor import gate
    return gate(Kl, side, t)
def turn(A, side, k):
    """le partenaire A donné : puissance K pour le k-ième instant de choc possible -> (K, oA, oB, instant)"""
    b = BASE[side]; rk = (A[0] - b['A'][0]) % 6
    B0, A0, oA0, oB0 = (rotwl(b[x], rk) for x in ('B', 'A', 'oA', 'oB'))
    s0 = next(s for s in range(8) if tshift(A0, s)[3] == A[3]); s = s0 + 8 * k
    As = tshift(A0, s); v = (A[1] - As[1], A[2] - As[2])
    f = lambda w: transwl(tshift(w, s), v)
    return f(B0), f(oA0), f(oB0), s + TC
def first_k(A, side, tmin):
    """plus petit k tel que le choc ait lieu après tmin"""
    _, _, _, t0 = turn(A, side, 0); return max(0, -((t0 - tmin) // 8))
TYPES = [(s, o) for s in '+-H' for o in (0, 1, 2)]   # o = 1 : suivre oA (le signal dévié) ; 2 : oB (la puissance déviée) ; 0 : K tout droit (= NON)
def follow(A, seq, ks):
    w = A; out = []
    for (side, o), k in zip(seq, ks):
        K, oA, oB, t = turn(w, side, k); out.append((K, w, side, t, oA, oB)); w = (oA, oB, K)[o - 1] if o else K
    return w, out
def solve2(A, seq, W, kfix=()):
    """k des 2 DERNIERS virages pour arriver exactement sur W (les premiers virages fixés par kfix) ; None si impossible"""
    n = len(seq); base = list(kfix) + [0, 0]
    w0, _ = follow(A, seq, base)
    if w0[0] != W[0] or w0[3] != W[3]: return None
    e1 = list(base); e1[n - 2] = 1; e2 = list(base); e2[n - 1] = 1
    w1, _ = follow(A, seq, e1); w2, _ = follow(A, seq, e2)
    a, c = w1[1] - w0[1], w1[2] - w0[2]; b, d = w2[1] - w0[1], w2[2] - w0[2]
    det = a * d - b * c
    if det == 0: return None
    rx, ry = W[1] - w0[1], W[2] - w0[2]
    k1n, k2n = d * rx - b * ry, -c * rx + a * ry
    if k1n % det or k2n % det: return None
    ks = list(kfix) + [k1n // det, k2n // det]
    w, out = follow(A, seq, ks); assert w == W
    return ks, out
SH = {}
for _t in TYPES:
    _A = (1, -25, 0, 4); _K, _oA, _oB, _ = turn(_A, _t[0], 0); _w = (_oA, _oB)[_t[1] - 1] if _t[1] else _K
    SH[_t] = ((_w[0] - _A[0]) % 6, (_w[3] - 4 * _w[0] - (_A[3] - 4 * _A[0])) % 8, 1 if _t[1] == 0 else 0)
def cls(w): return (w[3] - 4 * w[0]) % 8
def seqs(A, W, pol, n):
    """suites de n virages compatibles (direction, classe de phase, parité des NON) de A vers W"""
    dd, dc = (W[0] - A[0]) % 6, (cls(W) - cls(A)) % 8
    for seq in itertools.product(TYPES, repeat=n):
        a = sum(SH[t][0] for t in seq) % 6; c = sum(SH[t][1] for t in seq) % 8; p = sum(SH[t][2] for t in seq) % 2
        if a == dd and c == dc and p == pol: yield seq
def route(A, tA, W, tW, pol=0, gap=120, early=200, kr=60, ntur=(2, 3, 4), maxsol=200, step=None):
    """suites de virages de A (disponible dès tA) jusqu'à W (rejointe avant tW − early), chocs espacés d'au moins gap ;
    pol = 1 : le signal arrive inversé. Les virages libres (tous sauf les 2 derniers) sont pris aux instants tA + gap + 8·j·step
    (j < kr) après le choc précédent ; les 2 derniers sont résolus exactement. Renvoie les solutions (durée, types, ks, détails)."""
    sols = []
    for n in ntur:
        st = step or (6 if n == 3 else 10)
        for seq in seqs(A, W, pol, n):
            def rec(kf, w, tprev):
                if len(kf) == n - 2:
                    r = solve2(A, seq, W, tuple(kf))
                    if r is None: return
                    ks, out = r; ts = [o[3] for o in out]
                    if ts[0] < tA + gap or ts[-1] > tW - early or any(ts[q + 1] - ts[q] < gap for q in range(len(ts) - 1)): return
                    sols.append((ts[-1] - ts[0], seq, ks, out)); return
                side, o = seq[len(kf)]; k0 = first_k(w, side, tprev + gap)
                for jj in range(kr):
                    if len(sols) >= maxsol: return
                    k = k0 + jj * st; K, oA, oB, t = turn(w, side, k)
                    if t > tW: return
                    rec(kf + [k], (oA, oB, K)[o - 1] if o else K, t)
            rec([], A, tA)
            if len(sols) >= maxsol: break
    sols.sort(key=lambda z: z[0])
    return sols

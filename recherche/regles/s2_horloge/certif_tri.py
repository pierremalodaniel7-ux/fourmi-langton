"""S2 R-500 — CERTIFICAT : la famille triangle (famille.py) donne un CYCLE exact pour TOUT j ≥ j0 (dans chaque classe de parité).
Méthode (tout en entiers / fractions exactes) :
 1. Pour i = 0, 1, 2 (j = p + 2(i0 + i)), simulation exacte (hx.py) sur une période P ; chaque fourmi est « libre » quand c'est un
    vaisseau propre à distance > FREE de toutes les autres fourmis ; sinon elle est dans un « événement » (composante connexe
    (fourmi, temps) des fourmis non libres proches). Segments libres = (vaisseau virtuel, début, fin).
 2. Structure identique pour i = 0, 1, 2 et AFFINE en i (vaisseaux virtuels, temps, centres d'événements) ; chaque événement de i+1 est le
    translaté exact (espace-temps) de celui de i (mêmes entrées translatées ⇒ même évolution translatée, la règle étant invariante).
 3. Séparation pour tout i ≥ 0 par CONVEXITÉ : le centre continu x(t) d'un vaisseau est affine en (t, i) ; la distance hexagonale est
    une norme, donc m(i) = min_t dist est convexe en i ; m(0) ≥ seuil et m(1) ≥ m(0) ⇒ m(i) ≥ seuil pour tout i ≥ 0.
    Seuils : vaisseau–vaisseau, fourmis à ≥ 7 ; vaisseau–événement, fourmi à ≥ rayon + 7 du centre ; événement–événement simultanés.
 4. Fermeture : l'état au temps P (vaisseaux virtuels) = l'état au temps 0 : identité affine en i vraie pour i = 0, 1 (et 2) ⇒ pour tout i.
 ⇒ récurrence sur le temps : pour tout i, l'évolution réelle = l'évolution symbolique, et l'état revient exactement au temps P(i).
Usage : python3 s2_horloge/certif_tri.py parité i0"""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from famille import terme, P_attendu
from fa_lib import parts_of
from hx import step, ship_dir, PHASES
from demi_add_k import OFFS
from tri import virt
FREE = 14
FREE_BAS = 10
RHO = Fr(13, 8)
def hd(x, y): return (abs(x) + abs(y) + abs(x + y)) / 2
def analyse(j):
    T, c, s = terme(j); P = P_attendu(j)
    a, cs = parts_of(s); A = [list(t) for t in a]; G = {tuple(t): 1 for t in cs}; n = len(A)
    hist = []   # par temps : liste (virt ou None, pos, dmin) ; libre = vaisseau propre et dmin > FREE (hystérésis : > FREE_BAS si déjà libre, même vaisseau)
    prev = [None] * n
    for t in range(P + 1):
        row = []
        for k, (x, y, h) in enumerate(A):
            dmin = min(hd(x - b[0], y - b[1]) for l, b in enumerate(A) if l != k)
            v = None
            if dmin > FREE_BAS:
                v, near = virt((x, y, h), G, t)
                if v is not None and not (dmin > FREE or v == prev[k]): v = None
            row.append((v, (x, y), dmin)); prev[k] = v
        # cases non expliquées par les vaisseaux libres
        hist.append((row, set(G)))
        if t < P: step(A, G)
    return P, hist, n
def structure(j):
    P, hist, n = analyse(j)
    # segments
    segs = [[] for _ in range(n)]
    for t, (row, _) in enumerate(hist):
        for k, (v, p, d) in enumerate(row):
            if v is not None and segs[k] and segs[k][-1][0] == v and segs[k][-1][2] == t - 1: segs[k][-1][2] = t
            elif v is not None: segs[k].append([v, t, t])
    # événements : union-find sur (k, t) non libres
    par = {}
    def f(u):
        while par[u] != u: par[u] = par[par[u]]; u = par[u]
        return u
    for t, (row, _) in enumerate(hist):
        nf = [k for k in range(n) if row[k][0] is None]
        for k in nf:
            par[(k, t)] = (k, t)
            if t > 0 and hist[t - 1][0][k][0] is None: par[f((k, t))] = f((k, t - 1))
        for k, l in itertools.combinations(nf, 2):
            if hd(row[k][1][0] - row[l][1][0], row[k][1][1] - row[l][1][1]) <= FREE: par[f((k, t))] = f((l, t))
    comps = {}
    for u in par: comps.setdefault(f(u), []).append(u)
    evs = []
    for L in comps.values():
        ws = min(t for k, t in L); we = max(t for k, t in L); parts = sorted({k for k, t in L})
        z = hist[ws][0][parts[0]][1]
        # rayon : fourmis participantes et cases non portées par un vaisseau libre, pendant [ws, we]
        rad = 0
        for t in range(ws, we + 1):
            row, cells = hist[t]
            for k in parts: rad = max(rad, hd(row[k][1][0] - z[0], row[k][1][1] - z[1]))
            for q in cells:   # cases proches d'un participant (≤ FREE) et pas à ≤ 2 d'une fourmi libre
                if any(hd(q[0] - row[k][1][0], q[1] - row[k][1][1]) <= FREE for k in parts) and \
                   not any(row[k][0] is not None and hd(q[0] - row[k][1][0], q[1] - row[k][1][1]) <= 2 for k in range(n)):
                    rad = max(rad, hd(q[0] - z[0], q[1] - z[1]))
        evs.append({'ws': ws, 'we': we, 'parts': parts, 'z': z, 'rad': rad})
    evs.sort(key=lambda e: (e['ws'], e['parts']))
    return P, segs, evs, hist
def center(v, t):
    r, p, tau = v; d = ship_dir(r); s = Fr(tau + t, 8)
    return (p[0] + s * d[0], p[1] + s * d[1])
def mind(f1, f2, a, b):
    """min sur t ∈ [a, b] (réel) de hd(f1(t) − f2(t)), f affines en t : extrémités + points de rupture"""
    if a > b: return None
    def g(t):
        p, q = f1(t), f2(t); return hd(p[0] - q[0], p[1] - q[1])
    p0, q0 = f1(a), f2(a); p1, q1 = f1(a + 1), f2(a + 1)
    dx0, dy0 = p0[0] - q0[0], p0[1] - q0[1]; vx, vy = (p1[0] - q1[0]) - dx0, (p1[1] - q1[1]) - dy0
    cand = [a, b]
    for u0, w in ((dx0, vx), (dy0, vy), (dx0 + dy0, vx + vy)):
        if w != 0:
            tt = a - Fr(u0) / w
            if a <= tt <= b: cand.append(tt)
    return min(g(Fr(t)) for t in cand)
def lin(xs):
    """xs = valeurs pour i = 0, 1, 2 (nombres ou tuples imbriqués) : affine ?"""
    if isinstance(xs[0], (tuple, list)): return all(lin([x[k] for x in xs]) for k in range(len(xs[0])))
    return xs[2] - xs[1] == xs[1] - xs[0]
if __name__ == '__main__':
    par_, i0 = int(sys.argv[1]), int(sys.argv[2])
    S = [structure(par_ + 2 * (i0 + i)) for i in range(3)]
    ok = True
    def bad(*m):
        global ok; ok = False; print('ÉCHEC', *m)
    # 2. structure
    n = len(S[0][1])
    for k in range(n):
        if len({len(s[1][k]) for s in S}) != 1: bad('nb de segments', k)
    if len({len(s[2]) for s in S}) != 1: bad('nb d\'événements')
    if not ok: sys.exit(1)
    for k in range(n):
        for q in range(len(S[0][1][k])):
            vs = [s[1][k][q] for s in S]
            if len({v[0][0] for v in vs}) != 1 or len({v[0][2] for v in vs}) != 1: bad('dir/phase', k, q)
            if not lin([v[0][1] for v in vs]) or not lin([v[1] for v in vs]) or not lin([v[2] for v in vs]): bad('non affine', k, q, vs)
    for q in range(len(S[0][2])):
        es = [s[2][q] for s in S]
        if len({tuple(e['parts']) for e in es}) != 1 or len({e['rad'] for e in es}) != 1 or len({e['we'] - e['ws'] for e in es}) != 1: bad('événement', q)
        if not lin([e['ws'] for e in es]) or not lin([e['z'] for e in es]): bad('événement non affine', q)
        # translation exacte de l'évolution locale : positions des participants, relatives à z, au même temps relatif
        for i in (1, 2):
            e0, e1 = es[0], es[i]
            for dt in range(e0['we'] - e0['ws'] + 1):
                r0 = S[0][3][e0['ws'] + dt][0]; r1 = S[i][3][e1['ws'] + dt][0]
                for k in e0['parts']:
                    p0 = (r0[k][1][0] - e0['z'][0], r0[k][1][1] - e0['z'][1]); p1 = (r1[k][1][0] - e1['z'][0], r1[k][1][1] - e1['z'][1])
                    if p0 != p1: bad('événement non translaté', q, i, dt, k); break
    if not ok: sys.exit(1)
    P = [s[0] for s in S]
    # 3. séparation par convexité (i = 0 et i = 1)
    seuil_vv = 7 + 2 * RHO; npair = 0; worst = 99
    def segf(s, k, q):
        v = s[1][k][q][0]; return (lambda t, v=v: center(v, t))
    for k, l in itertools.combinations(range(n), 2):
        for q1 in range(len(S[0][1][k])):
            for q2 in range(len(S[0][1][l])):
                m = []
                for i in range(3):
                    s = S[i]; a = max(s[1][k][q1][1], s[1][l][q2][1]); b = min(s[1][k][q1][2], s[1][l][q2][2])
                    m.append(mind(segf(s, k, q1), segf(s, l, q2), Fr(a), Fr(b)))
                if all(x is None for x in m): continue
                if any(x is None for x in m): bad('recouvrement variable', k, l, q1, q2, m); continue
                npair += 1; worst = min(worst, m[0])
                if m[0] < seuil_vv or m[1] < m[0]: bad('séparation', k, l, q1, q2, [float(x) for x in m])
    nev = 0
    for q in range(len(S[0][2])):
        for k in range(n):
            if k in S[0][2][q]['parts']: continue
            for q2 in range(len(S[0][1][k])):
                m = []
                for i in range(3):
                    s = S[i]; e = s[2][q]; sg = s[1][k][q2]
                    a = max(e['ws'], sg[1]); b = min(e['we'], sg[2]); z = e['z']
                    m.append(mind(segf(s, k, q2), lambda t, z=z: z, Fr(a), Fr(b)))
                if all(x is None for x in m): continue
                if any(x is None for x in m): bad('recouvrement variable (év)', q, k, m); continue
                nev += 1
                need = S[0][2][q]['rad'] + 7 + RHO
                if m[0] < need or m[1] < m[0]: bad('séparation événement', q, k, [float(x) for x in m], float(need))
        for q2 in range(q + 1, len(S[0][2])):
            m = []
            for i in range(3):
                e, f_ = S[i][2][q], S[i][2][q2]
                if max(e['ws'], f_['ws']) <= min(e['we'], f_['we']): m.append(hd(e['z'][0] - f_['z'][0], e['z'][1] - f_['z'][1]))
                else: m.append(None)
            if all(x is None for x in m): continue
            if any(x is None for x in m): bad('simultanéité variable', q, q2); continue
            need = S[0][2][q]['rad'] + S[0][2][q2]['rad'] + 7
            if m[0] < need or m[1] < m[0]: bad('événements proches', q, q2, m, need)
    # 3b. toute case noire est portée par un vaisseau libre (≤ 2 de sa fourmi) ou par un événement actif (≤ FREE d'un participant)
    for i in range(3):
        P_, segs_, evs_, h = S[i]
        act = {}
        for e in evs_:
            for t in range(e['ws'], e['we'] + 1): act.setdefault(t, set()).update(e['parts'])
        for t, (row, cells) in enumerate(h):
            for q in cells:
                if not any((row[k][0] is not None and hd(q[0] - row[k][1][0], q[1] - row[k][1][1]) <= 2) or
                           (k in act.get(t, ()) and hd(q[0] - row[k][1][0], q[1] - row[k][1][1]) <= FREE) for k in range(n)):
                    bad('case orpheline', i, t, q); break
    # 4. fermeture : état à P = état à 0 (vérifié dans la simulation exacte pour chaque i)
    for i in range(3):
        h = S[i][3]
        if [r[1] for r in h[0][0]] != [r[1] for r in h[-1][0]] or h[0][1] != h[-1][1]: bad('fermeture', i)
    print('parité', par_, 'i0', i0, 'j =', [par_ + 2 * (i0 + i) for i in range(3)], 'P =', P,
          '| segments', sum(len(x) for x in S[0][1]), 'événements', len(S[0][2]), 'paires contrôlées', npair, '+', nev,
          '| plus petite distance (centres)', float(worst), '| CERTIFICAT', 'OK' if ok else 'ÉCHEC')
    for e in S[0][2]: print('   év', e['ws'], e['we'], e['parts'], 'z', e['z'], 'rayon', e['rad'])

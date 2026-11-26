#!/usr/bin/env python3
"""R-703 Géométrie de l'écran 2×2 : port « mise à 1 » = le démultiplexeur R-702 ; port « mise à 0 » = le même tourné de 120° (+2 crans)
et translaté de v. Pixel j (adresse j) : bascule R-341 tournée de rho_j = direction de la sortie O_j, centrée au point c_j où la sortie
O_j du port 1 passe sur la voie de mise à 1 ET la sortie O'_j du port 0 sur la voie de mise à 0 (intersection de deux droites du
réseau : toujours un point entier). On cherche v tel que : pixels séparés ; chaque pixel loin (≥ DPIX) de tous les rayons de tous
les cas des deux ports, sauf ses deux rayons ; pixel atteint après le dernier choc du port ; aucune paire de face entre ports.
Usage : python3 ecran_geo.py [rayon de recherche de v] -> ecran_geo.json"""
import sys, json, itertools, numpy as np
from traj import *
from rayons import head_on
import pixel
RV = int(sys.argv[1]) if len(sys.argv) > 1 else 60
DPIX = 11
REP = json.load(open(HERE + '/demux_retenu.json')); B = REP['B']
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
def tt(x): return norm(tuple(x))
INS = [tt(v) for v in B['T'].values()]; EXP = {c: [tt(t) for t in B['exp'][str(c)]] for c in CASES}
OUT = {c: tt(o) for c, o in zip(CASES, B['outs4'])}
T0, T1 = min(B['times'].values()), max(B['times'].values())
def port(T, rho, v): return movT(rotT(T, rho), v, 0)
def lanevec(r): return (to_label(movT((r, 0, 0, 0), (1, 0)))[1] - to_label((r, 0, 0, 0))[1], to_label(movT((r, 0, 0, 0), (0, 1)))[1] - to_label((r, 0, 0, 0))[1])
LV = [lanevec(r) for r in range(6)]
def center(Oset, Orst):
    """centre c du pixel : la mise à 1 tournée (direction de Oset) suit la voie de Oset, la mise à 0 celle de Orst"""
    rho = Oset[0]; S = rotT(pixel.SET['S'], rho); R = rotT(pixel.RST['S'], rho)
    assert R[0] == Orst[0]
    b1 = to_label(Oset)[1] - to_label(S)[1]; b2 = to_label(Orst)[1] - to_label(R)[1]
    u, w = LV[rho], LV[R[0]]; det = u[0] * w[1] - u[1] * w[0]
    x = (b1 * w[1] - b2 * u[1]); y = (u[0] * b2 - w[0] * b1)
    if x % det or y % det: return None
    return (x // det, y // det), rho
def ray_arr(T, t0, t1):
    L = to_label(T); return np.array([antpos(L, t) for t in range(t0, t1)])
def hdn(D): return (np.abs(D[..., 0]) + np.abs(D[..., 1]) + np.abs(D[..., 0] + D[..., 1])) // 2
# rayons du port 1 (temps de l'usage) : entrées sur [T0-5000, T1], sorties sur [T0, T1+5000]
RAYS1 = [(T, 'in') for T in INS] + [(T, 'out') for c in CASES for T in EXP[c]]
def rays_of(rho, v):
    out = []
    for T, k in RAYS1:
        U = port(T, rho, v); t0, t1 = (T0 - 5000, T1) if k == 'in' else (T0, T1 + 5000)
        out.append((U, ray_arr(U, t0, t1)))
    return out
R1 = rays_of(0, (0, 0))
def rot_arr(A, k):
    x, y = A[:, 0].copy(), A[:, 1].copy()
    for _ in range(k % 6): x, y = -y, x + y
    return np.stack([x, y], 1)
R1rot = [(port(U, 2, (0, 0)), rot_arr(a, 2)) for U, a in R1]
OUTARR = {c: ray_arr(OUT[c], T0 - 2000, T1 + 5000) for c in CASES}
def evaluate(v):
    O2 = {c: port(OUT[c], 2, v) for c in CASES}
    cs = {}
    for c in CASES:
        r = center(OUT[c], O2[c])
        if r is None: return None
        cs[c] = r[0]
    P = list(cs.values())
    if min(hd(p[0] - q[0], p[1] - q[1]) for p, q in itertools.combinations(P, 2)) < 2 * DPIX: return None
    # head-on entre ports
    ins2 = [port(T, 2, v) for T in INS]; outs1 = [T for c in CASES for T in EXP[c]]; outs2 = [port(T, 2, v) for T in outs1]
    if head_on(outs1, ins2) or head_on(outs2, INS): return None
    R2 = [(movT(U, v, 0), a + np.array(v)) for U, a in R1rot]; worst = 10 ** 9
    for c, p in cs.items():
        pa = np.array(p)
        for (U, arr) in R1 + R2:
            if same(U, OUT[c]) or same(U, O2[c]): continue
            d = int(hdn(arr - pa).min()); worst = min(worst, d)
            if d < DPIX: return None
        # pixel atteint après le dernier choc de chaque port
        for Oc, arr in ((OUT[c], OUTARR[c]), (O2[c], rot_arr(OUTARR[c], 2) + np.array(v))):
            tmin = int(np.argmin(hdn(arr - pa))) + T0 - 2000
            if tmin < T1 + 80: return None
    span = max(max(hd(*p) for p in P), hd(*v))
    return {'v': v, 'centres': {str(c): cs[c] for c in CASES}, 'rho': {str(c): OUT[c][0] for c in CASES}, 'marge': worst, 'taille': span}
if __name__ == '__main__':
    res = []
    for vx in range(-RV, RV + 1):
        for vy in range(-RV, RV + 1):
            e = evaluate((vx, vy))
            if e: res.append(e)
    res.sort(key=lambda e: (e['taille'], -e['marge']))
    print(len(res), 'translations v possibles ;', res[:3])
    json.dump(res[:50], open(HERE + '/ecran_geo.json', 'w'), indent=1)

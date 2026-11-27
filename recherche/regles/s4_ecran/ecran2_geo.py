#!/usr/bin/env python3
"""R-704 Géométrie de l'écran 2×2 avec DEUX démultiplexeurs DIFFÉRENTS (data/demux_tries.json) : port « 1 » = démux A (fixe),
port « 0 » = démux B tourné de rho0 et translaté de v ; adresses du port 0 éventuellement permutées (π) ; rôles éventuellement
inversés (le port A fait les mises à 0). Pixel j = bascule R-341 au croisement (entier) de la voie de mise à 1 et de la voie de mise à 0.
Étape 1 (vectorisée, exacte) : centres en aval des deux ports (après le dernier choc + 12), centres séparés ≥ 2·DPIX.
Étape 2 : chaque pixel à ≥ DPIX de tous les rayons (entrées, sorties des 4 cas, des 2 ports) sauf ses 2 rayons ; aucune paire de face.
Usage : python3 ecran2_geo.py [RV] [nA] -> data/ecran2_geo.json"""
import sys, json, itertools, numpy as np
from traj import *
from rayons import head_on
import pixel
RV = int(sys.argv[1]) if len(sys.argv) > 1 else 150; NA = int(sys.argv[2]) if len(sys.argv) > 2 else 49
DPIX = 11; MARGE = 12
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
L = json.load(open(HERE + '/data/demux_tries.json'))
def tt(x): return norm(tuple(x))
def lanevec(r): return (to_label(movT((r, 0, 0, 0), (1, 0)))[1] - to_label((r, 0, 0, 0))[1], to_label(movT((r, 0, 0, 0), (0, 1)))[1] - to_label((r, 0, 0, 0))[1])
LV = [lanevec(r) for r in range(6)]
def alongv(X, Y, r):
    for _ in range((-r) % 6): X, Y = -Y, X + Y
    return X - Y
def ab(T, t): p = antpos(to_label(T), t); return along(p[0], p[1], T[0])
def info(B):
    O = [tt(o) for o in B['outs4']]; T1 = max(B['times'].values()); T0 = min(B['times'].values())
    return {'O': O, 'T0': T0, 'T1': T1, 'ins': [tt(v) for v in B['T'].values()], 'exp': {c: [tt(t) for t in B['exp'][str(c)]] for c in CASES}}
VX, VY = np.meshgrid(np.arange(-RV, RV + 1), np.arange(-RV, RV + 1)); VX = VX.ravel(); VY = VY.ravel()
def feasible(IA, IB, rho0, role):
    """renvoie la liste des (π, indices v) faisables à l'étape 1"""
    OA = IA['O']; OB = [rotT(o, rho0) for o in IB['O']]; res = []
    for perm in itertools.permutations(range(4)):
        ok = np.ones(len(VX), bool); C = []
        for j in range(4):
            a, b = OA[j], OB[perm[j]]
            rho = a[0] if role == 'set1' else (a[0] - 2) % 6
            Sk, Rk = rotT(pixel.SET['S'], rho), rotT(pixel.RST['S'], rho)
            if role == 'set1':
                if b[0] != Rk[0]: ok = None; break
                Ta, Ka, Tb, Kb = a, Sk, b, Rk
            else:
                if b[0] != Sk[0] or a[0] != Rk[0]: ok = None; break
                Ta, Ka, Tb, Kb = a, Rk, b, Sk
            b1 = to_label(Ta)[1] - to_label(Ka)[1]
            b2 = to_label(Tb)[1] - to_label(Kb)[1] + LV[Tb[0]][0] * VX + LV[Tb[0]][1] * VY
            u, w = LV[Ta[0]], LV[Tb[0]]; det = u[0] * w[1] - u[1] * w[0]
            x = (b1 * w[1] - b2 * u[1]); y = (u[0] * b2 - w[0] * b1)
            ok &= (x % det == 0) & (y % det == 0); x //= det; y //= det
            ok &= alongv(x, y, Ta[0]) >= ab(Ta, IA['T1'] + 80) + MARGE
            ok &= alongv(x - VX, y - VY, Tb[0]) >= ab(Tb, IB['T1'] + 80) + MARGE
            C.append((x, y))
        if ok is None: continue
        for i, j in itertools.combinations(range(4), 2):
            dx, dy = C[i][0] - C[j][0], C[i][1] - C[j][1]
            ok &= (np.abs(dx) + np.abs(dy) + np.abs(dx + dy)) // 2 >= 2 * DPIX
        idx = np.nonzero(ok)[0]
        if len(idx): res.append((perm, idx, C))
    return res
def hdn(D): return (np.abs(D[..., 0]) + np.abs(D[..., 1]) + np.abs(D[..., 0] + D[..., 1])) // 2
def ray_arr(T, t0, t1): Lb = to_label(T); return np.array([antpos(Lb, t) for t in range(t0, t1)])
def rays(I, rho0, v):
    out = []
    for T in I['ins']: U = movT(rotT(T, rho0), v); out.append((U, ray_arr(U, I['T0'] - 5000, I['T1'])))
    for c in CASES:
        for T in I['exp'][c]: U = movT(rotT(T, rho0), v); out.append((U, ray_arr(U, I['T0'], I['T1'] + 5000)))
    return out
def full_check(IA, IB, rho0, v, perm, cs):
    insA = IA['ins']; outsA = [T for c in CASES for T in IA['exp'][c]]
    insB = [movT(rotT(T, rho0), v) for T in IB['ins']]; outsB = [movT(rotT(T, rho0), v) for c in CASES for T in IB['exp'][c]]
    if head_on(outsA, insB) or head_on(outsB, insA): return None
    RA = rays(IA, 0, (0, 0)); RB = rays(IB, rho0, v); worst = 10 ** 9
    for j in range(4):
        own = (IA['O'][j], movT(rotT(IB['O'][perm[j]], rho0), v)); pa = np.array(cs[j])
        for U, arr in RA + RB:
            if same(U, own[0]) or same(U, own[1]): continue
            d = int(hdn(arr - pa).min()); worst = min(worst, d)
            if d < DPIX: return None
    return worst
if __name__ == '__main__':
    I = [info(B) for B in L]; found = []; n1 = 0
    for ia in range(min(NA, len(L))):
        for ib in range(len(L)):
            for rho0 in range(6):
                for role in ('set1', 'rst1'):
                    for perm, idx, C in feasible(I[ia], I[ib], rho0, role):
                        n1 += len(idx)
                        sizes = np.maximum(np.abs(VX[idx]), np.abs(VY[idx]))
                        for k in idx[np.argsort(sizes)][:3]:
                            v = (int(VX[k]), int(VY[k])); cs = [(int(C[j][0][k]), int(C[j][1][k])) for j in range(4)]
                            w = full_check(I[ia], I[ib], rho0, v, perm, cs)
                            if w is not None:
                                span = max(max(hd(*p) for p in cs), hd(*v))
                                found.append({'A': ia, 'B': ib, 'rho0': rho0, 'role': role, 'perm': perm, 'v': v, 'centres': cs, 'marge': w, 'taille': span})
                                print('trouvé', found[-1], flush=True); break
    found.sort(key=lambda e: (e['taille'], -e['marge']))
    print('étape 1 :', n1, 'placements ; étape 2 :', len(found))
    json.dump(found, open(HERE + '/data/ecran2_geo.json', 'w'), indent=1)

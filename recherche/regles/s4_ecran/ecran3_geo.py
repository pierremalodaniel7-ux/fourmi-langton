#!/usr/bin/env python3
"""R-706 Géométrie de l'écran 2×2, version « kit au choix par pixel » : chaque pixel (M/R' de R-341) peut être écrit par
(SET0 = dir 0 voie 1, RST2 = dir 2 voie −2) [R-341, écart +120°] ou (SET5 = dir 5 voie 1, RST3 = dir 3 voie −2) [R-705, écart −120°].
Avec un démux A à 2 directions voisines {θ, θ+60°}, on prend −120° pour les sorties θ et +120° pour θ+60° : les 4 cônes de faisabilité
deviennent le MÊME cône de 60° ⇒ intersection non vide (R-704 : avec un seul kit, il n'y a qu'un rayon commun).
Port 0 = démux B tourné de rho0, translaté de v (grille), adresses permutées π. Étapes 1 et 2 comme ecran2_geo.py.
Usage : python3 ecran3_geo.py RV [pas] -> data/ecran3_geo.json"""
import sys, json, itertools, numpy as np
RV = int(sys.argv[1]) if len(sys.argv) > 1 else 120; ST = int(sys.argv[2]) if len(sys.argv) > 2 else 1
sys.argv = [sys.argv[0], '1', '0']
import ecran2_geo as G
_x, _y = np.meshgrid(np.arange(-RV, RV + 1, ST), np.arange(-RV, RV + 1, ST)); G.VX = _x.ravel(); G.VY = _y.ravel()
from traj import *
import pixel
KS = {'SET0': pixel.kit(pixel.M, 0, 1, 16), 'SET5': pixel.kit(pixel.M, 5, 1, 4),
      'RST2': pixel.kit(pixel.R2, 2, -2, 2), 'RST3': pixel.kit(pixel.R2, 3, -2, 10)}
PAIRS = [('SET0', 'RST2'), ('SET5', 'RST3')]
def feasible(IA, IB, rho0, role):
    OA = IA['O']; OB = [rotT(o, rho0) for o in IB['O']]; res = []
    for perm in itertools.permutations(range(4)):
        for kc in itertools.product(range(2), repeat=4):
            ok = np.ones(len(G.VX), bool); C = []; info = []
            for j in range(4):
                a, b = OA[j], OB[perm[j]]; ks, kr = PAIRS[kc[j]]; S, R = KS[ks]['S'], KS[kr]['S']
                if role == 'set1': rho = (a[0] - S[0]) % 6; Ka, Kb = rotT(S, rho), rotT(R, rho)
                else: rho = (a[0] - R[0]) % 6; Ka, Kb = rotT(R, rho), rotT(S, rho)
                if Kb[0] != b[0]: ok = None; break
                b1 = to_label(a)[1] - to_label(Ka)[1]
                b2 = to_label(b)[1] - to_label(Kb)[1] + G.LV[b[0]][0] * G.VX + G.LV[b[0]][1] * G.VY
                u, w = G.LV[a[0]], G.LV[b[0]]; det = u[0] * w[1] - u[1] * w[0]
                x = (b1 * w[1] - b2 * u[1]); y = (u[0] * b2 - w[0] * b1)
                ok &= (x % det == 0) & (y % det == 0); x //= det; y //= det
                ok &= G.alongv(x, y, a[0]) >= G.ab(a, IA['T1'] + 80) + G.MARGE
                ok &= G.alongv(x - G.VX, y - G.VY, b[0]) >= G.ab(b, IB['T1'] + 80) + G.MARGE
                C.append((x, y)); info.append((ks, kr, rho))
            if ok is None: continue
            for i, j in itertools.combinations(range(4), 2):
                dx, dy = C[i][0] - C[j][0], C[i][1] - C[j][1]
                ok &= (np.abs(dx) + np.abs(dy) + np.abs(dx + dy)) // 2 >= 2 * G.DPIX
            idx = np.nonzero(ok)[0]
            if len(idx): res.append((perm, kc, info, idx, C))
    return res
if __name__ == '__main__':
    I = [G.info(B) for B in G.L]; found = []; n1 = 0
    two = [i for i, x in enumerate(I) if len({o[0] for o in x['O']}) == 2]
    for ia in two:
        for ib in two:
            for rho0 in range(6):
                for role in ('set1', 'rst1'):
                    for perm, kc, info, idx, C in feasible(I[ia], I[ib], rho0, role):
                        n1 += len(idx)
                        sizes = np.maximum(np.abs(G.VX[idx]), np.abs(G.VY[idx]))
                        for q in idx[np.argsort(sizes)][:2]:
                            v = (int(G.VX[q]), int(G.VY[q])); cs = [(int(C[j][0][q]), int(C[j][1][q])) for j in range(4)]
                            w = G.full_check(I[ia], I[ib], rho0, v, perm, cs)
                            print('candidat', ia, ib, rho0, role, perm, kc, v, 'marge', w, flush=True)
                            if w is not None:
                                found.append({'A': ia, 'B': ib, 'rho0': rho0, 'role': role, 'perm': perm, 'kits': info, 'v': v, 'centres': cs,
                                              'marge': w, 'taille': max(max(hd(*p) for p in cs), hd(*v))}); break
        json.dump(sorted(found, key=lambda e: (e['taille'], -e['marge'])), open(G.HERE + '/data/ecran3_geo.json', 'w'), indent=1)
    print('étape 1 :', n1, '; retenus :', len(found))

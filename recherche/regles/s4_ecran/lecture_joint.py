#!/usr/bin/env python3
"""R-714 Écran 2×2 + port de LECTURE choisis ENSEMBLE (R-713 : aucun port de lecture pour les écrans déjà trouvés).
Pour chaque configuration de R-706 (démux A, démux B tourné de rho0 et translaté de v_B sur la grille |v_B| ≤ RV, permutation, kits),
les centres des pixels sont des fonctions entières de v_B (tableaux numpy). Port C = démux n (49) tourné de ρ, translaté de v_C ;
affectation sortie k -> (pixel j, droite de sonde s) de même direction ; équations de voie : LV[r_k]·v_C = voie_sonde(j, s) − voie_k.
On résout v_C avec 2 équations indépendantes (entier ?) et on teste les 2 autres, pour TOUTE la grille d'un coup. Puis « en aval ».
Usage : python3 lecture_joint.py RV [max résultats] [meme] -> data/lecture_joint.json (meme = 1 : démux B = démux A, comme R-707)"""
import sys, json, itertools, time
import numpy as np
RV = sys.argv[1] if len(sys.argv) > 1 else '60'; NMAXR = int(sys.argv[2]) if len(sys.argv) > 2 else 200; MEME = len(sys.argv) > 3 and sys.argv[3] == '1'; TR = sys.argv[3].split(':') if len(sys.argv) > 3 and ':' in sys.argv[3] else None   # « k0:k1 » = tranche de la liste des démux A
sys.argv = [sys.argv[0], RV, '1']
import ecran3_geo as E3
G = E3.G
from traj import *
import pixel
from exp_osc import setup
SONDES = [('M', 0, -3, 6), ('M', 3, 2, 8), ('M', 4, 2, 15), ('M', 1, -3, 15), ("R'", 0, 2, 3), ("R'", 3, -3, 7)]
TP = []
for o, r, l, ph in SONDES:
    E = setup(pixel.M if o == 'M' else pixel.R2, r, l, ph, 0); sh = tuple(E['ants'][-1]); sc = sorted(c for c in E['g'] if c not in E['states'][ph][1])
    TP.append(of_label(lab_piece((sh, sc), 0)))
SL = {(s, rho): to_label(rotT(TP[s], rho))[:2] for s in range(len(SONDES)) for rho in range(6)}   # (direction, voie) au centre (0, 0)
I = [G.info(B) for B in G.L]
PORTS = []
for n in range(len(G.L)):
    for rho in range(6):
        O = [rotT(o, rho) for o in I[n]['O']]
        PORTS.append((n, rho, [to_label(o)[:2] for o in O], [G.ab(o, I[n]['T1'] + 80) for o in O]))
def scan_config(cx, cy, rhos):
    """cx, cy : tableaux (4, N) des centres ; renvoie [(n, ρ, affectation, indices, vCx, vCy)]"""
    out = []
    for n, rho, lab, abk in PORTS:
        cand = [[(j, s) for j in range(4) for s in range(len(SONDES)) if SL[(s, rhos[j])][0] == lab[k][0]] for k in range(4)]
        if not all(cand): continue
        for asg in itertools.product(*cand):
            if len({a[0] for a in asg}) < 4: continue
            rhs = [SL[(s, rhos[j])][1] - lab[k][1] + G.LV[lab[k][0]][0] * cx[j] + G.LV[lab[k][0]][1] * cy[j] for k, (j, s) in enumerate(asg)]
            # deux équations indépendantes
            pair = None
            for a_, b_ in itertools.combinations(range(4), 2):
                u, w = G.LV[lab[a_][0]], G.LV[lab[b_][0]]
                if u[0] * w[1] - u[1] * w[0]: pair = (a_, b_); break
            if pair is None: continue
            a_, b_ = pair; u, w = G.LV[lab[a_][0]], G.LV[lab[b_][0]]; det = u[0] * w[1] - u[1] * w[0]
            nx = rhs[a_] * w[1] - u[1] * rhs[b_]; ny = u[0] * rhs[b_] - w[0] * rhs[a_]
            ok = (nx % det == 0) & (ny % det == 0); vx = nx // det; vy = ny // det
            for k in range(4):
                p = G.LV[lab[k][0]]; ok &= (p[0] * vx + p[1] * vy == rhs[k])
                j = asg[k][0]; ok &= G.alongv(cx[j] - vx, cy[j] - vy, lab[k][0]) >= abk[k] + G.MARGE
            idx = np.nonzero(ok)[0]
            if len(idx): out.append((n, rho, asg, idx, vx, vy))
    return out
if __name__ == '__main__':
    t0 = time.time(); two = [i for i, x in enumerate(I) if len({o[0] for o in x['O']}) == 2]; res = []; ncfg = 0
    for ia in (two[int(TR[0]):int(TR[1])] if TR else two):
        for ib in two:
            if MEME and ib != ia: continue
            print('paire', ia, ib, round(time.time() - t0), 's', flush=True)
            for rho0 in range(6):
                for role in ('set1', 'rst1'):
                    for perm, kc, info, idx, C in E3.feasible(I[ia], I[ib], rho0, role):
                        ncfg += 1
                        cx = np.array([C[j][0][idx] for j in range(4)]); cy = np.array([C[j][1][idx] for j in range(4)])
                        for n, rho, asg, jdx, vx, vy in scan_config(cx, cy, [info[j][2] for j in range(4)]):
                            for q in jdx[:3]:
                                g = idx[q]
                                res.append({'A': ia, 'B': ib, 'rho0': rho0, 'role': role, 'perm': perm, 'kits': info,
                                            'v': (int(G.VX[g]), int(G.VY[g])), 'centres': [(int(cx[j][q]), int(cy[j][q])) for j in range(4)],
                                            'C': n, 'rhoC': rho, 'affect': asg, 'vC': (int(vx[q]), int(vy[q]))})
                            print('trouvé', res[-1], flush=True)
                            if len(res) >= NMAXR: break
            json.dump(res, open(G.HERE + f"/data/lecture_joint{'_' + '-'.join(TR) if TR else ''}.json", 'w'), default=list)
    print('configurations', ncfg, '; solutions', len(res), '; durée', round(time.time() - t0), 's')

#!/usr/bin/env python3
"""R-704b Même recherche que ecran2_geo.py mais v pris dans une BANDE lointaine v = k·d_e + m·d_(e+1) (k ≤ KMAX, |m| ≤ MM) :
pour un démux A à 2 directions voisines, les cônes de faisabilité ne se coupent que dans une bande infinie (le long du rayon commun).
Usage : python3 ecran2_bande.py KMAX MM -> data/ecran2_bande.json"""
import sys, json, numpy as np
sys.argv = [sys.argv[0], '1', '0'] + sys.argv[1:]
import ecran2_geo as G
from traj import D
KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 1500; MM = int(sys.argv[4]) if len(sys.argv) > 4 else 40
I = [G.info(B) for B in G.L]
two = [i for i, x in enumerate(I) if len({o[0] for o in x['O']}) == 2]
found = []; n1 = 0
for ia in two:
    dirsA = sorted({o[0] for o in I[ia]['O']})
    for e in dirsA:
        k, m = np.meshgrid(np.arange(0, KMAX + 1), np.arange(-MM, MM + 1)); k = k.ravel(); m = m.ravel()
        G.VX = k * D[e][0] + m * D[(e + 1) % 6][0]; G.VY = k * D[e][1] + m * D[(e + 1) % 6][1]
        for ib in two:
            for rho0 in range(6):
                for role in ('set1', 'rst1'):
                    for perm, idx, C in G.feasible(I[ia], I[ib], rho0, role):
                        n1 += len(idx)
                        sizes = k[idx]
                        for q in idx[np.argsort(sizes)][:2]:
                            v = (int(G.VX[q]), int(G.VY[q])); cs = [(int(C[j][0][q]), int(C[j][1][q])) for j in range(4)]
                            w = G.full_check(I[ia], I[ib], rho0, v, perm, cs)
                            print('candidat', ia, ib, rho0, role, perm, v, cs, 'marge', w, flush=True)
                            if w is not None:
                                found.append({'A': ia, 'B': ib, 'rho0': rho0, 'role': role, 'perm': perm, 'v': v, 'centres': cs, 'marge': w,
                                              'taille': max(max(G.hd(*p) for p in cs), G.hd(*v))}); break
print('étape 1 :', n1, '; retenus :', len(found))
found.sort(key=lambda e: (e['taille'], -e['marge']))
json.dump(found, open(G.HERE + '/data/ecran2_bande.json', 'w'), indent=1)

#!/usr/bin/env python3
"""R-621 Croissance de l'enchaînement PAR GREFFE (R-619) en fonction du nombre de pas N (comptage exact sur les arbres, sans placement).
Module à N pas de v = arbre du pas 1 de v (chain2.S ; h1 : htree.h1_tree2, la version réutilisable R-616) dont chaque littéral w / ¬w
est remplacé par le module à N−1 pas de w (¬w : même arbre, littéraux inversés, même taille).
P_N(v) = P_1(v) + Σ_{usages de w dans l'arbre de v} P_{N−1}(w) ;  L_N(v) = Σ L_{N−1}(w) ;  L_0 = 1, P_0 = 0.
Usage : python3 grow.py [Nmax]  -> table + rayon spectral de la matrice des usages (taux de croissance par pas)"""
import sys, numpy as np
from chain2 import S
from htree import h1_tree2
from modules import VARS
def uses(t, acc):
    name, ins = t
    for it in ins:
        if isinstance(it, str): acc[it.lstrip('~')] = acc.get(it.lstrip('~'), 0) + 1
        else: uses(it, acc)
    return acc
def npow(t): return 1 + sum(npow(it) for it in t[1] if not isinstance(it, str))
T1 = {v: (h1_tree2() if v == 'h1' else S(v, 'm', 1)) for v in VARS}
U = {v: uses(T1[v], {}) for v in VARS}; P1 = {v: npow(T1[v]) for v in VARS}
M = np.array([[U[v].get(w, 0) for w in VARS] for v in VARS], dtype=object)
if __name__ == '__main__':
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print('usages (ligne v, colonne w) :', VARS); print(M)
    P = {v: 0 for v in VARS}; L = {v: 1 for v in VARS}
    for N in range(1, Nmax + 1):
        P = {v: P1[v] + sum(c * P[w] for w, c in U[v].items()) for v in VARS}
        L = {v: sum(c * L[w] for w, c in U[v].items()) for v in VARS}
        print(f'N={N}: puissances ' + ' '.join(f'{v}:{P[v]}' for v in VARS) + f' | total {sum(P.values())} ; littéraux total {sum(L.values())}')
    ev = np.linalg.eigvals(M.astype(float)); print('rayon spectral (croissance par pas) :', max(abs(ev)).round(3))
    sub = [v for v in VARS if v != 'h1']; Ms = np.array([[U[v].get(w, 0) for w in sub] for v in sub], float)
    print('sans h1 (sous-système fermé) :', max(abs(np.linalg.eigvals(Ms))).round(3))

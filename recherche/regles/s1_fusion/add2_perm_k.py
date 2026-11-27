"""S1 / R-405 : pour l'additionneur 2 bits « permutation » (add2_perm.build), 2 usages sur les 256 couples d'entrées, pour plusieurs k.
Usage : python3 s1_fusion/add2_perm_k.py piece D k1,k2,..."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from add2_perm import build, T
from circuit import check_multi
name, D = sys.argv[1], int(sys.argv[2]); rho = {'A': 0, 'B': 2}[name]
ALL = build(name, rho, D)
for k in map(int, sys.argv[3].split(',')):
    nb = 0; bad = []
    for e1, e2 in itertools.product(ALL.cases(), repeat=2):
        sup, good, _, _ = check_multi(ALL, [e1, e2], k, T0=T)
        if sup and good == 2: nb += 1
        else: bad.append((e1, e2, sup, good))
    print(name, D, 'k =', k, ':', nb, '/ 256', bad[:2], flush=True)

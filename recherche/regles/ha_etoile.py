#!/usr/bin/env python3
"""R-344 Demi-additionneur à S UNIQUE (« HA* ») : R-337 + UN vaisseau constant K5 qui croise S-V juste après la porte.
Dans le cas (0,1), le choc renvoie de quoi pousser K3 sur la voie de S, dans la case horaire de S-U : S sort au MÊME endroit et au MÊME
instant dans les cas (1,0) et (0,1) — les deux horaires de S sont égalisés sans retard géométrique.
Usage : python3 ha_etoile.py [variante 0|1]"""
import sys, json, random
from fa_lib import *
from circuit import *
V = int(sys.argv[1]) if len(sys.argv) > 1 else 0
VARIANTES = [  # (K, sortie C) — trouvées par fa_retard.py un (20 lignes « S et C sur une seule position », 3 placements distincts)
    (((31, 1, 3), [(31, 2)]), (1, -29, 973, 0)),
    (((33, -1, 1), [(32, -1), (32, 0), (33, -2)]), (0, 1, 999, 0)),
]
def HAstar(v=V):
    K, Cpos = VARIANTES[v]
    return Circuit([('K5', K, None), ('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')],
                   {'S': (lambda e: e['a'] ^ e['b'], [(0, 0, 968, 0)]), 'C': (lambda e: e['a'] & e['b'], [Cpos])})
if __name__ == '__main__':
    C = HAstar()
    print('4 cas, 2 moteurs :')
    for inp, ok, got, same in check_cases(C, 4000): print(' ', inp, got, 'OK' if ok else 'FAUX', '2 moteurs identiques' if same else 'DIFF')
    import itertools
    sup2 = 0
    for e1, e2 in itertools.product(C.cases(), repeat=2):
        sup, good, same, _ = check_multi(C, [e1, e2], 200); sup2 += sup and good == 2
    print('2 usages (16 suites), superposition exacte et justes :', sup2, '/ 16')
    for seed in range(3):
        random.seed(seed); seq = [random.choice(C.cases()) for _ in range(20)]
        sup, good, same, s = check_multi(C, seq, 200, engine2=(seed == 0))
        print(f'20 usages (graine {seed}) : superposition {sup}, justes {good}/20' + (f', 2 moteurs identiques {same}' if seed == 0 else ''))

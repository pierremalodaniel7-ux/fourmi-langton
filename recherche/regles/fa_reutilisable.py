#!/usr/bin/env python3
"""R-349 ADDITIONNEUR COMPLET RÉUTILISABLE : demi-additionneur R-337 (a, b) + retenue c = 1 vaisseau de direction 4 (fa_reuse.py).
Vérifications : 8 cas (2 moteurs) ; 2 usages 64/64 (superposition exacte) ; 20 usages au hasard dans UNE simulation (3 graines, 2 moteurs) ;
puis certificat « tout nombre d'usages » (circuit.certificat).
Usage : python3 fa_reutilisable.py [indice] [cert]"""
import sys, json, random, itertools
from fa_lib import *
from circuit import *
I = int(sys.argv[1]) if __name__ == '__main__' and len(sys.argv) > 1 else 0
g = json.load(open('data/fa_reuse_ok_024.json'))[I]
K = (tuple(g['K'][0]), [tuple(x) for x in g['K'][1]])
pieces = [('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')]
pieces.insert(min(g['c'][5], 4), ('c', K, 'c'))
FA = Circuit(pieces, {'S': (lambda e: (e['a'] + e['b'] + e['c']) % 2, [tuple(p) for p in g['PS']]),
                      'C': (lambda e: int(e['a'] + e['b'] + e['c'] >= 2), [tuple(p) for p in g['PC']])})
if __name__ == '__main__':
    print('c =', K, ' ordre', g['c'][5], ' S lu sur', g['PS'], ' C lu sur', g['PC'])
    r = check_cases(FA, 4000); print('8 cas :', sum(z[1] for z in r), '/8 ; 2 moteurs', all(z[3] for z in r))
    n2 = sum(1 for e1, e2 in itertools.product(FA.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(FA, [e1, e2], 200)))
    print('2 usages, 64 suites :', n2, '/64')
    res = {}
    for seed in range(3):
        random.seed(seed); seq = [random.choice(FA.cases()) for _ in range(20)]
        sup, good, same, s = check_multi(FA, seq, 200, engine2=True)
        print(f'20 usages (graine {seed}) : superposition exacte {sup}, {good}/20 justes, 2 moteurs identiques {same}', flush=True)
        res[seed] = dict(suite=[tuple(e.values()) for e in seq], justes=good, sup=sup, deux_moteurs=same)
    out = dict(c=g['K'], ordre=g['c'][5], S=g['PS'], C=g['PC'], k=200, resultats=res, un_usage={str(tuple(e.values())): FA.sit(e) for e in FA.cases()})
    if len(sys.argv) > 2:
        worst, per, fronts = certificat(FA, 200, 4000, J=int(sys.argv[2]))
        print('certificat : distance minimale', worst, 'par écart', per, '; paires de face', fronts)
        out['certificat'] = dict(distance_min=worst, par_ecart=per, fronts=fronts)
    json.dump(out, open('resumes/additionneur_complet_reutilisable.json', 'w'), ensure_ascii=False, indent=1)

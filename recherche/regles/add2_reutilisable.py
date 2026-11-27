#!/usr/bin/env python3
"""R-350 Additionneur 2 bits RÉUTILISABLE par enchaînement : étage 0 = demi-additionneur R-337 (a0, b0) → s0, c0 (1 vaisseau) ;
étage 1 = additionneur complet réutilisable R-349 (a1, b1, c) tourné de 4 crans et posé pour que sa pièce c suive EXACTEMENT c0.
16 cas (2 moteurs), puis 20 usages au même endroit (3 graines), superposition exacte, 2 moteurs.
Usage : python3 add2_reutilisable.py"""
import json, random, itertools
from compose import *
from fa_complet import cover
from fa_reutilisable import FA
T = 6000
HA = Circuit([('K3', K3, None), ('K2', K2, None), ('B', B, 'b0'), ('A', A, 'a0')])
c0 = (2, -28, 916, 0)
import sys
D = int(sys.argv[1]) if len(sys.argv) > 1 else 100
FA1 = slide(attach(FA, 'c', 4, c0, 4000), 'c', D)
FA1 = Circuit([(n, p, {'a': 'a1', 'b': 'b1', 'c': 'c'}.get(v, v)) for n, p, v in FA1.pieces])
O = {(e['a1'], e['b1'], e['c']): [tuple(x) for x in decode(*lotdump([FA1.sit(e)], T)[0])] for e in FA1.cases()}
PS1 = cover(O, lambda k: sum(k) % 2); PC1 = cover(O, lambda k: int(sum(k) >= 2))
OH = {(e['a0'], e['b0']): [tuple(x) for x in decode(*lotdump([HA.sit(e)], T)[0])] for e in HA.cases()}
PS0 = cover(OH, lambda k: k[0] ^ k[1])
print('s0 lu sur', PS0, '; s1 sur', PS1, '; c1 sur', PC1)
ALL = Circuit(HA.pieces + [(n, p, v) for n, p, v in FA1.pieces if n != 'c'],
              {'s0': (lambda e: e['a0'] ^ e['b0'], PS0),
               's1': (lambda e: (e['a1'] + e['b1'] + (e['a0'] & e['b0'])) % 2, [tuple(p) for p in PS1]),
               'c1': (lambda e: int(e['a1'] + e['b1'] + (e['a0'] & e['b0']) >= 2), [tuple(p) for p in PC1])})
r = check_cases(ALL, T)
print('16 cas :', sum(z[1] for z in r), '/16 ; 2 moteurs', all(z[3] for z in r))
res = {}
for seed in range(3):
    random.seed(seed); seq = [random.choice(ALL.cases()) for _ in range(20)]
    sup, good, same, s = check_multi(ALL, seq, 200, engine2=True)
    print(f'20 usages (graine {seed}) : superposition exacte {sup}, {good}/20 additions justes, 2 moteurs identiques {same}', flush=True)
    res[seed] = dict(justes=good, sup=sup, deux_moteurs=same)
json.dump(dict(PS0=PS0, PS1=PS1, PC1=PC1, seize=sum(z[1] for z in r), resultats=res,
               un_usage={str(tuple(e.values())): ALL.sit(e) for e in ALL.cases()}), open('resumes/additionneur2_reutilisable.json', 'w'), ensure_ascii=False, indent=1)

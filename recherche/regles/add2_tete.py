#!/usr/bin/env python3
"""R-345 Additionneur 2 bits par enchaînement (UN usage) : étage 0 = demi-additionneur R-337 (a0, b0) → s0, c0 (c0 = A décalé,
UNE route) ; étage 1 = additionneur complet « tête-bêche » (a1, b1, c) dont la retenue entrante c est REMPLACÉE par c0 (étage 1 tourné de
−60° et posé pour que sa pièce c suive exactement la route et l'horaire de c0). 16 cas, 2 moteurs.
Usage : python3 add2_tete.py"""
import json, itertools
from compose import *
from fa_complet import cover
T = 6000
FAj = json.load(open('resumes/additionneur_tete_beche.json'))
K = (tuple(FAj['germe_c'][0]), [tuple(c) for c in FAj['germe_c'][1]])
FA = Circuit([('c', K, 'c'), ('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')])
HA = Circuit([('K3', K3, None), ('K2', K2, None), ('B', B, 'b0'), ('A', A, 'a0')])
c0 = (2, -28, 916, 0)                 # sortie C du demi-additionneur R-337 au temps 4000
rho = 5                               # c (direction 3 dans le repère de FA) doit devenir direction 2
FA1 = attach(FA, 'c', rho, c0, 4000)
FA1 = Circuit([(n, p, {'a': 'a1', 'b': 'b1', 'c': 'c'}.get(v, v)) for n, p, v in FA1.pieces])
# positions de lecture de l'étage 1 (seul, avec sa propre pièce c), au temps T
O = {}
for e in FA1.cases():
    O[(e['a1'], e['b1'], e['c'])] = [tuple(x) for x in decode(*lotdump([FA1.sit(e)], T)[0])]
PS1 = cover(O, lambda k: sum(k) % 2); PC1 = cover(O, lambda k: int(sum(k) >= 2))
OH = {}
for e in HA.cases(): OH[(e['a0'], e['b0'])] = [tuple(x) for x in decode(*lotdump([HA.sit(e)], T)[0])]
PS0 = cover(OH, lambda k: k[0] ^ k[1])
print('étage 1 seul : S1 lu sur', PS1, '; C1 lu sur', PC1, '; étage 0 : s0 lu sur', PS0)
# circuit complet : la pièce c de l'étage 1 est retirée (c'est c0 qui arrive)
ALL = Circuit(HA.pieces + [(n, p, v) for n, p, v in FA1.pieces if n != 'c'])
ok = 0; same_all = True; lignes = []
for e in ALL.cases():
    s = ALL.sit(e); r = lotdump([s], T)[0]; d = decode(*r)
    if d is None: lignes.append(f'{e} : sale'); continue
    D = set(map(tuple, d))
    s0 = int(any(p in D for p in PS0)); s1 = int(any(tuple(p) in D for p in PS1)); c1 = int(any(tuple(p) in D for p in PC1))
    n = e['a0'] + e['b0'] + 2 * (e['a1'] + e['b1']); got = s0 + 2 * s1 + 4 * c1
    pa, pc = pyrun(s, T); same = sorted(pa) == sorted(map(tuple, r[0])) and sorted(pc) == sorted(map(tuple, r[1])); same_all &= same
    ok += got == n
    lignes.append(f"a = {e['a1']}{e['a0']}, b = {e['b1']}{e['b0']} : somme lue {c1}{s1}{s0} = {got}, attendu {n}  {'OK' if got == n else 'FAUX'}")
print('\n'.join(lignes))
print(f'{ok}/16 justes ; 2 moteurs identiques : {same_all}')
json.dump({'T': T, 'PS0': PS0, 'PS1': PS1, 'PC1': PC1, 'justes': f'{ok}/16', 'deux_moteurs': same_all,
           'cas': {str(tuple(e.values())): ALL.sit(e) for e in ALL.cases()}}, open('resumes/additionneur2_tete_beche.json', 'w'), ensure_ascii=False, indent=1)

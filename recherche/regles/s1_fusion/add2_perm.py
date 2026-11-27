#!/usr/bin/env python3
"""S1 / R-405 Additionneur 2 bits réutilisable, idée « permutation » : a + b + c est symétrique, donc la retenue c0 du demi-additionneur
R-337 peut entrer dans l'additionneur complet R-349 par sa pièce A (rho = 0) ou B (rho = 2) au lieu de c (R-350 : c, rho = 4, échec à
cause de K2 parallèle à c). L'étage 1 est posé (compose.attach) pour que la pièce choisie suive EXACTEMENT c0, puis glissé de D périodes.
Test 1 (rapide) : 16 cas propres, sorties lisibles (cover), 2 moteurs. Test 2 : 2 usages k = 200, 16 × 16 suites, superposition exacte.
Écrit au fur et à mesure dans s1_fusion/add2_perm.json.
Usage : python3 s1_fusion/add2_perm.py Dmin Dmax pas"""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from compose import attach, slide
from circuit import Circuit, check_multi, check_cases
from fa_lib import decode, lotdump
from fa_complet import cover
from lib1 import FA, HA
T = 9000
c0 = (2, -28, 916, 0)
HA0 = Circuit([(n, p, {'a': 'a0', 'b': 'b0'}.get(v, v)) for n, p, v in HA().pieces])
FAc = FA()
def build(name, rho, D):
    # variable de l'étage 1 portée par la pièce `name` = c0 ; les deux autres = a1, b1
    other = [v for v in ('a', 'b', 'c') if v != {'A': 'a', 'B': 'b', 'c': 'c'}[name]]
    ren = {other[0]: 'a1', other[1]: 'b1', {'A': 'a', 'B': 'b', 'c': 'c'}[name]: 'cc'}
    F1 = attach(FAc, name, rho, c0, 4000)
    if F1 is None: return None
    F1 = slide(F1, name, D)
    F1 = Circuit([(n, p, ren.get(v, v)) for n, p, v in F1.pieces])
    O = {}
    for e in F1.cases():
        d = decode(*lotdump([F1.sit(e)], T)[0])
        if d is None: return 'étage 1 seul sale'
        O[(e['a1'], e['b1'], e['cc'])] = [tuple(x) for x in d]
    PS1 = cover(O, lambda k: sum(k) % 2); PC1 = cover(O, lambda k: int(sum(k) >= 2))
    OH = {(e['a0'], e['b0']): [tuple(x) for x in decode(*lotdump([HA0.sit(e)], T)[0])] for e in HA0.cases()}
    PS0 = cover(OH, lambda k: k[0] ^ k[1])
    if None in (PS1, PC1, PS0): return 'sorties illisibles'
    cin = lambda e: e['a0'] & e['b0']
    # ordre de jeu : le bloc HA0 prend la place de la pièce `name` dans l'ordre de l'étage 1 (dans R-349 l'ordre compte : fourmis jouées
    # l'une après l'autre ; c0 est la fourmi B de HA0 et doit jouer là où jouait la pièce remplacée)
    i = [n for n, p, v in F1.pieces].index(name)
    rest = [(n + '1', p, v) for n, p, v in F1.pieces]
    ALL = Circuit(rest[:i] + HA0.pieces + rest[i + 1:],
                  {'s0': (lambda e: e['a0'] ^ e['b0'], sorted(PS0)),
                   's1': (lambda e: (e['a1'] + e['b1'] + cin(e)) % 2, sorted(PS1)),
                   'c1': (lambda e: int(e['a1'] + e['b1'] + cin(e) >= 2), sorted(PC1))})
    return ALL
if __name__ == '__main__':
    Dmin, Dmax, st = map(int, sys.argv[1:4])
    out = os.path.join(HERE, 'add2_perm.json'); res = json.load(open(out)) if os.path.exists(out) else []
    t0 = time.time()
    for name, rho in (('A', 0), ('B', 2)):
        for D in range(Dmin, Dmax, st):
            ALL = build(name, rho, D)
            if not isinstance(ALL, Circuit): print(name, D, ALL, flush=True); continue
            r = check_cases(ALL, T, engine2=False); n16 = sum(z[1] for z in r)
            line = dict(piece=name, rho=rho, D=D, seize=n16)
            if n16 == 16:
                bad = 0
                for e1, e2 in itertools.product(ALL.cases(), repeat=2):
                    sup, good, _, _ = check_multi(ALL, [e1, e2], 200)
                    if not (sup and good == 2): bad += 1
                    if bad: break
                line['deux_usages_ok'] = bad == 0
            print(line, '%.0f s' % (time.time() - t0), flush=True)
            res.append(line); json.dump(res, open(out, 'w'))

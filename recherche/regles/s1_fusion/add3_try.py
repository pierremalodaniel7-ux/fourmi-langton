#!/usr/bin/env python3
"""S1 / R-407 Additionneur 3 bits, essai direct : la retenue c1 de R-405 sort sur 3 routes possibles (selon le cas) ; on pose un 3e étage
R-349 dont une pièce (A, B ou c, rotation imposée par la direction) suit EXACTEMENT l'une des 3, glissé de D périodes, bloc R-405 joué au
rang de cette pièce. 64 cas : propres ? s0, s1, s2, c2 lisibles (cover) et justes ? Écrit s1_fusion/add3_try.json au fur et à mesure.
Usage : python3 s1_fusion/add3_try.py D1,D2,..."""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from add2_perm import build, T
from compose import attach, slide
from circuit import Circuit
from fa_lib import decode
import fa_lib
from fa_complet import cover
from lib1 import FA
T3 = 14000
ST1 = build('A', 0, 20); FAc = FA()
V = [tuple(v) for v in ST1.outputs['c1'][1]]          # 3 routes de c1 au temps T = 9 000
DIR = {'A': 2, 'B': 0, 'c': 4}; VAR = {'A': 'a', 'B': 'b', 'c': 'c'}
def build3(v, X, D):
    rho = (v[0] - DIR[X]) % 6
    F = attach(FAc, X, rho, v, T)
    if F is None: return None
    F = slide(F, X, D)
    oth = [w for w in 'abc' if w != VAR[X]]; ren = {oth[0]: 'a2', oth[1]: 'b2'}
    rest = [(n + '2', p, ren.get(w, w)) for n, p, w in F.pieces]
    i = [n for n, p, w in F.pieces].index(X)
    return Circuit(rest[:i] + ST1.pieces + rest[i + 1:])
if __name__ == '__main__':
    out = os.path.join(HERE, 'add3_try.json'); res = []
    t0 = time.time()
    for D in map(int, sys.argv[1].split(',')):
        for v, X in itertools.product(V, 'ABc'):
            C = build3(v, X, D)
            if C is None: continue
            cs = C.cases(); R = fa_lib.lotdump([C.sit(e) for e in cs], T3)
            O = {}; sale = 0
            for e, r in zip(cs, R):
                d = decode(*r)
                if d is None: sale += 1; continue
                O[tuple(e[w] for w in ('a0', 'b0', 'a1', 'b1', 'a2', 'b2'))] = [tuple(x) for x in d]
            line = dict(D=D, route=v, piece=X, propres=len(O))
            if sale == 0:
                c0 = lambda k: k[0] & k[1]; c1 = lambda k: int(k[2] + k[3] + c0(k) >= 2)
                fs = {'s0': lambda k: k[0] ^ k[1], 's1': lambda k: (k[2] + k[3] + c0(k)) % 2,
                      's2': lambda k: (k[4] + k[5] + c1(k)) % 2, 'c2': lambda k: int(k[4] + k[5] + c1(k) >= 2)}
                line['lisibles'] = {o: cover(O, f) is not None for o, f in fs.items()}
            print(line, '%.0f s' % (time.time() - t0), flush=True)
            res.append(line); json.dump(res, open(out, 'w'))

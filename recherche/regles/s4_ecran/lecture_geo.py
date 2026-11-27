#!/usr/bin/env python3
"""R-713 Port de LECTURE par adresse pour l'écran 2×2 de R-707 : un 3e démux C (l'un des 49 triés, tourné de ρ, translaté de v)
dont la sortie k passe EXACTEMENT sur la droite d'une sonde utile (R-708) du pixel π(k), en aval du démux.
Équations exactes : direction égale et voie égale (la voie varie linéairement avec v : LV[r]·v) ; 4 équations, 2 inconnues entières.
-> data/lecture_geo.json (solutions triées par |v|)"""
import sys, json, itertools
RANG = sys.argv[1] if len(sys.argv) > 1 else '0'
sys.argv = [sys.argv[0], RANG]
from traj import *
import pixel
import ecran_demo as E2
import ecran2_geo as G
from exp_osc import setup
SONDES = [('M', 0, -3, 6), ('M', 3, 2, 8), ('M', 4, 2, 15), ('M', 1, -3, 15), ("R'", 0, 2, 3), ("R'", 3, -3, 7)]   # R-708 + droites élargies (R-713)
TP = []
for o, r, l, ph in SONDES:
    E = setup(pixel.M if o == 'M' else pixel.R2, r, l, ph, 0); sh = tuple(E['ants'][-1]); sc = sorted(c for c in E['g'] if c not in E['states'][ph][1])
    TP.append(of_label(lab_piece((sh, sc), 0)))
PIX = [(E2.KIT[j]['rho'], E2.KIT[j]['c']) for j in range(4)]
TGT = [[movT(rotT(TP[s], PIX[j][0]), PIX[j][1], 0) for s in range(len(SONDES))] for j in range(4)]
TL = [[to_label(T)[:2] for T in row] for row in TGT]
def solve(eqs):
    """eqs = [((a, b), c)] : a·vx + b·vy = c ; solution entière unique ou None"""
    for i in range(len(eqs)):
        for k in range(i + 1, len(eqs)):
            (a, b), c = eqs[i]; (e, f), g = eqs[k]; det = a * f - b * e
            if det == 0: continue
            nx, ny = c * f - b * g, a * g - c * e
            if nx % det or ny % det: return None
            v = (nx // det, ny // det)
            return v if all(p * v[0] + q * v[1] == w for (p, q), w in eqs) else None
    return None
sol = []
for n, B in enumerate(G.L):
    O0 = [G.tt(o) for o in B['outs4']]; T1 = max(B['times'].values())
    for rho in range(6):
        O = [rotT(o, rho) for o in O0]; lab = [to_label(o)[:2] for o in O]
        for perm in itertools.permutations(range(4)):
            for ss in itertools.product(range(len(SONDES)), repeat=4):
                if any(lab[k][0] != TL[perm[k]][ss[perm[k]]][0] for k in range(4)): continue
                eqs = [(G.LV[lab[k][0]], TL[perm[k]][ss[perm[k]]][1] - lab[k][1]) for k in range(4)]
                v = solve(eqs)
                if v is None: continue
                # en aval : le pixel doit être devant le point d'émission de la sortie (abscisse le long de la direction)
                ok = True; marge = 10 ** 9
                for k in range(4):
                    Ok = movT(O[k], v, 0); c = PIX[perm[k]][1]
                    dd = along(c[0], c[1], Ok[0]) - G.ab(Ok, T1)
                    marge = min(marge, dd); ok &= dd > 12
                if ok: sol.append({'n': n, 'rho': rho, 'perm': perm, 'sondes': ss, 'v': v, 'aval': marge})
sol.sort(key=lambda e: abs(e['v'][0]) + abs(e['v'][1]))
json.dump(sol, open(HERE + f'/data/lecture_geo_{RANG}.json', 'w'), default=list)
print('placement', RANG, ':', len(sol), 'solutions ;', sol[:3])

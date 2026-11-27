#!/usr/bin/env python3
"""R-708 Sondes de lecture du pixel M/R' (à UN vaisseau, joué après l'objet) : pour chaque direction r, voie l, phase ph, issue exacte
sur M et sur R' : objet restant (périodique ? M, R' ou autre X), vaisseaux sortants (trajectoires). Moteur hx.py.
Cherché : une sonde LISIBLE = la sortie diffère selon l'état, et l'objet restant est M, R' ou un X qu'UN vaisseau remet en M / R'.
-> sondes.json"""
import json, collections
from traj import *
import pixel
from exp_osc import setup
def orbit_key(ants, cells, lim=3000):
    """forme canonique (ensemble des états de l'orbite) si l'objet est périodique (≤ lim), sinon None"""
    A = [list(a) for a in ants]; g = {c: 1 for c in cells}; A0 = [list(a) for a in ants]; g0 = dict(g); S = []
    for _ in range(lim):
        S.append((tuple(sorted(map(tuple, A))), tuple(sorted(g)))); step(A, g)
        if A == A0 and g == g0: return frozenset(S)
    return None
KM = orbit_key(*pixel.parse(pixel.M)); KR = orbit_key(*pixel.parse(pixel.R2))
def probe(osc, r, l, ph):
    try: E = setup(osc, r, l, ph, 0)
    except Exception: return None
    B = [list(a) for a in E['ants']]; g = dict(E['g'])
    for _ in range(E['T'] + 400): step(B, g)
    near = [tuple(b) for b in B if hd(b[0], b[1]) <= 8]; far = [tuple(b) for b in B if hd(b[0], b[1]) > 8]
    nc = [c for c in g if hd(*c) <= 8]; fc = [c for c in g if hd(*c) > 8]
    d = decode(far, fc)
    if d is None: return {'propre': False}
    outs = sorted(of_label(lab_of(x, E['T'] + 400)) for x in d)
    k = orbit_key(near, nc) if near else ('vide' if not nc else None)
    name = 'M' if k == KM else "R'" if k == KR else 'vide' if k == 'vide' else ('X' if k else 'non périodique')
    return {'propre': True, 'objet': name, 'sorties': outs, 'n_fourmis_objet': len(near), 'entree': of_label(lab_piece((tuple(E['ants'][-1]), sorted(c for c in E['g'] if c not in E['states'][ph][1])), 0))}
if __name__ == '__main__':
    res = {}; cnt = collections.Counter()
    for name, osc in (('M', pixel.M), ("R'", pixel.R2)):
        P = len(pixel.ORB[0 if name == 'M' else 1])
        for r in range(6):
            for l in range(-8, 9):
                for ph in range(P):
                    x = probe(osc, r, l, ph)
                    if x is None: continue
                    res[f'{name} {r} {l} {ph}'] = x; cnt[(name, x.get('objet', 'sale'), len(x.get('sorties', [])))] += 1
    for k, v in sorted(cnt.items(), key=str): print(k, v)
    json.dump(res, open(HERE + '/sondes.json', 'w'), default=list)

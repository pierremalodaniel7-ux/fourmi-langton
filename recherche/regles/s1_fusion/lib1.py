"""S1 : pièces communes (demi-additionneur R-337, additionneur complet R-349) reconstruites depuis resumes/*.json (data/ n'est pas
versionné), sorties détaillées par cas."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from fa_lib import decode, back, lotdump, sit, K3, K2, A, B
from circuit import Circuit
_g = json.load(open(os.path.join(HERE, '..', 'resumes', 'additionneur_complet_reutilisable.json')))
Kc = (tuple(_g['c'][0]), [tuple(x) for x in _g['c'][1]])
def FA():
    pieces = [('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')]
    pieces.insert(min(_g['ordre'], 4), ('c', Kc, 'c'))
    return Circuit(pieces, {'S': (lambda e: (e['a'] + e['b'] + e['c']) % 2, [tuple(p) for p in _g['S']]),
                            'C': (lambda e: int(e['a'] + e['b'] + e['c'] >= 2), [tuple(p) for p in _g['C']])})
def HA():
    return Circuit([('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')],
                   {'S': (lambda e: e['a'] ^ e['b'], [(0, 0, 1000, 0), (0, 0, 968, 0)]), 'C': (lambda e: e['a'] & e['b'], [(2, -28, 916, 0)])})
def outs(C, T=4000):
    """dict cas -> liste des vaisseaux décodés au temps T"""
    cs = C.cases(); R = lotdump([C.sit(e) for e in cs], T)
    return [(e, decode(*r)) for e, r in zip(cs, R)]
if __name__ == '__main__':
    for name, C in (('HA', HA()), ('FA', FA())):
        print(name)
        for e, d in outs(C): print('  ', e, d)

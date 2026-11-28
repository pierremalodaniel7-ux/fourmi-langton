"""T4 lecture : kits de la sonde R-708 (3 options) pour les pixels de l'écran T4 (même code que lecture_demo.kit, toutes options)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
from exp_osc import setup
OPTS = {0: ((0, -3, 6), (3, 1, 16)), 1: ((3, 2, 8), (0, -3, 5)), 2: ((4, 2, 15), (1, 1, 5))}
SR = json.load(open(os.path.join(S4, 'sondes_retour.json')))
def _orb(osc):
    a, c = pixel.parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; A0 = [list(x) for x in a]; g0 = dict(g); out = []
    while True:
        out.append(([tuple(x) for x in A], sorted(g))); TR.step(A, g)
        if A == A0 and g == g0: return out
def kits(o):
    (pr, pl, pph), (rr, rl, rph) = OPTS[o]
    XS = [x for x in SR if x['etat'] == 'M' and (x['r'], x['l'], x['ph']) == (pr, pl, pph)][0]['X']
    OSC = {'M': pixel.M, "R'": pixel.R2, 'X': XS}; ORB = {k: _orb(v) for k, v in OSC.items()}
    def kit(src, r, l, ph):
        E = setup(OSC[src], r, l, ph, 0); A = E['ants']; og = E['states'][ph][1]
        S = TR.of_label(TR.lab_piece((tuple(A[-1]), sorted(c for c in E['g'] if c not in og)), 0))
        B = [list(a) for a in A]; g = dict(E['g'])
        for _ in range(E['T']): TR.step(B, g)
        obj = (sorted(tuple(b) for b in B[:-1]), sorted(c for c in g if hd(*c) <= 6))
        out = TR.of_label(TR.lab_piece((tuple(B[-1]), sorted(c for c in g if hd(*c) > 6)), E['T']))
        fin = [(k, i) for k in ORB for i, (a, c) in enumerate(ORB[k]) if (sorted(a), c) == obj][0]
        return {'S': S, 'ph': ph, 'T': E['T'], 'out': out, 'src': src, 'dst': fin[0], 'fin': fin[1], 'r': r}
    K = {'lire0': kit('M', pr, pl, pph), 'reecr': kit('X', rr, rl, rph)}
    K.update({f'lire1_{p}': kit("R'", pr, pl, p) for p in range(12)})
    return K, ORB
def place(T, p, t=0):
    """trajectoire du kit (repère pixel) placée sur le pixel p (rho, centre) avec le temps 0 du kit à l'instant t"""
    return TR.movT(TR.rotT(T, p['rho']), tuple(p['c']), t)

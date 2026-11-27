"""S1 : appariement EXACT d'une fusion du catalogue R-400 (fusion1_ok.json) sur deux routes données (vaisseaux décodés au temps T, T multiple
de 8) : rotation + translation + glissement k tels que s1 suive X et s2 suive Y exactement. Voir match3.py (R-409)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from compose import attach, slide
from circuit import Circuit
from fa_lib import decode
from hx import rot, ship_dir
from fusion_reuse import make
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); KF = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
OK = json.load(open(os.path.join(HERE, 'fusion1_ok.json')))
GS = [Circuit(make(z, KF)) for z in OK]
def g(o):
    r, l, a, ph = o
    if (l + a) % 2: return None
    return rot(((l + a) // 2, (l - a) // 2), r)
def at(p, t):
    d = decode([p[0]], p[1])[0]; return (d[0], d[1], d[2] + 2 * (t // 8), d[3])
def matches(vx, vy, T):
    out = []
    for zi, z in enumerate(OK):
        rho = (vx[0] - z['r1'][0]) % 6
        if (z['r2'][0] + rho) % 6 != vy[0]: continue
        F = attach(GS[zi], 's1', rho, vx, T)
        if F is None: continue
        P = dict((n, p) for n, p, v in F.pieces); s2 = at(P['s2'], T)
        if s2[3] != vy[3]: continue
        a, b = g(s2), g(vy)
        if a is None or b is None: continue
        w = (b[0] - a[0], b[1] - a[1]); d1, d2 = ship_dir(vx[0]), ship_dir(vy[0]); dd = (d1[0] - d2[0], d1[1] - d2[1])
        if dd == (0, 0):
            if w != (0, 0): continue
            k = 0
        else:
            i = 0 if dd[0] else 1
            if w[i] % dd[i]: continue
            k = w[i] // dd[i]
            if (k * dd[0], k * dd[1]) != w: continue
        F2 = slide(F, 's1', k); P2 = dict((n, p) for n, p, v in F2.pieces)
        if at(P2['s1'], T) != tuple(vx) or at(P2['s2'], T) != tuple(vy): continue
        out.append(dict(z=zi, rho=rho, k=k, o=(z['o1'], z['o2']), K=P2['K']))
    return out

#!/usr/bin/env python3
"""R-601 Échanges (swaps) entre vaisseaux pairs : pour chaque géométrie d'échange g (B dir 0, A dir r ∈ {2,4}), décalages σ_B, σ_A des
sorties, et issue des 3 géométries décalées (B⊕σ_B, A), (B, A⊕σ_A), (B⊕σ_B, A⊕σ_A), dans les 2 ordres de jeu (moteur hx.py)."""
import json, collections
from s3lib import *
R = json.load(open('data/chocs_pairs.json'))
def issue(wA, wB, order, T):
    W = [wA, wB] if order == 0 else [wB, wA]
    a, c = run_py(sit_wls(W), T)
    d = decode(a, c, T)
    if d is None: return 'sale'
    if sorted(d) == sorted([wA, wB]): return 'T'
    return 'X'
def sub(w1, w0):  # w1 = w0 décalé : (dlane, dW)
    def lw(w):
        r, gx, gy, ph = w; X, Y = rot((gx, gy), -r % 6); return X + Y, 4 * (X - Y) + ph
    a, b = lw(w1), lw(w0); return (a[0] - b[0], a[1] - b[1])
def shift(w, s):   # applique le décalage (dlane, dW) à w (même direction)
    r, gx, gy, ph = w; X, Y = rot((gx, gy), -r % 6)
    L = X + Y + s[0]; WW = 4 * (X - Y) + ph + s[1]
    ph2 = WW % 4 + 4 * 0
    # 4·along + ph = WW avec 0 ≤ ph < 8 et along ≡ L (mod 2) : along = (WW - ph)/4
    for ph2 in range(8):
        if (WW - ph2) % 4 == 0 and ((WW - ph2) // 4 - L) % 2 == 0:
            al = (WW - ph2) // 4; X2, Y2 = (L + al) // 2, (L - al) // 2
            gx2, gy2 = rot((X2, Y2), r); return (r, gx2, gy2, ph2)
    raise ValueError
if __name__ == '__main__':
    out = []
    for c in R:
        if c['type'] != 'échangé': continue
        wA, wB = tuple(c['A']), tuple(c['B']); oA, oB = map(tuple, c['sorties'])
        # oA = sortie de direction 0 (place de B), oB = sortie de direction r
        sB = sub(oA, wB); sA = sub(oB, wA)
        assert shift(wB, sB) == oA and shift(wA, sA) == oB
        T = c['T']
        res = {}
        for nm, (a_, b_) in {'B+': (wA, shift(wB, sB)), 'A+': (shift(wA, sA), wB), 'AB+': (shift(wA, sA), shift(wB, sB))}.items():
            res[nm] = ''.join(issue(a_, b_, o, T) for o in (0, 1))
        other = [x for x in R if x['r'] == c['r'] and x['tau'] == c['tau'] and x['v'] == c['v'] and x['ordre'] != c['ordre']][0]['type']
        out.append(dict(r=c['r'], tau=c['tau'], v=c['v'], ordre=c['ordre'], autre_ordre=other, sB=sB, sA=sA, decales=res, A=wA, B=wB))
        print(c['r'], c['tau'], c['v'], 'ordre', c['ordre'], '(autre :', other + ')', 'σB', sB, 'σA', sA, res)
    json.dump(out, open('data/swaps.json', 'w'))

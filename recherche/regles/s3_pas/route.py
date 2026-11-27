#!/usr/bin/env python3
"""R-622 ROUTAGE d'un vaisseau-signal R2L2 par des « virages » (S3/T1, 27/11).
Virage = une porte NOR à UNE entrée (nor.BASE) : le signal s (ligne d'univers A) est le partenaire, on pose une puissance K constante
sur la bonne ligne pour que s la heurte à l'instant choisi. Si s est là : s part sur oA, K sur oB (deux copies de s) ; sinon K continue
tout droit (= ¬s). Donc un virage = COPIE (R-609) : 2 copies de s + ¬s, dans des directions fixées par le côté :
  côté '+' : oA = d−2, oB = d+1 ; côté '−' : oA = d+2, oB = d−1 ; 'H' (de face) : oA = d−2, oB = d−1 ; K tout droit = ¬s en d−1, d+1, d+3.
turn(A, side, k) : K, oA, oB, K tout droit, instant du choc — pour le k-ième instant possible (pas de 8) après l'instant 0 de A.
Rien de nouveau pour la simulation : géométrie de nor.gate retournée (le partenaire est donné, on cherche la puissance)."""
from s3lib import *
from nor import BASE, TC
def turn(A, side, k):
    """A : ligne du signal ; k ≥ 0 : choix de l'instant du choc (≈ 8 k + cst). Retour : (K, oA, oB, Kdroit, tchoc)"""
    b = BASE[side]; rotk = (A[0] - b['A'][0]) % 6
    B0, A0, oA0, oB0 = (rotwl(b[x], rotk) for x in ('B', 'A', 'oA', 'oB'))
    # tshift(A0, s) doit avoir la phase de A ; ensuite translation v
    s0 = next(s for s in range(8) if tshift(A0, s)[3] == A[3]); s = s0 + 8 * k
    As = tshift(A0, s); v = (A[1] - As[1], A[2] - As[2])
    f = lambda w: transwl(tshift(w, s), v)
    assert f(A0) == A
    return f(B0), f(oA0), f(oB0), f(B0), s + TC
def lane(w):
    """voie (entier) d'une ligne d'univers dans sa direction, et « temps de passage » τ : la ligne est (r, voie, τ) à translation près"""
    X, Y = rot(antpos(w, 0), -w[0] % 6); return X + Y
if __name__ == '__main__':
    A = (1, -25, 0, 4)
    for side in '+-H':
        K, oA, oB, Kd, t = turn(A, side, 3)
        print(side, 'K', K, 'oA', oA, 'oB', oB, 't', t)
def coord(w):
    """(r, voie ℓ, σ) : coordonnées entières d'une ligne d'univers ; σ augmente de 1 quand on avance la ligne d'un pas (tshift −1)"""
    X, Y = rot((w[1], w[2]), -w[0] % 6); return (w[0], X + Y, 8 * X + w[3])
OUTS = [(s, o) for s in '+-H' for o in (1, 2)]          # o = 1 : oA (le signal dévié), 2 : oB (la puissance déviée)
def follow(A, seq, ks):
    """applique une suite de virages ; renvoie (ligne finale, [(K, tchoc)])"""
    w = A; used = []
    for (side, o), k in zip(seq, ks):
        K, oA, oB, Kd, t = turn(w, side, k); used.append((K, t, side)); w = oA if o == 1 else oB
    return w, used

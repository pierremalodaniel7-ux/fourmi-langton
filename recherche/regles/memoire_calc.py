#!/usr/bin/env python3
"""R-346 Brancher le calcul sur la mémoire : une sortie C = a∧b (UN vaisseau) d'un circuit sert de vaisseau de mise à 1 de la bascule
R-341 (tournée pour que la direction colle). La bascule est posée SUR la route de C, à la phase voulue (M en phase 16 quand C passe le
point de départ de l'expérience R-341). Ensuite : état de la bascule lu dans la grille (M = 0, R' = 1).
Fonctions : place(circuit, sortie C) → pièces de la bascule ; etat(...) → 0 / 1 / '?'."""
import sys, json
from fa_lib import *
from circuit import *
from hx import rot, step
M = 'H:R2L2|0,0,1;1,-1,0|-1,1'; RP = 'H:R2L2|-1,0,3;1,1,0|-1,0;-1,1;0,-1;1,0;1,1'
SET = dict(r=0, l=1, ph=16, D=40)        # R-341 : mise à 1 = vaisseau direction 0, voie 1, M en phase 16, joué après M
RESET = dict(r=2, l=-2, ph=2, D=40)      # mise à 0 = vaisseau direction 2, voie −2, R' en phase 2, joué après R'
def orbit_list(s):
    a, c = parts_of(s); A = [list(x) for x in a]; g = {tuple(x[:2]): 1 for x in c}; A0 = [list(x) for x in A]; g0 = dict(g); L = []
    while True:
        L.append(([tuple(x) for x in A], sorted(g))); step(A, g)
        if A == A0 and g == g0: return L
OM, ORP = orbit_list(M), orbit_list(RP)
def rotp(p, rho, c):
    """rotation de rho crans autour de l'origine puis translation c"""
    x, y = rot((p[0], p[1]), rho); return (x + c[0], y + c[1])
def ship_pos(s):
    """position de référence (phase 0) d'un vaisseau décodé (r, voie, abscisse, phase) — abscisse et voie en repère tourné"""
    r, la, al, ph = s; X, Y = (la + al) // 2, (la - al) // 2
    return rot((X, Y), r)
def place(Cship, Tref, tstar, which=SET):
    """bascule (état M) placée pour que la sortie Cship (décodée au temps Tref, phase 0) arrive comme le vaisseau de mise à 1.
    tstar : instant (multiple de 8 après Tref − 8k) où le vaisseau C est au point de départ de l'expérience. Renvoie (pièces M à t = 0, centre, rho)."""
    r = Cship[0]; rho = (r - which['r']) % 6
    n = (Tref - tstar) // 8; assert (Tref - tstar) % 8 == 0 and Cship[3] == 0
    p = ship_pos(Cship); d = ship_dir(r); pos_t = (p[0] - n * d[0], p[1] - n * d[1])        # C au temps tstar (phase 0)
    # dans le repère de la bascule, le vaisseau de mise à 1 part de sp = -D·d0 + l·e0 (centre en 0)
    d0 = ship_dir(which['r']); e0 = rot((1, 0), which['r']); sp = (-which['D'] * d0[0] + which['l'] * e0[0], -which['D'] * d0[1] + which['l'] * e0[1])
    spr = rot(sp, rho); c = (pos_t[0] - spr[0], pos_t[1] - spr[1])
    ph0 = (which['ph'] - tstar) % len(OM)                      # phase de M à t = 0
    ants, cells = OM[ph0]
    return [(rotp(a, rho, c) + (((a[2] + rho) % 6),), [rotp(q, rho, c) for q in cells]) for a in ants[:1]] + \
           [(rotp(a, rho, c) + (((a[2] + rho) % 6),), []) for a in ants[1:]], c, rho, ph0
def etat(ants, cells, c, rho, t, rad=8):
    """0 si l'objet au centre c est M (une phase, tourné de rho), 1 si R', sinon '?'"""
    na = sorted(tuple(a) for a in ants if hd(a[0] - c[0], a[1] - c[1]) <= rad)
    nc = sorted(tuple(q[:2]) for q in cells if hd(q[0] - c[0], q[1] - c[1]) <= rad)
    for val, L in ((0, OM), (1, ORP)):
        for A_, C_ in L:
            if sorted(rotp(a, rho, c) + ((a[2] + rho) % 6,) for a in A_) == na and sorted(rotp(q, rho, c) for q in C_) == nc: return val
    return '?'
# ---------- version générale (n'importe quelle bascule de bascule_hexa.py) ----------
from exp_osc import setup
def kv(s): return dict(x.split('=') for x in s.split()[1:] if '=' in x)
def place_gen(osc, f, Cship, Tref, tstar):
    """expérience (osc, vaisseau f = dict r, l, ph, ord) tournée/translatée pour que le vaisseau de l'expérience soit le vaisseau Cship
    au temps tstar ; renvoie (pièces de l'objet à t = 0 (une pièce par fourmi), ordre 'avant'/'après', centre, rho, orbite)"""
    r0, l0, ph0, o0 = int(f['r']), int(f['l']), int(f['ph']), int(f['ord'])
    E = setup(osc, r0, l0, ph0, o0)
    rho = (Cship[0] - r0) % 6
    n = (Tref - tstar) // 8; p = ship_pos(Cship); d = ship_dir(Cship[0]); pos_t = (p[0] - n * d[0], p[1] - n * d[1])
    spr = rot(E['ship_start'], rho); c = (pos_t[0] - spr[0], pos_t[1] - spr[1])
    P = len(E['states']); ph_t0 = (ph0 - tstar) % P
    ants, cells = E['states'][ph_t0]
    cells = list(cells)
    pieces = [((*rotp(a, rho, c), (a[2] + rho) % 6), [rotp(q, rho, c) for q in (cells if i == 0 else [])]) for i, a in enumerate(ants)]
    orb = [([(*rotp(a, rho, c), (a[2] + rho) % 6) for a in A_], [rotp(q, rho, c) for q in g_]) for A_, g_ in E['states']]
    cen = rotp(E['center'], rho, c)
    return pieces, ('apres' if o0 == 0 else 'avant'), cen, rho, orb
def orbit_abs(osc_sit, rho, c):
    """orbite (états) d'une situation, tournée de rho autour de 0 puis translatée de c"""
    L = orbit_list(osc_sit)
    return [([(*rotp(a, rho, c), (a[2] + rho) % 6) for a in A_], [rotp(q, rho, c) for q in g_]) for A_, g_ in L]
def which_state(ants, cells, cen, orbs, rad=10):
    na = sorted(tuple(a) for a in ants if hd(a[0] - cen[0], a[1] - cen[1]) <= rad)
    nc = sorted(tuple(q[:2]) for q in cells if hd(q[0] - cen[0], q[1] - cen[1]) <= rad)
    for val, L in orbs:
        for A_, C_ in L:
            if sorted(A_) == na and sorted(C_) == nc: return val
    return '?'

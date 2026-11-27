#!/usr/bin/env python3
"""R-717 (T4) : BOUCLE D'EFFACEMENT. Le vaisseau c_ij' qui vient d'allumer le pixel continue tout droit (direction 0) ; 2 chocs du
catalogue R-700 (chacun avec un vaisseau « horloge » posé à t = 0) le tournent de −120° deux fois (0 -> 4 -> 2) pour qu'il revienne
sur la droite de mise à 0 RST2 du MÊME pixel (dir 2, voie −2) : le pixel s'éteint ssi il était allumé. Recherche exacte (entiers) :
voie de sortie = L0 + α·n1 + β·n2 (n1, n2 = glissements des chocs), puis instant d'arrivée -> u = e − a1 − 720.
Contraintes de phase (pas 2 au même endroit, retard D) : R' en phase 2 à l'arrivée ; M en phase 16/17 à l'arrivée du 2e vaisseau
SET dans les 2 histoires (c' = 0 : M jamais touché ; c' = 1 : SET puis RST). Sortie : t4/boucle_geo.json (familles de solutions)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
NOM = os.environ.get('NOM', 'placement'); PL = json.load(open(os.path.join(T4, NOM + '.json'))); RK = os.environ.get('RST', 'RST2'); TU = int(os.environ.get('TURN', 4))
CAT = TR.catalogue(os.environ.get('TOUS') is None)
TURN = [(k, i, o) for k, c in enumerate(CAT) for i in (0, 1) for o in (0, 1) if (c.outs[o][0] - c.ins[i][0]) % 6 == TU]
# dédoublonnage : un virage = (entrée i, sortie o) du choc aligné sur une même trajectoire
_seen = {}; _O = wl_to_T(STEP.out['c00'])
for k, i, o in TURN:
    C = CAT[k].align(i, _O, 0); key = (C.outs[o], C.te, tuple(sorted(C.ins)))
    _seen.setdefault(key, (k, i, o))
TURN = list(_seen.values())
print(len(CAT), 'chocs ;', len(TURN), 'virages de −120°', flush=True)
def lane(T): return TR.to_label(T)[1]
def V(T): return TR.to_label(T)[2]
res = {}
for nm in CASES:
    p = PL[nm]; O = wl_to_T(STEP.out[nm]); c = tuple(p['c']); a1 = p['arrivee']
    Kr = TR.movT(TR.rotT(kit(RK)['S'], p['rho']), c, 0); target = lane(Kr); sols = []
    for kA, iA, oA in TURN:
        CA0 = CAT[kA].align(iA, O, 0); S1_0 = CA0.outs[oA]
        CA1 = CAT[kA].align(iA, O, 1); S1_1 = CA1.outs[oA]
        for kB, iB, oB in TURN:
            def s2(S1, n2): return CAT[kB].align(iB, S1, n2).outs[oB]
            L00 = lane(s2(S1_0, 0)); al = lane(s2(S1_1, 0)) - L00; be = lane(s2(S1_0, 1)) - L00
            # n1, n2 >= NMIN avec L00 + al n1 + be n2 = target
            n0 = (a1 - CA0.te) // 8
            for n1 in range(n0 + 30, n0 + 700):
                q, rmd = divmod(target - L00 - al * n1, be) if be else (None, 1)
                if rmd or q is None: continue
                n2 = q; CA = CAT[kA].align(iA, O, n1); CB = CAT[kB].align(iB, CA.outs[oA], n2); S2 = CB.outs[oB]
                if S2[0] != Kr[0] or lane(S2) != target: continue
                e = V(Kr) - V(S2)
                if not TR.same(TR.movT(Kr, (0, 0), e), S2): continue
                if e <= CB.te + 8 * 30 or CB.te <= CA.te + 8 * 30: continue          # A puis B puis le pixel
                sols.append(dict(kA=kA, iA=iA, oA=oA, oB=oB, n1=n1, kB=kB, iB=iB, n2=n2, e=e, u=e - a1 - kit(p['kit'])['T'], uA=CA.te, uB=CB.te))
                break
    sols.sort(key=lambda s: s['u']); res[nm] = sols
    from collections import Counter
    print(nm, len(sols), 'familles ; u mod 12 :', sorted(Counter(s['u'] % 12 for s in sols).items()), '; u min', sols[0]['u'] if sols else None, flush=True)
json.dump(res, open(os.path.join(T4, 'boucle_geo_' + NOM + '_' + RK + '.json'), 'w'))

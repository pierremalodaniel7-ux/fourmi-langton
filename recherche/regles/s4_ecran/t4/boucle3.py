#!/usr/bin/env python3
"""R-718 (T4) : boucle d'effacement à 3 chocs 0 -> 4 -> 2 -> 3 (virages −120°, −120°, +60°) qui ramène le vaisseau c_ij' sur la
droite de mise à 0 RST3 (dir 3, voie −2) du même pixel. (La boucle à 2 chocs 0 -> 4 -> 2 vers RST2 donne toujours u ≡ 0 mod 3 alors
que R' demande u ≡ 1 ou 2 : impossible, R-717.) Tout est affine en (n1, n2, n3) (glissements des chocs) : coefficients mesurés,
puis contrôle exact du candidat retenu. Sortie : t4/boucle3_<NOM>.json"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
NOM = os.environ.get('NOM', 'placement'); PL = json.load(open(os.path.join(T4, NOM + '.json')))
CAT = TR.catalogue(False); O0 = wl_to_T(STEP.out['c00'])
def reps(tu):
    seen = {}
    for k, c in enumerate(CAT):
        for i in (0, 1):
            for o in (0, 1):
                if (c.outs[o][0] - c.ins[i][0]) % 6 != tu: continue
                C = c.align(i, O0, 0); seen.setdefault((C.outs[o], C.te, tuple(sorted(C.ins))), (k, i, o))
    return list(seen.values())
SEQ = [reps(4), reps(4), reps(1)]
print('virages :', [len(s) for s in SEQ], flush=True)
def lane(T): return TR.to_label(T)[1]
def V(T): return TR.to_label(T)[2]
def chain(O, tri, ns):
    X = O; chocs = []
    for (k, i, o), n in zip(tri, ns):
        C = CAT[k].align(i, X, n); chocs.append(C); X = C.outs[o]
    return X, chocs
def solve(nm, tri, RK):
    p = PL[nm]; O = wl_to_T(STEP.out[nm]); c = tuple(p['c']); a1 = p['arrivee']
    Kr = TR.movT(TR.rotT(kit(RK)['S'], p['rho']), c, 0); tg = lane(Kr)
    # bases : chaque choc à l'instant où arrive le précédent
    ns = []; X = O; t = a1
    for (k, i, o) in tri:
        C0 = CAT[k].align(i, X, 0); n = (t - C0.te) // 8; ns.append(n); C = CAT[k].align(i, X, n); X = C.outs[o]; t = C.te
    def G(d):
        X, ch = chain(O, tri, [b + x for b, x in zip(ns, d)]); return [lane(X), V(Kr) - V(X)] + [C.te for C in ch]
    g0 = G((0, 0, 0)); gs = [G(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    co = [[g[j] - g0[j] for g in gs] for j in range(len(g0))]
    al, be, ga = co[0]
    out = []
    for d1 in range(30, 300):
        for d2 in range(30, 300):
            if ga == 0: continue
            q, r = divmod(tg - g0[0] - al * d1 - be * d2, ga)
            if r or q < 30: continue
            d = (d1, d2, q); val = [g0[j] + co[j][0] * d1 + co[j][1] * d2 + co[j][2] * q for j in range(len(g0))]
            e, tA, tB, tC = val[1:]
            if not (a1 + 240 < tA < tB - 240 and tB < tC - 240 and tC < e - 240): continue
            out.append((e - a1 - kit(p['kit'])['T'], d))
            break
    return ns, g0, co, out, Kr
if __name__ == '__main__':
    rnd = random.Random(int(os.environ.get('GRAINE', 0))); RK = os.environ.get('RST', 'RST3a')
    from collections import Counter
    cnt = Counter(); best = []
    for it in range(int(os.environ.get('N', 40))):
        tri = [rnd.choice(s) for s in SEQ]
        ns, g0, co, out, Kr = solve('c00', tri, RK)
        for u, d in out: cnt[u % 12] += 1
        if out: best.append(dict(tri=tri, u=[u for u, _ in out[:50]]))
    print(RK, 'u mod 12 :', sorted(cnt.items()), flush=True)
    json.dump(best, open(os.path.join(T4, f'boucle3_{NOM}_{RK}.json'), 'w'))

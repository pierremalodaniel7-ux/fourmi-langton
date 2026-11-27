#!/usr/bin/env python3
"""R-720 (T4) : boucle d'effacement LONGUE (l'écran garde c' presque tout l'intervalle entre 2 pas). Chemin 0 -> 4 -> 3 -> 2
(virages −120°, −60°, −60°) vers la droite RST2 (dir 2, voie −2) : le vaisseau de retour repart en dir 2, jamais de face avec la sortie
c'' de l'usage suivant (sur la boucle 0->4->2->3 vers RST3, il repartirait de face sur la route de c'' : refusé). Délai u choisi dans
[D − 1440 − DMAX, D − 1440 − DMIN] avec u ≡ 14 (mod 84) (R' en phase 2 à l'arrivée ; M en 16/17 à l'arrivée du SET de l'usage 2, D ≡ 0
mod 168). Tout est affine en (n1, n2, n3). Puis contrôle exact et simulation (moteur C) pixel seul + germe, 16 états.
Usage : python3 boucle_long.py pixel [D] -> t4/boucle_long_<pixel>.json"""
import sys, os, json, random, time
os.environ.setdefault('SEQ', '4,5,5')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle3 as B3
import boucle_choix as BC
NOM = os.environ.get('NOM', 'placement'); PL = json.load(open(os.path.join(T4, NOM + '.json'))); RK = 'RST2'
DMIN, DMAX = int(os.environ.get('DMIN', 300)), int(os.environ.get('DMAX', 3000))
def affine(nm, tri):
    p = PL[nm]; O = wl_to_T(STEP.out[nm]); c = tuple(p['c']); a1 = p['arrivee']
    Kr = TR.movT(TR.rotT(kit(RK)['S'], p['rho']), c, 0)
    ns = []; X = O; t = a1
    for (k, i, o) in tri:
        C0 = B3.CAT[k].align(i, X, 0); n = (t - C0.te) // 8; ns.append(n); C = B3.CAT[k].align(i, X, n); X = C.outs[o]; t = C.te
    def G(d):
        X, ch = B3.chain(O, tri, [b + x for b, x in zip(ns, d)]); return [B3.lane(X), B3.V(Kr) - B3.V(X)] + [C.te for C in ch]
    g0 = G((0, 0, 0)); gs = [G(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    co = [[g[j] - g0[j] for g in gs] for j in range(len(g0))]
    # contrôle d'affinité en un point lointain
    dd = (2000, 1500, 1700); gv = G(dd); assert gv == [g0[j] + sum(co[j][k] * dd[k] for k in range(3)) for j in range(len(g0))]
    return ns, g0, co, Kr, O
def search(nm, tri, D):
    p = PL[nm]; a1 = p['arrivee']; KT = kit(p['kit'])['T']; ns, g0, co, Kr, O = affine(nm, tri)
    al, be, ga = co[0]; lo, hi = D - 1440 - DMAX, D - 1440 - DMIN; tg = B3.lane(Kr)
    val = lambda d: [g0[j] + sum(co[j][k] * d[k] for k in range(3)) for j in range(len(g0))]
    # ici (mesuré) : la voie ne dépend pas de d2 (be = 0) -> d3 fixé par d1 ; u = base + c1[1]·d2 : on vise u = 14 + 84 m directement
    if be != 0 or co[1][1] == 0: return None
    c1 = co[1]; best = None
    for d1 in range(100, 60000):
        q, r = divmod(tg - g0[0] - al * d1, ga)
        if r or q < 30: continue
        base = g0[1] - a1 - KT + c1[0] * d1 + c1[2] * q
        for m in range((lo - 14) // 84, (hi - 14) // 84 + 1):
            u = 14 + 84 * m; d2, r2 = divmod(u - base, c1[1])
            if r2 or d2 < 30 or not lo <= u <= hi: continue
            v = val((d1, d2, q)); e, tA, tB, tC = v[1:]
            if a1 + 240 < tA < tB - 240 and tB < tC - 240 and tC < e - 240: return dict(d=(d1, d2, q), u=e - a1 - KT, e=e)
    return None
if __name__ == '__main__':
    nm = sys.argv[1]; D = int(sys.argv[2]) if len(sys.argv) > 2 else 384888; rnd = random.Random(int(os.environ.get('GRAINE', 1)))
    envs = STEP.cases(); test = [e for e in envs if e['x'] == e['y'] == e['h0'] == e['h1'] == 0]; t0 = time.time(); tried = 0
    BC.PL = PL
    while time.time() - t0 < float(os.environ.get('TMAX', 900)):
        tri = [rnd.choice(s) for s in B3.SEQ]
        try: s = search(nm, tri, D)
        except AssertionError: print('non affine', tri, flush=True); continue
        if not s: continue
        tried += 1
        ns, g0, co, Kr, O = affine(nm, tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])]); e = B3.V(Kr) - B3.V(X)
        assert TR.same(TR.movT(Kr, (0, 0), e), X) and e == s['e']
        cand = dict(chocs=chocs, e=e, u=s['u'], toks=BC.order(chocs, tri))
        BC_want = lambda: None
        g, _, _ = BC.check(nm, cand, test, rst=RK)
        print(nm, 'u', s['u'], 'd', s['d'], 'test 16 :', g, f'{time.time()-t0:.0f} s', flush=True)
        if g == 16:
            json.dump(dict(pixel=nm, D=D, tri=tri, d=s['d'], u=s['u'], e=e, rst=RK, toks=[t if t == 'GERM' else [t[0], list(t[1])] for t in cand['toks']],
                           chocs=[dict(ins=C.ins, outs=C.outs, first=C.first, te=C.te) for C in chocs], essais=tried, s=round(time.time() - t0)),
                      open(os.path.join(T4, f'boucle_long_{nm}.json'), 'w'), indent=1)
            print('RETENU', nm, flush=True); sys.exit()
    print('rien trouvé', nm, tried)

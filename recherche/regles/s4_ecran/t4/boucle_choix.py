#!/usr/bin/env python3
"""R-718 (T4) : choix d'une boucle d'effacement à 3 chocs par pixel (t4/boucle3.py), avec u ≡ 22 ou 23 (mod 84) (phases : R' en 10/11
à l'arrivée de RST3, puis M en 16/17 à l'arrivée du 2e SET si D ≡ 0 mod 21). Contrôle exact (trajectoires) puis simulation (moteur C)
du pixel seul + germe sur les 256 états : le pixel s'allume ssi c' = 1, puis est éteint (M, phase prévue), reste = vaisseaux libres.
Usage : NOM=placement python3 boucle_choix.py [pixel]  -> t4/boucle_<pixel>.json"""
import sys, os, json, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import boucle3 as B3
NOM = os.environ.get('NOM', 'placement'); PL = json.load(open(os.path.join(T4, NOM + '.json')))
def order(chocs, tri):
    toks = ['GERM']; sig = 'GERM'; clocks = []
    for j, (C, (k, i, o)) in enumerate(zip(chocs, tri)):
        kap = ('K%d' % j, C.ins[1 - i]); name = kap[0]; names = [t if t == 'GERM' else t[0] for t in toks]; pos = names.index(sig)
        toks.insert(pos + 1 if C.first == i else pos, kap)
        if o != i: sig = name
    return toks
def make(nm, tri, d):
    p = PL[nm]; O = wl_to_T(STEP.out[nm]); ns, g0, co, out, Kr = B3.solve(nm, tri, 'RST3a')
    X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, d)]); e = B3.V(Kr) - B3.V(X)
    assert TR.same(TR.movT(Kr, (0, 0), e), X)
    return dict(chocs=chocs, e=e, u=e - p['arrivee'] - kit(p['kit'])['T'], toks=order(chocs, tri))
def check(nm, cand, envs, T=None):
    p = PL[nm]; PL1 = {k: (PL[k] if k == nm else None) for k in CASES}
    T = T or cand['e'] + 720 + 200
    sits = []
    for e in envs:
        A, G = [], []
        a, g = place_ordered(0, p['phase0'], p['rho'], tuple(p['c'])); A += a; G += g
        for tok in cand['toks']:
            if tok == 'GERM':
                for w in STEP.present(e): pa, cs = render3(w, 0); A.append(pa); G += cs
            else: (x, y, h), cs = TR.piece_at(tok[1], 0); A.append((x, y, h)); G += cs
        sits.append(S3L.sit(A, G))
    R = run_c(sits, T); good = 0
    for e, (a, c) in zip(envs, R):
        st = pixel.read_state(a, c, p['rho'], tuple(p['c']))
        ra = [x for x in a if hd(x[0] - p['c'][0], x[1] - p['c'][1]) > 6]; rc = [q for q in c if hd(q[0] - p['c'][0], q[1] - p['c'][1]) > 6]
        if spec(nm, e) == 1: want = (0, (8 + (cand['u'] % 12 == 11) + T - cand['e'] - 720) % 21)
        else: want = (0, (kit(p['kit'])['ph'] + T - p['arrivee']) % 21)
        good += st == want and decode3(ra, rc, T) is not None
    return good, sits, R
if __name__ == '__main__':
    nm = sys.argv[1]; rnd = random.Random(int(os.environ.get('GRAINE', 1))); t0 = time.time(); tried = 0
    envs = STEP.cases(); test = [e for e in envs if e['x'] == e['y'] == e['h0'] == e['h1'] == 0][:16]
    while time.time() - t0 < float(os.environ.get('TMAX', 600)):
        tri = [rnd.choice(s) for s in B3.SEQ]; ns, g0, co, out, Kr = B3.solve(nm, tri, 'RST3a')
        for u, d in out:
            if u % 84 not in (22, 23) or u > 9000: continue
            tried += 1; cand = make(nm, tri, d)
            g, _, _ = check(nm, cand, test)
            print(nm, 'u', u, 'd', d, 'test 16 :', g, flush=True)
            if g == 16:
                g2, _, _ = check(nm, cand, envs); print('  256 états :', g2, flush=True)
                if g2 == 256:
                    json.dump(dict(pixel=nm, tri=tri, d=d, u=cand['u'], e=cand['e'], toks=[t if t == 'GERM' else [t[0], list(t[1])] for t in cand['toks']],
                                   chocs=[dict(ins=C.ins, outs=C.outs, first=C.first, te=C.te) for C in cand['chocs']], essais=tried, s=round(time.time() - t0)),
                              open(os.path.join(T4, f'boucle_{nm}.json'), 'w'), indent=1)
                    print('RETENU', nm, flush=True); sys.exit()
            break
    print('rien trouvé', nm, tried)

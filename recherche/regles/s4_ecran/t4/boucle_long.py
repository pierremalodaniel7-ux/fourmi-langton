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
NOM = os.environ.get('NOM', 'placement'); PL = json.load(open(os.path.join(T4, NOM + '.json'))); RK = os.environ.get('RST', 'RST2')
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
    # cas général : d3 = (tg − g0 − al·d1 − be·d2) / ga ; u affine en (d1, d2) une fois d3 éliminé (réel) ; on balaie d1, on encadre d2
    c1 = co[1]; K0u = g0[1] - a1 - KT
    def u_of(d1, d2, d3): return K0u + c1[0] * d1 + c1[1] * d2 + c1[2] * d3
    # pentes réelles de u en d1 et d2 (d3 éliminé)
    s1 = c1[0] - c1[2] * al / ga; s2 = c1[1] - c1[2] * be / ga; s0 = K0u + c1[2] * (tg - g0[0]) / ga
    RES = [int(x) for x in os.environ.get('RES', '14').split(',')]
    for d1 in range(30, 60000):
        if s2 == 0: break
        x1, x2 = sorted(((lo - s0 - s1 * d1) / s2, (hi - s0 - s1 * d1) / s2))
        for d2 in range(max(30, int(x1) - 1), int(x2) + 2):
            q, r = divmod(tg - g0[0] - al * d1 - be * d2, ga)
            if r or q < 30: continue
            u = u_of(d1, d2, q)
            if not (lo <= u <= hi and u % 84 in RES): continue
            v = val((d1, d2, q)); e, tA, tB, tC = v[1:]
            if a1 + 240 < tA < tB - 240 and tB < tC - 240 and tC < e - 240: return dict(d=(d1, d2, q), u=e - a1 - KT, e=e)
    return None
def pretest(nm, cand, D, O):
    """la boucle seule (sans germe ni pixel), hx.py : (1) signal absent : les 3 horloges seules jusqu'à D + 13 000 -> que des vaisseaux,
    0 case orpheline ; (2) signal présent : le vaisseau c_nm' (libre, après le pixel) + les horloges, de a1 + 800 à e + 200 -> le retour
    est EXACTEMENT sur la droite RST, le reste = vaisseaux propres"""
    p = PL[nm]; toks = cand['toks']
    def pieces(t, with_sig):
        A, G = [], []
        for tok in toks:
            if tok == 'GERM':
                if not with_sig: continue
                (x, y, h), cs = TR.piece_at(O, t)
            else: (x, y, h), cs = TR.piece_at(tok[1], t)
            A.append((x, y, h)); G += cs
        return S3L.sit(A, G)
    T1 = D + 13000; a, c = run_py(pieces(0, False), T1); dp, bd, orph = decode_partiel(a, c, T1)
    if bd or orph: return 'absent sale'
    t0 = p['arrivee'] + 800; T2 = cand['e'] + 200; a, c = run_py(pieces(t0, True), T2 - t0)
    from lib4 import labels_at
    L = labels_at(a, c, T2)
    if L is None: return 'présent sale'
    want = TR.to_label(cand['X'])
    return 'ok' if want in L else 'présent : retour absent'
def test2(nm, cand, D, envs):
    """2 usages (usage 2 = R-61(s0)), pixel nm seul + sa boucle, hx.py sur 2 cœurs, lecture après le 2e SET : pixel = c'' (état + phase),
    les 8 sorties de l'usage 2 justes, reste propre"""
    from multiprocessing import Pool
    import ecran_deux_pas as E2
    p = PL[nm]; a1 = p['arrivee']; a2 = a1 + D; T = a2 + 720 + 100; jobs = []
    for e0 in envs:
        e1 = E2.rl(e0); A, G = [], []
        a, g = place_ordered(0, p['phase0'], p['rho'], tuple(p['c'])); A += a; G += g
        for tok in cand['toks']:
            if tok == 'GERM':
                for u, ee in ((0, e0), (D, e1)):
                    for w in STEP.present(ee): pa, cs = render3(S3L.tshift(w, u), 0); A.append(pa); G += cs
            else: (x, y, h), cs = TR.piece_at(tok[1], 0); A.append((x, y, h)); G += cs
        jobs.append((S3L.sit(A, G), T))
    with Pool(2) as pool: R = pool.starmap(run_py, jobs)
    good = 0
    for e0, (a, c) in zip(envs, R):
        e1 = E2.rl(e0); st = pixel.read_state(a, c, p['rho'], tuple(p['c']))
        ra = [x for x in a if hd(x[0] - p['c'][0], x[1] - p['c'][1]) > 6]; rc = [q for q in c if hd(q[0] - p['c'][0], q[1] - p['c'][1]) > 6]
        d = decode3(ra, rc, T); outs_ok = d is not None and all(int(S3L.tshift(STEP.out[k], D) in d) == spec(k, e1) for k in STEP.names if k != nm)
        ok = outs_ok and isinstance(st, tuple) and st[0] == spec(nm, e1); good += ok
        if os.environ.get('DIAG'):
            dp, bd, orph = decode_partiel(ra, rc, T); print('    non-vaisseaux', bd[:6], 'orphelines', len(orph), 'sorties (partiel)', {k: int(S3L.tshift(STEP.out[k], D) in dp) for k in STEP.names}, flush=True)
            print('   ', (spec(nm, e0), spec(nm, e1)), 'pixel', st, 'propre', d is not None, 'sorties', {k: int(S3L.tshift(STEP.out[k], D) in (d or [])) for k in STEP.names}, 'attendu', {k: spec(k, e1) for k in STEP.names}, flush=True)
    return good
if __name__ == '__main__':
    nm = sys.argv[1]; D = int(sys.argv[2]) if len(sys.argv) > 2 else 384888; rnd = random.Random(int(os.environ.get('GRAINE', 1)))
    import ecran_deux_pas as E2
    envs = STEP.cases(); t0 = time.time(); tried = 0
    test = []
    for want in ((1, 1), (1, 0), (0, 1), (0, 0)):
        test += [e for e in envs if (spec(nm, e), spec(nm, E2.rl(e))) == want][:1]
    BC.PL = PL
    import conflits as CF; GSEG = CF.germ_segments(D)
    while time.time() - t0 < float(os.environ.get('TMAX', 900)):
        tri = [rnd.choice(s) for s in B3.SEQ]
        try: s = search(nm, tri, D)
        except AssertionError: print('non affine', tri, flush=True); continue
        if not s: continue
        tried += 1
        ns, g0, co, Kr, O = affine(nm, tri); X, chocs = B3.chain(O, tri, [b + x for b, x in zip(ns, s['d'])]); e = B3.V(Kr) - B3.V(X)
        assert TR.same(TR.movT(Kr, (0, 0), e), X) and e == s['e']
        cand = dict(chocs=chocs, e=e, u=s['u'], toks=BC.order(chocs, tri), X=X)
        pt = pretest(nm, cand, D, O)
        if pt != 'ok': print('  pré-test :', pt, flush=True); continue
        okg, wst = CF.loop_ok(nm, PL, tri, chocs, e, D, GSEG)
        if not okg: print('  conflit géométrique :', wst[0], flush=True); continue
        # signal absent : les 3 horloges filent tout droit ; elles ne doivent pas se croiser (distance >= 12 sur [0, D + 13 000])
        from lib4 import closest
        KL = [TR.to_label(C.ins[1 - i]) for C, (k, i, o) in zip(chocs, tri)]
        g = test2(nm, cand, D, test)
        print(nm, 'u', s['u'], 'd', s['d'], 'test 2 usages (4 états, hx.py) :', g, f'{time.time()-t0:.0f} s', flush=True)
        if g == 4:
            json.dump(dict(pixel=nm, D=D, tri=tri, d=s['d'], u=s['u'], e=e, rst=RK, toks=[t if t == 'GERM' else [t[0], list(t[1])] for t in cand['toks']],
                           chocs=[dict(ins=C.ins, outs=C.outs, first=C.first, te=C.te) for C in chocs], essais=tried, s=round(time.time() - t0)),
                      open(os.path.join(T4, f'boucle_long_{nm}.json'), 'w'), indent=1)
            print('RETENU', nm, flush=True); sys.exit()
    print('rien trouvé', nm, tried)

#!/usr/bin/env python3
"""R-720 (T4) : DEUX PAS DE SUITE À L'ÉCRAN, boucles d'effacement LONGUES (t4/boucle_long_<pixel>.json, chemin 0->4->3->2 vers RST2).
Germe R-617 utilisé 2 fois au même endroit (usage 2 retardé de D, entrées = s1 = R-61(s0)), 4 pixels, 4 boucles (12 horloges), tout
posé à t = 0, UNE simulation par état initial. Lectures exactes (état + phase prévus de chaque pixel) :
  tA  = juste après le pas 1 (écran = c'),  tA2 = juste avant le premier effacement (écran = c' encore, ≈ 380 000 pas plus tard),
  tB  = après les effacements (tout éteint), tC = après le pas 2 (écran = c'').
hx.py (pas à pas, les 4 lectures en un passage) sur les états [i0, i1) -> t4/data_deux_pas/hx_<i0>_<i1>.json ;
moteur C à tC (option C) sur les 256 états -> t4/data_deux_pas/c_tC.json. Usage : python3 deux_pas_long.py hx i0 i1 | C"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import ecran_deux_pas as E2
PL = json.load(open(os.path.join(T4, 'placement.json')))
LOOP = {nm: json.load(open(os.path.join(T4, f'boucle_long_{nm}.json'))) for nm in CASES}
D = LOOP['c00']['D']; assert all(LOOP[nm]['D'] == D for nm in CASES)
E2.LOOP = LOOP; E2.PL = PL
MFIN = {('RST3a', 10): 8, ('RST3a', 11): 9, ('RST2', 2): 0}
def predict(e0, nm, t):
    e1 = E2.rl(e0); p = PL[nm]; a1 = p['arrivee']; K = kit(p['kit']); L = LOOP[nm]; e = L['e']; a2 = a1 + D
    if spec(nm, e0) == 0: hist = (0, (K['ph'] + t - a1) % 21); mph_a2 = (K['ph'] + D) % 21
    else:
        rph = (K['fin'] + e - a1 - 720) % 12; mf = MFIN[(L['rst'], rph)]
        hist = (1, (K['fin'] + t - a1 - 720) % 12) if t < e else (0, (mf + t - e - 720) % 21)
        mph_a2 = (mf + a2 - e - 720) % 21
    if t < a2 + 720 or spec(nm, e1) == 0: return hist
    return (1, ({16: 0, 17: 1}[mph_a2] + t - a2 - 720) % 12)
TA = max(PL[nm]['arrivee'] for nm in CASES) + 800
TA2 = min(LOOP[nm]['e'] for nm in CASES) - 20
TB = max(LOOP[nm]['e'] for nm in CASES) + 720 + 50
TC = max(PL[nm]['arrivee'] for nm in CASES) + D + 720 + 100
assert TA < TA2 < TB < min(PL[nm]['arrivee'] for nm in CASES) + D
TOKS = E2.tokens()
# R-723 : ports de lecture (t4/lecture_<pixel>_<t>.json), ajoutés en fin de liste (ils ne touchent que leur pixel)
import glob
LECT = sorted(glob.glob(os.path.join(T4, 'lecture_c*_*.json'))) if os.environ.get('LECT') else []
LECTS = [json.load(open(f)) for f in LECT]
for L in LECTS: TOKS = TOKS + [(f"L{L['pixel']}_{L['tr']}_{t[0]}", tuple(t[1])) for t in L['toks']]
def lectures(dp, T, e0):
    labs = [TR.of_label(TR.lab_piece(render3(w, T), T)) for w in dp]
    return {f"{L['pixel']}@{L['tr']}": [int(any(TR.same(tuple(L['sonde']), x) for x in labs)), spec(L['pixel'], e0)] for L in LECTS}
def sit_of(e0): return build_sit([e0, E2.rl(e0)], [0, D], PL, clocks=TOKS)
def check(e0, t, a, c):
    scr, ra, rc = read_screen(a, c, PL); want = {nm: predict(e0, nm, t) for nm in CASES}
    dp, bd, orph = decode_partiel(ra, rc, t)
    return dict(juste=all(scr[nm] == want[nm] for nm in CASES), propre=not bd and not orph,
                lu={nm: list(scr[nm]) if isinstance(scr[nm], tuple) else scr[nm] for nm in CASES}), dp
def empreinte(a, c):
    import hashlib; return hashlib.md5(repr((sorted(map(tuple, a)), sorted(map(tuple, c)))).encode()).hexdigest()
OUT = os.path.join(T4, 'data_deux_pas'); os.makedirs(OUT, exist_ok=True)
if __name__ == '__main__':
    envs = STEP.cases(); mode = sys.argv[1]
    if mode == 'hx':
        i0, i1 = int(sys.argv[2]), int(sys.argv[3]); res = {}; fn = os.path.join(OUT, f'hx{"_lect" if LECTS else ""}_{i0}_{i1}.json')
        for i in range(i0, i1):
            t0 = time.time(); a_, c_ = S3L.parse(sit_of(envs[i])); A = [list(x) for x in a_]; G = {tuple(q): 1 for q in c_}; t = 0; r = {}
            for nom, T in (('tA', TA), ('tA2', TA2), ('tB', TB), ('tC', TC)):
                for _ in range(T - t): TR.step(A, G)
                t = T; ck, dp = check(envs[i], T, [tuple(x) for x in A], sorted(G)); r[nom] = ck
                if nom == 'tA2' and LECTS: r['lectures'] = lectures(dp, T, envs[i]); ck['juste'] &= all(v[0] == v[1] for v in r['lectures'].values())
            e1 = E2.rl(envs[i]); r['sorties_usage2'] = all(int(S3L.tshift(STEP.out[k], D) in dp) == spec(k, e1) for k in STEP.names)
            r['empreinte'] = empreinte([tuple(x) for x in A], list(G))
            r['s'] = round(time.time() - t0); res[i] = r
            json.dump(dict(D=D, lectures=dict(tA=TA, tA2=TA2, tB=TB, tC=TC), res=res), open(fn, 'w'))
            print(i, {k: (v['juste'], v['propre']) for k, v in r.items() if isinstance(v, dict) and 'juste' in v}, 'sorties', r['sorties_usage2'], r['s'], 's', flush=True)
    else:
        t0 = time.time(); R = run_c([sit_of(e) for e in envs], TC); res = {}
        for i, (a, c) in enumerate(R):
            ck, dp = check(envs[i], TC, a, c); ck['empreinte'] = empreinte(a, c); res[i] = ck
        json.dump(dict(D=D, tC=TC, res=res, s=round(time.time() - t0), lectures=LECT), open(os.path.join(OUT, 'c_tC' + ('_lect' if LECTS else '') + '.json'), 'w'))
        print('C : justes', sum(v['juste'] for v in res.values()), 'propres', sum(v['propre'] for v in res.values()), round(time.time() - t0), 's')

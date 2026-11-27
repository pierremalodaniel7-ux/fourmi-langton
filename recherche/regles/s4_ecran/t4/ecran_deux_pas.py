#!/usr/bin/env python3
"""R-719 (T4) : DEUX PAS DE SUITE À L'ÉCRAN. Le germe du pas complet R-617 sert 2 fois au même endroit (usage 2 retardé de D, ses
vaisseaux d'entrée = l'état s1 = R-61(s0), posés à t = 0 comme dans step.multi_check), avec les 4 pixels (t4/placement.json) et,
pour chaque pixel, sa boucle d'effacement (t4/boucle_<pixel>.json : 3 vaisseaux horloges). Lectures exactes (état + phase prévus) :
t_A (pas 1 affiché = c'), t_B (après les boucles : tout éteint), t_C (pas 2 affiché = c''). Tout posé à t = 0, UNE simulation par
état initial s0. Moteur C sur les 256 états ; hx.py (2e moteur) sur NPY états.
Usage : python3 ecran_deux_pas.py [NPY] [D]  -> t4/ecran_deux_pas.json"""
import sys, os, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
PL = json.load(open(os.path.join(T4, os.environ.get('NOM', 'placement') + '.json')))
LOOP = {nm: json.load(open(os.path.join(T4, f'boucle_{nm}.json'))) for nm in CASES}
def rl(e):                                   # le pas R-61 (vraie fourmi RL sur le tore 2×2), bit par bit
    s = {nm: spec(nm, e) for nm in ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11']}; s['h1'] = spec('h1', e); return s
def tokens():
    pre, post = [], []
    for nm in CASES:
        t = LOOP[nm]['toks']; g = t.index('GERM')
        pre += [(f'{nm}_{x[0]}', tuple(x[1])) for x in t[:g]]; post += [(f'{nm}_{x[0]}', tuple(x[1])) for x in t[g + 1:]]
    return pre + ['GERM'] + post
def predict(e0, D):
    """état + phase attendus de chaque pixel aux 3 lectures"""
    e1 = rl(e0); KT = 720; out = {}
    for nm in CASES:
        p = PL[nm]; a1 = p['arrivee']; ph1 = kit(p['kit'])['ph']; L = LOOP[nm]; e = L['e']; a2 = a1 + D
        def at(t, nm=nm, a1=a1, ph1=ph1, e=e, a2=a2, p=p):
            if spec(nm, e0) == 0:                 # jamais allumé au pas 1
                if t < a2 + KT or e1[nm] == 0: return (0, (ph1 + t - a1) % 21) if t < a2 + KT or e1[nm] == 0 else None
            else:
                if t < e: return (1, (kit(p['kit'])['fin'] + t - a1 - KT) % 12)
                rph = (kit(p['kit'])['fin'] + e - a1 - KT) % 12; mfin = {10: 8, 11: 9}[rph]
                if t < a2 + KT or e1[nm] == 0: return (0, (mfin + t - e - KT) % 21)
            # allumé au pas 2 : phase de M à a2 -> kit SET0a (16, R' 0) ou SET0b (17, R' 1)
            mph = at(a2 - 1, nm, a1, ph1, e, a2, p)[1]; mph = (mph + 1) % 21; fin = {16: 0, 17: 1}[mph]
            return (1, (fin + t - a2 - KT) % 12)
        out[nm] = at
    return out, e1
if __name__ == '__main__':
    NPY = int(sys.argv[1]) if len(sys.argv) > 1 else 4; D = int(sys.argv[2]) if len(sys.argv) > 2 else 384888
    assert D % 168 == 0 and D >= 384741
    t0 = time.time(); envs = STEP.cases(); toks = tokens()
    tA = max(PL[nm]['arrivee'] for nm in CASES) + 800; tB = max(LOOP[nm]['e'] for nm in CASES) + 720 + 50
    tC = max(PL[nm]['arrivee'] for nm in CASES) + D + 720 + 100
    assert tA < min(LOOP[nm]['e'] for nm in CASES)
    sits = [build_sit([e, rl(e)], [0, D], PL, clocks=toks) for e in envs]
    rep = dict(D=D, lectures=dict(tA=tA, tB=tB, tC=tC), fourmis=sits[0].split('|')[1].count(';') + 1)
    print('fourmis à t = 0 :', rep['fourmis'], '; lectures', tA, tB, tC, flush=True)
    res = {}
    for nom, T in (('A', tA), ('B', tB), ('C', tC)):
        t1 = time.time(); R = run_c(sits, T); good = 0; clean = 0; bad = []
        for e, (a, c) in zip(envs, R):
            pr, e1 = predict(e, D); scr, ra, rc = read_screen(a, c, PL); want = {nm: pr[nm](T) for nm in CASES}
            ok = all(scr[nm] == want[nm] for nm in CASES); good += ok; d = decode3(ra, rc, T); clean += d is not None
            if not ok: bad.append(dict(s0=e, lu={k: str(v) for k, v in scr.items()}, attendu={k: str(v) for k, v in want.items()}))
        res[nom] = dict(t=T, justes=good, propres=clean, mauvais=bad[:4], s=round(time.time() - t1)); print(nom, res[nom], flush=True)
        if nom == 'C': RC = R
        rep['res'] = res; json.dump(rep, open(os.path.join(T4, 'ecran_deux_pas.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    sel = random.Random(0).sample(range(256), NPY); same = 0; t1 = time.time()
    for i in sel:
        pa, pc = run_py(sits[i], tC); a, c = RC[i]; ok = sorted(pa) == sorted(a) and sorted(pc) == sorted(c); same += ok
        print('hx.py état', i, ok, f'{time.time()-t1:.0f} s', flush=True)
        rep['py'] = dict(etats=sel, identiques=same, s=round(time.time() - t1))
        json.dump(rep, open(os.path.join(T4, 'ecran_deux_pas.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    rep['duree_s'] = round(time.time() - t0); json.dump(rep, open(os.path.join(T4, 'ecran_deux_pas.json'), 'w'), ensure_ascii=False, indent=1, default=str)

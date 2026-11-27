#!/usr/bin/env python3
"""R-715 (T4) : l'écran 2×2 branché sur le pas complet R-617. Pixels M (OFF) posés à t = 0 sur les 4 sorties c00' c10' c01' c11'
(t4/placement.json) ; le vaisseau de sortie de c_ij' (présent ssi c_ij' = 1) fait la mise à 1 (R' = ON) en passant.
Vérifie, pour les 256 états : écran lu (état exact + phase de chaque pixel) = (c00', c10', c01', c11') de R-61, et le reste = vaisseaux
libres. Moteur C sur les 256 ; hx.py sur NPY états (les 16 états de cases avec x = y = h = 0, puis un échantillon).
Usage : python3 ecran_un_pas.py [NPY]  -> t4/ecran_un_pas.json"""
import sys, os, json, time, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
PL = json.load(open(os.path.join(T4, 'placement.json')))
def pixels_init(PL, phases=None):
    A, G = [], []
    for nm in CASES:
        p = PL[nm]; a, g = place_ordered(0, p['phase0'] if phases is None else phases[nm], p['rho'], tuple(p['c'])); A += a; G += g
    return A, G
def situation(e_list, delays=None, extra=None, PL=PL, phases=None):
    """pixels d'abord (ordre de jeu), puis les vaisseaux du pas (usage u retardé de delays[u]) et des vaisseaux en plus"""
    A, G = pixels_init(PL, phases); W = []
    for u, e in enumerate(e_list): W += [S3L.tshift(w, (delays or [0])[u]) for w in STEP.present(e)]
    W += extra or []
    for w in W:
        a, cs = render3(w, 0); A.append(a); G += cs
    assert len(set(G)) == len(G)
    return S3L.sit(A, G)
def lire(ants, cells, PL=PL):
    scr = {nm: pixel.read_state(ants, cells, PL[nm]['rho'], tuple(PL[nm]['c'])) for nm in CASES}
    near = lambda q: any(hd(q[0] - PL[nm]['c'][0], q[1] - PL[nm]['c'][1]) <= 6 for nm in CASES)
    ra = [a for a in ants if not near(a)]; rc = [q for q in cells if not near(q)]
    return scr, ra, rc
if __name__ == '__main__':
    NPY = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    t0 = time.time(); envs = STEP.cases(); TR_ = max(PL[nm]['arrivee'] for nm in CASES) + kit('SET0a')['T'] + 100
    sits = [situation([e]) for e in envs]; R = run_c(sits, TR_)
    good = 0; clean = 0; bad = []; res = []
    for e, (a, c) in zip(envs, R):
        scr, ra, rc = lire(a, c); want = {nm: spec(nm, e) for nm in CASES}
        lu = {nm: (scr[nm][0] if isinstance(scr[nm], tuple) else '?') for nm in CASES}
        d = decode3(ra, rc, TR_); ok = lu == want; good += ok; clean += d is not None
        if not ok or d is None: bad.append(dict(etat=e, lu=lu, attendu=want, propre=d is not None))
    print(f'moteur C : 256 états, écran juste {good}/256, reste propre {clean}/256 — T = {TR_}, {time.time()-t0:.0f} s', flush=True)
    # 2e moteur
    sel = [i for i, e in enumerate(envs) if e['x'] == e['y'] == e['h0'] == e['h1'] == 0]
    rnd = random.Random(0); rest = [i for i in range(256) if i not in sel]; sel += rnd.sample(rest, max(0, NPY - len(sel)))
    t1 = time.time(); same = 0
    for i in sel:
        pa, pc = run_py(sits[i], TR_); a, c = R[i]; same += sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
    print(f'hx.py : {same}/{len(sel)} états finaux identiques au moteur C — {time.time()-t1:.0f} s', flush=True)
    json.dump(dict(T=TR_, justes=good, propres=clean, py_identiques=same, py_n=len(sel), py_etats=sel, mauvais=bad[:8],
                   placement=PL, duree_s=round(time.time() - t0)), open(os.path.join(T4, 'ecran_un_pas.json'), 'w'), ensure_ascii=False, indent=1)

import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import ecran_deux_pas as E2
D = int(sys.argv[1]) if len(sys.argv) > 1 else 384888; e0 = STEP.cases()[0]; e1 = E2.rl(e0); print('s0', e0, '\ns1', e1, '\ns2', E2.rl(e1))
for name, toks in (('avec boucles', E2.tokens()), ('sans boucles', None)):
    s = build_sit([e0, e1], [0, D], E2.PL, clocks=toks); T = max(E2.PL[nm]['arrivee'] for nm in CASES) + D + 720 + 100
    t0 = time.time(); a, c = run_py(s, T); scr, ra, rc = read_screen(a, c, E2.PL); d = decode3(ra, rc, T)
    outs = {nm: int(S3L.tshift(STEP.out[nm], D) in (d or [])) for nm in STEP.names}
    print(name, f'{time.time()-t0:.0f} s', scr, 'sorties usage 2 :', outs, 'attendu', {nm: spec(nm, e1) for nm in STEP.names})

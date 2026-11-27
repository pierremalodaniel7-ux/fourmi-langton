import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import ecran_deux_pas as E2
D = int(sys.argv[1]); e0 = STEP.cases()[0]; e1 = E2.rl(e0)
s = build_sit([e0, e1], [0, D], E2.PL, clocks=E2.tokens())
for TT in [int(x) for x in sys.argv[2:]]:
    a, c = run_py(s, TT); scr, ra, rc = read_screen(a, c, E2.PL); d = decode3(ra, rc, TT)
    print(TT, scr, 'propre', d is not None)
    if d is not None:
        w = S3L.tshift(STEP.out['c00'], D); print(' c00 usage 2 présent', w in d)
        # vaisseaux les plus proches du point où devrait être c00''
        p = S3L.antpos(w, TT); near = sorted((hd(S3L.antpos(x, TT)[0] - p[0], S3L.antpos(x, TT)[1] - p[1]), x) for x in d)[:4]; print(' proches', near)
    else:
        print(' fourmis non décodées près de c00 :', [x for x in ra if hd(x[0] + 2705, x[1] - 752) < 3000][:10])

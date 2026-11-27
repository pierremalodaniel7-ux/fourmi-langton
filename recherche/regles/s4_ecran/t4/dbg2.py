import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import ecran_deux_pas as E2
D = int(sys.argv[1]); e0 = STEP.cases()[0]; e1 = E2.rl(e0)
W = [w for w in STEP.present(e0)] + [S3L.tshift(w, D) for w in STEP.present(e1)]
s = S3L.sit_wls(W); T = 11866 + D + 820
for TT in (D + STEP.tmax + 1200, T):
    a, c = run_py(s, TT); d = decode3(a, c, TT)
    print(TT, 'propre', d is not None, {nm: int(S3L.tshift(STEP.out[nm], D) in (d or [])) for nm in STEP.names})

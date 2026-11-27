"""S2 : analyse d'une orbite (segments de vol libre de chaque fourmi). Usage : python3 s2_horloge/anal.py n"""
import sys, json
sys.path.insert(0, '.')
from hx import step, PHASES
from demi_add_k import OFFS, lane
from fa_lib import along, parts_of
from exp_osc import hd
def segs(s, T):
    a, c = parts_of(s); A = [list(t) for t in a]; G = {tuple(t[:2]): 1 for t in c}
    cur = [None]*len(A); out = [[] for _ in A]
    for t in range(T+1):
        for i, (x, y, h) in enumerate(A):
            ok = all(hd(x-b[0], y-b[1]) > 6 for j, b in enumerate(A) if j != i)
            k = None
            if ok:
                near = frozenset((p[0]-x, p[1]-y) for p in G if hd(p[0]-x, p[1]-y) <= 2)
                k = PHASES.get((h, near))
            if k:
                r, ph = k; gx, gy = x-OFFS[(r, ph)][0], y-OFFS[(r, ph)][1]
                key = (r, lane(gx, gy, r))
                if cur[i] and cur[i][0] == key: cur[i][2] = t; cur[i][4] = (x, y)
                else:
                    cur[i] = [key, t, t, (x, y), (x, y)]; out[i].append(cur[i])
            else: cur[i] = None
        step(A, G)
    return out
if __name__ == '__main__':
    H = json.load(open('resumes/horloges_6_fourmis.json'))
    n = int(sys.argv[1]); h = H[n]
    o = segs(h['situation'], h['P'])
    for i, L in enumerate(o):
        print('fourmi', i, [(k[0], k[1], k[2], k[3], k[4]) for k in L if k[2]-k[1] >= 16])

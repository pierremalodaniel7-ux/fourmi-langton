"""S2 R-506 — lit anti_k*_*.json : séquence compressée des états des deux pixels (A = fourmis 2,3 ; B = 0,1) sur une période.
Usage : python3 s2_horloge/anti_check.py fichier n"""
import sys, json, itertools
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import anti_pixel as ap
from hx import rot
from fa_lib import parts_of
from hx import step
W = json.load(open(sys.argv[1])); w = W[int(sys.argv[2])]; k = w['k']
a, c = parts_of(ap.W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
M = ap.local(A, G, (0, 1)); O_M = ap.orbit(*M)
for _ in range(1000): step(A, G)   # milieu du 1er ON (plage 438-1115)
Rp = ap.local(A, G, (0, 1)); O_R = ap.orbit(*Rp)
def rt(o, k):
    a_, c_ = o; cx, cy = a_[0][0], a_[0][1]
    return [(*rot((x - cx, y - cy), k), (h + k) % 6) for x, y, h in a_], [rot((x - cx, y - cy), k) for x, y in c_]
tA = ap.timeline(w['sit'], (2, 3), O_M, O_R, 2 * ap.P); tB = ap.timeline(w['sit'], (0, 1), ap.orbit(*rt(M, k)), ap.orbit(*rt(Rp, k)), 2 * ap.P)
def rl(s): return [(ch, len(list(g))) for ch, g in itertools.groupby(s)]
print('A', rl(tA)[:30]); print('B', rl(tB)[:30])
both = ''.join('x' if {x, y} == {'0', '1'} else ('=' if x == y and x != '?' else '?') for x, y in zip(tA, tB))
print('opp', both.count('x'), 'same', both.count('='), '?', both.count('?'), 'sur', len(both)); print(rl(both)[:30])

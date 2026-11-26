"""S2 R-500 — famille « triangle » : choc fixe au coin C0 (A = vaisseau dir 0 virtuel (0,0) phase 0 ; B = vaisseau dir 5 virtuel
(0,2) phase 7, B joués avant A), T = 133 + 8 j. Construit le terme j directement (tri.py : rotation R = rot120 + c_j).
Usage : python3 s2_horloge/famille.py jmin jmax [pas]  → CYCLE fourmi_r pour chaque j."""
import sys
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from tri import collide, adv, R, at
from tri_test import build
from hx import rot
from outils_r import lot
A = (0, (0, 0), 0); B = (5, (0, 2), 7); ORDER = 1
A2, B2 = collide(A, B, ORDER)
def terme(j):
    T = 133 + 8 * j
    a2 = adv(A2, T); assert a2[2] == A[2]
    q = rot(A[1], 2); c = (a2[1][0] - q[0], a2[1][1] - q[1])
    assert R(adv(B2, T), c) == B
    return T, c, build(A, B, c, ORDER)
def P_attendu(j): return 3 * (133 + 8 * j) - (36 if j % 2 == 0 else 18)
if __name__ == '__main__':
    j0, j1 = int(sys.argv[1]), int(sys.argv[2]); st = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    js = list(range(j0, j1 + 1, st)); sits = [terme(j)[2] for j in js]
    out = lot(sits, max(P_attendu(j) for j in js) + 10)
    ok = 0
    for j, l in zip(js, out):
        f = l.split('|'); good = f[3] == 'CYCLE' and int(f[5]) == P_attendu(j); ok += good
        if not good: print('ÉCART', j, l[:100])
    print('termes', j0, '..', j1, 'pas', st, ':', ok, '/', len(js), 'CYCLE avec P = 3T − 36 (j pair) / 3T − 18 (j impair)')
    print('ex. j =', js[-1], 'T =', terme(js[-1])[0], 'c =', terme(js[-1])[1], sits[-1])

"""S2 R-500 — 2e moteur (hx.py) : retour exact de l'état complet au temps P pour quelques termes j (et pas avant, aux diviseurs P/3)."""
import sys
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from famille import terme, P_attendu
from fa_lib import parts_of
from hx import step
for j in [int(x) for x in sys.argv[1:]]:
    T, c, s = terme(j); P = P_attendu(j)
    a, cs = parts_of(s); A0 = [list(t) for t in a]; G0 = {tuple(t): 1 for t in cs}
    A = [list(t) for t in A0]; G = dict(G0); first = None
    for t in range(1, P + 1):
        step(A, G)
        if A == A0 and G == G0: first = t; break
    print('j', j, 'P attendu', P, 'premier retour exact (hx.py)', first, 'OK' if first == P else 'ÉCART')

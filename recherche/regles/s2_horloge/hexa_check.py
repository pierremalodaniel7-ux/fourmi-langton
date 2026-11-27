"""S2 R-512 — 2e moteur : premier retour exact (hx.py) de chaque hexagramme propre (hexagramme_propres.json) = période fourmi_r ?
Usage : python3 s2_horloge/hexa_check.py"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
H = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 's2_horloge/hexagramme_propres.json')); ok = 0
for h in H:
    a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; A0 = [tuple(q) for q in A]; G0 = dict(G)
    for t in range(1, h['P'] + 1):
        step(A, G)
        if [tuple(q) for q in A] == A0 and G == G0: break
    ok += (t == h["P"] and t > 100 and [tuple(q) for q in A] == A0 and G == G0)
print('hx.py premier retour = période fourmi_r :', ok, '/', len(H))

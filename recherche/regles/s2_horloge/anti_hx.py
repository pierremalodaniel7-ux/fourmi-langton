"""S2 R-506 — 2e moteur (hx.py) : premier retour exact de la machine à 2 pixels opposés. Usage : anti_hx.py fichier n"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
w = json.load(open(sys.argv[1]))[int(sys.argv[2])]
a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
s0 = (tuple(map(tuple, A)), frozenset(G))
for t in range(1, 20001):
    step(A, G)
    if (tuple(map(tuple, A)), frozenset(G)) == s0: print('premier retour exact :', t, 'fourmis', len(A), 'cases', len(G)); break
else: print('pas de retour en 20000')
print(w['sit'])

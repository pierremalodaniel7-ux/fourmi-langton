"""T2 — contrôle d'une horloge + bascule de phase (t2_tb_horloge*.json) : 2e moteur (hx.py, premier retour exact), horloge exacte
(fourmis 2.. = horloge seule, sauf pendant les passages), phase de l'objet au début de chaque tour (objet seul : orbite de période p0).
Usage : python3 s2_horloge/t2_tb_check.py fichier.json rang"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import numpy as np
from hx import step
from fa_lib import parts_of
from deux_horloges import traj
from exp_osc import hd
H = json.load(open(sys.argv[1])); h = H[int(sys.argv[2])]; P0, P = h['P0'], h['P']
clocks = [w for w in json.load(open('s2_horloge/tri_cycles_rB5.json')) if w['P'] <= 1200]
if 'exact' in sys.argv[1]:
    one = {}
    for w in clocks: one.setdefault(w['P'], w)
    clocks = list(one.values())
w = clocks[h['clock']]
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; A0 = [tuple(q) for q in A]; G0 = dict(G)
for t in range(1, 2 * P + 1):
    step(A, G)
    if [tuple(q) for q in A] == A0 and G == G0: break
print('hx.py : premier retour exact', t, '(fourmi_r :', P, ')')
X = traj(h['sit'], P); XC = traj(w['sit'], h['t'] + P)[h['t']:]
d = (X[:, 2:] != XC).any(-1).any(-1)
print('horloge : pas où une fourmi diffère de l\'horloge seule :', int(d.sum()), '/', P)
# phase de l'objet : orbite de l'objet seul à partir de l'état initial (fourmis 0, 1 + ses cases)
o0 = (a[0][0], a[0][1])
def obj(A, G): return (tuple(map(tuple, A[:2])), frozenset(q for q in G if hd(q[0] - o0[0], q[1] - o0[1]) <= 5))
A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; st0 = obj(A, G)
B = [list(x) for x in st0[0]]; GB = {q: 1 for q in st0[1]}; orb = {}
for k in range(400): orb.setdefault(obj(B, GB), k); step(B, GB)
p0 = min(k for s, k in orb.items() if k > 0 and s == st0) if False else len(orb)
lap = []
for t in range(P + 1):
    if t % P0 == 0: lap.append((t, orb.get(obj(A, G))))
    step(A, G)
print('objet seul : période', len(orb), '; phase de l\'objet au début de chaque tour (None = hors orbite) :', lap)
print('sans les vaisseaux, la phase avancerait de', P0 % len(orb), 'par tour')

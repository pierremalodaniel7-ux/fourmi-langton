"""T2 — contrôle d'une machine t2_sym (3 copies d'objet, fourmis 0-5 ; horloge 6-11) : hx.py (premier retour), horloge exacte ?,
phase de chaque copie (objet seul) au début de chaque tour. Usage : python3 s2_horloge/t2_sym_check.py fichier.json rang"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from deux_horloges import traj
from exp_osc import hd
H = json.load(open(sys.argv[1])); h = H[int(sys.argv[2])]; P0, P = h['P0'], h['P']
one = {}
for w in json.load(open('s2_horloge/tri_cycles_rB5.json')):
    if w['P'] <= 1200: one.setdefault(w['P'], w)
w = list(one.values())[h['clock']] if 'clock' in h else None
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; A0 = [tuple(q) for q in A]; G0 = dict(G)
for t in range(1, 2 * P + 1):
    step(A, G)
    if [tuple(q) for q in A] == A0 and G == G0: break
print('hx.py premier retour', t, '(fourmi_r', P, ')')
X = traj(h['sit'], P); XC = traj(w['sit'], h['t'] + P)[h['t']:]
print('horloge : pas où une fourmi diffère de l\'horloge seule :', int((X[:, 6:] != XC).any(-1).any(-1).sum()), '/', P)
for k in range(3):
    o0 = (a[2 * k][0], a[2 * k][1])
    def obj(A, G): return (tuple(map(tuple, A[2 * k:2 * k + 2])), frozenset(q for q in G if hd(q[0] - o0[0], q[1] - o0[1]) <= 4))
    A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; st0 = obj(A, G)
    B = [list(x) for x in st0[0]]; GB = {q: 1 for q in st0[1]}; orb = {}
    for i in range(400): orb.setdefault((tuple(map(tuple, B)), frozenset(GB)), i); step(B, GB)
    lap = []
    for t in range(P + 1):
        if t % P0 == 0: lap.append(orb.get(obj(A, G)))
        step(A, G)
    print('copie', k, ': période seule', len(orb), '; phase au début des tours', lap, '; sans vaisseaux : +', P0 % len(orb), 'par tour')

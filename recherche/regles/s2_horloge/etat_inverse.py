"""S2 R-508b — la bascule R-341 frappée dans le « mauvais » état : machine R-502 n° 0 dont le pixel est posé ALLUMÉ (R') au départ au lieu de M.
On essaie toutes les phases de R' (R' seul joué φ pas, φ < 400) ; critère : issue fourmi_r de toute la machine (8 fourmis).
Usage : python3 s2_horloge/etat_inverse.py"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
import anti_pixel as ap
W = ap.W; P = W['P']
a, c = parts_of(W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
A0 = [tuple(q) for q in A]; M = ap.local(A, G, (0, 1))
st = []; snaps = []
O_M = ap.orbit(*M)
for t in range(P):
    st.append(ap.norm(*ap.local(A, G, (0, 1))) in O_M); snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
t_on = max(range(P), key=lambda t: (not st[t]) and all(not st[(t + d) % P] for d in range(-150, 150)))
Rp = ap.local([list(q) for q in snaps[t_on][0]], snaps[t_on][1], (0, 1))
clockA = A0[2:]; clockC = [q for q in c if tuple(q) not in set(M[1])]
lines = []; B = [list(q) for q in Rp[0]]; GB = {q: 1 for q in Rp[1]}
for ph in range(400):
    lines.append(fmt([tuple(q) for q in B] + clockA, list(GB) + [tuple(q) for q in clockC])); step(B, GB)
out = lot(lines, 6 * P + 10)
I = collections.Counter(l.split('|')[3] + ('' if l.split('|')[3] != 'CYCLE' else ' P=' + l.split('|')[5]) for l in out)
print('t_on', t_on, 'issues :', I)
json.dump([{'phase': i, 'sit': s, 'issue': l.split('|')[3], 't': l.split('|')[5]} for i, (s, l) in enumerate(zip(lines, out))], open('s2_horloge/etat_inverse.json', 'w'))

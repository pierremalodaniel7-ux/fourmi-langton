"""S2 R-507 — vérification du compteur 2 bits : (1) fourmi_r CYCLE, (2) hx.py premier retour exact, (3) lectures sur 3 périodes
(simulation hx indépendante du calcul de marge). Usage : compteur_check.py s2_horloge/compteur5.json n"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from outils_r import lot
import anti_pixel as ap
from compteur5 import OM, OR
w = json.load(open(sys.argv[1]))[int(sys.argv[2])]; P = w['P2']
l = lot([w['sit']], 3 * P + 10)[0].split('|'); print('fourmi_r :', l[3], l[4], l[5])
a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; n1 = int(w['bit1'].split()[1].split(',')[0])
s0 = (tuple(map(tuple, A)), frozenset(G)); ret = None
L = w['lectures']; tick = L[1] - L[0]; reads = {L[0] + (n * w['P1']) // (2 * w['clignotements_par_periode']) for n in range(3 * len(L))}
seq = []
for t in range(1, 3 * P + 1):
    if t - 1 in reads:
        b0 = ap.norm(*ap.local(A, G, (0, 1))); b1 = ap.norm(*ap.local(A, G, (n1, n1 + 1)))
        f = lambda x: '0' if x in OM else ('1' if x in OR else '?')
        seq.append(f(b1) + f(b0))
    step(A, G)
    if ret is None and (tuple(map(tuple, A)), frozenset(G)) == s0: ret = t
print('hx.py premier retour exact :', ret, ' fourmis', len(A))
print('lectures (bit1 bit0) toutes les', tick, 'pas :', ' '.join(seq))

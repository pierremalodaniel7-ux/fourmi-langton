"""S2 R-502 — 2e moteur : premier retour exact de la machine pixel (hx.py) + chronologie ON/OFF. Usage : pixel_hx.py fichier.json index"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from pixel_check import timeline
W = json.load(open(sys.argv[1])); w = W[int(sys.argv[2])]; Bs = json.load(open('data/bascules_exactes.json'))
a, c = parts_of(w['sit']); A0 = [list(t) for t in a]; G0 = {tuple(t): 1 for t in c}; A = [list(t) for t in A0]; G = dict(G0)
first = None
for t in range(1, w['P'] + 1):
    step(A, G)
    if A == A0 and G == G0: first = t; break
print('fourmi_r : CYCLE', w['P'], '| hx.py premier retour exact :', first, 'OK' if first == w['P'] else 'ÉCART')
st, ch = timeline(w, Bs)
print(dict(collections.Counter(st)))
print('chronologie (t, état) :', ch)

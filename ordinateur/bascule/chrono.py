#!/usr/bin/env python3
"""chrono.py honnetes.json i : rejoue la bascule i avec le 2e moteur (Python) ; tous les 200 pas, dit si la pièce
(fourmis 2.. et cases de sa zone) est EXACTEMENT dans un état de l'orbite S0 ou de l'orbite S1 (en place)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
os.environ['CY']='cycles2.json'
import recherche_lib as RL
from bascule import situ_piece
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.environ.get('S1F','cyclesS1.json'))))
H=json.load(open(sys.argv[1])); h=H[int(sys.argv[2])]
def etats(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return {(tuple(a),frozenset(c for c in no if c in vis)) for a,no in L}, vis
ic,s=h['hit']['S0'][:2]; A0,C0,p0=RL.piece0(ic,s)
O0,V0=etats(situ_piece(A0,C0),p0); e=S1L[h['hit']['S1']]; O1,V1=etats(e['situation'],e['periode'])
turn,ants,noir=charge(h['situation']); n=len(ants); prev=None; log=[]
for t in range(h['T']+1):
    if t%200==0:
        P=tuple(tuple(a) for a in ants[2:])
        st='S0' if (P,frozenset(c for c in noir if c in V0)) in O0 else ('S1' if (P,frozenset(c for c in noir if c in V1)) in O1 else '…')
        if st!=prev: log.append((t,st,tuple(ants[0]),tuple(ants[1]))); prev=st
    pas(turn,ants,noir,range(n))
for x in log: print(x)
print('fin',h['T'],[tuple(a) for a in ants])

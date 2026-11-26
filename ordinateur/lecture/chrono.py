#!/usr/bin/env python3
"""chrono.py chaine.json k honnetes.json i [EXTRA] : chronologie des états de la pièce (moteur2, toutes les 100 pas) pour
le préfixe k de la chaîne, prolongée de EXTRA pas."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1])); h=H[int(sys.argv[2])]; hb=json.load(open(sys.argv[3]))[int(sys.argv[4])]
EX=int(sys.argv[5]) if len(sys.argv)>5 else 40000
b=Bascule({'hit':hb['hit'],'situation':h['situation'],'T':h['T']})
turn,ants,noir=charge(h['situation']); prev=None; log=[]
for t in range(h['T']+EX+1):
    if t%100==0:
        st=b.etat([tuple(a) for a in ants],noir)
        if st!=prev: log.append((t,st)); prev=st
    pas(turn,ants,noir,range(len(ants)))
print(log)

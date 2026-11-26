#!/usr/bin/env python3
"""paire2.py chaine.json honnetes.json i : pourquoi la 2e paire ON/OFF n'efface pas sa ligne ? (a) après la 1re paire, la pièce
est-elle à la MÊME phase que la pièce seule (non perturbée) ? (b) témoin : la 2e paire SEULE (germes 3 et 4, pièce S0 neuve,
sans la 1re paire) : RETOUR exact ? cases restantes sur la ligne ? (c) chaîne complète : cases restantes. src/fourmi + moteur2."""
import sys, json
from lib import *
H=json.load(open(sys.argv[1])); hb=json.load(open(sys.argv[2]))[int(sys.argv[3])]; h=H[-1]; m=h['impulsions']
b=Bascule({'hit':hb['hit'],'situation':h['situation'],'T':h['T']})
r,A,C=parse(h['situation']); npc=b.npc; P=A[m:]; probes=A[:m]
germs=[C[11*k:11*k+11] for k in range(m)]   # ordre des cases : germe 1, pièce, germe 2, germe 3… (chaine.py ajoute à la fin)
nP=len(C)-11*m; G1=C[:11]; Cp=C[11:11+nP]; Gs=[G1]+[C[11+nP+11*k:11+nP+11*k+11] for k in range(m-1)]
# (a) phase de la pièce après la 1re paire
turn,an,no=charge(h['situation']); turn2,a2,n2=charge(situ(P,Cp)); diff=[]
for t in range(30001):
    if t in (16000,20000,25000,30000):
        same=[tuple(x) for x in an[-npc:]]==[tuple(x) for x in a2]
        diff.append((t,same))
    pas(turn,an,no,range(len(an))); pas(turn2,a2,n2,range(npc))
print('(a) pièce de la chaîne = pièce seule (même phase) aux pas :',diff)
# (b) 2e paire seule : germes 3 et 4 (fourmis 1 et 0) + pièce
sitb=situ([probes[0],probes[1]]+P,Gs[2]+Gs[3]+Cp)
(o,an,ce),=lot([sitb],h['T']+20000,'p2','-retour'); print('(b) 2e paire seule :',o.split('|')[3],o.split('|')[5],o.split('|')[6][:60])
(o,an,ce),=lot([sitb],h['T']+20000,'p2'); print('    sans -retour : pièce',b.etat(an,ce),'; sorties',destins(o)[:2])
def ligne(ce,src):
    return sum(1 for x,y in ce if abs((x+y)-(src[0]+src[1]))<=12 and 15<x<src[0]-15)
print('    cases sur la ligne (entre la pièce et la source 3, hors 15 cases aux bouts) :',ligne(ce,probes[1][:2]))
(o,an,ce),=lot([h['situation']],h['T']+20000,'p2'); print('(c) chaîne complète : pièce',b.etat(an,ce),'; cases sur la même portion :',ligne(ce,probes[1][:2]))

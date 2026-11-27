#!/usr/bin/env python3
"""ecran2.py : écran de 2 pixels = 2 bascules T (chaine_2.json et chaine_1.json, 3 impulsions chacune : ON, OFF, ON).
Pixel B est translaté de (BX,BY) et retardé de Δ = 104·m pas : son état de départ est son état « Δ pas avant »,
calculé exactement par réversibilité (gomme, Δ pas en ordre inversé, gomme). Une seule situation ; chronologie des 2 pixels (moteur Python) ; vérif finale src/fourmi.
Écrit ../../data/bascule/ecran2.json (situation, T, chronologies) et des images PGM/PNG."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
from bascule import G, E, situ_piece
os.environ['CY']='cycles2.json'
import recherche_lib as RL
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json')))
Hh=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'honnetes.json')))
BX,BY,m=0,4000,int(sys.argv[1]) if len(sys.argv)>1 else 30
def etats(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return L, vis
def pixel(ich,dx,dy,m):
    ch=json.load(open(f'../../data/bascule/chaine_{ich}.json'))[-1]; h=Hh[ich]
    ic,s=h['hit']['S0'][:2]; A0,C0,p0=RL.piece0(ic,s); L0,V0=etats(situ_piece(A0,C0),p0)
    e=S1L[h['hit']['S1']]; L1,V1=etats(e['situation'],e['periode'])
    r,a,c=ch['situation'].split('|'); an=[tuple(map(int,x.split(','))) for x in a.split(';')]
    npc=len(A0); sondes=an[:-npc]; cells=[tuple(map(int,x.split(',')[:2])) for x in c.split(';') if x]
    piece_cells=set(C0); germ_cells=[x for x in cells if x not in piece_cells]
    k=(-104*m)%p0; Ak,Ck=L0[k]                                  # pièce recalée
    sondes=[(x+2*m,y-2*m,d) for x,y,d in sondes]; germ_cells=[(x+2*m,y-2*m) for x,y in germ_cells]
    tr=lambda p:(p[0]+dx,p[1]+dy)
    ants=[(x+dx,y+dy,d) for x,y,d in sondes]+[(x+dx,y+dy,d) for x,y,d in Ak]
    cs=[tr(p) for p in germ_cells]+[tr(p) for p in Ck]
    O0={(tuple((x+dx,y+dy,d) for x,y,d in A),frozenset(tr(p) for p in N if p in V0)) for A,N in L0}
    O1={(tuple((x+dx,y+dy,d) for x,y,d in A),frozenset(tr(p) for p in N if p in V1)) for A,N in L1}
    V0t={tr(p) for p in V0}; V1t={tr(p) for p in V1}
    return ants,cs,npc,(O0,V0t,O1,V1t),ch['T']+104*m
antsA,csA,nA,KA,TA=pixel(2,0,0,0); antsB,csB,nB,KB,TB=pixel(1,BX,BY,0)
# retard exact du pixel B par réversibilité : état au temps −Δ = R ∘ (Δ pas, ordre inversé) ∘ R (état au temps 0)
from moteur2 import gomme
DELTA=104*m
turn,anb,nob=charge('RL|'+';'.join(f'{x},{y},{d}' for x,y,d in antsB)+'|'+';'.join(f'{x},{y}' for x,y in csB))
ref=([tuple(a) for a in anb],set(nob))
gomme(anb)
for _ in range(DELTA): pas(turn,anb,nob,range(len(anb)-1,-1,-1))
gomme(anb)
antsB=[tuple(a) for a in anb]; csB=sorted(nob)
t2,an2,no2=charge('RL|'+';'.join(f'{x},{y},{d}' for x,y,d in antsB)+'|'+';'.join(f'{x},{y}' for x,y in csB))
for _ in range(DELTA): pas(t2,an2,no2,range(len(an2)))
assert ([tuple(a) for a in an2],set(no2))==ref, 'retard non exact'
print('pixel B retardé de',DELTA,'pas : état à −Δ calculé (',len(csB),'cases), retour exact vérifié')
TB=TB+DELTA
# ordre : sondes A, sondes B, pièce A, pièce B (les deux systèmes sont loin : l'ordre entre eux n'a pas d'effet)
sA,pA=antsA[:-nA],antsA[-nA:]; sB,pB=antsB[:-nB],antsB[-nB:]
ants=sA+sB+pA+pB; T=max(TA,TB)
sit='RL|'+';'.join(f'{x},{y},{d}' for x,y,d in ants)+'|'+';'.join(f'{x},{y}' for x,y in csA+csB)
iA=list(range(len(sA)+len(sB),len(sA)+len(sB)+nA)); iB=list(range(len(sA)+len(sB)+nA,len(ants)))
def st(K,an,no,idx):
    O0,V0,O1,V1=K; P=tuple(tuple(an[i]) for i in idx)
    if (P,frozenset(c for c in no if c in V0)) in O0: return 'OFF'
    if (P,frozenset(c for c in no if c in V1)) in O1: return 'ON'
    return '…'
turn,an,no=charge(sit); log=[]; prev=None; snaps={}
for t in range(T+1):
    if t%100==0:
        e=(st(KA,an,no,iA),st(KB,an,no,iB))
        if e!=prev: log.append((t,)+e); prev=e
    if t<T: pas(turn,an,no,range(len(an)))
print('chronologie (pas, pixel A, pixel B) :'); [print(x) for x in log]
o=subprocess.run([E,'-T',str(T),sit],capture_output=True,text=True).stdout.split('|')
print('src/fourmi fin :',o[6][-160:].strip()); print('Python fin   :',' '.join(f'{a[0]},{a[1]}' for a in an))
json.dump({'situation':sit,'T':T,'chronologie':log,'pixels':{'A':[0,0],'B':[BX,BY]},'retard_B':m},open('../../data/bascule/ecran2.json','w'))

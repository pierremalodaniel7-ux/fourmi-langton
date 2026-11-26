#!/usr/bin/env python3
"""multi_paires.py NOM : paires ON/OFF sur des lignes DIFFÉRENTES (4 directions, voies variées) pour la bascule 185 (S0 = bascules4).
1) tirs simples sur S0 (4 rotations, voies à ≤ 8, 4 avancées, toutes phases) : « écriture » = la pièce change, ses fourmis restent,
   la sonde part ; 2) pour chaque écriture, paire = même germe + rattrapeur en (c0+δ+e, −c0−δ) derrière (δ ∈ [−6,6], e ∈ {−3,−1,1,3}) :
   paire propre = RETOUR exact (fourmi 0 en R(départ de 1) ET 1 en R(départ de 0)) + pièce revenue EXACTEMENT au pas 0 (cases à ≤ 3).
Tout dans le repère tourné ; résultats ramenés au repère de base. → data/lecture/multi_NOM.json"""
import sys, json, collections
from lib import *
L4=json.load(open('bascules4.json')); e=[x for x in L4 if x['nom']==sys.argv[1]][0]
_,A0,C0=parse(e['S0']); p0=e['p0']; D=50; c0=123
def rotA(A,r):
    for _ in range(r%4): A=[(-y,x,(d+1)%4) for x,y,d in A]
    return A
def rotC(C,r):
    for _ in range(r%4): C=[(-y,x) for x,y in C]
    return C
def orb(A,C,p):
    turn,an,no=charge(situ(A,C)); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return L,vis
writes=[]
for r in range(4):
    Ar,Cr=rotA(A0,r),rotC(C0,r); L,vis=orb(Ar,Cr,p0); zone={(x+dx,y+dy) for x,y in vis for dx in range(-2,3) for dy in range(-2,3)}
    Z3={(x+dx,y+dy) for x,y in vis for dx in range(-3,4) for dy in range(-3,4)}
    sits=[];meta=[]
    for tx in range(-2*D-24,-2*D+25):
        for ty in range(2*D-24,2*D+25):
            if not (4*D<=-tx+ty<4*D+4) or not any(abs((x+y)-(-tx-ty))<=8 for x,y in zone): continue
            for s in range(p0):
                An,N=L[s]; sits.append(situ([(-tx,-ty,2)]+An,[(x-tx,y-ty) for x,y in G]+list(N))); meta.append((tx,ty,s))
    K0={(tuple(a),frozenset(c for c in n if c in Z3)) for a,n in L}
    for (tx,ty,s),(o,an,ce) in zip(meta,lot(sits,15000,'mp')):
        P=tuple(an[1:]); a=an[0]
        if (P,frozenset(c for c in ce if c in Z3)) in K0: continue
        if any(x[:2] not in Z3 for x in P) or max(abs(a[0]),abs(a[1]))<40: continue
        writes.append((r,tx,ty,s))
print(len(writes),'écritures (4 rotations)',flush=True)
# 2) paires
res=[]
for r in range(4):
    Ar,Cr=rotA(A0,r),rotC(C0,r); L,vis=orb(Ar,Cr,p0); Z3={(x+dx,y+dy) for x,y in vis for dx in range(-3,4) for dy in range(-3,4)}
    sits=[];meta=[]
    for (rr,tx,ty,s) in writes:
        if rr!=r: continue
        An,N=L[s]; g1=(-tx,-ty)
        for dl in range(-3,4):
            for ee in (-1,1):
                c=c0+dl; g2=(g1[0]+c+ee,g1[1]-c)
                sits.append(situ([(g2[0],g2[1],2),(g1[0],g1[1],2)]+An,[(x+g1[0],y+g1[1]) for x,y in G]+[(x+g2[0],y+g2[1]) for x,y in G]+list(N)))
                meta.append((tx,ty,s,dl,ee,g1,g2))
    for m,(o,an,ce) in zip(meta,lot(sits,45000,'mq','-retour')):
        f=o.split('|')
        if f[3]!='RETOUR': continue
        tx,ty,s,dl,ee,g1,g2=m
        ok0=tuple(an[0])==(g1[0],g1[1]-1,0); ok1=tuple(an[1])==(g2[0],g2[1]-1,0)
        An,N=L[s]; exact=tuple(map(tuple,an[2:]))==tuple(An) and {c for c in ce if c in Z3}=={c for c in N if c in Z3}
        if ok0 and ok1 and exact: res.append({'r':r,'tx':tx,'ty':ty,'phase':s,'dl':dl,'e':ee,'t':int(f[5]),'diff':int(f[6].split('diff=')[1].split()[0])})
c=collections.Counter((x['r'],x['tx']+x['ty']) for x in res)
print(len(res),'paires propres ; (rotation, voie x+y du germe) :',sorted(c.items()))
json.dump({'writes':writes,'paires':res},open(f'../../data/lecture/multi_{sys.argv[1]}.json','w'))

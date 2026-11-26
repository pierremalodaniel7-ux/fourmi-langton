#!/usr/bin/env python3
"""verif.py FAM NOM : vérifie les candidats de lecture d'une pièce (data/rlem/FAM_*.jsonl) avec un critère STRICT :
après le tir, toutes les cases à distance ≤ 4 des cases visitées par l'orbite doivent être celles d'une phase de l'état
(S0 ou S1) — pas seulement l'anneau ; contrôle par moteur2.py (2e moteur). Rejoue aussi la lecture 2 fois de suite."""
import sys, json, glob
sys.path.insert(0, '../lecture'); sys.argv+=[]
from lib import charge, pas, situ, parse, lot, destins, voie, G, py_final
exec(open('rlem.py').read().split("for idx,pc in enumerate(P):")[0].split("FAM,K,M=")[0])
D=50; ZD=int(os.environ.get("ZD",2))
FAM,NOM=sys.argv[1],sys.argv[2]
R=[json.loads(l) for f in sorted(glob.glob(f'../../data/rlem/{FAM}_[0-9]*.jsonl')) for l in open(f)]
r0=[r for r in R if r['nom']==NOM][0]; pc=[p for p in json.load(open(f'../../data/rlem/{FAM}_pieces.json')) if p['nom']==NOM][0]
def rotA(A,r):
    for _ in range(r%4): A=[(-y,x,(d+1)%4) for x,y,d in A]
    return A
def rotC(C,r):
    for _ in range(r%4): C=[(-y,x) for x,y in C]
    return C
def etats_zone(A,C,p,r):
    Ar,Cr=rotA(A,r),rotC(C,r); turn,an,no=charge(situ(Ar,Cr)); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    Z={(x+dx,y+dy) for x,y in vis for dx in range(-ZD,ZD+1) for dy in range(-ZD,ZD+1)}
    return {(tuple(a),frozenset(c for c in n if c in Z)) for a,n in L},Z,L
def tir(L,s,key,shots=1):
    tx,ty=map(int,key.split(',')); An,N=L[s]; cells=[(x-tx,y-ty) for x,y in G]+list(N); A=[(-tx,-ty,2)]+list(An)
    for k in range(1,shots):            # lectures répétées : germes supplémentaires plus loin sur la même voie
        gx,gy=-tx+60*k,-ty-60*k; A=[(gx,gy,2)]+A; cells+=[(x+gx,y+gy) for x,y in G]
    return situ(A,cells)
def classe(an,ce,npc,E0,Z0,E1,Z1,nprobe):
    P=tuple(tuple(a) for a in an[nprobe:nprobe+npc])
    if (P,frozenset(c for c in ce if c in Z0)) in E0: return 'S0'
    if (P,frozenset(c for c in ce if c in Z1)) in E1: return 'S1'
    return '?'
_,A0,C0=parse(pc['situation']); p0=pc['periode']; npc=len(A0)
for s1 in r0['S1']:
    if not s1['lectures'] and not s1['n_retours']: continue
    _,A1,C1=parse(s1['situation']); p1=s1['periode']
    print('S1',s1['situation'][:60],'p',p1)
    for x in s1['lectures']:
        r=int(x['cle'].split(':')[0]); key=x['cle'].split(':')[1]
        E0,Z0,L0=etats_zone(A0,C0,p0,r); E1,Z1,L1=etats_zone(A1,C1,p1,r)
        for nom,L,s in (('S0',L0,x['S0'][0][0]),('S1',L1,x['S1'][0][0])):
            for n in (1,2):
                sit=tir(L,s,key,n); T=15000+n*8000
                (o,an,ce),=lot([sit],T,'vf'); st=classe(an,ce,npc,E0,Z0,E1,Z1,n)
                a2,n2=py_final(sit,int(o.split('|')[5]))
                print(f'   lecture {x["cle"]} : {nom} phase {s}, {n} tir(s) → {st} ; sorties {destins(o)[:n]} ; moteur2 {"=" if a2==an and n2==ce else "≠"}')
    for rr in s1['retours'][:1]:
        r,key,s=rr[0],rr[1],rr[2]; E0,Z0,L0=etats_zone(A0,C0,p0,r); E1,Z1,L1=etats_zone(A1,C1,p1,r)
        sit=tir(L1,s,key); (o,an,ce),=lot([sit],15000,'vf'); print(f'   effacement {r}:{key} phase {s} : S1 → {classe(an,ce,npc,E0,Z0,E1,Z1,1)} (strict) sortie {destins(o)[0]}')
    w=s1['ecriture']; E0,Z0,L0=etats_zone(A0,C0,p0,w[0]); E1,Z1,L1=etats_zone(A1,C1,p1,w[0])
    sit=tir(L0,w[2],w[1]); (o,an,ce),=lot([sit],15000,'vf'); print(f'   écriture {w[0]}:{w[1]} phase {w[2]} : S0 → {classe(an,ce,npc,E0,Z0,E1,Z1,1)} (strict) sortie {destins(o)[0]}')

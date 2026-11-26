#!/usr/bin/env python3
"""funcseq.py FAM NOM IS1 SEQ : test FONCTIONNEL d'un candidat (fils idéalisés). Opérations : a = écriture, c = effacement,
b = lecture (relevées par rlem.py). Chaque opération : autoroute neuve (germe R-20) arrivant quand la pièce est à la phase voulue
(on attend), simulation 15 000 pas, puis on ne garde que les fourmis de la pièce et les cases à distance ≤ 3 des cases visitées
(la sonde et sa trace lointaine sont « parties dans le fil »). État reconnu : S0 / S1 (orbite + cases à distance ≤ ZD, ZD=1).
Affiche la suite (état, sortie). src/fourmi (tirs) ; moteur2.py (recontrôle du 1er tir)."""
import sys, json, glob, os
sys.path.insert(0, '../lecture')
from lib import charge, pas, situ, parse, lot, destins, voie, G, py_final
ZD=int(os.environ.get('ZD',1)); T=15000
_CACHE={}
def run(FAM,NOM,IS1,SEQ):
    if FAM not in _CACHE: _CACHE[FAM]=[json.loads(l) for f in sorted(glob.glob(f'../../data/rlem/{FAM}_[0-9]*.jsonl')) for l in open(f)]
    R=_CACHE[FAM]
    r0=[r for r in R if r['nom']==NOM][0]; pc=[p for p in json.load(open(f'../../data/rlem/{FAM}_pieces.json')) if p['nom']==NOM][0]
    s1=r0['S1'][IS1]
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
    _,A0,C0=parse(pc['situation']); p0=pc['periode']; _,A1,C1=parse(s1['situation']); p1=s1['periode']; npc=len(A0)
    L0,V0=orb(A0,C0,p0); L1,V1=orb(A1,C1,p1)
    Z=lambda V,d:{(x+dx,y+dy) for x,y in V for dx in range(-d,d+1) for dy in range(-d,d+1)}
    ZZ=Z(V0|V1,3)
    def etat(A,C):
        Cs=set(C)
        for nom,L,V in (('S0',L0,V0),('S1',L1,V1)):
            z=Z(V,ZD)
            for s,(a,n) in enumerate(L):
                if tuple(map(tuple,A))==tuple(a) and {c for c in Cs if c in z}=={c for c in n if c in z}: return nom,s
        return '?',None
    ops={'a':s1['ecriture'][:3],'c':s1['retours'][0][:3] if s1['retours'] else None}
    if s1['lectures']:
        x=s1['lectures'][0]; ops['b']=(int(x['cle'].split(':')[0]),x['cle'].split(':')[1],{'S0':x['S0'][0][0],'S1':x['S1'][0][0]})
    A,C=list(A0),list(C0); out=[]
    for k,op in enumerate(SEQ):
        st,ph=etat(A,C)
        if st=='?': out.append((op,'pièce abîmée')); break
        r,key,phw=ops[op] if op!='b' else (ops['b'][0],ops['b'][1],ops['b'][2][st])
        # attendre la phase voulue (le circuit choisit l'instant d'arrivée)
        L=L0 if st=='S0' else L1; p=len(L); w=(phw-ph)%p
        turn,an,no=charge(situ(A,C))
        for _ in range(w): pas(turn,an,no,range(npc))
        Ar,Cr=rotA([tuple(a) for a in an],r),rotC(list(no),r); tx,ty=map(int,key.split(','))
        sit=situ([(-tx,-ty,2)]+Ar,[(x-tx,y-ty) for x,y in G]+Cr)
        (o,an2,ce),=lot([sit],T,'fs'); d=destins(o)[0]
        if k==0:
            a2,n2=py_final(sit,int(o.split('|')[5])); ok2=(a2==an2 and n2==ce)
        else: pass
        P=rotA([tuple(a) for a in an2[1:]],4-r); Cb=[c for c in rotC(list(ce),4-r) if c in ZZ]
        if any(a[:2] not in ZZ for a in P): out.append((op,'fourmi de la pièce partie',P,o.split('|')[3])); break
        A,C=P,Cb; st2,_=etat(A,C); out.append((op,st,'→',st2,d))
    return out,ok2

if __name__=='__main__':
    out,ok2=run(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])
    print(sys.argv[2],'S1 n°',sys.argv[3],':',' | '.join(' '.join(map(str,o)) for o in out)); print('   (moteur2 sur le 1er tir :','identique)' if ok2 else 'DIFFÉRENT)')

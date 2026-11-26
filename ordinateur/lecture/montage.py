#!/usr/bin/env python3
"""montage.py NOM ORDRE : écritures/effacements successifs de la bascule NOM avec des PAIRES sur des lignes DIFFÉRENTES
(paires propres de multi_paires.py). ORDRE = indices des paires (ex. 4,0,5 ; une paire peut revenir plus tard).
La paire k est reculée de a cases le long de sa ligne (son rattrapeur de c0 + a + δ) pour arriver après la fin de la paire k−1.
Recherche gloutonne de (a, δ) ; succès = RETOUR exact de la paire k (ses 2 sondes chacune en R(départ de l'autre)), pièce en S0,
et chronologie complète (moteur2) S0,S1,S0,…. Tout est simulé ENSEMBLE (src/fourmi). → data/lecture/montage_NOM.json"""
import sys, json, math
from lib import *
NOM=sys.argv[1]; ORDRE=[int(x) for x in sys.argv[2].split(',')]
L4=json.load(open('bascules4.json')); e=[x for x in L4 if x['nom']==NOM][0]; _,A0,C0=parse(e['S0']); p0=e['p0']
MP=json.load(open(f'../../data/lecture/multi_{NOM}.json'))['paires']; c0=123; MINW=int(os.environ.get('MINW',1000))
hb={'185':0,'186':1,'572':2}.get(NOM)
b=Bascule(json.load(open('../bascule/honnetes.json'))[hb]) if hb is not None else None
def rotP(x,y,d,r):
    for _ in range(r%4): x,y,d=-y,x,(d+1)%4
    return x,y,d
def orbL(A,C,p):
    turn,an,no=charge(situ(A,C)); L=[]
    for _ in range(p): L.append(([tuple(a) for a in an],sorted(no))); pas(turn,an,no,range(len(an)))
    return L
L0=orbL(A0,C0,p0)
def germes(P,a,dl):
    """germes (impulsion, rattrapeur) de la paire P reculée de a, en repère de base"""
    g1=(-P['tx']+a,-P['ty']-a); c=c0+P['dl']+a+dl; g2=(g1[0]+c+P['e'],g1[1]-c); r=(4-P['r'])%4
    q1=rotP(g1[0],g1[1],2,r); q2=rotP(g2[0],g2[1],2,r)
    cel=[rotP(x+g1[0],y+g1[1],0,r)[:2] for x,y in G]+[rotP(x+g2[0],y+g2[1],0,r)[:2] for x,y in G]
    return q1,q2,cel
P0=MP[ORDRE[0]]; An,N=L0[P0['phase']]          # la pièce part à la phase de la 1re paire (repère de base : même indice)
def construit(choix):
    ants=[];cells=[]
    for k,(a,dl) in list(enumerate(choix))[::-1]:
        q1,q2,cel=germes(MP[ORDRE[k]],a,dl); ants+=[q2,q1]
    for k,(a,dl) in enumerate(choix): cells+=germes(MP[ORDRE[k]],a,dl)[2]
    return situ(ants+An,cells+list(N))
def chrono(sit,T):
    turn,a2,no=charge(sit); prev=None; log=[]
    for t in range(T+1):
        if t%100==0:
            st=b.etat([tuple(x) for x in a2],no)
            if st!=prev: log.append((t,st)); prev=st
        if t<T: pas(turn,a2,no,range(len(a2)))
    return log
OUT=f'../../data/lecture/montage_{NOM}_{sys.argv[2].replace(",","-")}.json'
choix=[(0,0)]; tret=[MP[ORDRE[0]]['t']]
for k in range(1,len(ORDRE)):
    amin=max(0,math.ceil((tret[-1]+3000)/52)-101); sits=[];meta=[]
    for a in range(amin,amin+40):
        for dl in range(*map(int,os.environ.get("DL","-6,7,2").split(","))): sits.append(construit(choix+[(a,dl)])); meta.append((a,dl))
    T=int(2.3*52*(101+amin+40))+20000; cand=[]
    for (a,dl),(o,an,ce) in zip(meta,lot(sits,T,'mt','-retour -dumpbox -40,-40,40,40')):
        f=o.split('|')
        if f[3]!='RETOUR': continue
        q1,q2,_=germes(MP[ORDRE[k]],a,dl)
        R=lambda q:(q[0]-[0,1,0,-1][q[2]],q[1]-[-1,0,1,0][q[2]],(q[2]+2)%4)
        if tuple(an[0])==R(q1) and tuple(an[1])==R(q2) and b.etat(an,ce)=='S0': cand.append((int(f[5]),a,dl))
    cand.sort(); print('paire',k+1,'(n°',ORDRE[k],') : a ∈',[amin,amin+40],':',len(cand),'RETOUR exacts + S0',cand[:4],flush=True)
    ok=None
    for ts,a,dl in cand[:40]:
        log=chrono(construit(choix+[(a,dl)]),ts+1500)
        # écriture = la pièce quitte S0 au moins MINW pas (S1 de la ligne a, ou un autre état écrit), puis revient en S0
        seq=[]
        for (t,s_),(t2,_) in zip(log,log[1:]+[(ts+1500,None)]):
            v='S0' if s_=='S0' else 'X'
            if seq and seq[-1][0]==v: seq[-1][1]+=t2-t
            else: seq.append([v,t2-t])
        motif=[v for v,d in seq if d>=MINW or v=='S0']
        cm=[]
        for v in motif:
            if not cm or cm[-1]!=v: cm.append(v)
        if cm==(['S0','X']*(k+2))[:2*(k+1)+1]: ok=(a,dl,ts,log); break
    if not ok: print('   pas de chronologie correcte'); break
    choix.append(ok[:2]); tret.append(ok[2]); print('   retenue a',ok[0],'δ',ok[1],'RETOUR',ok[2],'chronologie',ok[3],flush=True)
    sit=construit(choix); (o,an,ce),=lot([sit],ok[2],'mt')
    a2,n2=py_final(sit,ok[2]); print('   moteur2 au pas',ok[2],':','identique' if a2==an and n2==ce else 'DIFFÉRENT')
    json.dump({'ordre':ORDRE[:k+1],'choix':choix,'t_retour':tret,'chronologie':ok[3],'situation':sit},open(OUT,'w'))

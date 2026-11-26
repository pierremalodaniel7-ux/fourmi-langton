#!/usr/bin/env python3
"""paires.py honnetes.json i NPAIRES : empile des PAIRES ON/OFF sur la ligne a (bascule honnête i). Paire 1 = la paire honnête.
Paire k : germe « impulsion » en p1 + (a+dp, −a), germe « rattrapeur » en p1 + (a+dp, −a) + (c+1, −c) avec c = a + c0 + δ
(c0 = écart de la paire honnête : le rattrapeur doit rattraper l'impulsion APRÈS la pièce, donc l'écart grandit avec la distance).
a ≥ a_min : l'impulsion k passe la dernière source après la fin (RETOUR + 6 000 pas) de la paire k−1.
Succès : RETOUR exact de la paire k (src/fourmi -retour : fourmi 1 en R(départ de la fourmi 0)) avec la pièce en S0 ;
chronologie complète (moteur2) S0,S1,S0,…,S0 ; on garde le candidat qui laisse le moins de cases près de la pièce.
→ data/lecture/paires_i.json (reprise)."""
import sys, json, collections, math
from lib import *
H=json.load(open(sys.argv[1])); i=int(sys.argv[2]); hb=H[i]; NP=int(sys.argv[3]); b=Bascule(hb)
DA,DP,DD=int(os.environ.get('DA',20)),int(os.environ.get('DP',10)),int(os.environ.get('DD',8))
r,A,C=parse(hb['situation']); Pa=A[2:]; Cp=C[11:-11]; G1,G2=C[:11],C[-11:]; p1,p2=A[1],A[0]
c0=p1[1]-p2[1]; e0=(p2[0]-p1[0])-c0                       # p2 = p1 + (c0+e0, −c0)
OUT=f'../../data/lecture/paires_{i}.json'
etat=json.load(open(OUT)) if os.path.exists(OUT) else {'paires':[[0,0,0]],'t_retour':[None]}
def germes(L):
    """L = [(a,dp,δ)] → [(impulsion, rattrapeur)] en positions absolues"""
    out=[]
    for a,dp,dl in L:
        q1=(p1[0]+a+dp,p1[1]-a); c=a+c0+dl if a else c0; q2=(q1[0]+c+e0,q1[1]-c); out.append((q1,q2))
    return out
def construit(L):
    ants=[]; cells=[]
    for q1,q2 in germes(L)[::-1]: ants+=[(q2[0],q2[1],2),(q1[0],q1[1],2)]
    for q1,q2 in germes(L): cells+=[(x+q1[0],y+q1[1]) for x,y in G]+[(x+q2[0],y+q2[1]) for x,y in G]
    return situ(ants+Pa,cells+Cp)
def chrono(sit,T):
    turn,a2,no=charge(sit); prev=None; log=[]
    for t in range(0,T+1):
        if t%100==0:
            st=b.etat([tuple(x) for x in a2],no)
            if st!=prev: log.append((t,st)); prev=st
        if t<T: pas(turn,a2,no,range(len(a2)))
    return log
if etat['t_retour'][0] is None:
    (o,an,ce),=lot([construit(etat['paires'])],60000,'pr','-retour'); etat['t_retour']=[int(o.split('|')[5])]
while len(etat['paires'])<NP:
    L=etat['paires']; gl=germes(L); s_last=max(q[1][0]-p1[0] for q in gl)      # recul (en x) de la source la plus lointaine
    amin=s_last+math.ceil((etat['t_retour'][-1]+6000)/52)-0
    sits=[];meta=[]
    for a in range(amin,amin+DA):
        for dp in range(-DP,DP+1):
            for dl in range(-DD,DD+1):
                sits.append(construit(L+[[a,dp,dl]])); meta.append((a,dp,dl))
    T=int(2.4*52*(amin+DA+2*c0))+30000
    print(f'paire {len(L)+1} : a ∈ [{amin},{amin+DA}), {len(sits)} essais, T = {T}',flush=True)
    R=lot(sits,T,'pr','-retour -dumpbox -30,-30,40,40'); cand=[]
    for (a,dp,dl),(o,an,ce) in zip(meta,R):
        f=o.split('|')
        if f[3]!='RETOUR' or 'fourmi 1 ' not in f[6] or int(f[5])<52*a: continue
        if b.etat(an,ce)!='S0': continue
        cand.append((sum(1 for x,y in ce if -30<=x<=40 and -30<=y<=40),a,dp,dl,int(f[5])))
    cand.sort(); print('   ',len(cand),'candidats (RETOUR après la pièce + S0) ; meilleurs',cand[:4],flush=True)
    ok=None
    for near,a,dp,dl,ts in cand[:25]:
        log=chrono(construit(L+[[a,dp,dl]]),ts+2000); seq=[s for t,s in log if s!='…']
        if seq==(['S0','S1']*(len(L)+2))[:2*(len(L)+1)+1]: ok=(a,dp,dl,ts,near,log); break
    if not ok: print('   aucune ne donne la bonne chronologie'); break
    a,dp,dl,ts,near,log=ok; L.append([a,dp,dl]); etat['t_retour'].append(ts); etat.update({'chrono':log,'situation':construit(L),'cases_pres_piece':near})
    json.dump(etat,open(OUT,'w')); print('   paire',len(L),'retenue',(a,dp,dl),'retour',ts,'cases près de la pièce',near,'chronologie',log,flush=True)

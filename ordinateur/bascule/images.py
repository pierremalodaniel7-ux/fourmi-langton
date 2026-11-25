#!/usr/bin/env python3
"""images.py : figures de la nuit du 25/11 (moteur2.py ; cases noires = noir, fourmis = rouge) → resultats/bascule/*.png"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from moteur2 import charge, pas, gomme
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../resultats/bascule')
def snaps(sit,times,order=None):
    turn,an,no=charge(sit); n=len(an); S={}; t=0
    for T in sorted(times):
        while t<T: pas(turn,an,no,order or range(n)); t+=1
        S[T]=([tuple(a) for a in an],set(no))
    return S
def dessine(ax,st,box,titre):
    import numpy as np
    an,no=st; x0,y0,x1,y1=box; W=x1-x0+1; H=y1-y0+1; sc=max(1,max(W,H)//700)
    im=np.ones(((H+sc-1)//sc,(W+sc-1)//sc))
    for x,y in no:
        if x0<=x<=x1 and y0<=y<=y1: im[(y-y0)//sc,(x-x0)//sc]=0
    ax.imshow(im,cmap='gray',vmin=0,vmax=1,extent=(x0-0.5,x1+0.5,y1+0.5,y0-0.5),interpolation='nearest')
    A=[a for a in an if x0<=a[0]<=x1 and y0<=a[1]<=y1]
    ax.scatter([a[0] for a in A],[a[1] for a in A],s=18,c='red',marker='o')
    ax.set_xlim(x0-0.5,x1+0.5); ax.set_ylim(y1+0.5,y0-0.5); ax.set_title(titre,fontsize=8); ax.set_xticks([]); ax.set_yticks([])
G="0,1;1,2;2,3;2,2;2,1;2,0;3,0;3,-1;2,-2;1,-2;-2,-1"
# 1. gomme
turn,an,no=charge("RL|0,0,B|"+G)
for _ in range(10400): pas(turn,an,no,[0])
st1=([tuple(a) for a in an],set(no)); gomme(an)
for _ in range(5200): pas(turn,an,no,[0])
st2=([tuple(a) for a in an],set(no))
for _ in range(5200): pas(turn,an,no,[0])
st3=([tuple(a) for a in an],set(no))
f,ax=plt.subplots(1,3,figsize=(11,4)); B=(-205,-10,10,205)
dessine(ax[0],st1,B,'germe R-20 + 10 400 pas (autoroute 104)'); dessine(ax[1],st2,B,'gomme : R appliquée, + 5 200 pas'); dessine(ax[2],st3,B,'+ 10 400 pas : germe seul (11 cases)')
plt.tight_layout(); plt.savefig(f'{OUT}/1_gomme.png',dpi=110); plt.close()
# 2. bascule 572 (chaîne à 3 impulsions)
ch=json.load(open('../../data/bascule/chaine_2.json'))[-1]
times=[0,6000,7000,15000,ch['T']]
S=snaps(ch['situation'],times)
f,ax=plt.subplots(1,4,figsize=(12,3.4)); Bz=(-6,-6,12,12)
for a,t,lab in zip(ax,[0,7000,15000,ch['T']],['S0 (OFF) au départ','S1 (ON) après la 1re autoroute','S0 (OFF) après la 2e','S1 (ON) après la 3e']):
    dessine(a,S[t],Bz,f'pas {t} : {lab}')
plt.tight_layout(); plt.savefig(f'{OUT}/2_bascule_zoom.png',dpi=120); plt.close()
c2=json.load(open('../../data/bascule/chaine_2.json'))[0]
tt=[0,6000,8000,12000,16000,c2['T']]; S2=snaps(c2['situation'],tt)
f,ax=plt.subplots(2,3,figsize=(12,8))
for a,t in zip(ax.flat,tt):
    nb=len(S2[t][1]); dessine(a,S2[t],(-150,-350,350,150),f'2 impulsions, pas {t} : {nb} cases noires')
plt.tight_layout(); plt.savefig(f'{OUT}/3_bascule_vue.png',dpi=100); plt.close()
# 3. écran 2 pixels
E2=json.load(open('../../data/bascule/ecran2.json'))
ts=[0,7000,12000,19000,30000,E2['T']]
S=snaps(E2['situation'],ts)
f,ax=plt.subplots(2,len(ts),figsize=(2.2*len(ts),4.8))
etat={}
for t in ts:
    e=[x for x in E2['chronologie'] if x[0]<=t][-1]; etat[t]=e[1:]
for j,t in enumerate(ts):
    dessine(ax[0][j],S[t],(-6,-6,12,12),f'A, pas {t} : {etat[t][0]}')
    dessine(ax[1][j],S[t],(-6,3994,12,4012),f'B, pas {t} : {etat[t][1]}')
plt.tight_layout(); plt.savefig(f'{OUT}/4_ecran_2pixels.png',dpi=110); plt.close()
print('ok')

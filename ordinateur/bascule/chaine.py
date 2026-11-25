#!/usr/bin/env python3
"""chaine.py honnetes.json i NMAX : bascule « T » (une même ligne d'entrée). Part de la bascule honnête i (2 tirs : S0→S1→S0)
et ajoute gloutonnement des germes (impulsion m+1 : voie décalée dp ∈ [−8,8], avancée sh ∈ 0..3, recul j ≥ précédent + 2) dont
l'effet est d'inverser l'état. Chaque étape retenue est vérifiée par la chronologie complète (src/fourmi pour la recherche,
moteur Python pour la chronologie) : la suite des états de la pièce doit être S0,S1,S0,S1,… exactement (en place).
Sortie : ../../data/bascule/chaine_<i>.json (situation finale, T, chronologie)."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
from bascule import G, E, situ_piece
os.environ['CY']='cycles2.json'
import recherche_lib as RL
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json')))
H=json.load(open(sys.argv[1])); i=int(sys.argv[2]); h=H[i]; NMAX=int(sys.argv[3])
def etats(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],set(no))); pas(turn,an,no,range(len(an)))
    return {(tuple(a),frozenset(c for c in no if c in vis)) for a,no in L}, vis
ic,s=h['hit']['S0'][:2]; A0,C0,p0=RL.piece0(ic,s); O0,V0=etats(situ_piece(A0,C0),p0)
e=S1L[h['hit']['S1']]; O1,V1=etats(e['situation'],e['periode']); npc=len(A0)
def etat(an,ce):
    P=tuple(an[-npc:])
    if (P,frozenset(x for x in ce if x in V0)) in O0: return 'S0'
    if (P,frozenset(x for x in ce if x in V1)) in O1: return 'S1'
    return '…'
def chrono(sit,T,pasx=100):
    turn,ants,noir=charge(sit); prev=None; log=[]
    for t in range(T+1):
        if t%pasx==0:
            st=etat([tuple(a) for a in ants],noir)
            if st!=prev: log.append((t,st)); prev=st
        if t<T: pas(turn,ants,noir,range(len(ants)))
    return log,[tuple(a) for a in ants]
sit=h['situation']; T=h['T']; m=2; jprev=h['k']
r,a,c=sit.split('|'); g=tuple(map(int,a.split(';')[0].split(',')[:2]))
hist=[{'impulsions':2,'situation':sit,'T':T}]
while m<NMAX:
    r,a,c=sit.split('|'); want='S1' if m%2==0 else 'S0'
    lines=[]; meta=[]
    for j in range(40,100):
        for dp in range(-8,9):
            for sh in range(4):
                gx=g[0]+2*j+sh; gy=g[1]-2*j+dp-sh
                g3=[(x+gx,y+gy) for x,y in G]
                lines.append(f'RL|{gx},{gy},2;'+a+'|'+c+';'+';'.join(f'{x},{y}' for x,y in g3)); meta.append((j,dp,sh,gx,gy))
    T2=T+104*140
    open(f'/tmp/claude-0/ch{i}.txt','w').write('\n'.join(lines)+'\n')
    if os.path.exists(f'/tmp/claude-0/ch{i}.dump'): os.remove(f'/tmp/claude-0/ch{i}.dump')
    subprocess.run(f"{E} -T {T2} -dump /tmp/claude-0/ch{i}.dump -lot < /tmp/claude-0/ch{i}.txt > /dev/null",shell=True)
    trouve=None
    for (j,dp,sh,gx,gy),l,s2 in zip(meta,open(f'/tmp/claude-0/ch{i}.dump'),lines):
        d=l.strip().split('|'); an=[tuple(map(int,x.split(','))) for x in d[-2].split(';')]
        ce={tuple(map(int,x.split(',')[:2])) for x in d[-1].split(';') if x}
        if etat(an,ce)!=want: continue
        log,fin=chrono(s2,T2)
        seq=[st for t,st in log if st!='…']
        attendu=['S0','S1']*((m+2)//2+1)
        if seq==attendu[:m+2]: trouve=(j,dp,sh,gx,gy,s2,log); break
    if not trouve: print('impulsion',m+1,': rien trouvé'); break
    j,dp,sh,gx,gy,sit,log=trouve; g=(gx,gy); T=T2; m+=1
    print('impulsion',m,': germe',(gx,gy),'chronologie',log,flush=True)
    hist.append({'impulsions':m,'situation':sit,'T':T,'chronologie':log})
    json.dump(hist,open(f'../../data/bascule/chaine_{i}.json','w'))

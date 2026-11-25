#!/usr/bin/env python3
"""lecture.py IC_S0 IS1 : pour la bascule (S0 = cycles2[IC_S0] phase 0, S1 = cyclesS1[IS1], même repère = repère du tir 1),
une autoroute 104 neuve (germe R-20, venant du NE) sur chaque voie utile et à TOUTES les phases de S0 et de S1 :
direction de sortie de la sonde + état de la pièce après (même orbite en place ?). Une voie de lecture = résultat identique
pour toutes les phases d'un même état, et différent entre S0 et S1. Calcul : src/fourmi -dump (1 cœur)."""
import sys, json, os, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
from bascule import G, E, situ_piece, dans
os.environ['CY']='cycles2.json'
import recherche_lib as RL
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cyclesS1.json')))
ic=int(sys.argv[1]); i1=int(sys.argv[2]); ROT=int(sys.argv[3]) if len(sys.argv)>3 else 0; D=50
A0,C0,p0=RL.piece0(ic,0); e=dict(S1L[i1])
def rot(sit):                                   # rotation de 90°·ROT : (x,y) → (−y,x), cap +1 (la règle RL est invariante)
    r,a,c=sit.split('|')
    A=[tuple(map(int,t.split(','))) for t in a.split(';')]; C=[tuple(map(int,t.split(','))) for t in c.split(';') if t]
    for _ in range(ROT): A=[(-y,x,(d+1)%4) for x,y,d in A]; C=[(-y,x) for x,y in C]
    return situ_piece(A,C)
A0s=rot(situ_piece(A0,C0)); e['situation']=rot(e['situation'])
def orbite_etats(sit,p):
    turn,an,no=charge(sit); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],sorted(no))); pas(turn,an,no,range(len(an)))
    return L, vis
E0,V0=orbite_etats(A0s,p0); E1,V1=orbite_etats(e['situation'],e['periode'])
K0={(tuple(a),frozenset(c for c in n if c in V0)) for a,n in E0}; K1={(tuple(a),frozenset(c for c in n if c in V1)) for a,n in E1}
zone={(x+dx,y+dy) for x,y in V0|V1 for dx in range(-3,4) for dy in range(-3,4)}
lines=[]; meta=[]
for tx in range(-2*D-24,-2*D+25):
    for ty in range(2*D-24,2*D+25):
        if not (4*D<=-tx+ty<4*D+4): continue
        # la bande de l'autoroute libre passe-t-elle près de la pièce ? (droite x+y = −tx−ty+1 à ±12 près)
        if not any(abs((x+y)-(-tx-ty))<=12 for x,y in zone): continue
        for nom,EE in (('S0',E0),('S1',E1)):
            for s,(A,N) in enumerate(EE):
                cells=[(x-tx,y-ty) for x,y in G]+list(N)
                lines.append(f"RL|{-tx},{-ty},B;"+';'.join(f'{x},{y},{d}' for x,y,d in A)+'|'+';'.join(f'{x},{y}' for x,y in cells)); meta.append((tx,ty,nom,s))
f=f'/tmp/claude-0/lec{os.getpid()}'
open(f+'.txt','w').write('\n'.join(lines)+'\n')
if os.path.exists(f+'.dump'): os.remove(f+'.dump')
out=subprocess.run(f"{E} -T 25000 -retour -dump {f}.dump -lot < {f}.txt",shell=True,capture_output=True,text=True).stdout.splitlines()
R=collections.defaultdict(list)
for (tx,ty,nom,s),o,dl in zip(meta,out,open(f+'.dump')):
    d=dl.strip().split('|'); an=[tuple(map(int,x.split(','))) for x in d[-2].split(';')]
    ce={tuple(map(int,x.split(',')[:2])) for x in d[-1].split(';') if x}
    P=tuple(an[1:]); st='S0' if (P,frozenset(c for c in ce if c in V0)) in K0 else ('S1' if (P,frozenset(c for c in ce if c in V1)) in K1 else '?')
    det=o.split('|')[6].split(' boite')[0].split()[0] if o.split('|')[3]!='RETOUR' else 'R'
    sortie=','.join(det.split(',')[1:3]) if det not in ('-','R') else det
    if st=='?' and any(not dans(a[0],a[1]) for a in an[1:]): st='détruite'
    R[(tx,ty,nom)].append((sortie,st))
res=[]
for (tx,ty) in sorted({(k[0],k[1]) for k in R}):
    a=collections.Counter(R[(tx,ty,'S0')]); b=collections.Counter(R[(tx,ty,'S1')])
    res.append({'voie':[tx,ty],'S0':dict((f'{k[0]}>{k[1]}',v) for k,v in a.items()),'S1':dict((f'{k[0]}>{k[1]}',v) for k,v in b.items())})
json.dump(res,open(f'../../data/bascule/lecture_{ic}_{i1}_r{ROT}.json','w'),indent=0)
def sorties(d): return {k.split('>')[0] for k in d}
for r in res:
    # lecture : chaque état garde son orbite pour toutes ses phases, et les sorties diffèrent
    k0=all(k.endswith('>S0') for k in r['S0']); k1=all(k.endswith('>S1') for k in r['S1'])
    if k0 and k1 and sorties(r['S0'])!=sorties(r['S1']): print('LECTURE :',r)
    elif sorties(r['S0']).isdisjoint(sorties(r['S1'])) and '-2,2' not in sorties(r['S0'])|sorties(r['S1']): print('sorties disjointes :',r)
print(len(lines),'tirs ;',len(res),'voies')

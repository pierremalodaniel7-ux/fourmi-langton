# cascade.py — convoi 104×N : lâcher une fourmi avec un bloc, puis recommencer sur le reste du convoi, jusqu'à 1 fourmi.
# À chaque étage : on essaie les blocs (1 case, ou 2 cases voisines) posés sur le chemin futur du convoi restant.
import sys; sys.path.insert(0,'..')
import banc1, sim, json
banc1.F='../../src/fourmi'
T=600000
def etage(s,N,u):
    f=banc1.fourmi_lot([s],T)[0]; ants,_=banc1.details(f)
    idx=[i for i,a in enumerate(ants) if a and (a[1],a[2])==u]
    if len(idx)!=N: return None,'convoi absent'
    t0=max(ants[i][3] for i in idx); P=104; t1=t0+5*P; m=8
    _,_,_,pos=sim.run(s,t1+P+1,trace=True)
    fresh=sorted({(p[i][0]+m*u[0],p[i][1]+m*u[1]) for p in pos[t1:t1+P] for i in idx})
    blocs=[[c] for c in fresh]+[[c,(c[0]+1,c[1])] for c in fresh]
    lines=[s+(';' if s.split('|')[2] else '')+';'.join(f'{x},{y}' for x,y in b) for b in blocs]
    out=banc1.fourmi_lot(lines,T); good=[]
    for b,l,f in zip(blocs,lines,out):
        if f is None or f[3]!='AUTOROUTES': continue
        a2,_=banc1.details(f); hw=[a for a in a2 if a]
        keep=[a for a in hw if (a[1],a[2])==u]; oth=[a for a in hw if (a[1],a[2])!=u]
        if len(keep)==N-1 and len(oth)==1 and (N-1==1 or f'A104(2,2)x{N-1}' in f[4]):
            good.append((oth[0][3],b,l,(oth[0][1],oth[0][2])))
    good.sort(key=lambda g:(g[3]!=(2,2),g[0]))   # préférence : lâcher vers ↘ (sens des puissances), puis le plus tôt
    return good,len(blocs)
s0='RL|0,0,H;-2,0,B;-2,2,D|'; u=(-2,-2)
g3,n3=etage(s0,3,u); print('N=3 :',len(g3),'/',n3); best=[]
for t,b,s1,d in g3[:40]:
    g2,n2=etage(s1,2,u)
    if g2:
        t2,b2,s2,d2=g2[0]; best.append(dict(bloc1=b,dir1=d,debut1=t,bloc2=b2,dir2=d2,debut2=t2,choix2=len(g2),germe=s2))
        print('cascade 3->2->1 :',b,d,t,'puis',b2,d2,t2,'(',len(g2),'/',n2,')',flush=True)
print(len(best),'cascades complètes sur',min(40,len(g3)))
json.dump(best,open('cascade.json','w'),ensure_ascii=False,indent=1)

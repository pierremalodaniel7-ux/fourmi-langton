# lacher.py — convoi 104×N contre 1 case (toutes les cases de son chemin sur 1 période) et contre des blocs 2 cases voisins.
# Issue cherchée : (N-1) fourmis toujours groupées dans le sens d'origine + 1 fourmi en 104 dans un autre sens.
import sys; sys.path.insert(0,'..')
import banc1, sim, json
banc1.F='../../src/fourmi'
from collections import Counter
CONV={'Tandem 104x2':'RL|0,0,H;-2,0,B|','Convoi 104x3':'RL|0,0,H;-2,0,B;-2,2,D|'}
T=400000
rep={}
for nom,s in CONV.items():
    f=banc1.fourmi_lot([s],T)[0]; ants,_=banc1.details(f); N=len(ants)
    P,dx,dy,t0=ants[0]; t0=max(a[3] for a in ants); u=(dx,dy)
    t1=t0+5*P; _,_,_,pos=sim.run(s,t1+P+1,trace=True); m=8
    fresh=sorted({(p[i][0]+m*dx,p[i][1]+m*dy) for p in pos[t1:t1+P] for i in range(N)})
    blocs=[[c] for c in fresh]+[[c,(c[0]+1,c[1])] for c in fresh]+[[c,(c[0],c[1]+1)] for c in fresh]
    lines=[s+';'.join(f'{x},{y}' for x,y in b) for b in blocs]
    out=banc1.fourmi_lot(lines,T); cnt=Counter(); good=[]
    for b,f in zip(blocs,out):
        sig=f[4]; a2,_=banc1.details(f)
        hw=[a for a in a2 if a]; 
        keep=sum(1 for a in hw if (a[1],a[2])==u); other=[(a[1],a[2]) for a in hw if (a[1],a[2])!=u]
        ok = f[3]=='AUTOROUTES' and f'A104(2,2)x{N-1}' in sig and len(other)==1 and keep==N-1
        cnt[sig if not ok else 'LÂCHER PROPRE']+=1
        if ok: good.append((b,other[0],sig))
    rep[nom]=dict(n=len(blocs),issues=cnt.most_common(8),good=good[:10])
    print(nom,'départ',u,'dès',t0,'| essais',len(blocs)); [print('   ',k,v) for k,v in cnt.most_common(8)]; print('   lâchers propres :',good[:5])
json.dump(rep,open('lacher.json','w'),ensure_ascii=False,indent=1,default=str)

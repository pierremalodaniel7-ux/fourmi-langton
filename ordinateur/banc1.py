# banc1.py — Objectif 1 : chaque autoroute contre (a) 1 case noire à chaque phase, (b) des murs (lignes) à toutes les phases.
import sim, subprocess, sys, json, math
from collections import Counter
F='../src/fourmi'
AUT={ # nom : (situation, pas de base)
 'A104 (1 fourmi)':'RL|0,0,D|-2,-2;-1,-2;0,-1;1,0;-2,1;1,1;-2,2;0,2;-1,3;0,3;0,4',
 'A102 Couple (2)':'RL|0,0,H;-10,-9,D|',
 'A96 Convoi (2+nid)':'RL|0,0,B;1,3,D;2,6,D;3,9,H|',
 'A52 Train (4)':'RL|0,0,H;0,1,H;0,2,B;0,3,B|',
 'A16 Flèche (4)':'RL|0,0,H;-1,-2,H;1,-2,D;-1,1,D|',
 'A108 Suiveuse (3)':'RL|0,0,H;2,-6,G;4,-12,H|',
 'LLLR A52':'LLLR|0,0,H|',
 'LLLLR A84':'LLLLR|0,0,H|',
 'LLR A18':'LLR|0,0,H|',
}
def fourmi_lot(lines,T):
    import concurrent.futures as cf
    half=[lines[0::2],lines[1::2]]
    def go(ls):
        p=subprocess.run([F,'-T',str(T),'-lot'],input='\n'.join(ls)+'\n',capture_output=True,text=True); return p.stdout.strip().split('\n')
    with cf.ThreadPoolExecutor(2) as ex: r=list(ex.map(go,half))
    out={}
    for o in r[0]+r[1]:
        if o: f=o.split('|'); out['|'.join(f[:3])]=f
    return [out[l] for l in lines]
def details(f):
    toks=f[6].split(' boite')[0].split(); ants=[]
    for t in toks:
        if t=='-': ants.append(None)
        else: P,dx,dy,d=map(int,t.split(',')); ants.append((P,dx,dy,d))
    box=f[6].split('boite ')[1].split()[0]
    return ants,box
def ang(u,v):  # angle de u vers v en degrés (y vers le bas : + = sens horaire à l'écran)
    a=math.degrees(math.atan2(v[1],v[0])-math.atan2(u[1],u[0])); a=(a+180)%360-180; return round(a)
def main(T=400000,only=None):
    base=[AUT[k] for k in AUT]; res=fourmi_lot(base,T); rep={}
    for (nom,s),f in zip(AUT.items(),res):
        if only and only not in nom: continue
        ants,box=details(f)
        hw=[a for a in ants if a]; 
        if not hw: print(nom,'pas d autoroute',f[3:5]); continue
        P,dx,dy,t0=max(hw,key=lambda a:a[3])  # fourmi la plus tardive
        t0=max(a[3] for a in hw); u=(dx,dy)
        # cases fraîches : positions de toutes les fourmis-autoroutes sur 1 période, après t0+20P, décalées de m périodes
        t1=t0+5*P; _,_,_,pos=sim.run(s,t1+P+1,trace=True)
        idx=[i for i,a in enumerate(ants) if a and (a[1],a[2])==u]
        m=8; fresh=sorted({(p[i][0]+m*dx,p[i][1]+m*dy) for p in pos[t1:t1+P] for i in idx})
        tests=[]
        for c in fresh: tests.append(('case',c,{c}))
        # murs : ligne de longueur 401 centrée en c0 (position de tête + m périodes), 4 directions, plein / pointillé, décalée de 0..7 cases vers l'avant
        hx,hy=pos[t1][idx[0]]; c0=(hx+m*dx,hy+m*dy); n=math.hypot(dx,dy); fw=(round(dx/n) if abs(dx)/n>0.38 else 0, round(dy/n) if abs(dy)/n>0.38 else 0)
        for wd in [(1,0),(0,1),(1,1),(1,-1)]:
            for pat in (1,2):
                for s_ in range(8):
                    cs={(c0[0]+fw[0]*s_+k*wd[0],c0[1]+fw[1]*s_+k*wd[1]) for k in range(-200,201) if k%pat==0}
                    tests.append((f'mur{wd}{"plein" if pat==1 else "pointillé"}',s_,cs))
        lines=[s.split('|')[0]+'|'+s.split('|')[1]+'|'+';'.join(filter(None,[s.split('|')[2]]+[f'{x},{y}' for x,y in sorted(cs)])) for _,_,cs in tests]
        out=fourmi_lot(lines,T)
        rows=[]
        for (kind,ph,cs),f in zip(tests,out):
            a2,box2=details(f); _,_,tc,_=sim.run(s,t1+m*P+2*P,watch=cs)  # contact (2e moteur)
            dirs=Counter((a[1],a[2]) for a in a2 if a); nonc=sum(1 for a in a2 if a is None)
            fin=max((a[3] for a in a2 if a),default=None)
            rows.append(dict(kind=kind,ph=str(ph),issue=f[3],sig=f[4],dirs={str(k):v for k,v in dirs.items()},nonc=nonc,
                             tc=tc,chaos=(fin-tc if fin is not None and tc else None),angles=sorted({ang(u,k) for k in dirs}),box=box2))
        rep[nom]=dict(base=f[4],P=P,u=u,t0=t0,nfresh=len(fresh),rows=rows)
        print(nom,'fait',len(rows),flush=True)
    return rep
if __name__=='__main__':
    T=int(sys.argv[1]) if len(sys.argv)>1 else 400000; only=sys.argv[2] if len(sys.argv)>2 else None
    rep=main(T,only); json.dump(rep,open(f'banc1_{only or "tout"}.json','w'),indent=0)

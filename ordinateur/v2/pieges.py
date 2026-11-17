# pieges.py — piste 5 : cycle court posé devant l'autoroute 104 ↙ (germe 0,0,D + 11 cases), origine du piège en
# (cx,cy) = (-160+p+s, 160+p-s), 4 rotations. Classement exact par trap.c (cycle EXACT des fourmis bornées).
import subprocess, json, sys
BIN='./trapL'
from collections import Counter
SRC_A='0,0,D'; SRC_C=[(-2,-2),(-1,-2),(0,-1),(1,0),(-2,1),(1,1),(-2,2),(0,2),(-1,3),(0,3),(0,4)]
CYC={'Tourniquet 4':('-1,-1,H;0,0,D','0,0'),'Petit Grain 8':('-1,-2,D;-2,-1,H','-2,-2'),
     'Rouage 8':('2,-2,H;1,-1,D;0,-1,B;0,-2,H','1,0;1,-2;1,-1;2,-2;0,0;0,-3;1,-3'),
     'Petite Rosace 16':('-2,-3,H;1,1,H;3,-2,D;-1,1,D;2,3,B;-1,-1,B;-3,2,G;1,-1,G','')}
def rot(r,x,y):
    for _ in range(r): x,y=-y,x
    return x,y
def piege(nom,r,cx,cy):
    a,c=CYC[nom]; ants=[];cells=[]
    for t in a.split(';'):
        x,y,d=t.split(','); X,Y=rot(r,int(x),int(y)); ants.append(f'{X+cx},{Y+cy},{"HDBG"[("HDBG".index(d)+r)%4]}')
    for t in filter(None,c.split(';')):
        x,y=map(int,t.split(',')); X,Y=rot(r,x,y); cells.append(f'{X+cx},{Y+cy}')
    return ants,cells
def situ(nom,r,cx,cy):
    a,c=piege(nom,r,cx,cy)
    return 'RL|'+';'.join([SRC_A]+a)+'|'+';'.join([f'{x},{y}' for x,y in SRC_C]+c)
def run(lines,T):
    import concurrent.futures as cf
    def go(ls):
        p=subprocess.run([BIN],input=''.join(f'{l} {T}\n' for l in ls),capture_output=True,text=True); return p.stdout.strip().split('\n')
    with cf.ThreadPoolExecutor(2) as ex: r=list(ex.map(go,[lines[0::2],lines[1::2]]))
    out=[None]*len(lines); out[0::2]=r[0]; out[1::2]=r[1]; return out
FL={(-2,2):'↙',(2,2):'↘',(-2,-2):'↖',(2,-2):'↗'}
def resume(o):
    if o=='BORD': return 'BORD',None
    t=o.split(); hw=[x for x in t if x.startswith('A')]; nb=t.count('B'); cyc=[t[i+1] for i,x in enumerate(t) if x=='CYC']
    dirs=[]
    for h in hw:
        P,rest=h[1:].split(':'); dx,dy,u=map(int,rest.split(',')); dirs.append((int(P),FL.get((dx,dy),f'{dx},{dy}'),u))
    return ('TOUT COINCÉ' if 'TOUT' in t else f"{len(hw)} autoroute(s) {[d[:2] for d in dirs]} + {nb} bornée(s) {'cycle '+cyc[0] if cyc else ('pas de cycle' if nb else '')}"),dirs
if __name__=='__main__':
    T=200000; cas=[(n,r,p,s) for n in CYC for r in range(4) for p in range(-8,9) for s in range(4)]
    lines=[situ(n,r,-160+p+s,160+p-s) for n,r,p,s in cas]; out=run(lines,T)
    cnt=Counter(); capt=[]
    for (n,r,p,s),l,o in zip(cas,lines,out):
        res,dirs=resume(o); cnt[res.split(' [')[0] if 'autoroute' in res else res]+=1
        if 'cycle' in res and dirs is not None and len(dirs)==1 and dirs[0][0]==104: capt.append(dict(cycle=n,rot=r,p=p,s=s,issue=res,germe=l,brut=o))
    for k,v in cnt.most_common(12): print(v,k)
    print(len(capt),'captures : cycle exact + 1 seule 104 éjectée')
    for c in capt[:40]: print(' ',c['cycle'],'r',c['rot'],'p',c['p'],'s',c['s'],c['issue'])
    json.dump(capt,open('pieges.json','w'),ensure_ascii=False,indent=1)

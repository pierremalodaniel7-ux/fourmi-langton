# 5c : le cycle laissé par une capture capture-t-il une 2e autoroute ? 2e source = germe 104 tourné, placé pour viser le piège.
import pieges as Pg, json, subprocess, sys
sys.path.insert(0,'..'); import portes as Pt
from collections import Counter
caps=[x for x in json.load(open('pieges_vrais.json')) if x['type']=='capture']
caps=sorted(caps,key=lambda x:x['periode'])[:12]
lines=[];meta=[]
for x in caps:
    cx,cy=-160+x['p']+x['s'],160+x['p']-x['s']
    for r in range(4):             # 2e source arrivant de 4 directions, partant à ~250 cases du piège
        D=Pt.DIRS[r]; L=125
        for off in range(-3,4):     # voie : décalage perpendiculaire
            px,py=cx-D[0]*L//2+off*(1 if D[0]*D[1]<0 else -1), cy-D[1]*L//2+off
            (a,cells)=Pt.germe(px,py,r)
            s=x['germe'].split('|'); st=s[0]+'|'+s[1]+f';{a[0]},{a[1]},{a[2]}|'+s[2]+';'+';'.join(f'{u},{v}' for u,v in cells)
            lines.append(st); meta.append((x['cycle'],x['rot'],x['p'],x['s'],x['periode'],r,off))
Pg.BIN='./trapL'; out=Pg.run(lines,200000)
cnt=Counter(); good=[]
for m,l,o in zip(meta,lines,out):
    if o=='BORD': cnt['BORD']+=1; continue
    t=o.split(); hw=[z for z in t if z.startswith('A')]; cyc='CYC' in t
    n0=1  # avant : 1 éjectée ; après une 2e capture propre : 2 éjectées en tout + cycle
    k='TOUT' if 'TOUT' in t else (f'{len(hw)} autoroutes + cycle' if cyc else f'{len(hw)} autoroutes, pas de cycle')
    cnt[k]+=1
    if cyc and len(hw)==2 and all(z.startswith('A104') for z in hw): good.append(dict(m=m,o=o,germe=l))
for k,v in cnt.most_common(): print(v,k)
print(len(good),'doubles captures (cycle exact + 2 autoroutes 104 au total) ; ex :',[g['m'] for g in good[:6]])
json.dump(good,open('reuse.json','w'),ensure_ascii=False,indent=1)

# convoi.py — construction gloutonne de convois 104×N : à un convoi 104×(N-1), ajouter une fourmi dans [-R,R]² × 4 caps
# et garder les placements qui donnent la signature A104(2,2)xN (toutes les fourmis groupées, < 64 cases).
import subprocess, sys, json
F='../../src/fourmi'
def lot(lines,T=200000):
    import concurrent.futures as cf
    def go(ls):
        p=subprocess.run([F,'-T',str(T),'-lot'],input='\n'.join(ls)+'\n',capture_output=True,text=True); return p.stdout.strip().split('\n')
    with cf.ThreadPoolExecutor(2) as ex: r=list(ex.map(go,[lines[0::2],lines[1::2]]))
    out={}
    for o in r[0]+r[1]:
        f=o.split('|'); out['|'.join(f[:3])]=f
    return [out.get(l) for l in lines]
conv=['0,0,H','-2,0,B','-2,2,D']; R=int(sys.argv[1]) if len(sys.argv)>1 else 6; Nmax=int(sys.argv[2]) if len(sys.argv)>2 else 15
res={3:(';'.join(conv),'A104x3')}
while len(conv)<Nmax:
    occ={tuple(map(int,a.split(',')[:2])) for a in conv}
    cand=[f'{x},{y},{d}' for x in range(-R,R+1) for y in range(-R,R+1) for d in 'HDBG' if (x,y) not in occ]
    lines=['RL|'+';'.join(conv+[c])+'|' for c in cand]
    out=lot(lines); n=len(conv)+1; good=[]
    for c,f in zip(cand,out):
        if f and f[3]=='AUTOROUTES' and f[4]==f'A104(2,2)x{n}':
            t0=max(int(t.split(',')[3]) for t in f[6].split(' boite')[0].split())
            good.append((t0,c,f[6].split(' boite')[1]))
    if not good: print('N =',n,': aucun placement (sur',len(cand),')'); break
    good.sort(); t0,c,box=good[0]; conv.append(c); res[n]=(';'.join(conv),f'A104x{n} dès {t0}, {len(good)} placements, boîte{box}')
    print('N =',n,':',len(good),'placements ; retenu',c,'autoroute dès',t0,flush=True)
json.dump(res,open(f'convois_R{R}.json','w'),ensure_ascii=False,indent=1)

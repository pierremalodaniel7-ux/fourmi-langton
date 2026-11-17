# OU LLR à 2 étages : P1 = NOR(a,b) (sort ↘ ssi a=b=0) ; P2 part ↗ sur la voie x+y = L2, croise la ligne de P1 plus loin.
import subprocess, sys
sys.path.insert(0,'..'); import sim
P1='-141,-40,G'
res=[]
for L2 in range(200,232):
  for D in (600,602,604,606):
    w=-100-D
    if (w+L2)%2: continue
    p2=f'{(w+L2)//2},{(L2-w)//2},B'
    lines=[]
    for a in (0,1):
      for b in (0,1):
        ants=(['0,0,H'] if a else [])+(['32,32,H'] if b else [])+[P1,p2]
        lines.append('LLR|'+';'.join(ants)+'|')
    o=subprocess.run(['./trapL'],input=''.join(f'{l} 40000\n' for l in lines),capture_output=True,text=True).stdout.strip().split('\n')
    out=[x.split()[-1] if not x.startswith('BORD') else 'BORD' for x in o]
    got=[int(z.startswith('A18:1,-1')) for z in out]
    if got==[0,1,1,1]: res.append((L2,D,p2,out))
print(len(res),'placements de P2 donnent OU 4/4 (moteur C) ; ex :',res[:3])
if res:
    L2,D,p2,_=res[0]; ok=0
    for a in (0,1):
      for b in (0,1):
        ants=(['0,0,H'] if a else [])+(['32,32,H'] if b else [])+[P1,p2]
        _,_,_,pos=sim.run('LLR|'+';'.join(ants)+'|',40000,trace=True); i=len(ants)-1
        d=(pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1])
        ok+= int(d==(1,-1))==int(a or b)
    print('Python :',ok,'/4 pour',p2)

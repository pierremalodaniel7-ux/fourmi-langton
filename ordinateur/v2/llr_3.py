# 3 étages LLR : P1 = NOR (↘), P2 = NON(P1) = OU (↗), P3 = NON(P2) = NOR (↖ continue ssi P2 absente).
import subprocess, sys
sys.path.insert(0,'..'); import sim
P1='-141,-40,G'; P2='-250,450,B'
res=[]
for w3 in range(-20,12):
  for k in range(2):
    L=1100+k*2 + ((w3+1100) % 2)   # parité x+y ≡ x-y
    p3=f'{(w3+L)//2},{(L-w3)//2},D'    # cap D -> autoroute ↖ (vu plus haut : D donne (-1,-1))
    lines=['LLR|'+';'.join((['0,0,H'] if a else [])+(['32,32,H'] if b else [])+[P1,P2,p3])+'|' for a in (0,1) for b in (0,1)]
    o=subprocess.run(['./trapL'],input=''.join(f'{l} 60000\n' for l in lines),capture_output=True,text=True).stdout.strip().split('\n')
    got=[int(x.split()[-1].startswith('A18:-1,-1')) if not x.startswith('BORD') else -1 for x in o]
    res.append(((w3,L,p3),got))
good=[r for r in res if r[1]==[1,0,0,0]]
print(len(good),'/',len(res),'placements de P3 donnent NOR 4/4 en 3 étages (moteur C)')
if good:
    p3=good[0][0][2]; ok=0
    for a in (0,1):
      for b in (0,1):
        ants=(['0,0,H'] if a else [])+(['32,32,H'] if b else [])+[P1,P2,p3]
        _,_,_,pos=sim.run('LLR|'+';'.join(ants)+'|',60000,trace=True); i=len(ants)-1
        d=(pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1]); ok+= int(d==(-1,-1))==int(a==b==0)
    print('Python :',ok,'/4 pour P3 =',p3)

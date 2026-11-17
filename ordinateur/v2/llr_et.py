# ET LLR = NOR(NON a, NON b). A = -500,500,H (voie x+y≈1, part de x-y = -1000) ; B = 32,32,H (voie ≈65, part de x-y = 0).
# Pa (cap G -> ↘) sur x-y = -1200, part de x+y ≈ -443 ; Pb (cap D -> ↖) sur x-y = -300, part de x+y ≈ 620 ;
# Q (cap B -> ↗) sur la voie x+y = LQ entre 1 et 65, part de x-y ≈ -1700 : Q continue ↗ ssi a ET b.
import subprocess, sys, itertools
sys.path.insert(0,'..'); import sim
def ant(w,l,d):
    if (w+l)%2: l+=1
    return f'{(w+l)//2},{(l-w)//2},{d}'
found=[]
for LQ in range(20,48):
  for da,db,dq in itertools.product((0,2),(0,2),(0,2)):
    Pa=ant(-1200,-443-da,'G'); Pb=ant(-300,620+db,'D'); Q=ant(-1700-dq,LQ,'B')
    lines=['LLR|'+';'.join((['-500,500,H'] if a else [])+(['32,32,H'] if b else [])+[Pa,Pb,Q])+'|' for a in (0,1) for b in (0,1)]
    o=subprocess.run(['./trapL'],input=''.join(f'{l} 60000\n' for l in lines),capture_output=True,text=True).stdout.strip().split('\n')
    got=[int(x.split()[-1].startswith('A18:1,-1')) if not x.startswith('BORD') else -1 for x in o]
    if got==[0,0,0,1]: found.append((LQ,Pa,Pb,Q))
print(len(found),'/',28*8,'placements donnent ET 4/4 (moteur C)', found[:2])
if found:
    LQ,Pa,Pb,Q=found[0]; ok=0
    for a in (0,1):
      for b in (0,1):
        ants=(['-500,500,H'] if a else [])+(['32,32,H'] if b else [])+[Pa,Pb,Q]
        _,_,_,pos=sim.run('LLR|'+';'.join(ants)+'|',60000,trace=True); i=len(ants)-1
        d=(pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1]); ok+= int(d==(1,-1))==int(a and b)
    print('Python :',ok,'/4 ; germe',Pa,Pb,Q)

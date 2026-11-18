# compare creux (C, hachage) et sim.py (Python) sur des situations : nb cases non blanches + déplacement final de chaque fourmi
import sys, subprocess; sys.path.insert(0,'..'); import sim
cas=[("RL|0,0,H||",11000),("RL|0,0,H;40,0,G||",20000),("RL|2,1,B;3,-5,H;5,2,B||",30000),("LLR|0,0,H;30,-7,G;-12,9,D||",20000),
     ("RLR|0,0,H||",5000),("LLRR|0,0,H;5,5,B||",8000),("RL|0,0,H|1,0;0,1;-3,2;5,5,1|",15000)]
out=subprocess.run(['./creux'],input=''.join(f'{s} {T}\n' for s,T in cas),capture_output=True,text=True).stdout.strip().split('\n')
ok=0
for (s,T),o in zip(cas,out):
    ants,g,_,pos=sim.run(s,T,trace=True)
    nz=sum(1 for v in g.values() if v)
    py=[f"{pos[-1][i][0]-pos[-19][i][0]},{pos[-1][i][1]-pos[-19][i][1]},{min(p[i][0]+p[i][1] for p in pos[-18:])},{min(p[i][0]-p[i][1] for p in pos[-18:])}" for i in range(len(ants))]
    c=o.split(); same = c[1]==f"noires={nz}" and c[2:]==py; ok+=same
    print('OK ' if same else 'DIFF',s,T,c[1],nz)
print(ok,'/',len(cas))

# revérification piste 3 avec sim.py (Python) : période et déplacement de chaque fourmi à la fin
import sys; sys.path.insert(0,'..'); import sim
def per(s,T):
    _,_,_,pos=sim.run(s,T,trace=True); out=[]
    for i in range(len(pos[0])):
        for P in range(1,400):
            d=(pos[-1][i][0]-pos[-1-P][i][0],pos[-1][i][1]-pos[-1-P][i][1])
            if d!=(0,0) and all((pos[-1-k][i][0]-pos[-1-k-P][i][0],pos[-1-k][i][1]-pos[-1-k-P][i][1])==d for k in range(3*P)):
                out.append((P,d)); break
        else: out.append(None)
    return out
for s in sys.argv[1:]: print(s, per(s,int(40000)))

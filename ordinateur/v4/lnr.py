# R-10 LⁿR : suite des couleurs lues pas à pas (compressée), pour chercher une structure uniforme en n
import sys; sys.path.insert(0,'..'); import sim
DX,DY=sim.DX,sim.DY
def run(n,T):
    q=n+1; g={}; a=[0,0,0]; lu=[]; pos=[]
    for t in range(T):
        k=(a[0],a[1]); c=g.get(k,0); lu.append(c); a[2]=(a[2]+(1 if c==n else 3))&3; g[k]=(c+1)%q; a[0]+=DX[a[2]]; a[1]+=DY[a[2]]; pos.append((a[0],a[1],a[2]))
    return lu,pos,g
for n in range(3,8):
    P=16*n+4; t0=24*n+7; lu,pos,g=run(n,t0+3*P)
    print(n,'transitoire:',''.join('R' if c==n else str(c) for c in lu[:t0]))
    print('  periode   :',''.join('R' if c==n else str(c) for c in lu[t0:t0+P]), 'depl',pos[t0+P-1][0]-pos[t0-1][0],pos[t0+P-1][1]-pos[t0-1][1])

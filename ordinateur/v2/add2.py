# add2.py — additionneur 2 bits à UNE puissance : a1, b1 doublés (2 germes parallèles = poids 2).
import sys; sys.path.insert(0,'..')
import portes as Pt, sim, json, itertools, subprocess, os
GATE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','gate')
E=list(itertools.product((0,1),repeat=4))   # (a1,a0,b1,b0)
LAM={'a0':0,'b0':128,'a1':(256,384),'b1':(512,640)}
def gin(e):
    a1,a0,b1,b0=e; g=[]
    if a0: g.append(Pt.germe(0,0,0))
    if b0: g.append(Pt.germe(64,64,0))
    if a1: g+= [Pt.germe(128,128,0),Pt.germe(192,192,0)]
    if b1: g+= [Pt.germe(256,256,0),Pt.germe(320,320,0)]
    return g
val=lambda e: e[1]+e[3]+2*e[0]+2*e[2]
def P(w=-121,s=-391): return Pt.germe((w+s)//2,(s-w)//2,3)
def run2(situs,T):
    import concurrent.futures as cf
    def go(ls):
        p=subprocess.run([GATE],input=''.join(f'{s} {T}\n' for s in ls),capture_output=True,text=True)
        return [ 'BORD' if l.startswith('BORD') else [None if t=='X' else tuple(map(int,t.split(','))) for t in l.split()] for l in p.stdout.strip().split('\n')]
    with cf.ThreadPoolExecutor(2) as ex: r=list(ex.map(go,[situs[0::2],situs[1::2]]))
    out=[None]*len(situs); out[0::2]=r[0]; out[1::2]=r[1]; return out
if __name__=='__main__':
    r=run2([Pt.situ(gin(e)+[P()]) for e in E],130000)
    base=r[0][-1][2]
    for e,o in zip(E,r): print(e,'v =',val(e),'voie P - L =',None if o=='BORD' or o[-1] is None else (o[-1][0],o[-1][1],o[-1][2]-base))

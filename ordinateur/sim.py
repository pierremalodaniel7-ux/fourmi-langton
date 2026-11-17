# sim.py — 2e moteur indépendant (Python, entiers), règles carrées L/R/N/U, fourmis jouées dans l'ordre.
# Conventions du projet : 0=H(0,-1) 1=D(1,0) 2=B(0,1) 3=G(-1,0), y vers le bas, R=+1.
DX=[0,1,0,-1]; DY=[-1,0,1,0]; CAP={'H':0,'D':1,'B':2,'G':3}; TURN={'R':1,'L':3,'N':0,'U':2}
def parse(s):
    r,a,c=(s.split('|')+['',''])[:3]
    ants=[]
    for t in a.split(';'):
        t=t.strip()
        if t: x,y,d=t.split(','); ants.append([int(x),int(y),CAP[d.strip()] if d.strip() in CAP else int(d)])
    cells={}
    for t in c.split(';'):
        t=t.strip()
        if t:
            p=t.split(','); cells[(int(p[0]),int(p[1]))]=int(p[2]) if len(p)>2 else 1
    return r.strip(),ants,cells
def run(s,T,watch=None,trace=False):
    """renvoie (ants, grille, t_contact, positions) ; t_contact = 1er pas où une fourmi entre dans watch"""
    r,ants,g=parse(s); q=len(r); K=[TURN[ch] for ch in r]; tc=None; pos=[]
    for t in range(T):
        for a in ants:
            k=(a[0],a[1]); c=g.get(k,0); a[2]=(a[2]+K[c])&3; g[k]=(c+1)%q
            a[0]+=DX[a[2]]; a[1]+=DY[a[2]]
            if watch is not None and tc is None and (a[0],a[1]) in watch: tc=t+1
        if trace: pos.append([(a[0],a[1]) for a in ants])
    return ants,g,tc,pos

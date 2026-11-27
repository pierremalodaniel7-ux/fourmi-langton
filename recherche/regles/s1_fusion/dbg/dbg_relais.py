import sys, os, json, collections
sys.argv=['x','0','1']; __file__='s1_fusion/add2_fusion.py'
sys.path.insert(0,'.'); sys.path.insert(0,'s1_fusion')
exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
st=collections.Counter()
for zi in range(0,60,3):
    z=RL[zi]
    dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
    for sin, other in (('s1','s2'),('s2','s1')):
        P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho=(2-rin)%6
        base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != other])
        for D1 in (0, 300):
          Dv = slide(attach(base, sin, rho, c0, 4000), sin, D1)
          Rd = lotdump([Circuit(Dv.pieces).sit({'x':1,'y':1}), Circuit([(n,p,v) for n,p,v in Dv.pieces if n!=sin]).sit({})], T)
          ok_alone = decode(*Rd[0]) is not None and decode(*Rd[1]) is not None
          for ordre in (0,1):
            dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
            pcs = HA0.pieces + dpcs if ordre == 0 else dpcs + HA0.pieces
            C1 = Circuit(pcs); R = lotdump([C1.sit(e) for e in C1.cases()], T)
            dirty = tuple(i for i,r in enumerate(R) if decode(*r) is None)
            st[(sin, D1, ordre, ok_alone, dirty)] += 1
for k,v in sorted(st.items(), key=str): print(v,k)
print('----')
z=RL[0]; dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
sin,other='s1','s2'
base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != other])
Dv = attach(base, sin, 0, c0, 4000)
Rd = lotdump([Circuit(Dv.pieces).sit({'x':1,'y':1}), Circuit([(n,p,v) for n,p,v in Dv.pieces if n!=sin]).sit({})], T)
print('relais seul avec c0', decode(*Rd[0])); print('sans', decode(*Rd[1]))
dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
C1 = Circuit(HA0.pieces + dpcs); R = lotdump([C1.sit(e) for e in C1.cases()], T)
for e,r in zip(C1.cases(),R): print(e, decode(*r))
print('O\' du json', z['Op'], 'order', z['c'])

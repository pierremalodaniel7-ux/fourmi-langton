import sys, collections
sys.argv=['x','0','1','s1_fusion/fusion3_122_0_2.json']; __file__='s1_fusion/add2_fusion.py'
sys.path.insert(0,'.'); sys.path.insert(0,'s1_fusion')
exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
st=collections.Counter()
for zi in range(0,30,5):
  z=RL[zi]; dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
  sin='s1'; P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho=(2-rin)%6
  base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != 's2'])
  for D1 in (0,40,120):
    Dv = slide(attach(base, sin, rho, c0, 4000), sin, D1)
    dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
    pcs = HA0.pieces + dpcs
    C1 = Circuit(pcs); R = lotdump([C1.sit(e) for e in C1.cases()], T)
    d=[decode(*r) for r in R]
    if None in d: print(zi,D1,'sale', [i for i,x in enumerate(d) if x is None]); continue
    ins = [(n,route(p)) for n, p, v in pcs]
    fr=[(s,n) for v_ in d for s in v_ for n,e in ins if front(s[:2],e)]
    print(zi, D1, 'face', set(fr))

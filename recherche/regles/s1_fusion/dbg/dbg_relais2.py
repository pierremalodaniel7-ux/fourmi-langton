import sys
sys.argv=['x','0','1']; __file__='s1_fusion/add2_fusion.py'
sys.path.insert(0,'.'); sys.path.insert(0,'s1_fusion')
exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
for zi in (0, 3, 6):
  z=RL[zi]; dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
  for sin in ('s1','s2'):
    P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho=(2-rin)%6
    Df = attach(dev, sin, rho, c0, 4000)
    Rd = lotdump([Df.sit(e) for e in ({'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1})], T)
    print(zi, sin, [decode(*r) for r in Rd], [p[0] for n,p,v in Df.pieces])
  R0 = lotdump([dev.sit(e) for e in ({'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1})], 4000)
  print('  frame', [decode(*r) for r in R0], z['Op'])

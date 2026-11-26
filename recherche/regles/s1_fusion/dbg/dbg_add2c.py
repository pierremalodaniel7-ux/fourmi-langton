import sys
sys.argv=['x','0','1','s1_fusion/data_relais122_s5.json']; __file__='s1_fusion/add2_fusion.py'
sys.path.insert(0,'.'); sys.path.insert(0,'s1_fusion')
exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
from diag import diag
z = RL[0]; dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
sin='s1'; P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho = (2 - rin) % 6
Dv = attach(Circuit([(n,p,v) for n,p,v in dev.pieces if n!='s2']), sin, rho, c0, 4000)
cp=(3, -55, 1835, 5)
F1 = attach(FAc, 'c', (cp[0]-4)%6, cp, T)
for e in ({'a':0,'b':0},{'a':1,'b':0},{'a':0,'b':1}):
  ha = HA0.sit({'a0':1,'b0':1})
  rel = sit([p for n,p,v in Dv.pieces if n!=sin])
  fa = sit([p for n,p,v in F1.pieces if n!='c' and (v is None or e.get(v))])
  # le relais et FA1 ont besoin de leur entrée : on compare au circuit « relais + c0 » et « FA1 + c » : modules = (HA0+relais), FA1 avec c
  print(e, diag([('HA0+relais', sit([p for n,p,v in HA0.pieces] + [p for n,p,v in Dv.pieces if n!=sin])), ('FA1', fa)], 3000)[:6])

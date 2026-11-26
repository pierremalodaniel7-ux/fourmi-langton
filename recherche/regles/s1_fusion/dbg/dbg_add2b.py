import sys, collections
sys.argv=['x','0','1','s1_fusion/data_relais122_s5.json']; __file__='s1_fusion/add2_fusion.py'
sys.path.insert(0,'.'); sys.path.insert(0,'s1_fusion')
exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
from hx import ship
# FA attaché à un vaisseau isolé de même trajectoire que c0 : 8 cas
F1 = attach(FAc, 'c', (2-4)%6, c0, 4000)
F1 = Circuit(F1.pieces, None)
cs = F1.cases(); R = lotdump([F1.sit(e) for e in cs], T)
O = {(e['a'],e['b'],e['c']): [tuple(x) for x in decode(*r)] for e,r in zip(cs,R)}
print('FA tourné seul : S', cover(O, lambda k: sum(k)%2), 'C', cover(O, lambda k: int(sum(k)>=2)))
cnt=0
for zi in range(0, 60):
  z = RL[zi]; dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
  for sin, other in (('s1', 's2'), ('s2', 's1')):
    P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho = (2 - rin) % 6
    base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != other])
    for D1, ordre in itertools.product((0, 40, 120), (0, 1)):
        Dv = slide(attach(base, sin, rho, c0, 4000), sin, D1)
        dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
        pcs = HA0.pieces + dpcs if ordre == 0 else dpcs + HA0.pieces
        C1 = Circuit(pcs); R = lotdump([C1.sit(e) for e in C1.cases()], T)
        if any(decode(*r) is None for r in R): continue
        O = {(e['a0'], e['b0']): [tuple(x) for x in decode(*r)] for e, r in zip(C1.cases(), R)}
        Df = slide(attach(dev, sin, rho, c0, 4000), sin, D1)
        Rd = lotdump([Df.sit(e) for e in ({'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1})], T)
        dd = [decode(*r) for r in Rd]
        new = (set(map(tuple, dd[1])) & set(map(tuple, dd[2]))) - set(map(tuple, dd[0]))
        cps = [x for x in new if x in O[(1, 1)] and all(x not in O[k] for k in O if k != (1, 1))]
        if len(cps) != 1: continue
        cp = cps[0]; rho2 = (cp[0] - 4) % 6
        F1 = attach(FAc, 'c', rho2, cp, T)
        # FA1 seul (sans étage 0) attaché à cp : marche-t-il ?
        F1s = Circuit(F1.pieces); cs = F1s.cases(); R = lotdump([F1s.sit(e) for e in cs], T)
        Os = {(e['a'],e['b'],e['c']): (decode(*r) and [tuple(x) for x in decode(*r)]) for e,r in zip(cs,R)}
        print(zi, sin, D1, ordre, 'cp', cp, 'FA1 seul: S', cover(Os, lambda k: sum(k)%2) if None not in Os.values() else 'sale')
        pcs2 = pcs + [(n + '1', p, {'a': 'a1', 'b': 'b1'}.get(v, v)) for n, p, v in F1.pieces if n != 'c']
        C2 = Circuit(pcs2); cs = C2.cases(); R2 = lotdump([C2.sit(e) for e in cs], T)
        bad = [tuple(e.values()) for e, r in zip(cs, R2) if decode(*r) is None]
        print('   16 cas sales :', bad)
        cnt += 1
        if cnt > 5: sys.exit()

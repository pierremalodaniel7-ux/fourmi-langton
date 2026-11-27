import sys, os, json
sys.argv=['x','0','1']
HERE='s1_fusion'; sys.path.insert(0,'.'); sys.path.insert(0,HERE)
__file__='s1_fusion/add2_fusion.py'; exec(open('s1_fusion/add2_fusion.py').read().split("a0, a1 = int")[0])
z=RL[0]
dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
print(z['pieces'])
for sin, other in (('s1','s2'),('s2','s1')):
    P = dict((n, p) for n, p, v in dev.pieces)[sin]; rin = decode([P[0]], P[1])[0][0]; rho=(2-rin)%6
    base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != other])
    Dv = attach(base, sin, rho, c0, 4000)
    for ordre in (0,1):
        dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
        pcs = HA0.pieces + dpcs if ordre == 0 else dpcs + HA0.pieces
        C1 = Circuit(pcs)
        R = lotdump([C1.sit(e) for e in C1.cases()], T)
        for e, r in zip(C1.cases(), R): print(sin, ordre, e, decode(*r), len(r[1]))
        O = {(e['a0'], e['b0']): [tuple(x) for x in decode(*r)] for e, r in zip(C1.cases(), R) if decode(*r)}
        if len(O)==4:
            Pc = cover(O, lambda k: k[0] & k[1]); print('Pc', Pc)
            cp=Pc[0]; rho2=(cp[0]-4)%6
            F1 = attach(FAc, 'c', rho2, cp, 4000)
            pcs2 = pcs + [(n + '1', p, {'a': 'a1', 'b': 'b1'}.get(v, v)) for n, p, v in F1.pieces if n != 'c']
            C2 = Circuit(pcs2); cs=C2.cases(); R2 = lotdump([C2.sit(e) for e in cs], T)
            for e, r in zip(cs, R2): print('  ', e, decode(*r))
            break

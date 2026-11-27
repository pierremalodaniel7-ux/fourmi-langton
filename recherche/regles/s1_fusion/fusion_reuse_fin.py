#!/usr/bin/env python3
"""S1 / R-406 Fusions à 1 constant revues avec le critère FIN de croisement (R-404) : deux vaisseaux libres à contresens ne
s'influencent que si la somme de leurs voies est dans [−3, 1] (distance minimale ≤ 1) ; ailleurs ils se croisent exactement.
On refiltre les 1 529 fusions (fusion1_ok.json) avec ce critère, puis 2 usages (9 suites, superposition exacte), 20 usages (3 graines).
Usage : python3 s1_fusion/fusion_reuse_fin.py"""
import sys, os, json, random, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fa_lib import decode, lotdump
from circuit import check_multi
from fusion_reuse import Excl, route, make
def front_fin(s, e): return (s[0] - e[0]) % 6 == 3 and -3 <= s[1] + e[1] <= 1
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); K = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
ok = json.load(open(os.path.join(HERE, 'fusion1_ok.json'))); rk = route(K)
keep = []
for z in ok:
    ins = [tuple(z['r1']), tuple(z['r2']), rk]
    outs = {tuple(o[:2]) for q in (0, 1, 2) for o in z['out%d' % q]}
    if any(front_fin(s, e) for s in outs for e in ins): continue
    keep.append(z)
print('sans route de face (critère fin) :', len(keep), '/', len(ok), flush=True)
Cs = [Excl(make(z, K)) for z in keep]
R = lotdump([C.sit(e) for C in Cs for e in C.cases()], 4000)
good = []; st = collections.Counter()
for n, (z, C) in enumerate(zip(keep, Cs)):
    d = [decode(*R[3 * n + q]) for q in range(3)]
    if None in d: st['sale'] += 1; continue
    d = [set(map(tuple, x)) for x in d]
    com = (d[1] & d[2]) - d[0]
    if len(com) != 1: st['O ambigu'] += 1; continue
    O = sorted(com)[0]
    shadow = any(p[0] == O[0] and abs(p[1] - O[1]) <= 6 for p in d[0])
    C.outputs = {'O': (lambda e: e['x'] | e['y'], [O])}
    n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
    st[('ombre' if shadow else 'sans ombre', n2 == 9)] += 1
    if n2 == 9 and not shadow: good.append((z, C, O))
print(dict(st), flush=True)
out = []
for z, C, O in good[:40]:
    r20 = []
    for seed in range(3):
        random.seed(seed); seq = [random.choice(C.cases()) for _ in range(20)]
        sup, gd, same, s = check_multi(C, seq, 200, engine2=(seed == 0)); r20.append((sup, gd, same))
    out.append(dict(r1=z['r1'], r2=z['r2'], O=O, usages20=r20, pieces=[(n, p, v) for n, p, v in C.pieces], out=[z['out0'], z['out1'], z['out2']]))
    print('fusion 1 constant', z['r1'], z['r2'], '→', O, r20, flush=True)
json.dump(out, open(os.path.join(HERE, 'fusion_fin.json'), 'w'))

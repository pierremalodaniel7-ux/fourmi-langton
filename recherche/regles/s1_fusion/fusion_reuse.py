#!/usr/bin/env python3
"""S1 / R-401 Fusions à 1 constant (fusion1_ok.json) : lesquelles sont RÉUTILISABLES ?
1) filtre « pas de route de face » (sortie d'un usage sur l'axe d'une entrée, sens opposé, ≤ 6 voies) ;
2) 2 usages (k = 200 périodes) : les 9 suites (x, y) ∈ {00, 10, 01}², superposition exacte + sortie juste ;
3) 20 usages au hasard dans UNE simulation (2 moteurs) ; 4) certificat « tout nombre d'usages » (circuit.certificat).
Usage : python3 s1_fusion/fusion_reuse.py [nb max pour le certificat]"""
import sys, os, json, random, itertools, collections, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from fa_lib import decode, back, lotdump, sit
from circuit import Circuit, check_multi, check_cases, certificat
BK = 60
class Excl(Circuit):
    """circuit dont les entrées sont exclusives (au plus une à 1)"""
    def cases(self):
        out = [dict((v, 0) for v in self.vars)]
        for v in self.vars: out.append(dict((w, int(w == v)) for w in self.vars))
        return out
def route(p):
    s = decode([tuple(p[0])], [tuple(c) for c in p[1]]); return tuple(s[0][:2])
def front(s, e): return (s[0] - e[0]) % 6 == 3 and abs(s[1] + e[1]) <= 6
def make(z, K):
    s1 = back((tuple(z['s1'][0]), [tuple(c) for c in z['s1'][1]]), BK)
    s2 = back((tuple(z['s2'][0]), [tuple(c) for c in z['s2'][1]]), BK)
    Kb = back(K, BK)
    P1 = ('s1', s1, 'x'); P2 = ('s2', s2, 'y'); PK = ('K', Kb, None)
    o = (z['o1'], z['o2'])
    pieces = {(0, 0): [P1, P2, PK], (1, 1): [PK, P1, P2], (0, 1): [P1, PK, P2], (1, 0): [P2, PK, P1]}[o]
    return pieces
if __name__ == '__main__':
    NC = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    D = json.load(open(os.path.join(HERE, 'fusion1.json'))); K = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
    ok = json.load(open(os.path.join(HERE, 'fusion1_ok.json')))
    t0 = time.time(); keep = []
    for z in ok:
        ins = [tuple(z['r1']), tuple(z['r2']), route(K)]
        outs = {tuple(o[:2]) for q in (0, 1, 2) for o in z['out%d' % q]}
        if any(front(s, e) for s in outs for e in ins): continue
        keep.append(z)
    print('sans route de face :', len(keep), '/', len(ok), flush=True)
    # sorties lues au temps 4000 (pièces reculées de BK périodes)
    C0 = [Excl(make(z, K)) for z in keep]
    L = []
    for C in C0: L += [C.sit(e) for e in C.cases()]
    R = lotdump(L, 4000)
    good = []
    for n, (z, C) in enumerate(zip(keep, C0)):
        d = [decode(*R[3 * n + q]) for q in range(3)]
        if None in d: continue
        com = (set(map(tuple, d[1])) & set(map(tuple, d[2]))) - set(map(tuple, d[0]))
        if len(com) != 1: continue
        O = sorted(com)[0]
        C.outputs = {'O': (lambda e: e['x'] | e['y'], [O])}
        good.append((z, C, O))
    print('3 cas justes (T = 4000) :', len(good), flush=True)
    two = []
    for z, C, O in good:
        n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
        if n2 == 9: two.append((z, C, O))
    print('2 usages 9/9 (superposition exacte) :', len(two), ' temps', round(time.time() - t0), 's', flush=True)
    cnt = collections.Counter((z['r1'][0], z['r2'][0], O[0]) for z, C, O in two)
    print('(dir s1, dir s2, dir O) :', cnt.most_common())
    json.dump([dict(z, O4000=O, pieces=[(n, p, v) for n, p, v in C.pieces]) for z, C, O in two], open(os.path.join(HERE, 'fusion_reuse2.json'), 'w'))
    # 20 usages + certificat pour les NC premières (une par type (dir s1, dir s2, dir O) d'abord)
    order = []; seen = set()
    for t in two:
        k = (t[0]['r1'][0], t[0]['r2'][0], t[2][0])
        if k not in seen: seen.add(k); order.append(t)
    order += [t for t in two if t not in order]
    out = []
    for z, C, O in order[:NC]:
        r20 = []
        for seed in range(3):
            random.seed(seed); seq = [random.choice(C.cases()) for _ in range(20)]
            sup, gd, same, s = check_multi(C, seq, 200, engine2=(seed == 0))
            r20.append((sup, gd, same))
        worst, per, fronts = certificat(C, 200, 4000, J=8, log=lambda *a: None)
        rec = dict(r1=z['r1'], r2=z['r2'], O=O, usages20=r20, cert_min=worst, cert=per, fronts=fronts,
                   pieces=[(n, p, v) for n, p, v in C.pieces])
        out.append(rec)
        print('fusion', z['r1'], z['r2'], '→', O, ': 20 usages', r20, ' certificat min', worst, per[:4], 'face', len(fronts), flush=True)
        json.dump(out, open(os.path.join(HERE, 'fusion_reuse_cert.json'), 'w'))

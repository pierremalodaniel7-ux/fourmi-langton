#!/usr/bin/env python3
"""R-313 Miroirs-oscillateurs : un cycle exact à 2 fourmis (objet fixe) posé sur la voie de B (décalages [-W,W]²).
Issues : B déviée proprement ? l'oscillateur reste-t-il borné ? Puis RÉUTILISATION : 2e autoroute A sur la même voie,
m périodes devant (A touche d'abord) : B ressort-elle sur la même direction ET la même voie que A ?
Usage : python3 osc_miroir.py REGLE [W] [nb_osc]"""
import sys, json, collections
from banc import launcher, sit, path, outcome, K, TB
from outils_r import lot, parse, geo
G = json.load(open('data/germes_regles.json'))
rule = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 3; NO = int(sys.argv[3]) if len(sys.argv) > 3 else 40
g = G[rule]; P, D = g['P'], tuple(g['D']); _, M = geo(rule)
ant, cells = launcher(g); t2 = K * P
X = path(rule, [ant], cells, t2, t2)[0][:2]
sol = outcome(rule, lot([sit(rule, [ant], cells)], TB)[0], 0, P, D)
# oscillateurs : cycles à 2 fourmis (cycles2.py), un exemple par (période, forme) jusqu'à NO
cand = []
for d0 in range(M):
    for x in range(-2, 3):
        for y in range(-2, 3):
            if (x, y) == (0, 0): continue
            for d1 in range(M):
                cand.append(f"{rule}|0,0,{d0};{x},{y},{d1}|")
                for cx in range(-1, 2):
                    for cy in range(-1, 2): cand.append(f"{rule}|0,0,{d0};{x},{y},{d1}|{cx},{cy}")
osc = []; seen = set()
for s, l in zip(cand, lot(cand, 1 << 14)):
    d = parse(l)
    if d['issue'] == 'CYCLE' and int(d['sig'][1:]) <= 60:
        key = (d['sig'], d['boite'])
        if key in seen: continue
        seen.add(key); osc.append((d['sig'], s))
osc = osc[:NO]
print(rule, 'oscillateurs distincts (période, boîte) :', len(osc), [o[0] for o in osc])
def place(s, at):
    r, a, c = s.split('|')
    ants = [tuple(map(int, t.split(','))) for t in a.split(';') if t]
    cs = {}
    for t in c.split(';'):
        if t: x, y = map(int, t.split(',')[:2]); cs[(x + at[0], y + at[1])] = 1
    return [(x + at[0], y + at[1], d) for x, y, d in ants], cs
confs = []
for k, (sig, s) in enumerate(osc):
    for i in range(-W, W + 1):
        for j in range(-W, W + 1):
            oa, oc = place(s, (X[0] + i, X[1] + j))
            c = dict(cells); c.update(oc)
            confs.append((k, i, j, oa, oc, sit(rule, [ant] + oa, c)))
res = lot([c[5] for c in confs], 1 << 18)
st = collections.Counter(); good = []
for c, l in zip(confs, res):
    d = parse(l); ob = outcome(rule, l, 0, P, D)
    bounded = all(a is None for a in d['ants'][1:]) and d['issue'] != 'CYCLE'
    k = ('B ' + ob[0], 'dir' + str(ob[1]) if ob[0] == 'propre' else '', 'osc borné' if bounded else 'osc parti')
    if ob[0] == 'propre' and ob[1] == 0 and ob[2] == sol[2]: k = ('B transparent', '', k[2])
    st[k] += 1
    if ob[0] == 'propre' and not (ob[1] == 0 and ob[2] == sol[2]) and bounded: good.append((c, ob))
print('  issues :', dict(st.most_common()))
# réutilisation : A devant de m périodes sur la même voie
MS = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [10, 30]
for m in MS:
    a2, c2 = launcher(g, 0, (m * D[0], m * D[1]))
    L = []
    for (k, i, j, oa, oc, _), ob in good:
        oa2 = [(x + m * D[0], y + m * D[1], dd) for x, y, dd in oa]; oc2 = {(x + m * D[0], y + m * D[1]): v for (x, y), v in oc.items()}
        c = dict(cells); c.update(c2); c.update(oc2)
        L.append(sit(rule, [ant, a2] + oa2, c))
    R = lot(L, max(1 << 19, 2 * m * P + (1 << 18))) if L else []
    same = 0; ex = []; dirs = collections.Counter()
    for l, ((k, i, j, oa, oc, s0), ob1) in zip(R, good):
        d = parse(l); ob, oa_ = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, D)
        bounded = all(a is None for a in d['ants'][2:])
        if ob[0] == 'propre' and oa_[0] == 'propre' and ob[1] == oa_[1] and ob[2] == oa_[2] and bounded:
            same += 1; dirs[ob[1]] += 1
            if len(ex) < 6: ex.append(s0)
    print(f"  m={m} : miroirs propres {len(good)}, 2e autoroute identique (même direction, même voie, oscillateur toujours borné) : {same}  directions {dict(dirs)}")
    json.dump({'regle': rule, 'm': m, 'n': len(confs), 'propres': len(good), 'reutilisables': same, 'dirs': {str(k): v for k, v in dirs.items()}, 'exemples': ex},
              open(f"data/oscmiroir_{rule.replace(':', '_')}_m{m}.json", 'w'))

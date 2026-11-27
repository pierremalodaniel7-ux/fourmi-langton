#!/usr/bin/env python3
"""R-616 (suite) h1' réutilisable : descente sur conflits exacts + 5 × couples (sortie logiquement possible, vaisseau entrant) de
directions opposées à < 7 voies (critère (c) du certificat, calculé sur les segments infinis de diag2 avec leurs masques de cas).
Si 0 couple et ≤ 8 conflits : simulation 256 cas ; si juste : certificat rapide (cert2). Usage : python3 opt10.py graine secondes départ.json"""
import sys, json, random, time
from modules import nodes
from htree import build, h1_tree2
from nor import Layout
from diag2 import conflicts2, segments2, INF
from s3lib import antpos
from reuse import lane_of
from cert2 import certificate2
seed, secs = int(sys.argv[1]), float(sys.argv[2]); p = json.load(open(sys.argv[3])); Dm, Gm = p['D'], p['G']
root = build(h1_tree2()); names = [n.name for n in nodes(root)]; rnd = random.Random(seed)
def opp(L):
    outs = {s[1] for s in segments2(L) if s[3] == INF}; ins = [w for _, _, w in L.ships]; n = 0
    for o in outs:
        lo = [lane_of(antpos(o, t), o[0]) for t in range(8)]
        for i in ins:
            if (o[0] - i[0]) % 6 == 3:
                li = [lane_of(antpos(i, t), o[0]) for t in range(8)]
                if min(abs(x - y) for x in lo for y in li) < 7: n += 1
    return n
def evaluate(Dm, Gm):
    L = Layout(root, Dmap=Dm, Gmap=Gm); c = len(conflicts2(L)); o = opp(L); return c + 5 * o, c, o
s, c, o = evaluate(Dm, Gm); t0 = time.time(); it = 0; tested = set()
log = open(f'data/opt10_{seed}.log', 'a'); print('départ', s, c, o, file=log, flush=True)
while time.time() - t0 < secs:
    it += 1; D2, G2 = dict(Dm), dict(Gm)
    for _ in range(rnd.choice((1, 1, 2, 3))):
        n = rnd.choice(names); big = rnd.random() < 0.3
        if rnd.random() < 0.6: D2[n] = max(8, min(300, D2[n] + (rnd.randint(-60, 60) if big else rnd.randint(-8, 8))))
        else: G2[n] = max(8, min(60, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
    s2, c2, o2 = evaluate(D2, G2)
    if s2 <= s:
        if s2 < s: print(f'{it} {time.time()-t0:.0f}s score {s2} (conflits {c2}, opposés {o2})', file=log, flush=True)
        Dm, Gm, s, c, o = D2, G2, s2, c2, o2
        json.dump(dict(D=Dm, G=Gm, htree=2, a=0, conflits=c, opposes=o), open(f'data/opt10_{seed}.json', 'w'))
        key = json.dumps([Dm, Gm], sort_keys=True)
        if o == 0 and c <= 8 and key not in tested:
            tested.add(key); L = Layout(root, Dmap=Dm, Gmap=Gm); r = L.check()
            bad = sum(1 for x in r if x[2] != x[3]); dirty = sum(1 for x in r if not x[1])
            print(f'   simulation : {bad} faux, {dirty} sales / {len(r)}', file=log, flush=True)
            if bad == 0 and dirty == 0:
                json.dump(dict(D=Dm, G=Gm, htree=2, a=0), open(f'data/opt10_JUSTE_{seed}_{it}.json', 'w'))
                try: okc, delta, info = certificate2(L, log=lambda x: print('   ' + x, file=log, flush=True))
                except AssertionError as ex: okc = False; print('   certificat : échec', str(ex)[:200], file=log, flush=True)
                if okc: json.dump(dict(D=Dm, G=Gm, htree=2, a=0, delta=delta), open(f'data/opt10_OK_{seed}.json', 'w')); break
print('fin', it, s, file=log, flush=True)

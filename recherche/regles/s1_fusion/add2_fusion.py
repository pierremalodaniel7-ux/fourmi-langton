#!/usr/bin/env python3
"""S1 / R-405 Additionneur 2 bits RÉUTILISABLE : étage 0 = demi-additionneur R-337 (a0, b0) → s0, c0 ;
c0 passe par un « relais » = fusion propre à 2 constants (fusion2_1.json) dont UNE seule entrée est branchée (l'autre absente) :
le relais tourne c0 vers une autre route O' ; puis l'additionneur complet R-349 (a1, b1, c) est posé pour que sa pièce c suive
EXACTEMENT O' (compose.attach) et glissé de D2 périodes le long de O'. But : éloigner le constant K2 de R-349 (parallèle à c) de la
porte de l'étage 0 (cause de l'échec R-350).
Étapes : (1) HA0 + relais : 4 cas propres, O' présent ⟺ a0∧b0 ; (2) 16 cas propres et justes (s0, s1, c1 lus sur ≤ 3 positions) ;
(3) 2 usages (k = 200) sur 40 suites au hasard, superposition exacte. Écrit au fur et à mesure.
Usage : python3 s1_fusion/add2_fusion.py <début> <fin> [fichier de relais] (tranche d'indices de relais distincts)"""
import sys, os, json, random, itertools, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from compose import attach, slide, rotate
from circuit import Circuit, check_multi, check_cases
from fa_lib import decode, lotdump, sit
from fa_complet import cover
from lib1 import FA, HA
from fusion_reuse import route, front
T = 8000
c0 = (2, -28, 916, 0)
HA0 = Circuit([(n, p, {'a': 'a0', 'b': 'b0'}.get(v, v)) for n, p, v in HA().pieces])
FAc = FA()
# relais distincts
SRC = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'fusion2_1.json')
G = json.load(open(SRC))
seen = {}; RL = []
for z in G:
    k = (z.get('base'), tuple(decode([tuple(z['Kp'][0])], [tuple(c) for c in z['Kp'][1]])[0]), z['c'][5])
    if k in seen: continue
    seen[k] = 1; RL.append(z)
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
out_path = os.path.join(HERE, 'add2_fusion_%s_%d_%d.json' % (os.path.basename(SRC).split('.')[0], a0, a1))
found = []; stats = collections.Counter(); t0 = time.time()
INS0 = [route(p) for n, p, v in HA0.pieces]
for zi in range(a0, min(a1, len(RL))):
    z = RL[zi]
    dev = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in z['pieces']])
    for sin, other in (('s1', 's2'), ('s2', 's1')):
        P = dict((n, p) for n, p, v in dev.pieces)[sin]
        rin = decode([P[0]], P[1])[0][0]
        rho = (2 - rin) % 6
        base = Circuit([(n, p, v) for n, p, v in dev.pieces if n != other])
        for D1, ordre in itertools.product((0, 40, 120), (0, 1)):
            Dv = attach(base, sin, rho, c0, 4000)
            if Dv is None: stats['parité'] += 1; continue
            Dv = slide(Dv, sin, D1)
            dpcs = [(n + "'", p, None) for n, p, v in Dv.pieces if n != sin]
            pcs = HA0.pieces + dpcs if ordre == 0 else dpcs + HA0.pieces
            # ordre : HA0 d'abord, puis le relais (les pièces du relais gardent leur ordre relatif)
            C1 = Circuit(pcs)
            R = lotdump([C1.sit(e) for e in C1.cases()], T)
            O = {}
            ok = True
            for e, r in zip(C1.cases(), R):
                d = decode(*r)
                if d is None: ok = False; break
                O[(e['a0'], e['b0'])] = [tuple(x) for x in d]
            if not ok: stats['étage 0 + relais sale'] += 1; continue
            # sortie O' attendue : le relais COMPLET (2 entrées) transporté par la même transformation, cas x seul et y seul
            Df = slide(attach(dev, sin, rho, c0, 4000), sin, D1)
            Rd = lotdump([Df.sit(e) for e in ({'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1})], T)
            dd = [decode(*r) for r in Rd]
            if None in dd: stats['relais seul sale'] += 1; continue
            new = (set(map(tuple, dd[1])) & set(map(tuple, dd[2]))) - set(map(tuple, dd[0]))
            cps = [x for x in new if x in O[(1, 1)] and all(x not in O[k] for k in O if k != (1, 1))]
            if len(cps) != 1: stats['c0\' absent ou ambigu'] += 1; continue
            cp = cps[0]
            ins = [route(p) for n, p, v in pcs]
            if any(front(s[:2], e) for v_ in O.values() for s in v_ for e in ins): stats['route de face (étage 0)'] += 1; continue
            if cp[0] == 2 and abs(cp[1] - c0[1]) <= 8: stats['c0\' parallèle à c0 (essayé quand même)'] += 1
            rho2 = (cp[0] - 4) % 6
            for D2 in (0, 60, 200):
                F1 = attach(FAc, 'c', rho2, cp, T)
                if F1 is None: stats['parité2'] += 1; continue
                F1 = slide(F1, 'c', D2)
                pcs2 = pcs + [(n + '1', p, {'a': 'a1', 'b': 'b1'}.get(v, v)) for n, p, v in F1.pieces if n != 'c']
                C2 = Circuit(pcs2)
                cs = C2.cases(); R2 = lotdump([C2.sit(e) for e in cs], T)
                O2 = {}; ok = True
                for e, r in zip(cs, R2):
                    d = decode(*r)
                    if d is None: ok = False; break
                    O2[(e['a0'], e['b0'], e['a1'], e['b1'])] = [tuple(x) for x in d]
                if not ok: stats['16 cas : sale'] += 1; continue
                f_s0 = lambda k: k[0] ^ k[1]
                f_s1 = lambda k: (k[2] + k[3] + (k[0] & k[1])) % 2
                f_c1 = lambda k: int(k[2] + k[3] + (k[0] & k[1]) >= 2)
                P0, P1, P2 = cover(O2, f_s0), cover(O2, f_s1), cover(O2, f_c1)
                if any(x in (None, 'grand') for x in (P0, P1, P2)): stats['16 cas : sorties illisibles'] += 1; continue
                ins2 = [route(p) for n, p, v in pcs2]
                if any(front(s[:2], e) for v_ in O2.values() for s in v_ for e in ins2): stats['16 cas : route de face'] += 1; continue
                C2.outputs = {'s0': (lambda e: e['a0'] ^ e['b0'], P0),
                              's1': (lambda e: (e['a1'] + e['b1'] + (e['a0'] & e['b0'])) % 2, P1),
                              'c1': (lambda e: int(e['a1'] + e['b1'] + (e['a0'] & e['b0']) >= 2), P2)}
                # 2 usages : 40 suites au hasard
                random.seed(zi); nb = 0
                for _ in range(40):
                    e1, e2 = random.choice(cs), random.choice(cs)
                    sup, good, same, s = check_multi(C2, [e1, e2], 200, T0=T)
                    nb += sup and good == 2
                if nb < 40: stats['2 usages < 40/40'] += 1; continue
                stats['OK'] += 1
                rec = dict(relais=zi, sin=sin, D1=D1, ordre=ordre, D2=D2, c0p=cp, S0=P0, S1=P1, C1=P2, pieces=[(n, p, v) for n, p, v in C2.pieces])
                found.append(rec); json.dump(found, open(out_path, 'w'))
                print('ADDITIONNEUR 2 BITS 16/16, 2 usages 40/40 :', zi, sin, D1, ordre, D2, 'c0\'', cp, flush=True)
    if zi % 10 == 0:
        print(f'relais {zi} : {dict(stats)} {round(time.time() - t0)} s', flush=True)
json.dump(found, open(out_path, 'w'))
print('fin', a0, a1, dict(stats), round(time.time() - t0), 's')

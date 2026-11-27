"""S2 R-505 — généralisation de compteur2 : chaînes alternées a, b, a, b, … (routes fixées) de conversions EXACTES, jusqu'à 2K
conversions ; on cherche le premier retour à l'orbite de X0 (même place) après 2k conversions (k tours) et on note si les états
intermédiaires (après chaque tour) sont distincts. k = 2 : bit qui bascule à chaque tour ; k = 4 : compteur modulo 4.
Usage : python3 s2_horloge/compteur3.py K"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from compteur2 import tir, exacts, orbit_set, canon
K = int(sys.argv[1])
osc = [l.split('| ', 1)[1].strip() for l in open('data/osc2.txt')]
E1 = exacts(tir(osc))
paths = [[e] for e in E1]          # chemin = liste de conversions ; routes : a = e1 route, b = e2 route
memo = {}
def conv_from(objs):
    need = [o for o in objs if o not in memo]
    if need:
        L = exacts(tir(need))
        for o in need: memo[o] = []
        for e in L: memo[e[0]].append(e)
    return memo
orbs = {}; found = collections.Counter(); win = []
for step_ in range(2, 2 * K + 1):
    objs = sorted({p[-1][1] for p in paths}); conv_from(objs)
    new = []
    for p in paths:
        for e in memo[p[-1][1]]:
            if step_ == 2:
                if e[2][0] != (p[0][2][0] + 3) % 6: continue
            else:
                if e[2] != p[step_ % 2 == 0 and 1 or 0][2] if False else e[2] != (p[1][2] if step_ % 2 == 0 else p[0][2]): continue
            new.append(p + [e])
    paths = new
    if step_ % 2 == 0:
        keep = []
        for p in paths:
            X0 = p[0][0]
            if X0 not in orbs: orbs[X0] = orbit_set(X0, int(p[0][3]['p']))
            if canon(p[-1][1]) in orbs[X0]:
                states = [canon(p[i][1]) for i in range(1, len(p), 2)]
                inter = [p[i][1] for i in range(1, len(p) - 1, 2)]
                distinct = all(canon(x) not in orbs[X0] for x in inter)
                found[(step_ // 2, distinct)] += 1
                if distinct and step_ // 2 >= 2: win.append([(e[0], e[1], e[2], e[3]) for e in p])
            else: keep.append(p)
        paths = keep
    print('conversions', step_, ': chemins ouverts', len(paths), ' retours (tours, états intermédiaires ≠ X0) :', dict(found), flush=True)
    if len(paths) > 200000: print('trop de chemins, arrêt'); break
json.dump(win, open('s2_horloge/compteur3_K%d.json' % K, 'w'))
print('cycles à ≥ 2 tours :', len(win))

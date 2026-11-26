#!/usr/bin/env python3
"""R-340 Bascule R2L2 à UN vaisseau : un vaisseau s1 change l'oscillateur R en R' (et ressort), un vaisseau s2 remet R' en R, AU MÊME ENDROIT.
Étape 1 : miroir2 tir (CONV=1) sur les oscillateurs → conversions R → R' (R' = « restant », coordonnées absolues).
Étape 2 : miroir2 tir sur chaque R' distinct → conversions R' → R'' ; on garde celles où R'' est EXACTEMENT une phase de R (même place).
Usage : python3 bascule_hexa.py data/osc2.txt"""
import sys, subprocess, json, collections
from hx import step
src = sys.argv[1]
def tir(lines):
    out = subprocess.run(['./miroir2', 'tir', '40', '0'], input='\n'.join(lines) + '\n', capture_output=True, text=True, env={'CONV': '1'}).stdout
    return [l for l in out.splitlines() if l.startswith(('CONV', 'MIRT', 'DECT'))]
def parse_sit(s):
    s = s.strip(); rule, a, c = s.split('|')[:3]
    return [tuple(map(int, t.split(','))) for t in a.split(';') if t], frozenset(tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t)
def orbit(ants, cells):
    A = [list(a) for a in ants]; g = {c: 1 for c in cells}; S = set(); A0 = [list(a) for a in ants]; g0 = dict(g)
    for t in range(5000):
        S.add((frozenset(map(tuple, A)), frozenset(g)))
        step(A, g)
        if A == A0 and g == g0: return S
    return S
osc = [l.split('| ', 1)[1].strip() for l in open(src) if l.startswith('OSC')]
L1 = tir(['OSC 0 0 | ' + o for o in osc])
print('conversions R → R\' :', len(L1)); sys.stdout.flush()
# R' distincts
by_R2 = collections.defaultdict(list)
for l in L1:
    R = l.split(' | ')[1].strip(); R2 = l.split('restant ')[1].strip()
    by_R2[R2].append((R, l.split(' | ')[0]))
print('R\' distincts :', len(by_R2)); sys.stdout.flush()
R2s = list(by_R2)
L2 = []
for i in range(0, len(R2s), 200): L2 += tir(['OSC 0 0 | ' + r for r in R2s[i:i + 200]])
orbs = {}
found = []
for l in L2:
    R2 = l.split(' | ')[1].strip(); R3 = l.split('restant ')[1].strip()
    a3, c3 = parse_sit(R3); key3 = (frozenset(a3), c3)
    for R, info1 in by_R2[R2]:
        if R not in orbs: orbs[R] = orbit(*parse_sit(R))
        if key3 in orbs[R]: found.append({'R': R, 's1': info1, 'R2': R2, 's2': l.split(' | ')[0]})
print('bascules R → R\' → R trouvées :', len(found))
for f in found[:10]: print(' ', f['R'], '|', f['s1'], '||', f['s2'])
json.dump(found, open('data/bascules_' + src.split('/')[-1].replace('.txt', '') + '.json', 'w'))

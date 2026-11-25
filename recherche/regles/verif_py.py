#!/usr/bin/env python3
"""2e moteur (Python pur, indépendant de fourmi_r) : rejoue une situation (carré, hexa « H: »), T tours, et donne pour chaque fourmi
son déplacement sur les P derniers tours. Usage : python3 verif_py.py fichier.json|situation T P"""
import sys, json, re
SQ = [(0,-1),(1,0),(0,1),(-1,0)]; HX = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
def sim(s, T, P):
    rule, a, c = s.split('|')
    if rule.startswith('H:'):
        tk = {'N':0,'R1':1,'R2':2,'U':3,'L2':4,'L1':5}; K = [tk[t] for t in re.findall(r'R1|R2|L1|L2|N|U', rule[2:])]; Dd = HX; M = 6
    else: K = [{'L':3,'R':1,'N':0,'U':2}[ch] for ch in rule]; Dd = SQ; M = 4
    q = len(K); g = {}
    for t in c.split(';'):
        if t: v = list(map(int, t.split(','))); g[(v[0], v[1])] = (v[2] if len(v) > 2 else 1) % q
    ants = [list(map(int, t.split(','))) for t in a.split(';') if t]
    hist = []
    for t in range(T):
        for an in ants:
            k = g.get((an[0], an[1]), 0); an[2] = (an[2] + K[k]) % M; g[(an[0], an[1])] = (k + 1) % q
            an[0] += Dd[an[2]][0]; an[1] += Dd[an[2]][1]
        if t >= T - P - 1: hist.append([(x, y) for x, y, _ in ants])
    return [(hist[-1][i][0] - hist[0][i][0], hist[-1][i][1] - hist[0][i][1]) for i in range(len(ants))], [tuple(p) for p in hist[-1]]
if __name__ == '__main__':
    s = sys.argv[1]
    if s.endswith('.json'): s = json.load(open(s))['situation']
    d, pos = sim(s, int(sys.argv[2]), int(sys.argv[3]))
    print(' '.join(f"{x},{y}" for x, y in d))

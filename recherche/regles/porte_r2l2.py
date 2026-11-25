#!/usr/bin/env python3
"""R-314 Porte d'interaction R2L2 (choc (60°, −120°, +120°) de R-310) : table de vérité 4/4 + cases laissées dans la zone du choc.
Puis RÉUTILISATION de la zone : on rejoue le même choc 2 fois de suite au même endroit (2e paire lancée 40 périodes derrière)."""
import subprocess, json
from outils_r import parse
R = 'H:R2L2'
def run(ants, cells, T=4000, dump=True):
    s = f"{R}|" + ';'.join(ants) + '|' + ';'.join(cells)
    out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input=s + '\n', capture_output=True, text=True).stdout.splitlines()
    d = parse([l for l in out if not l.startswith('DUMP')][0])
    dc = [l for l in out if l.startswith('DUMP')][0].split('|')[2]
    cs = [tuple(map(int, c.split(',')[:2])) for c in dc.split(';') if c]
    return s, d, cs
B = (['0,0,4'], ['1,0'])                 # vaisseau B (part vers (1,-1))
A = (['-1,-34,5'], ['-1,-33'])           # vaisseau A (tourné de 60°)
X = (30, -30)
res = {}
for a in (0, 1):
    for b in (0, 1):
        ants = (A[0] if a else []) + (B[0] if b else []); cells = (A[1] if a else []) + (B[1] if b else [])
        if not ants: res[(a, b)] = 'rien'; continue
        s, d, cs = run(ants, cells)
        zone = [c for c in cs if abs(c[0] - X[0]) + abs(c[1] - X[1]) < 60]
        outs = [f"{x[1]},{x[2]}" if x else '?' for x in d['ants']]
        res[(a, b)] = f"{d['sig']} directions {outs} fin {d['fin']} cases dans la zone du choc : {len(zone)}"
        print(f"a={a} b={b} : {res[(a, b)]}")
# réutilisation : 2 chocs successifs au même endroit
k = 40
B2 = ([f"{-k},{k},4"], [f"{1-k},{k}"]); A2 = ([f"{-1-k},{-34+k},5"], [f"{-1-k},{-33+k}"])
s, d, cs = run(A[0] + B[0] + A2[0] + B2[0], A[1] + B[1] + A2[1] + B2[1], 8000)
print('2 chocs successifs :', d['sig'], [f"{x[1]},{x[2]}" if x else '?' for x in d['ants']], d['fin'])
json.dump({str(k): v for k, v in res.items()} | {'deux_chocs': s, 'sortie': d['sig']}, open('data/porte_r2l2.json', 'w'))

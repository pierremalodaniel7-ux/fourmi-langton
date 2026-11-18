#!/usr/bin/env python3
"""t1relatif.py "BASE" CAP [K2] : « BASE + une case noire n'importe où » complet (T1 relatif, cf. T5/R-90, R-93).
BASE : cases (y vers le bas) d'une configuration DÉJÀ pivotée pour que son autoroute ait la dérive (-2,+2) ; CAP = cap initial.
1) certificat T0 de la base ; 2) boîte d'activité avant T0+104 ; 3) (C) classes lointaines + preuves (relatif.py) ;
4) (A) zone proche (boîte + bande jusqu'à K2) calculée avec fourmi -cert ; 5) bilan. (B) : argument direct (certifié à T0)."""
import sys, re, subprocess, os
here = os.path.dirname(os.path.abspath(__file__)); F = here + '/../../../src/fourmi'
B, CAP = sys.argv[1], sys.argv[2]; K2 = int(sys.argv[3]) if len(sys.argv) > 3 else 400
o = subprocess.run([F, '-T', '400000000', '-cert', f'RL|0,0,{CAP}|{B}'], capture_output=True, text=True).stdout
m = re.search(r'CERT (\d+) .* 104,(-?\d+),(-?\d+),', o); T0 = int(m.group(1)); assert (m.group(2), m.group(3)) == ('-2', '2'), o
cells = {tuple(map(int, c.split(','))) for c in B.split(';')}
g = set(cells); x = y = 0; d = 'HDBG'.index(CAP); dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]; X = [0, 0]; Y = [0, 0]
for s in range(T0 + 104):
    X = [min(X[0], x), max(X[1], x)]; Y = [min(Y[0], y), max(Y[1], y)]
    c = (x, y) in g; d = (d + (3 if c else 1)) % 4; g ^= {(x, y)}; x += dx[d]; y += dy[d]
for (a, b) in cells: X = [min(X[0], a), max(X[1], a)]; Y = [min(Y[0], b), max(Y[1], b)]
print(f'# base T0={T0} activité x{X} y{Y}', flush=True)
r = subprocess.run(['python3', here + '/relatif.py', B, str(T0), str(K2), CAP], capture_output=True, text=True)
ok = r.stdout.count('\nOK') + r.stdout.startswith('OK'); ko = r.stdout.count('ECHEC')
js = re.search(r'diagonales touchées \[(-?\d+), .*?\[.*?(-?\d+)\] \d+', r.stderr); j0, j1 = int(js.group(1)), int(js.group(2))
print(f'# (C) {r.stderr.strip().splitlines()[-1]} ; bande x+y in [{j0},{j1}]', flush=True)
lines = []
for yy in range(Y[0] - 3, K2):
    for xx in range(min(X[0] - 3, j0 - 2 - yy), max(X[1] + 3, j1 + 2 - yy) + 1):
        if (X[0] - 3 <= xx <= X[1] + 3 and Y[0] - 3 <= yy <= Y[1] + 3) or (j0 - 2 <= xx + yy <= j1 + 2):
            lines.append(f'RL|0,0,{CAP}|{B};{xx},{yy}\n')
out = subprocess.run([F, '-T', '400000000', '-cert', '-lot'], input=''.join(lines), capture_output=True, text=True).stdout
n = out.count('|CERT '); certs = [int(v) for v in re.findall(r'\|CERT (\d+)', out)]
print(f'# (A) {n}/{len(lines)} certifiées ; max {max(certs) if certs else "-"}', flush=True)
print('# BILAN :', 'DEMONTRE (sous réserve de relecture)' if n == len(lines) and ko == 0 else 'INCOMPLET')

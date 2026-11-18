#!/usr/bin/env python3
"""pingpong.py PROFONDEUR : chaîne de demi-tours aussi COURTE que possible (É7). À chaque étape, parmi les cases de la bande de
l'autoroute finale courante (repérée sur 2 périodes à partir du certificat), on cherche la plus PROCHE de la position de la fourmi
au certificat (distance le long de la dérive) qui provoque un demi-tour : l'autoroute finale part dans la direction opposée.
Sortie : étape, case ajoutée, distance à la fourmi au moment du certificat, pas certifié, direction."""
import sys, re, subprocess, os
F = os.path.dirname(os.path.abspath(__file__)) + '/../../../src/fourmi'
def lot(confs):
    inp = ''.join('RL|0,0,H|' + ';'.join(f'{x},{y}' for x, y in c) + '\n' for c in confs)
    out = []
    for l in subprocess.run([F, '-T', '400000000', '-cert', '-lot'], input=inp, capture_output=True, text=True).stdout.splitlines():
        m = re.search(r'\|CERT (\d+) .* 104,(-?\d+),(-?\d+),', l)
        out.append((int(m.group(1)), (int(m.group(2)), int(m.group(3)))) if m else None)
    return out
def posT(cells, T):   # position de la fourmi au pas T (simulation directe)
    g = set(cells); x = y = d = 0; DX = [0, 1, 0, -1]; DY = [-1, 0, 1, 0]
    for _ in range(T):
        c = (x, y) in g; d = (d + (3 if c else 1)) % 4; g ^= {(x, y)}; x += DX[d]; y += DY[d]
    return x, y
cells = []; prof = int(sys.argv[1])
r = lot([cells])[0]
for e in range(1, prof + 1):
    T, (dx, dy) = r; ax, ay = posT(cells, T); ux, uy = dx // 2, dy // 2
    found = None
    for k in range(1, 400):                          # k demi-périodes devant la fourmi
        cand = [cells + [(ax + ux * k + j * uy, ay + uy * k - j * ux)] for j in range(-12, 13)]
        res = lot(cand)
        for c, rr in zip(cand, res):
            if rr and rr[1] == (-dx, -dy):             # demi-tour : direction finale opposée
                found = (k, c[-1], rr); break
        if found: break
    if not found: print('étape', e, ': aucun demi-tour trouvé à moins de 400 demi-périodes', flush=True); break
    k, cell, r = found; cells.append(cell)
    print(f'étape {e} : case {cell} à {k} demi-périodes devant la fourmi (pas {T}, fourmi en ({ax},{ay})) ; certifié {r[0]}, direction {r[1]} ; boîte des cases {max(max(abs(a),abs(b)) for a,b in cells)}', flush=True)

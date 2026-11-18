#!/usr/bin/env python3
"""Chaîne de demi-tours : à chaque étape, ajoute une case noire dans la classe « demi-tour » de l'autoroute finale
courante (classe où le pas certifié croît de 104 par unité d'éloignement au lieu de 52), à distance K.
Usage : chaine_demitours.py PROFONDEUR K"""
import subprocess, re, sys, os
F = os.path.join(os.path.dirname(__file__), '../../../src/fourmi')
def run(cells):
    s = 'RL|0,0,H|' + ';'.join(f'{x},{y}' for x, y in cells)
    o = subprocess.run([F, '-T', '60000000', '-cert', s], capture_output=True, text=True).stdout
    m = re.search(r'\|(\d+)\|CERT (\d+) .* 104,(-?\d+),(-?\d+),\d+ boite \S+ fin (-?\d+),(-?\d+)', o)
    return tuple(map(int, m.groups())) if m else None
def lot(confs):
    inp = ''.join('RL|0,0,H|' + ';'.join(f'{x},{y}' for x, y in c) + '\n' for c in confs)
    o = subprocess.run([F, '-T', '60000000', '-cert', '-lot'], input=inp, capture_output=True, text=True).stdout
    res = []
    for l in o.splitlines():
        m = re.search(r'CERT (\d+) .* 104,(-?\d+),(-?\d+),', l); res.append((int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None)
    return res
depth, K = int(sys.argv[1]), int(sys.argv[2]); cells = []
r = run(cells); print('etape 0', r, flush=True)
for e in range(1, depth + 1):
    t, c, dx, dy, fx, fy = r; ux, uy = dx // 2, dy // 2
    cand = [(j, k) for j in range(-30, 31) for k in (K, K + 1)]
    A = lot([cells + [(fx + ux * k + j, fy + uy * k)] for j, k in cand])
    B = lot([cells + [(fx + ux * (k + 2) + j, fy + uy * (k + 2))] for j, k in cand])
    ut = [(j, k) for (j, k), a, b in zip(cand, A, B) if a and b and b[0] - a[0] == 208]
    if not ut: print('etape', e, 'pas de classe demi-tour trouvée', flush=True); break
    j, k = ut[0]; cells.append((fx + ux * k + j, fy + uy * k)); r = run(cells)
    print('etape', e, 'classes demi-tour', ut, '-> cases', cells, 'resultat', r, flush=True)
    if not r: print('NON CERTIFIÉ'); break

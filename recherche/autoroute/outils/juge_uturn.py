#!/usr/bin/env python3
"""juge_uturn.py FICHIER.cert < sortie de ./ant uturn (une ligne '<commande> :: <sortie>') :
verdict par classe : U2 (position -d, même cap, fenêtre recopiée), U1, U3, U4' (lectures neuves après s+104 :
p < L, ou dans W, ou hors des diagonales Δ), Z selon la direction finale d' (lue dans le .cert) :
d' = +d (-2,+2) -> fenêtre finale hors Δ ; sinon -> max p de la fenêtre < L."""
import re, sys
dirs = {}
for l in open(sys.argv[1]):
    f = l.split('|'); cs = [tuple(map(int, c.split(','))) for c in f[2].split(';')]
    x0, y0 = cs[0]; off = ' '.join(f'{x-x0} {y-y0}' for x, y in cs[1:])
    dirs[(x0 + y0, y0, off)] = re.search(r' 104,(-?\d+),(-?\d+),', l).groups()
ok = ko = 0
for l in sys.stdin:
    cmd, res = l.split(' :: ')
    a = cmd.split(); J, K, off = int(a[1]), int(a[2]), ' '.join(a[5:])
    d = dirs[(J, K, off)]
    u2 = re.search(r'a\(s\+P\)-a\(s\)=\(2,2\) cap (\d)->\1, .*recopiee : OK', res) is not None
    u = all(f'({x} OK)' in res for x in ('U1', 'U3')) and '(U4 OK' in res
    if d == ('-2', '2'): z = 'fenetre finale hors Δ : OUI' in res
    else: z = '(Z OK)' in res
    v = u2 and u and z; ok += v; ko += (not v)
    if not v: print('ECHEC', cmd, 'dir', d, 'U2', u2, 'U134', u, 'Z', z)
print('# uturn OK', ok, 'ECHEC', ko)

# dirs.py — regroupe les autoroutes (lignes E| de hw) par DIRECTION.
# Carré : on tourne (dx,dy) d'un quart de tour jusqu'à dx>0, dy>=0 ; pente a = dy/dx (fraction exacte ; y vers le bas).
# Hexagonal (coordonnées axiales q,r ; écran x = q + r/2, y = r·√3/2) : on tourne de 60° jusqu'à q>0, r>=0 ;
#   pente a = √3·r/(2q+r).
# Usage : python3 dirs.py fichiers...   -> écrit dirs.json (une entrée par (grille, direction), meilleurs exemples)
import sys, json, math
from fractions import Fraction
def canon4(dx, dy):
    for _ in range(4):
        if (dx > 0 and dy >= 0): return dx, dy
        dx, dy = -dy, dx
    return dx, dy
def canon6(a, b):
    for _ in range(6):
        if a > 0 and b >= 0: return a, b
        a, b = -b, a + b
    return a, b
D = {}
for fn in sys.argv[1:]:
    for L in open(fn):
        p = L.rstrip('\n').split('|')
        if len(p) < 9 or p[0] != 'E': continue
        _, rule, k, P, dx, dy, t, f, c = p
        k, P, dx, dy, t = int(k), int(P), int(dx), int(dy), int(t)
        if P == 0 or (dx == 0 and dy == 0): continue
        hexa = rule.startswith('H:')
        if hexa:
            a, b = canon6(dx, dy); g = math.gcd(a, b); key = ('hex', a // g, b // g)
            ang = math.degrees(math.atan2(b * math.sqrt(3) / 2, a + b / 2)); pente = f"√3·{b//g}/{2*(a//g)+b//g}"
        else:
            a, b = canon4(dx, dy); g = math.gcd(a, b); key = ('carre', a // g, b // g)
            ang = math.degrees(math.atan2(b, a)); pente = str(Fraction(b, a))
        nf = len(f.split(';')); nc = len([x for x in c.split(';') if x.strip()])
        e = {'regle': rule, 'groupe': k, 'periode': P, 'dep': [dx, dy], 'dep_canon': [a, b], 'n_fourmis': nf, 'n_cases': nc, 'fourmis': f, 'cases': c, 'fichier': fn.split('/')[-1], 't_sortie': t}
        kk = str(key)
        if kk not in D: D[kk] = {'grille': key[0], 'dir': [key[1], key[2]], 'angle': round(ang, 3), 'pente': pente, 'n': 0, 'regles': {}, 'ex': []}
        d = D[kk]; d['n'] += 1; d['regles'][rule] = d['regles'].get(rule, 0) + 1
        d['ex'].append(e); d['ex'] = sorted(d['ex'], key=lambda e: (len(e['regle']), e['n_fourmis'] + e['n_cases'], e['periode']))[:5]
json.dump(sorted(D.values(), key=lambda d: (d['grille'], d['angle'])), open('dirs.json', 'w'), ensure_ascii=False, indent=0)
for d in sorted(D.values(), key=lambda d: (d['grille'], d['angle'])):
    e = d['ex'][0]
    print(f"{d['grille']:5s} dir {str(d['dir']):10s} angle {d['angle']:7.2f}° pente {d['pente']:10s} n={d['n']:6d} règles={len(d['regles']):4d} | ex: {e['regle']} {e['groupe']}f P={e['periode']} dep={e['dep']} | {e['fourmis'][:40]} | {e['cases'][:30]}")

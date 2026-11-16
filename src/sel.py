# sel.py — pour chaque direction de dirs.json : écarte les artefacts, revérifie le meilleur exemple dans le SYSTÈME COMPLET
# (hwv : rien n'est retiré, table de hachage) et garde la 1re situation qui redonne la même direction.
import json, subprocess, re, math, sys
from fractions import Fraction
T = sys.argv[1] if len(sys.argv) > 1 else '6000000'
D = json.load(open('dirs.json'))
def canon4(dx, dy):
    for _ in range(4):
        if dx > 0 and dy >= 0: return dx, dy
        dx, dy = -dy, dx
def canon6(a, b):
    for _ in range(6):
        if a > 0 and b >= 0: return a, b
        a, b = -b, a + b
out = []
for d in D:
    cands = [e for e in d['ex'] if e['periode'] > 2 and not (e['regle'] in ('RL', 'LR') and e['periode'] in (2, 4, 10, 12))]
    ok = None
    for e in cands:
        pts = e['cases']
        r = subprocess.run(['./hwv', e['regle'], T, e['fourmis'].replace(' ', ''), pts.replace(' ', '')], capture_output=True, text=True, timeout=900).stdout
        for m in re.finditer(r'fourmi (\d+) : periode (\d+) deplacement \((-?\d+),(-?\d+)\) debut (-?\d+)', r):
            i, P, dx, dy, deb = map(int, m.groups())
            if P == 0 or (dx == 0 and dy == 0) or int(T) - deb < max(50 * P, 1000000): continue
            c = canon6(dx, dy) if d['grille'] == 'hex' else canon4(dx, dy)
            g = math.gcd(*c)
            if [c[0] // g, c[1] // g] == d['dir']:
                ok = dict(e, verif_periode=P, verif_dep=[dx, dy], verif_debut=deb, verif_fourmi=i, verif_T=int(T)); break
        if ok: break
    d['verifie'] = ok
    out.append(d)
    print(d['grille'], d['dir'], d['pente'], 'OK' if ok else 'NON CONFIRMÉ', (ok['regle'], ok['verif_periode'], ok['verif_dep'], ok['verif_debut']) if ok else '', flush=True)
json.dump(out, open('dirs_verif.json', 'w'), ensure_ascii=False, indent=0)

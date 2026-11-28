"""T2 — filtre des conversions de tbascule.py étape 2 : on enlève les tirs sans effet (vaisseau exact ET objet = X0 non perturbé).
On classe : objet changé d'orbite / objet seulement déphasé ; vaisseau exact / retardé (même voie) / décalé de voie."""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tbascule import orbit
D = '../../data/t2/'; T1 = 700
O = json.load(open(D + 'objets.json')); C = json.load(open(D + 'conversions.json'))
orbs = {}; fin = {}; keep = []; cnt = collections.Counter()
def lane(v):
    r, p, tau = v; d = ship_dir(r); return p[0] * d[1] - p[1] * d[0]
def along(v):
    r, p, tau = v; d = ship_dir(r); return (p[0] * d[0] + p[1] * d[1]) * 8 // (d[0]*d[0] + d[1]*d[1]) + tau   # temps d'avance (pas)
for c in C:
    o = O[c['o']]; a, cc = parts_of(o['sit'])
    if c['o'] not in orbs: orbs[c['o']] = orbit(a, cc, o['p'])
    key = (c['o'], (c['ph'] + T1) % o['p'])
    if key not in fin:
        A = [list(t) for t in a]; G = {tuple(t): 1 for t in cc}
        for _ in range((c['ph'] + T1) % o['p']): step(A, G)
        fin[key] = (tuple(map(tuple, A)), frozenset(G))
    xa, xc = parts_of(c['X1']); st = (tuple(map(tuple, xa)), frozenset(map(tuple, xc)))
    sh = (0, (c['k'] - 40, 40), c['tau']); v1 = (c['v1'][0], tuple(c['v1'][1]), c['v1'][2])
    same_obj = st == fin[key]; in_orb = st in orbs[c['o']]; exact = v1 == sh
    if same_obj and exact: cnt['sans effet'] += 1; continue
    dl = lane(v1) - lane(sh); dt = along(v1) - along(sh)
    kind = ('X1 = X0' if same_obj else 'X0 déphasé' if in_orb else 'X1 ≠ X0') + ' / ' + ('exact' if exact else 'retard' if dl == 0 else 'voie')
    cnt[kind] += 1; c['dl'] = dl; c['dt'] = dt; c['kind'] = kind; keep.append(c)
print(dict(cnt))
json.dump(keep, open(D + 'conversions_effet.json', 'w'))

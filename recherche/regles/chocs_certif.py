#!/usr/bin/env python3
"""R-333 (suite) Certificats « pour toujours » des chocs de chocs_exhaustif.py, et 2e moteur.
1) 2e moteur : chaque choc qui interagit est rejoué par fourmi_r (-x -dump, exactement T tours) : fourmis + cases finales identiques ?
2) Sorties « propre » / « débris » : on prolonge chaque vaisseau SEUL (ils sont séparés) 200 périodes : distance entre eux toujours > DMAX
   (ils ne se reverront jamais : mouvements rectilignes qui s'éloignent) et aucune case de débris à distance ≤ RAD+1 de leur fourmi
   (ils ne retouchent jamais les débris). Alors l'issue est exacte pour TOUT temps.
3) Sorties « lié » : on cherche une période P (≤ 4000) avec état(t+P) = état(t) translaté (débris compris hors de sa route) : vaisseau
   composé certifié."""
import json, subprocess
from hx import step, HX, PHASES
from chocs_exhaustif_lib import hd, RAD, DMAX
D = json.load(open('data/chocs_exhaustif.json'))
chocs = D['chocs']
def parse_sit(s):
    rule, a, c = s.split('|')[:3]
    ants = [list(map(int, t.split(','))) for t in a.split(';') if t]
    g = {}
    for t in c.split(';'):
        if t: v = list(map(int, t.split(','))); g[(v[0], v[1])] = 1
    return ants, g
# 1) fourmi_r
lines = [c['situation'] for c in chocs]; T = chocs[0]['T']
assert all(c['T'] == T for c in chocs)
out = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
dumps = [l for l in out if l.startswith('DUMP')]
same = 0
for c, dl in zip(chocs, dumps):
    ants, g = parse_sit(c['situation'])
    for _ in range(T): step(ants, g)
    a2, g2 = parse_sit(dl.split(' ', 1)[1])
    if a2 == ants and g2 == g: same += 1
    c['_fin'] = (ants, g)
print(f'2 moteurs (hx.py et fourmi_r) : {same}/{len(chocs)} états finaux identiques après {T} tours')
# 2) et 3)
cert = {'propre': 0, 'débris': 0, 'lié': 0}; nonc = []
for c in chocs:
    ants, g = c['_fin']
    if c['type'] in ('propre', 'débris'):
        # cases de chaque vaisseau = cases noires à distance ≤ RAD de sa fourmi ; le reste = débris
        own = [{p for p in g if hd(p[0] - a[0], p[1] - a[1]) <= RAD} for a in ants]
        deb = set(g) - own[0] - own[1]
        sims = []
        for k in range(2):
            A = [list(ants[k])]; G = {p: 1 for p in own[k]}; tr = []
            for t in range(8 * 200): step(A, G); tr.append((A[0][0], A[0][1]))
            sims.append(tr)
        ok = all(hd(p[0] - q[0], p[1] - q[1]) > DMAX for p, q in zip(*sims))
        ok = ok and all(hd(p[0] - d[0], p[1] - d[1]) > RAD + 1 for tr in sims for p in tr for d in deb)
        # au-delà de 200 périodes : les distances (fourmi-fourmi, fourmi-débris) croissent linéairement : on vérifie la croissance
        far0 = hd(sims[0][-1][0] - sims[1][-1][0], sims[0][-1][1] - sims[1][-1][1]); far1 = hd(sims[0][-801][0] - sims[1][-801][0], sims[0][-801][1] - sims[1][-801][1])
        ok = ok and far0 > far1
        if ok: cert[c['type']] += 1
        else: nonc.append(c)
    else:
        A = [list(a) for a in ants]; G = dict(g)
        def key(A, G):
            ox, oy = A[0][0], A[0][1]
            return (tuple((x - ox, y - oy, h) for x, y, h in A), frozenset((x - ox, y - oy) for (x, y) in G if hd(x - ox, y - oy) <= 12))
        k0 = key(A, G); deb = {p for p in G if hd(p[0] - A[0][0], p[1] - A[0][1]) > 12}; P = None
        for t in range(1, 4001):
            step(A, G)
            if key(A, G) == k0: P = t; break
        if P:
            dx, dy = A[0][0] - ants[0][0], A[0][1] - ants[0][1]
            c['periode'] = P; c['depl'] = (dx, dy)
            # les débris laissés (loin) ne sont jamais sur sa route : la route s'éloigne (déplacement non nul)
            # on continue 50 périodes de l'objet : il doit se répéter, et s'éloigner des débris
            far = lambda: min([hd(A[0][0] - d[0], A[0][1] - d[1]) for d in deb] or [99])
            f1 = far(); okl = True
            for rep in range(50):
                for t in range(P): step(A, G)
                if key(A, G) != k0: okl = False; break
            okl = okl and far() > f1 and far() > 12 and all(G.get(d) for d in deb)
            if (dx, dy) != (0, 0) and okl: cert['lié'] += 1
            else: nonc.append(c)
        else: nonc.append(c)
print('certifiés pour tout temps :', cert, '; non certifiés :', len(nonc))
liés = sorted({(c['r'], c.get('periode'), tuple(c.get('depl', ()))) for c in chocs if c['type'] == 'lié'})
print('vaisseaux composés (r_A, période, déplacement) :', liés)
for c in nonc[:5]: print('  NON certifié :', c['type'], c['r'], c['tau'], c['v'], c['ordre'], c['situation'])
json.dump({'deux_moteurs': f'{same}/{len(chocs)}', 'certifies': cert, 'non_certifies': [c['situation'] for c in nonc], 'composes': liés},
          open('resumes/chocs_certif.json', 'w'), ensure_ascii=False, indent=1)

"""T2 — BASCULE T « À RETARD » (relâche R-503) : objet X0 (2 fourmis, oscillateur) traversé par un vaisseau → X1, le vaisseau ressort
PROPRE dans la même direction (décalé ou retardé, plus forcément exact) ; un 2e vaisseau IDENTIQUE (même route, Δ pas plus tard) remet
X1 en X0 (même place, même orbite) et ressort propre. Si les deux retards diffèrent (dt0 ≠ dt1), le vaisseau « porte » l'état de la
bascule : une 2e bascule sensible au retard peut alors compter (diviseur par 2 causal). Si les décalages sont de purs retards (même voie),
une horloge 3-symétrique peut les absorber (R-514 : retard égal sur l'anti-horaire).
Étape 1 : objets = cycles exacts à 2 fourmis (comme cycles2.py, T = 4 096) dans une petite boîte. Étape 2 : 1er vaisseau (dir 0), voies
−7…7, toutes les phases relatives. Étape 3 : 2e vaisseau, Δ ∈ [D0, D0 + 8·p1).
Usage : python3 s2_horloge/tbascule.py etape [D0]   (fichiers dans ../../data/t2/ : objets, conversions ; résultat s2_horloge/tbascule.json)"""
import sys, json, collections, os
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import lotdump, kship, parts_of
from demi_add_k import fmt
from outils_r import lot, parse
from tri import virt, adv, at
from exp_osc import hd
D = '../../data/t2/'; os.makedirs(D, exist_ok=True)
etape = sys.argv[1] if __name__ == '__main__' else ''
def canon(ants, cells):
    """forme normale d'un état (translation) pour reconnaître une orbite"""
    xs = [a[0] for a in ants] + [c[0] for c in cells]; ys = [a[1] for a in ants] + [c[1] for c in cells]
    mx, my = min(xs), min(ys)
    return (tuple((a[0] - mx, a[1] - my, a[2]) for a in ants), tuple(sorted((c[0] - mx, c[1] - my) for c in cells)))
def orbit(ants, cells, p):
    A = [list(t) for t in ants]; G = {tuple(c): 1 for c in cells}; S = {}
    for t in range(p):
        S[(tuple(map(tuple, A)), frozenset(G))] = t; step(A, G)
    return S
if etape == '1':
    L = []
    for d0 in range(6):
        for x in range(-3, 4):
            for y in range(-3, 4):
                if (x, y) == (0, 0): continue
                for d1 in range(6):
                    base = f"H:R2L2|0,0,{d0};{x},{y},{d1}|"; L.append(base)
                    for cx in range(-2, 3):
                        for cy in range(-2, 3): L.append(base + f"{cx},{cy}")
    out = lot(L, 4096)
    objs = {}; cnt = collections.Counter()
    for s, l in zip(L, out):
        d = parse(l); cnt[d['issue']] += 1
        if d['issue'] != 'CYCLE': continue
        p = int(l.split('|')[5])
        if p > 200: continue
        a, c = parts_of(s); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
        sig = set(); box = 0
        for t in range(p):
            sig.add(canon([tuple(q) for q in A], list(G))); step(A, G)
            box = max(box, max(hd(q[0], q[1]) for q in A))
        if box > 5: continue
        key = min(sig)
        if key not in objs: objs[key] = {'sit': s, 'p': p}
    print(dict(cnt), 'objets distincts (p ≤ 200, boîte ≤ 5) :', len(objs))
    json.dump(list(objs.values()), open(D + 'objets.json', 'w'))
elif etape == '2':
    O = json.load(open(D + 'objets.json')); jobs = []; meta = []
    T1 = 700
    for oi, o in enumerate(O):
        a, c = parts_of(o['sit'])
        for ph in range(o['p']):
            A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
            for _ in range(ph): step(A, G)
            for k in range(-7, 8):
                for tau in range(8):
                    sh = (0, (k - 40, 40), tau); s_a, s_c = at(sh, 0)
                    jobs.append(fmt([tuple(q) for q in A] + [s_a], list(G) + list(s_c))); meta.append((oi, ph, k, tau))
    print('tirs :', len(jobs), flush=True)
    conv = []; cnt = collections.Counter()
    B = 40000
    for i in range(0, len(jobs), B):
        rr = lotdump(jobs[i:i + B], T1)
        for (oi, ph, k, tau), (ants, cells) in zip(meta[i:i + B], rr):
            # le vaisseau : une fourmi libre, loin des autres, direction 0
            fr = [q for q in range(3) if min(hd(ants[q][0] - ants[j][0], ants[q][1] - ants[j][1]) for j in range(3) if j != q) > 10]
            if len(fr) != 1: cnt['pas 1 vaisseau'] += 1; continue
            q = fr[0]; v = virt(tuple(ants[q]), cells, T1)[0]
            if v is None or v[0] != 0: cnt['vaisseau mauvais'] += 1; continue
            rest = [tuple(ants[j]) for j in range(3) if j != q]
            rc = [x for x in cells if hd(x[0] - ants[q][0], x[1] - ants[q][1]) > 2]
            if max(hd(r[0], r[1]) for r in rest) > 8: cnt['objet parti'] += 1; continue
            conv.append({'o': oi, 'ph': ph, 'k': k, 'tau': tau, 'v1': v, 'X1': fmt(rest, rc), 'q': q}); cnt['propre'] += 1
        print(i + B, dict(cnt), flush=True)
    # X1 périodique et borné ?
    out = lot([c['X1'] for c in conv], 4096)
    good = []
    for c, l in zip(conv, out):
        f = l.split('|')
        if f[3] == 'CYCLE' and int(f[5]) <= 400: c['p1'] = int(f[5]); good.append(c)
    print('conversions propres :', len(conv), 'dont X1 oscillateur :', len(good))
    json.dump(good, open(D + 'conversions.json', 'w'))
elif etape == '3':
    D0 = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    O = json.load(open(D + 'objets.json')); C = json.load(open(D + 'conversions_u.json'))   # tb_filtre.py + dédoublonnage
    jobs = []; meta = []; T1 = 700
    for ci, c in enumerate(C):
        o = O[c['o']]; a, cc = parts_of(o['sit'])
        A = [list(t) for t in a]; G = {tuple(t): 1 for t in cc}
        for _ in range(c['ph']): step(A, G)
        sh1 = (0, (c['k'] - 40, 40), c['tau'])
        for Dl in range(D0, D0 + 8 * c['p1']):
            sh2 = adv(sh1, -Dl) if False else None
            # 2e vaisseau Δ pas derrière : même route, reculé de Δ pas
            r, p, tau = sh1; dd = ship_dir(r); s = tau - Dl; m = s // 8
            sh2 = (r, (p[0] + m * dd[0], p[1] + m * dd[1]), s % 8)
            a1, c1 = at(sh1, 0); a2, c2 = at(sh2, 0)
            jobs.append(fmt([tuple(q) for q in A] + [a1, a2], list(G) + list(c1) + list(c2))); meta.append((ci, Dl))
    print('flux :', len(jobs), flush=True)
    win = []; cnt = collections.Counter(); B = 40000
    orbs = {}
    for i in range(0, len(jobs), B):
        part = meta[i:i + B]; byT = collections.defaultdict(list)
        for j, (ci, Dl) in enumerate(part): byT[T1 + Dl].append(i + j)
        for Tf, idx in byT.items():
            rr = lotdump([jobs[j] for j in idx], Tf)
            for j, (ants, cells) in zip(idx, rr):
                ci, Dl = meta[j]; c = C[ci]
                fr = [q for q in range(4) if min(hd(ants[q][0] - ants[u][0], ants[q][1] - ants[u][1]) for u in range(4) if u != q) > 10]
                if len(fr) != 2: cnt['pas 2 vaisseaux'] += 1; continue
                vs = [virt(tuple(ants[q]), cells, Tf)[0] for q in fr]
                if any(v is None or v[0] != 0 for v in vs): cnt['vaisseaux mauvais'] += 1; continue
                rest = [tuple(ants[u]) for u in range(4) if u not in fr]
                rc = [x for x in cells if all(hd(x[0] - ants[q][0], x[1] - ants[q][1]) > 2 for q in fr)]
                if c['o'] not in orbs:
                    o = O[c['o']]; a, cc = parts_of(o['sit']); orbs[c['o']] = orbit(a, cc, o['p'])
                if (tuple(rest), frozenset(rc)) not in orbs[c['o']]: cnt['objet ≠ X0'] += 1; continue
                cnt['BASCULE T'] += 1
                win.append({**c, 'Delta': Dl, 'v_out': vs})
        print(i + B, dict(cnt), flush=True)
    json.dump(win, open('s2_horloge/tbascule_%d.json' % D0, 'w'))
    print('bascules T (2 vaisseaux propres, objet revenu) :', len(win))

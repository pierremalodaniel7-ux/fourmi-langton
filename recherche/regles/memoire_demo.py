#!/usr/bin/env python3
"""R-346 Démo « calcul → mémoire » : à chaque usage u, le demi-additionneur R-337 calcule a∧b ; la sortie C (1 vaisseau) arrive sur la
bascule (choisie par memoire_cherche.py) et la met à 1 ; on LIT le pixel (état de l'objet dans la grille) ; si le pixel vaut 1, un
vaisseau de remise à 0 (prévu d'avance par l'opérateur qui connaît le bit lu, car la bascule n'est pas idempotente, R-340/R-342) le remet
à 0 avant l'usage suivant. N usages au même endroit dans UNE simulation (toutes les pièces posées à t = 0), 2 moteurs.
Usage : python3 memoire_demo.py [fichier candidats] [N] [graine] [max candidats]"""
import sys, json, random
from memoire_calc import *
from compose import advance, rotate, translate
src = sys.argv[1] if len(sys.argv) > 1 else 'data/memoire_ok_1600.json'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
MAXC = int(sys.argv[4]) if len(sys.argv) > 4 else 400
tstar = 1600; CS = (2, -28, 916, 0)
HA = Circuit([('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')])
def shift_piece(p, s):
    """pièce-vaisseau retardée de s pas (posée plus en arrière sur sa route)"""
    n = (s + 7) // 8; return advance(back(p, n), 8 * n - s)
def free_ship_at(r, start, t):
    """pièce posée à t = 0 qui sera, au temps t, le vaisseau ship(r, start) (phase 0)"""
    n = (t + 7) // 8; sa, sc = ship(r, start); p = back((sa, [sc]), n)
    return advance(p, 8 * n - t)
def evolve(osc_state, steps):
    A_ = [list(a) for a in osc_state[0]]; g = {tuple(q): 1 for q in osc_state[1]}
    for _ in range(steps): step(A_, g)
    return (sorted(map(tuple, A_)), sorted(g))
def build(x, seq):
    f1, f2 = kv(x['s1']), kv(x['s2'])
    E1 = setup(x['R'], int(f1['r']), int(f1['l']), int(f1['ph']), int(f1['ord']))
    E2 = setup(x['R2'], int(f2['r']), int(f2['l']), int(f2['ph']), int(f2['ord']))
    p1, p2 = len(E1['states']), len(E2['states'])
    k = 200
    while (8 * k) % p1: k += 1
    pieces, o1, cen, rho, orb = place_gen(x['R'], f1, CS, 4000, tstar)
    c = (cen[0] - rot(E1['center'], rho)[0], cen[1] - rot(E1['center'], rho)[1])
    OR1 = orbit_abs(x['R'], rho, c); OR2 = orbit_abs(x['R2'], rho, c)
    key = lambda s: (sorted(map(tuple, s[0])), sorted(map(tuple, s[1])))
    K1 = [key(s) for s in OR1]; K2_ = [key(s) for s in OR2]
    # fin de l'expérience 1 : phase de R' à t_set + T1 (expérience seule, dans son repère puis tournée)
    A_ = [list(a) for a in E1['ants']]; g = dict(E1['g'])
    for _ in range(E1['T']): step(A_, g)
    obj = (sorted(tuple(a) for a in A_ if hd(a[0] - E1['center'][0], a[1] - E1['center'][1]) <= E1['R']),
           sorted(q for q in g if hd(q[0] - E1['center'][0], q[1] - E1['center'][1]) <= E1['R']))
    L2 = orbit_list(x['R2']); i1 = [ (sorted(map(tuple, s[0])), sorted(map(tuple, s[1]))) for s in L2].index(obj)
    A_ = [list(a) for a in E2['ants']]; g = dict(E2['g'])
    for _ in range(E2['T']): step(A_, g)
    obj2 = (sorted(tuple(a) for a in A_ if hd(a[0] - E2['center'][0], a[1] - E2['center'][1]) <= E2['R']),
            sorted(q for q in g if hd(q[0] - E2['center'][0], q[1] - E2['center'][1]) <= E2['R']))
    L1 = orbit_list(x['R']); i2 = [(sorted(map(tuple, s[0])), sorted(map(tuple, s[1]))) for s in L1].index(obj2)
    ph1, ph2 = int(f1['ph']), int(f2['ph'])
    P = []; events = []; tsets = []
    cur = (0, (ph1 - tstar) % p1, 0)              # (0 = R / 1 = R', indice de phase, instant de référence)
    t_next = tstar
    for u, inp in enumerate(seq):
        # instant de passage de C : premier t ≥ t_next où R est en phase ph1 (le demi-additionneur est décalé d'autant de pas)
        ts = t_next
        while (cur[1] + ts - cur[2]) % p1 != ph1: ts += 1
        sft = ts - tstar; tsets.append(ts)
        P_u = [shift_piece(p, sft) for p in HA.parts(inp)]
        if inp['a'] & inp['b']:
            t0 = ts + E1['T'] + 16
            tr = t0
            while (i1 + tr - (ts + E1['T'])) % p2 != ph2: tr += 1
            sp2 = rotp(E2['ship_start'], rho, c); r2 = (int(f2['r']) + rho) % 6
            P_u = P_u + [('reset', free_ship_at(r2, sp2, tr), int(f2['ord']))]
            events.append((u, ts, tr)); cur = (0, i2, tr + E2['T'])
            t_next = max(ts + 8 * k, tr + E2['T'] + 400)
        else:
            t_next = ts + 8 * k
        P.append(P_u)
    k = 0
    return dict(k=k, pieces=pieces, o1=o1, P=P, cen=cen, K1=K1, K2=K2_, E1T=E1['T'], E2T=E2['T'], events=events, tsets=tsets)
def run(x, seq, engine2=False):
    b = build(x, seq)
    if b is None: return None
    k = b['k']
    # ordre de jeu : objet avant ou après les vaisseaux selon l'expérience 1 (le vaisseau de remise à 0 suit son propre ordre,
    # identique à l'ordre 1 dans les bascules retenues : on le vérifie)
    obj = b['pieces']; rest = []; resets_after = []; resets_before = []
    for P_u in b['P']:
        for it in P_u:
            if isinstance(it, tuple) and len(it) == 3 and it[0] == 'reset':
                (resets_after if it[2] == 0 else resets_before).append(it[1])
            else: rest.append(it)
    before = (rest if b['o1'] == 'avant' else []) + resets_before
    after = (rest if b['o1'] == 'apres' else []) + resets_after
    S = sit(before + obj + after)
    T_end = b['tsets'][-1] + 3200
    times = [ts + b['E1T'] + 8 for ts in b['tsets']]
    # une simulation, arrêts aux instants de lecture (fourmi_r relancé depuis l'état précédent)
    a, cc = parts_of(S); state = sit([(tuple(t), []) for t in a][:0]) if False else S
    cur = S; tprev = 0; vals = []
    for t in times + [T_end]:
        r = lotdump([cur], t - tprev)[0]
        cur = fmt(r[0], r[1]); tprev = t
        na = sorted(tuple(z) for z in r[0] if hd(z[0] - b['cen'][0], z[1] - b['cen'][1]) <= 10)
        nc = sorted(tuple(z) for z in r[1] if hd(z[0] - b['cen'][0], z[1] - b['cen'][1]) <= 10)
        vals.append(0 if (na, nc) in b['K1'] else 1 if (na, nc) in b['K2'] else '?')
    final = r
    same = None
    if engine2:
        pa, pc = pyrun(S, T_end); same = sorted(pa) == sorted(map(tuple, final[0])) and sorted(pc) == sorted(map(tuple, final[1]))
    far_a = [z for z in final[0] if hd(z[0] - b['cen'][0], z[1] - b['cen'][1]) > 10]; far_c = [z for z in final[1] if hd(z[0] - b['cen'][0], z[1] - b['cen'][1]) > 10]
    clean = decode(far_a, far_c) is not None
    return dict(vals=vals, clean=clean, same=same, k=k, S=S, T=T_end)
if __name__ == '__main__':
    C = json.load(open(src)); random.seed(seed)
    seq = [{'a': random.randint(0, 1), 'b': random.randint(0, 1)} for _ in range(N)]
    want = [e['a'] & e['b'] for e in seq]
    print('suite :', ''.join(f"{e['a']}{e['b']} " for e in seq)); n_ok = 0
    for i, x in enumerate(C[:MAXC]):
        res = run(x, seq)
        if res is None: continue
        good = sum(1 for v, w in zip(res['vals'][:-1], want) if v == w)
        if good == N and res['clean'] and res['vals'][-1] == 0:
            n_ok += 1
            if n_ok <= 3:
                r2 = run(x, seq, engine2=True)
                print(f'candidat {i} : {good}/{N} lectures justes, propre, fin = 0, k = {res["k"]}, 2 moteurs identiques : {r2["same"]}')
                print('  lu :', ''.join(map(str, res['vals'][:-1])), ' attendu :', ''.join(map(str, want)))
                json.dump(dict(bascule=x, k=res['k'], suite=seq, lus=res['vals'], situation=res['S'], T=res['T'], deux_moteurs=r2['same']),
                          open(f'data/memoire_demo_{i}_{seed}.json', 'w'))
    print('candidats qui marchent :', n_ok, '/', min(MAXC, len(C)))

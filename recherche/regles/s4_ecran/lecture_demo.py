#!/usr/bin/env python3
"""R-709 LECTURE + RÉÉCRITURE du pixel M/R' (R-708) : sonde = 1 vaisseau direction 0, voie −3 (repère du pixel).
  ON (R') : la sonde TRAVERSE sans rien changer (vrai pour les 12 phases) -> elle ressort tout droit : lu 1.
  OFF (M, phase 6) : M devient X (2 fourmis, période 21) et la sonde ressort DÉVIÉE : lu 0 ; puis réécriture X -> M par 1 vaisseau
  (direction 3, voie 1, X en phase 16), envoyée seulement si on a lu 0.
Démo : N écritures au hasard (mise à 1 / à 0 seulement si le bit change), chaque écriture suivie d'une lecture (+ réécriture si 0),
UNE simulation, tout posé à t = 0 ; état final = superposition exacte prévue ; 2 moteurs (fourmi_r, hx.py).
Usage : python3 lecture_demo.py [N] [graine] -> lecture_demo.json"""
import sys, json, random
from traj import *
import pixel
from exp_osc import setup
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20; SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0
GAP = 400
OPT = {0: ((0, -3, 6), (3, 1, 16)), 1: ((3, 2, 8), (0, -3, 5)), 2: ((4, 2, 15), (1, 1, 5))}[int(sys.argv[3]) if len(sys.argv) > 3 else 0]
SR = json.load(open(HERE + '/sondes_retour.json'))
XS = [x for x in SR if x['etat'] == 'M' and (x['r'], x['l'], x['ph']) == OPT[0]][0]['X']
OSC = {'M': pixel.M, "R'": pixel.R2, 'X': XS}
def orbit_ordered(osc):
    a, c = pixel.parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; A0 = [list(x) for x in a]; g0 = dict(g); out = []
    while True:
        out.append(([tuple(x) for x in A], sorted(g))); step(A, g)
        if A == A0 and g == g0: return out
ORBO = {k: orbit_ordered(v) for k, v in OSC.items()}
def kit(src, r, l, ph):
    E = setup(OSC[src], r, l, ph, 0); A = E['ants']; og = E['states'][ph][1]
    S = of_label(lab_piece((tuple(A[-1]), sorted(c for c in E['g'] if c not in og)), 0))
    B = [list(a) for a in A]; g = dict(E['g'])
    for _ in range(E['T']): step(B, g)
    obj = (sorted(tuple(b) for b in B[:-1]), sorted(c for c in g if hd(*c) <= 6))
    out = of_label(lab_piece((tuple(B[-1]), sorted(c for c in g if hd(*c) > 6)), E['T']))
    dst = [k for k in ORBO for i, (a, c) in enumerate(ORBO[k]) if (sorted(a), c) == obj]
    fin = [(k, i) for k in ORBO for i, (a, c) in enumerate(ORBO[k]) if (sorted(a), c) == obj][0]
    return {'S': S, 'ph': ph, 'T': E['T'], 'out': out, 'src': src, 'dst': fin[0], 'fin': fin[1]}
K = {'set': kit('M', 0, 1, 16), 'rst': kit("R'", 2, -2, 2), 'lire0': kit('M', *OPT[0]), 'reecr': kit('X', *OPT[1])}
K.update({f'lire1_{p}': kit("R'", OPT[0][0], OPT[0][1], p) for p in range(12)})
assert all(K[f'lire1_{p}']['out'] == K[f'lire1_{p}']['S'] and K[f'lire1_{p}']['dst'] == "R'" for p in range(12))
assert K['lire0']['out'] != K['lire0']['S'] and K['lire0']['dst'] == 'X' and K['reecr']['dst'] == 'M'
PER = {k: len(v) for k, v in ORBO.items()}
def prefix_ok(ops):
    """le préfixe déjà planifié donne-t-il EXACTEMENT la superposition prévue ? (fourmi_r) — les vaisseaux qui se croisent de face
    (sortie d'une sonde / entrée d'une réécriture) doivent se traverser : on décale l'opération d'une période de l'objet sinon"""
    s = sit(ops); T = ops[-1][1] + 2400
    (a, c), = [lotdump([s], T)[0]]
    fa = [tuple(x) for x in a if hd(x[0], x[1]) > 6]; fc = [tuple(x) for x in c if hd(*x) > 6]
    d = decode(fa, fc); got = sorted(of_label(lab_of(z, T)) for z in d) if d else None
    return got == sorted(norm(movT(K[n]['out'], (0, 0), t)) for n, t in ops)
def plan(bits, init_phase=0):
    st, tr, pr = 'M', 0, init_phase; t = GAP; ops = []
    def do(name, t):
        nonlocal st, tr, pr
        k = K[name]; assert k['src'] == st
        while (pr + t - tr) % PER[st] != k['ph']: t += 1
        for essai in range(60):
            if prefix_ok(ops + [(name, t)]): break
            t += PER[st]
        else: raise RuntimeError(f'pas de retard possible pour {name}')
        ops.append((name, t)); st, tr, pr = k['dst'], t + k['T'], k['fin']; return t + GAP
    for b in bits:
        if b == 1 and st == 'M': t = do('set', t)
        if b == 0 and st == "R'": t = do('rst', t)
        if st == "R'": t = do(f'lire1_{(pr + t - tr) % 12}', t)       # la sonde est la même : seul le nom dit la phase
        else: t = do('lire0', t); t = do('reecr', t)
    return ops, t
def sit(ops, init_phase=0):
    a, c = ORBO['M'][init_phase]; A = list(a); C = list(c)
    for name, t in ops:
        p = piece_at(movT(K[name]['S'], (0, 0), t), 0); A.append(p[0]); C += p[1]
    return fmt(A, C)
if __name__ == '__main__':
    random.seed(SEED); bits = [random.randint(0, 1) for _ in range(N)]
    ops, tend = plan(bits); s = sit(ops); T = tend + 2000
    (a, c), = [lotdump([s], T)[0]]
    pa, pc = pyrun(s, T); same2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
    obj_a = [x for x in a if hd(x[0], x[1]) <= 6]; obj_c = [x for x in c if hd(*x) <= 6]
    fa = [tuple(x) for x in a if hd(x[0], x[1]) > 6]; fc = [tuple(x) for x in c if hd(*x) > 6]
    d = decode(fa, fc); got = sorted(of_label(lab_of(z, T)) for z in d) if d else None
    want = sorted(norm(movT(K[n]['out'], (0, 0), t)) for n, t in ops)
    lus = []
    for n, t in ops:
        if n.startswith('lire'):
            straight = norm(movT(K[n]['S'], (0, 0), t)) in (got or []); dev = norm(movT(K['lire0']['out'], (0, 0), t)) in (got or [])
            lus.append(1 if straight and not dev else 0 if dev and not straight else '?')
    st = 'M' if (sorted(map(tuple, obj_a)), sorted(map(tuple, obj_c))) in [(sorted(x), y) for x, y in ORBO['M']] else \
         "R'" if (sorted(map(tuple, obj_a)), sorted(map(tuple, obj_c))) in [(sorted(x), y) for x, y in ORBO["R'"]] else '?'
    ok = lus == bits and got == want
    print(f'graine {SEED} : {N} bits {bits}\n  {len(ops)} vaisseaux, t = {T} ; lus {lus} ; justes {sum(x == y for x, y in zip(lus, bits))}/{N} ; '
          f'superposition exacte {got == want} ; état final {st} (attendu {"R" + chr(39) if bits[-1] else "M"}) ; 2 moteurs {same2}')
    json.dump({'graine': SEED, 'bits': bits, 'lus': lus, 'operations': ops, 'superposition': got == want, 'deux_moteurs': same2, 'T': T,
               'etat_final': st, 'situation': s}, open(HERE + f'/lecture_demo_{SEED}.json', 'w'), ensure_ascii=False)

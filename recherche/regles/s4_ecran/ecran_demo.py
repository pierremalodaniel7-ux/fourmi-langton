#!/usr/bin/env python3
"""R-707 ÉCRAN 2×2 ADRESSABLE (R2L2 hexagonal) : port « 1 » = démux A (data/demux_tries.json), port « 0 » = démux B tourné de rho0,
translaté de v (placement de ecran3_geo.py) ; 4 pixels = bascules M/R' (R-341, kits R-705) aux croisements.
Une opération = (port, adresse) = 1 vaisseau W + les vaisseaux d'adresse présents + K, posés à t = 0 avec un retard d (pas exact).
Chaque retard est choisi (≥ précédent + GAP) pour que le vaisseau arrive au pixel dans la bonne phase.
Démo : motif 1 (diagonale), motif 2 (anti-diagonale), motif 3 (« L »), puis tout éteint. UNE simulation, tout posé à t = 0.
Lecture de l'écran à chaque étape (état exact de chaque pixel), 2 moteurs (fourmi_r et hx.py) aux mêmes instants.
Usage : python3 ecran_demo.py [rang dans data/ecran3_geo.json] -> ecran_demo.json, images ecran_motif_*.png"""
import sys, json, time
from traj import *
import pixel
RANG = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sys.argv = [sys.argv[0], '1', '1']
import ecran3_geo as E
import ecran2_geo as G
CASES = G.CASES; GAP = 1600
P = json.load(open(HERE + '/data/ecran3_geo.json'))[RANG]
BA, BB = G.L[P['A']], G.L[P['B']]; IA, IB = G.info(BA), G.info(BB)
ROT = {'A': 0, 'B': P['rho0']}; MOV = {'A': (0, 0), 'B': tuple(P['v'])}; DEM = {'A': BA, 'B': BB}; INF = {'A': IA, 'B': IB}
SETPORT = 'A' if P['role'] == 'set1' else 'B'
def addr(port, j):
    """adresse à envoyer sur le port pour toucher le pixel j (pixel j = sortie j du port A)"""
    return CASES[j] if port == 'A' else CASES[P['perm'][j]]
def port_traj(port, T, d): return movT(rotT(tt(T), ROT[port]), MOV[port], d)
def tt(x): return norm(tuple(x))
def op_pieces(port, ad, d):
    B = DEM[port]; out = []
    for n in B['order']:
        if n in ('a1', 'a0') and not {'a1': ad[0], 'a0': ad[1]}[n]: continue
        out.append(piece_at(port_traj(port, B['T'][n], d), 0))
    return out
def out_traj(port, j, d):
    k = j if port == 'A' else P['perm'][j]
    return port_traj(port, DEM[port]['outs4'][k], d)
KIT = {}
for j in range(4):
    ks, kr, rho = P['kits'][j]; c = tuple(P['centres'][j])
    KIT[j] = {'rho': rho, 'c': c, 1: E.KS[ks], 0: E.KS[kr]}      # 1 = mise à 1 (M -> R'), 0 = mise à 0 (R' -> M)
def kit_delay(j, val, port, d):
    """instant δ où le kit (mise à val) du pixel j est « à son temps 0 » quand le port tire avec le retard d"""
    K = KIT[j]; Ka = movT(rotT(K[val]['S'], K['rho']), K['c'], 0); O = out_traj(port, j, d)
    dl = to_label(Ka)[2] - to_label(O)[2]
    assert same(movT(Ka, (0, 0), dl), O), (j, val, port)
    return dl
PER = {0: len(pixel.ORB[0]), 1: len(pixel.ORB[1])}
def fin_phase(kit, dst):
    return pixel.ORB[dst].index(kit['obj'])
def schedule(ops):
    """ops = [(pixel, valeur)] -> liste (port, adresse, retard) + états initiaux (phase de M à t = 0)"""
    st = {j: None for j in range(4)}  # (état, t_ref, phase_ref)
    init = {}; out = []; d = 0
    for j, val in ops:
        port = SETPORT if val == 1 else ('B' if SETPORT == 'A' else 'A')
        need = KIT[j][val]['ph']; src = 1 - val; p = PER[src]
        while True:
            dl = kit_delay(j, val, port, d)
            if st[j] is None: break
            s, tr, pr = st[j]; assert s == src, ('écriture inutile', j, val)
            if (pr + dl - tr) % p == need: break
            d += 1
        if st[j] is None:
            init[j] = (need - dl) % PER[0]; assert val == 1
        st[j] = (val, dl + KIT[j][val]['T'], fin_phase(KIT[j][val], val))
        out.append((port, addr(port, j), d, j, val, dl)); d += GAP
    return out, init, d
def orbit_ordered(osc):
    """orbite en gardant l'ORDRE DE JEU des fourmis (pixel.ORB les trie : faux quand 2 fourmis sont sur la même case)"""
    a, c = pixel.parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; A0 = [list(x) for x in a]; g0 = dict(g); out = []
    while True:
        out.append(([tuple(x) for x in A], sorted(g))); step(A, g)
        if A == A0 and g == g0: return out
ORBO = {0: orbit_ordered(pixel.M), 1: orbit_ordered(pixel.R2)}
def place_ordered(state, phase, rho, c):
    a, g = ORBO[state][phase]
    A = [(rot((x, y), rho)[0] + c[0], rot((x, y), rho)[1] + c[1], (h + rho) % 6) for x, y, h in a]
    return A, [(rot(q, rho)[0] + c[0], rot(q, rho)[1] + c[1]) for q in g]
def situation(ops_sched, init):
    A, C = [], []
    for j in range(4):
        a, g = place_ordered(0, init[j], KIT[j]['rho'], KIT[j]['c']); A += a; C += g
    for port, ad, d, j, val, dl in ops_sched:
        for p in op_pieces(port, ad, d): A.append(p[0]); C += p[1]
    return fmt(A, C)
def screen(ants, cells):
    return [pixel.read_state(ants, cells, KIT[j]['rho'], KIT[j]['c']) for j in range(4)]
MOTIFS = [('motif 1 (diagonale)', [(0, 1), (3, 1)]), ('motif 2 (anti-diagonale)', [(0, 0), (3, 0), (1, 1), (2, 1)]),
          ('motif 3 (« L »)', [(3, 1)]), ('tout éteint', [(1, 0), (2, 0), (3, 0)])]
def draw(ants, cells, title, fn, scr):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    xs = [P['centres'][j][0] for j in range(4)]; ys = [P['centres'][j][1] for j in range(4)]
    def cart(x, y): return x + y / 2, -y * 3 ** .5 / 2
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.5), gridspec_kw={'width_ratios': [3, 1.3]})
    for j in range(4):
        on = isinstance(scr[j], tuple) and scr[j][0] == 1; r_, c_ = CASES[j]
        ax2.add_patch(plt.Rectangle((c_, 1 - r_), .92, .92, color='#ffcc00' if on else '#223'))
        ax2.text(c_ + .46, 1 - r_ + .46, f'{r_}{c_}', ha='center', va='center', color='#000' if on else '#ccc')
    ax2.set_xlim(-.1, 2); ax2.set_ylim(-.1, 2); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_title('écran lu (a1 a0)', fontsize=9)
    box = lambda x, y: min(xs) - 25 <= x <= max(xs) + 25 and min(ys) - 25 <= y <= max(ys) + 25
    pc = [cart(*c) for c in cells if box(*c)]; pa = [cart(a[0], a[1]) for a in ants if box(a[0], a[1])]
    if pc: ax.scatter(*zip(*pc), s=8, c='#333', marker='h')
    if pa: ax.scatter(*zip(*pa), s=30, c='#d62728')
    for j in range(4):
        X, Y = cart(*P['centres'][j]); on = isinstance(scr[j], tuple) and scr[j][0] == 1
        ax.add_patch(plt.Circle((X, Y), 6, color='#ffcc00' if on else '#9ab', alpha=.35))
        ax.text(X, Y + 8, f"{CASES[j][0]}{CASES[j][1]} : {'ON' if on else 'OFF'}", ha='center', fontsize=9)
    ax.set_aspect('equal'); ax.set_title(title, fontsize=10); ax.axis('off'); fig.savefig(fn, dpi=110, bbox_inches='tight'); plt.close(fig)
if __name__ == '__main__':
    t0 = time.time(); ops = [o for _, m in MOTIFS for o in m]
    sch, init, dend = schedule(ops)
    s = situation(sch, init); na = s.split('|')[1].count(';') + 1
    print('placement', {k: P[k] for k in ('A', 'B', 'rho0', 'role', 'perm', 'v', 'centres')})
    print(len(sch), 'opérations ; retards', [x[2] for x in sch], ';', na, 'fourmis à t = 0')
    # instants de lecture : juste avant l'opération qui suit chaque motif (et fin)
    k = 0; checks = []
    for name, m in MOTIFS:
        k += len(m); tchk = sch[k][2] if k < len(sch) else dend + 2000
        want = {}
        checks.append((name, tchk))
    rep = {'placement': P, 'operations': [{'port': x[0], 'adresse': x[1], 'retard': x[2], 'pixel': CASES[x[3]], 'valeur': x[4]} for x in sch],
           'phases_initiales': init, 'fourmis': na, 'lectures': []}
    exp_on = set(); k = 0; allok = True
    for (name, m), (_, tchk) in zip(MOTIFS, checks):
        for j, val in m: (exp_on.add if val else exp_on.discard)(j)
        (a, c), = [lotdump([s], tchk)[0]]
        pa, pc = pyrun(s, tchk); same2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
        scr = screen(a, c); lu = [x[0] if isinstance(x, tuple) else '?' for x in scr]; want = [1 if j in exp_on else 0 for j in range(4)]
        ok = lu == want; allok &= ok and same2
        print(f'{name:26s} t = {tchk:6d} : lu {lu} attendu {want} -> {ok} ; 2 moteurs identiques {same2} ; {len(a)} fourmis')
        rep['lectures'].append({'motif': name, 't': tchk, 'lu': lu, 'attendu': want, 'juste': ok, 'deux_moteurs': same2, 'fourmis': len(a)})
        draw(a, c, f'Écran 2×2 R2L2 — {name} (t = {tchk})', HERE + f'/ecran_motif_{len(rep["lectures"])}.png', scr)
    rep['situation'] = s; rep['tout_juste'] = allok; rep['duree_s'] = round(time.time() - t0)
    json.dump(rep, open(HERE + '/ecran_demo.json', 'w'), ensure_ascii=False, indent=1, default=list)
    print('TOUT JUSTE' if allok else 'ÉCHEC', '; durée', rep['duree_s'], 's')

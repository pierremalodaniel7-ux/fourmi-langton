#!/usr/bin/env python3
"""R-710 ÉCRAN 4×4 (R2L2 hexagonal) = 4 BLOCS 2×2 de R-707 (même placement : démux n° 8 + sa copie tournée de 180°, kits R-705),
translatés de b·S·(D0 + D1) (b = 0..3) : direction 30° = bissectrice de deux directions de vol ⇒ toute route (droite de direction
r·60°) qui passe par un bloc reste à ≥ S·√3/2 − rayon des autres blocs (calcul exact ci-dessous, test « loin »).
Adresse d'un pixel (ligne R, colonne C) de l'écran 4×4 : bloc = 2·(R // 2) + (C // 2), choisi par la LIGNE D'ENTRÉE (le bloc où on
tire) ; dans le bloc, 2 bits (a1 a0) = (R % 2, C % 2) décodés par le démultiplexeur (R-702). [Pas de démux devant les blocs : OUVERT.]
Démo : dessin 1 « visage », dessin 2 « anneau », puis tout éteint. UNE simulation, tout posé à t = 0, 2 moteurs (fourmi_r, hx.py).
Usage : python3 ecran4_demo.py [S] -> ecran4_demo.json, ecran4_dessin_*.png"""
import sys, json, time
S = int(sys.argv[1]) if len(sys.argv) > 1 else 400
sys.argv = [sys.argv[0]]
import ecran_demo as E2
from traj import *
import pixel
P, CASES, GAP = E2.P, E2.CASES, E2.GAP
VB = [(b * S * 2, -b * S) for b in range(4)]          # b·S·(D0 + D1), D0 = (1, -1), D1 = (1, 0)
def pt(port, T, d, b): return movT(E2.port_traj(port, T, d), VB[b], 0)
def op_pieces(port, ad, d, b):
    B = E2.DEM[port]; out = []
    for n in B['order']:
        if n in ('a1', 'a0') and not {'a1': ad[0], 'a0': ad[1]}[n]: continue
        out.append(piece_at(pt(port, B['T'][n], d, b), 0))
    return out
def out_traj(port, j, d, b):
    k = j if port == 'A' else P['perm'][j]
    return pt(port, E2.DEM[port]['outs4'][k], d, b)
def centre(b, j): c = E2.KIT[j]['c']; return (c[0] + VB[b][0], c[1] + VB[b][1])
def kit_delay(b, j, val, port, d):
    K = E2.KIT[j]; Ka = movT(rotT(K[val]['S'], K['rho']), centre(b, j), 0); O = out_traj(port, j, d, b)
    dl = to_label(Ka)[2] - to_label(O)[2]
    assert same(movT(Ka, (0, 0), dl), O), (b, j, val, port)
    return dl
PER = E2.PER
def schedule(ops):
    """ops = [((b, j), valeur)] -> [(port, adresse, retard, b, j, valeur)], phases initiales des 16 pixels (tous OFF à t = 0)"""
    st = {}; init = {}; out = []; d = 0
    for (b, j), val in ops:
        port = E2.SETPORT if val == 1 else ('B' if E2.SETPORT == 'A' else 'A')
        need = E2.KIT[j][val]['ph']; src = 1 - val; p = PER[src]
        while True:
            dl = kit_delay(b, j, val, port, d)
            if (b, j) not in st: break
            s, tr, pr = st[(b, j)]; assert s == src, ('écriture inutile', b, j, val)
            if (pr + dl - tr) % p == need: break
            d += 1
        if (b, j) not in st:
            init[(b, j)] = (need - dl) % PER[0]; assert val == 1
        st[(b, j)] = (val, dl + E2.KIT[j][val]['T'], E2.fin_phase(E2.KIT[j][val], val))
        out.append((port, E2.addr(port, j), d, b, j, val)); d += GAP
    for b in range(4):
        for j in range(4): init.setdefault((b, j), 0)
    return out, init, d
def situation(sch, init):
    A, C = [], []
    for b in range(4):
        for j in range(4):
            a, g = E2.place_ordered(0, init[(b, j)], E2.KIT[j]['rho'], centre(b, j)); A += a; C += g
    for port, ad, d, b, j, val in sch:
        for p in op_pieces(port, ad, d, b): A.append(p[0]); C += p[1]
    return fmt(A, C)
def bj(R, C): return (2 * (R // 2) + C // 2, CASES.index((R % 2, C % 2)))
def screen(ants, cells):
    return [[pixel.read_state(ants, cells, E2.KIT[bj(R, C)[1]]['rho'], centre(*bj(R, C))) for C in range(4)] for R in range(4)]
VISAGE = ["X..X", "....", "X..X", ".XX."]
ANNEAU = [".XX.", "X..X", "X..X", ".XX."]
VIDE = ["....", "....", "....", "...."]
def ops_between(a, b):
    """opérations pour passer du dessin a au dessin b (on n'écrit que ce qui change : extinctions d'abord)"""
    off = [(bj(R, C), 0) for R in range(4) for C in range(4) if a[R][C] == 'X' and b[R][C] == '.']
    on = [(bj(R, C), 1) for R in range(4) for C in range(4) if a[R][C] == '.' and b[R][C] == 'X']
    return off + on
ETAPES = [('dessin 1 (visage)', VISAGE), ('dessin 2 (anneau)', ANNEAU), ('tout éteint', VIDE)]
def loin(rayon=200):
    """distance (hexagonale, exacte) de chaque centre de pixel d'un bloc à toutes les routes passant par les pixels des autres
    blocs : une route de direction r par le point q = {q + k·D[r]} ; on borne inférieurement par min sur k entier"""
    worst = 10 ** 9
    for b1 in range(4):
        for b2 in range(4):
            if b1 == b2: continue
            for j1 in range(4):
                for j2 in range(4):
                    p, q = centre(b1, j1), centre(b2, j2)
                    for r in range(6):
                        dx, dy = D[r]
                        # k réel le plus proche puis voisins entiers (la distance hex est convexe en k)
                        best = min(hd(p[0] - q[0] - k * dx, p[1] - q[1] - k * dy) for k in range(-3 * S * 4, 3 * S * 4 + 1))
                        worst = min(worst, best)
    return worst
def draw(scr, ants, cells, title, fn):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    def cart(x, y): return x + y / 2, -y * 3 ** .5 / 2
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={'width_ratios': [2.6, 1]})
    for R in range(4):
        for C in range(4):
            on = isinstance(scr[R][C], tuple) and scr[R][C][0] == 1
            ax2.add_patch(plt.Rectangle((C, 3 - R), .92, .92, color='#ffcc00' if on else '#223'))
    ax2.set_xlim(-.1, 4); ax2.set_ylim(-.1, 4); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_title('écran 4×4 lu', fontsize=9)
    pc = [cart(*c) for c in cells]; pa = [cart(a[0], a[1]) for a in ants]
    if pc: ax.scatter(*zip(*pc), s=2, c='#333', marker='h')
    if pa: ax.scatter(*zip(*pa), s=6, c='#d62728')
    for R in range(4):
        for C in range(4):
            X, Y = cart(*centre(*bj(R, C))); on = isinstance(scr[R][C], tuple) and scr[R][C][0] == 1
            ax.add_patch(plt.Circle((X, Y), 14, color='#ffcc00' if on else '#9ab', alpha=.6))
    xs = [cart(*centre(b, j))[0] for b in range(4) for j in range(4)]; ys = [cart(*centre(b, j))[1] for b in range(4) for j in range(4)]
    ax.set_xlim(min(xs) - 250, max(xs) + 250); ax.set_ylim(min(ys) - 250, max(ys) + 250)
    ax.set_aspect('equal'); ax.set_title(title, fontsize=10); ax.axis('off'); fig.savefig(fn, dpi=110, bbox_inches='tight'); plt.close(fig)
if __name__ == '__main__':
    t0 = time.time()
    plan = []; prev = VIDE
    for name, dsn in ETAPES: plan.append((name, ops_between(prev, dsn))); prev = dsn
    ops = [o for _, m in plan for o in m]
    sch, init, dend = schedule(ops); s = situation(sch, init); na = s.split('|')[1].count(';') + 1
    marge = loin()
    print(f'S = {S} ; marge pixels / routes des autres blocs = {marge} ; {len(sch)} opérations ; {na} fourmis à t = 0 ; fin {dend}')
    rep = {'S': S, 'VB': VB, 'marge_routes': marge, 'operations': [{'port': x[0], 'adresse': x[1], 'retard': x[2], 'bloc': x[3],
           'pixel_bloc': CASES[x[4]], 'valeur': x[5]} for x in sch], 'fourmis': na, 'lectures': []}
    k = 0; allok = True
    for i, (name, m) in enumerate(plan):
        k += len(m); tchk = sch[k][2] if k < len(sch) else dend + 2000
        (a, c), = [lotdump([s], tchk)[0]]
        pa, pc = pyrun(s, tchk); same2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
        scr = screen(a, c); lu = [''.join('X' if (isinstance(x, tuple) and x[0] == 1) else ('.' if isinstance(x, tuple) else '?') for x in row) for row in scr]
        want = ETAPES[i][1]; ok = lu == want; allok &= ok and same2
        print(f'{name:20s} t = {tchk:6d} : lu {lu} attendu {want} -> {ok} ; 2 moteurs {same2} ; {len(a)} fourmis')
        rep['lectures'].append({'etape': name, 't': tchk, 'lu': lu, 'attendu': want, 'juste': ok, 'deux_moteurs': same2, 'fourmis': len(a)})
        draw(scr, a, c, f'Écran 4×4 R2L2 — {name} (t = {tchk})', HERE + f'/ecran4_dessin_{i + 1}.png')
    rep['situation'] = s; rep['tout_juste'] = allok; rep['duree_s'] = round(time.time() - t0)
    json.dump(rep, open(HERE + f'/ecran4_demo.json', 'w'), ensure_ascii=False, indent=1, default=list)
    print('TOUT JUSTE' if allok else 'ÉCHEC', '; durée', rep['duree_s'], 's')

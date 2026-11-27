#!/usr/bin/env python3
"""T4 : images « avant / après » de l'écran. En haut : la vraie fourmi RL sur le tore 2×2 (R-61) ; en bas : les 4 pixels SIMULÉS
(cases noires et fourmis réelles autour de chaque centre, rangés comme les cases (x en colonnes, y en lignes)), lus exactement.
Usage : python3 images.py un  [i_état]   -> t4/ecran_un_pas_<i>.png   (R-715 : t = 0 et après le pas)
        python3 images.py deux [i_état]  -> t4/ecran_deux_pas_<i>.png (R-720 : t = 0, pas 1, pas 2 ; boucles longues)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def cart(x, y): return x + y / 2, -y * 3 ** .5 / 2
def draw_torus(ax, e, title):
    for nm in CASES:
        i, j = int(nm[1]), int(nm[2]); on = e[nm] == 1
        ax.add_patch(plt.Rectangle((i, 1 - j), .94, .94, color='#222' if on else '#eee', ec='#999'))
    ax.plot(e['x'] + .47, 1 - e['y'] + .47, 'o', ms=16, color='#d62728')
    ax.text(e['x'] + .47, 1 - e['y'] + .47, f"{e['h1']}{e['h0']}", ha='center', va='center', color='w', fontsize=8)
    ax.set_xlim(-.1, 2.05); ax.set_ylim(-.1, 2.05); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)
def draw_screen(ax, ants, cells, PL, title, R=7):
    scr, _, _ = read_screen(ants, cells, PL)
    for nm in CASES:
        i, j = int(nm[1]), int(nm[2]); c = PL[nm]['c']; st = scr[nm]; on = isinstance(st, tuple) and st[0] == 1
        ox, oy = i * 2.2 * R, -j * 2.2 * R
        ax.add_patch(plt.Rectangle((ox - R, oy - R), 2 * R, 2 * R, color='#fff3b0' if on else '#dde4ee', zorder=0))
        for q in cells:
            if hd(q[0] - c[0], q[1] - c[1]) <= R - 1:
                X, Y = cart(q[0] - c[0], q[1] - c[1]); ax.scatter(ox + X, oy + Y, s=40, c='#222', marker='h', zorder=1)
        for a in ants:
            if hd(a[0] - c[0], a[1] - c[1]) <= R - 1:
                X, Y = cart(a[0] - c[0], a[1] - c[1]); ax.scatter(ox + X, oy + Y, s=30, c='#d62728', zorder=2)
        lab = 'ON' if on else ('OFF' if isinstance(st, tuple) else '?')
        ax.text(ox, oy + R + .8, f"{nm} : {lab}", ha='center', fontsize=8)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)
if __name__ == '__main__':
    mode = sys.argv[1]; i = int(sys.argv[2]) if len(sys.argv) > 2 else 0; e0 = STEP.cases()[i]
    import ecran_deux_pas as E2
    PL = json.load(open(os.path.join(T4, 'placement.json')))
    if mode == 'un':
        import ecran_un_pas as E1
        s = E1.situation([e0]); TA = json.load(open(os.path.join(T4, 'ecran_un_pas.json')))['T']
        shots = [(0, e0, 'avant (t = 0)'), (TA, E2.rl(e0), f'après 1 pas (t = {TA})')]
    else:
        L = json.load(open(os.path.join(T4, 'deux_pas_long.json'))); D = L['D']; E2.LOOP = L['boucles']
        s = build_sit([e0, E2.rl(e0)], [0, D], PL, clocks=E2.tokens())
        e1 = E2.rl(e0); shots = [(0, e0, 'avant (t = 0)'), (L['lectures']['tA'], e1, f"pas 1 (t = {L['lectures']['tA']})"),
                                 (L['lectures']['tA2'], e1, f"pas 1, plus tard (t = {L['lectures']['tA2']})"), (L['lectures']['tC'], E2.rl(e1), f"pas 2 (t = {L['lectures']['tC']})")]
    n = len(shots); fig, axs = plt.subplots(2, n, figsize=(3.2 * n, 6.2))
    for k, (t, e, ttl) in enumerate(shots):
        a, c = run_py(s, t) if t else S3L.parse(s)
        draw_torus(axs[0][k], e, 'vraie fourmi RL (tore 2×2)\n' + ttl); draw_screen(axs[1][k], a, c, PL, 'écran simulé (R2L2)\n' + ttl)
    fig.suptitle(f'Écran de la fourmi — état initial n° {i} (cases noires = 1, rond = fourmi, chiffres = cap h1h0)', fontsize=10)
    fn = os.path.join(T4, f'ecran_{mode}_pas_{i}.png'); fig.savefig(fn, dpi=110, bbox_inches='tight'); print(fn)

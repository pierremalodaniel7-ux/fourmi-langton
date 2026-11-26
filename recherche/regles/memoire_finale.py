#!/usr/bin/env python3
"""R-335 Mémoire 1 bit R2L2 RÉUTILISABLE, sans aucune case fixe, et écran 2 pixels (OFF = vide).
Bit 1 = oscillateur M = « H:R2L2|0,0,1;1,-1,0|-1,1 » (2 fourmis + 1 case, période 21, son propre renversé) ; bit 0 = rien.
ÉCRIRE 1 = film à l'envers de la destruction Da (ord 0, r 1, voie 0, phase 9) : 3 vaisseaux arrivent, M apparaît, 1 vaisseau repart.
LIRE = sonde Db (ord 0, r 2, voie −2, phase 11) : bit 1 → M part en 3 vaisseaux (sorties 3, 2, 4), la case redevient vide ; bit 0 → la
sonde traverse le vide. Toutes les routes vont dans les directions 2, 3, 4 (un demi-plan) : jamais de choc frontal en vol.
Test : 20 bits au hasard écrits puis relus l'un après l'autre AU MÊME ENDROIT, dans UNE simulation (tous les vaisseaux posés à t = 0).
Vérification : bit lu = nombre de vaisseaux qui s'éloignent du pixel, nés de la lecture (3 ↔ 1, 1 ↔ 0) ; état du pixel après chaque
écriture et chaque lecture ; 2e moteur fourmi_r (-x -dump) à 5 instants. Usage : python3 memoire_finale.py [nb_bits] [graine]"""
import sys, json, random, subprocess
import ecran
from hx import step, ship_dir, sit
from exp_osc import hd
ecran.O2 = M = "H:R2L2|0,0,1;1,-1,0|-1,1"
DA, DB = (0, 1, 0, 9), (0, 2, -2, 11)
pair = ecran.Pair(DA, DB)
def demo_memoire(bits, G=1600, P=(0, 0)):
    plan = []; tw = []; tr = []
    for i, b in enumerate(bits):
        t0 = 2 * i * G
        if b: plan.append(('écrit', P, t0)); tw.append(t0)
        tread = pair.t_erase(t0, t0 + G) if b else (t0 + G + 7) // 8 * 8
        plan.append(('efface', P, tread)); tr.append(tread)
    ants, cells = ecran.build(pair, plan)
    TEND = 2 * len(bits) * G + 1600
    def etat(A, g): return pair.lire(A, g, P)
    def compte(A, g, t0):
        n = 0
        for a in A:
            d = hd(a[0] - P[0], a[1] - P[1])
            if 15 < d < pair.TE // 8 + 25:
                sid = ecran.ships_of([a], {c: 1 for c in g if hd(c[0] - a[0], c[1] - a[1]) <= 2})[0]
                if sid:
                    v = ship_dir(sid[0])
                    if hd(a[0] + v[0] - P[0], a[1] + v[1] - P[1]) > d: n += 1
        return n
    checks = []
    for i, b in enumerate(bits):
        checks.append((2 * i * G + G - 16, (lambda A, g, i=i: ('avant lecture', i, etat(A, g)))))
        checks.append((tr[i] + pair.TE, (lambda A, g, i=i: ('lu', i, compte(A, g, 0)))))
        checks.append((2 * (i + 1) * G - 16, (lambda A, g, i=i: ('après lecture', i, etat(A, g)))))
    vals, A, g = ecran.simulate(ants, cells, checks, TEND, P)
    return plan, ants, cells, vals, TEND
if __name__ == '__main__':
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 20; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 26)
    bits = [random.randint(0, 1) for _ in range(nb)]
    plan, ants, cells, vals, TEND = demo_memoire(bits)
    lus = {v[1]: v[2] for v in vals if v[0] == 'lu'}; av = {v[1]: v[2] for v in vals if v[0] == 'avant lecture'}; ap = {v[1]: v[2] for v in vals if v[0] == 'après lecture'}
    justes = 0
    for i, b in enumerate(bits):
        bit_lu = 1 if lus[i] == 3 else 0 if lus[i] == 1 else '?'
        ok = bit_lu == b and (av[i].startswith('ON') if b else av[i] == 'OFF') and ap[i] == 'OFF'
        justes += ok
        print(f'usage {i + 1:2d} : écrit {b}, pixel avant lecture {av[i]:3s}, vaisseaux nés de la lecture {lus[i]} → lu {bit_lu}, après {ap[i]}', 'OK' if ok else 'FAUX')
    print(f'{justes}/{nb} usages justes ; {len(ants)} fourmis')
    # 2e moteur
    s0 = sit(ants, sorted(cells)); times = [TEND // 5, 2 * TEND // 5, 3 * TEND // 5, 4 * TEND // 5, TEND]
    A = [list(a) for a in ants]; g = dict(cells); t = 0; same = 0
    for ts in times:
        while t < ts: step(A, g); t += 1
        out = subprocess.run(['./fourmi_r', '-T', str(ts), '-x', '-dump', s0], capture_output=True, text=True).stdout
        d = [l for l in out.splitlines() if l.startswith('DUMP')][0].split(' ', 1)[1]
        _, da, dc = d.split('|')[:3]
        fa = [list(map(int, x.split(','))) for x in da.split(';') if x]; fc = {tuple(map(int, x.split(',')[:2])) for x in dc.split(';') if x}
        same += (fa == A and fc == set(g))
    print(f'2 moteurs : {same}/{len(times)} états identiques (hx.py et fourmi_r, jusqu\'à t = {TEND})')
    # écran 2 pixels avec ce pixel
    planE, antsE, cellsE, SNAP, vE = ecran.screen(pair)
    print('écran 2 pixels (P1, P2) aux instants', SNAP, ':', vE)
    json.dump({'oscillateur': M, 'ecriture': DA, 'lecture': DB, 'bits': bits, 'justes': f'{justes}/{nb}', 'deux_moteurs': f'{same}/{len(times)}',
               'situation_memoire': s0, 'ecran': vE, 'situation_ecran': sit(antsE, sorted(cellsE))},
              open('resumes/memoire.json', 'w'), ensure_ascii=False, indent=1)

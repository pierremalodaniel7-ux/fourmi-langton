#!/usr/bin/env python3
"""R-711 Écran 4×4 : ordonnancement GLOUTON avec contrôle exact. ecran4_demo.py (retards fixes, GAP) échoue : des vaisseaux d'entrée
d'opérations futures (posés à t = 0, loin en amont) croisent des débris d'opérations passées. Ici, pour chaque opération k (dans
l'ordre), on essaie les retards d compatibles avec la phase du pixel (d, d + p, d + 2p, …) et on garde le premier qui passe le CONTRÔLE :
simulation (fourmi_r) des opérations 0..k jusqu'à tc = d + 2 000 ; (a) les 16 pixels sont exactement dans l'état attendu ;
(b) tout le reste se décode en vaisseaux libres dont l'ensemble des étiquettes est EXACTEMENT celui prévu par le calcul sur les
trajectoires (sorties des opérations faites + entrées des opérations à venir) ⇒ aucune interaction imprévue jusqu'à tc.
Puis vérification finale à 2 moteurs (fourmi_r, hx.py) aux 3 lectures.  Usage : python3 ecran4_glouton.py [S] [essais max]"""
import sys, json, time
S = int(sys.argv[1]) if len(sys.argv) > 1 else 400; NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 60
sys.argv = [sys.argv[0], str(S)]
import ecran4_demo as E4
E2 = E4.E2
from traj import *
import pixel
def expected_labels(sch):
    L = []
    for port, ad, d, b, j, val in sch:
        for T in E2.DEM[port]['exp'][str(tuple(ad))]: L.append(to_label(E4.pt(port, T, d, b)))
    return sorted(L)
def check(sch, init, want_state, tc):
    s = E4.situation(sch, init); (a, c), = [lotdump([s], tc)[0]]
    a = [tuple(x) for x in a]; c = [tuple(x) for x in c]
    cs = [E4.centre(b, j) for b in range(4) for j in range(4)]
    near = lambda p: any(hd(p[0] - q[0], p[1] - q[1]) <= 6 for q in cs)
    for (b, j), v in want_state.items():
        r = pixel.read_state(a, c, E2.KIT[j]['rho'], E4.centre(b, j))
        if not (isinstance(r, tuple) and r[0] == v): return False, f'pixel {(b, j)} lu {r}'
    fa = [x for x in a if not near(x)]; fc = [x for x in c if not near(x)]
    lab = labels_at(fa, fc, tc)
    if lab is None: return False, 'débris non décodable'
    if lab != expected_labels(sch): return False, f'étiquettes : {len(lab)} lues / {len(expected_labels(sch))} prévues'
    return True, 'ok'
def greedy(ops):
    st = {}; init = {}; sch = []; d = 0; state = {(b, j): 0 for b in range(4) for j in range(4)}; log = []
    for k, ((b, j), val) in enumerate(ops):
        port = E2.SETPORT if val == 1 else ('B' if E2.SETPORT == 'A' else 'A')
        need = E2.KIT[j][val]['ph']; p = E2.PER[1 - val]; tries = 0; why = []
        while True:
            dl = E4.kit_delay(b, j, val, port, d)
            if (b, j) in st:
                s_, tr, pr = st[(b, j)]
                if (pr + dl - tr) % p != need: d += 1; continue
            ini = dict(init)
            if (b, j) not in st: ini[(b, j)] = (need - dl) % E2.PER[0]
            full = dict(ini); [full.setdefault((bb, jj), 0) for bb in range(4) for jj in range(4)]
            cand = sch + [(port, E2.addr(port, j), d, b, j, val)]
            ws = dict(state); ws[(b, j)] = val
            ok, msg = check(cand, full, ws, d + 2000); tries += 1
            if ok: break
            why.append((d, msg))
            if tries >= NMAX: raise SystemExit(f'op {k} {(b, j, val)} : aucun retard sur {NMAX} essais ; {why[:5]}')
            d += 1
        init = ini; sch = cand; state = ws
        st[(b, j)] = (val, dl + E2.KIT[j][val]['T'], E2.fin_phase(E2.KIT[j][val], val))
        log.append({'op': k, 'bloc': b, 'pixel': j, 'valeur': val, 'retard': d, 'essais': tries, 'refus': why[:3]})
        print(f'op {k:2d} bloc {b} pixel {j} -> {val} : retard {d} ({tries} essai(s))', flush=True)
        d += E2.GAP
    full = dict(init); [full.setdefault((bb, jj), 0) for bb in range(4) for jj in range(4)]
    return sch, full, d, log
if __name__ == '__main__':
    t0 = time.time(); plan = []; prev = E4.VIDE
    for name, dsn in E4.ETAPES: plan.append((name, E4.ops_between(prev, dsn))); prev = dsn
    ops = [o for _, m in plan for o in m]
    sch, init, dend, log = greedy(ops)
    s = E4.situation(sch, init); na = s.split('|')[1].count(';') + 1
    rep = {'S': S, 'VB': E4.VB, 'fourmis': na, 'journal_glouton': log, 'operations': [{'port': x[0], 'adresse': x[1], 'retard': x[2],
           'bloc': x[3], 'pixel_bloc': E2.CASES[x[4]], 'valeur': x[5]} for x in sch], 'lectures': []}
    k = 0; allok = True
    for i, (name, m) in enumerate(plan):
        k += len(m); tchk = sch[k][2] if k < len(sch) else dend + 2000
        (a, c), = [lotdump([s], tchk)[0]]
        pa, pc = pyrun(s, tchk); same2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
        scr = E4.screen(a, c); lu = [''.join('X' if (isinstance(x, tuple) and x[0] == 1) else ('.' if isinstance(x, tuple) else '?') for x in row) for row in scr]
        want = E4.ETAPES[i][1]; ok = lu == want; allok &= ok and same2
        print(f'{name:20s} t = {tchk:6d} : lu {lu} attendu {want} -> {ok} ; 2 moteurs {same2} ; {len(a)} fourmis')
        rep['lectures'].append({'etape': name, 't': tchk, 'lu': lu, 'attendu': want, 'juste': ok, 'deux_moteurs': same2, 'fourmis': len(a)})
        E4.draw(scr, a, c, f'Écran 4×4 R2L2 — {name} (t = {tchk})', HERE + f'/ecran4_dessin_{i + 1}.png')
    okf, msg = check(sch, init, {(b, j): 0 for b in range(4) for j in range(4)}, dend + 2000)
    rep['controle_final_etiquettes'] = msg; allok &= okf
    rep['situation'] = s; rep['tout_juste'] = allok; rep['duree_s'] = round(time.time() - t0)
    json.dump(rep, open(HERE + '/ecran4_glouton.json', 'w'), ensure_ascii=False, indent=1, default=list)
    print('contrôle final (étiquettes exactes) :', msg); print('TOUT JUSTE' if allok else 'ÉCHEC', '; durée', rep['duree_s'], 's')

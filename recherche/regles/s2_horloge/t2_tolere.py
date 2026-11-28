"""T2 — une horloge triangle « absorbe »-t-elle un petit décalage d'UN vaisseau (ce que fait le demi-additionneur R-337, R-509) ?
Pour chaque horloge (tri_cycles_rB5.json, les n plus petites), chaque fourmi k, on prend l'instant où elle est vaisseau libre loin des autres,
on la décale de δ (case, distance hexa ≤ 2) et de dt pas (avance/retard) et on teste CYCLE (fourmi_r, T = 20 P).
Usage : python3 s2_horloge/t2_tolere.py n"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step
from fa_lib import parts_of
from tri import virt, at, adv
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
n = int(sys.argv[1]); Pmin = int(sys.argv[2]) if len(sys.argv) > 2 else 0
W = sorted(json.load(open('s2_horloge/tri_cycles_rB5.json')), key=lambda w: w['P']) ; W = [w for w in W if w['P'] >= Pmin][:n]
D = [(x, y) for x in range(-2, 3) for y in range(-2, 3) if hd(x, y) <= 2]
tot = collections.Counter(); hits = []
for wi, w in enumerate(W):
    P = w['P']; a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    done = set(); lines = []; meta = []
    for t in range(P):
        for k in range(6):
            if k in done: continue
            v, near = virt(A[k], G, 0)
            if v is None or min(hd(A[k][0] - q[0], A[k][1] - q[1]) for j, q in enumerate(A) if j != k) < 9: continue
            done.add(k)
            mine = {(A[k][0] + u, A[k][1] + z) for u, z in near}
            others = [tuple(q) for j, q in enumerate(A) if j != k]; oc = [p for p in G if p not in mine]
            v0 = (v[0], v[1], v[2])   # virtuel « au temps 0 » relatif : on reconstruit le vaisseau au temps 0
            for dx, dy in D:
                for dt in range(-7, 8):
                    if (dx, dy, dt) == (0, 0, 0): continue
                    r, p, tau = adv(v0, dt + 64) if dt + 64 >= 0 else None
                    sh = (r, (p[0] + dx - 8 * 0, p[1] + dy), tau)
                    # adv de 64 pas puis on recule l'origine de 64 pas (8 périodes de vaisseau = 8 cases)
                    from hx import ship_dir
                    d = ship_dir(r); sh = (r, (sh[1][0] - 8 * d[0], sh[1][1] - 8 * d[1]), tau)
                    an, cl = at(sh, 0)
                    ants = others[:k] + [tuple(an)] + others[k:]
                    lines.append(fmt(ants, oc + list(cl))); meta.append((k, dx, dy, dt, t))
        step(A, G)
    out = lot(lines, 20 * P + 10)
    for m, l, o in zip(meta, lines, out):
        f = o.split('|'); tot[f[3]] += 1
        if f[3] == 'CYCLE':
            hits.append({'P0': P, 'k': m[0], 'dx': m[1], 'dy': m[2], 'dt': m[3], 't': m[4], 'P': int(f[5]), 'sit': l})
    print(wi, P, dict(tot), 'CYCLE', len(hits), flush=True)
print(collections.Counter((h['P0'], h['P'], h['dx'], h['dy'], h['dt']) for h in hits).most_common(30))
json.dump(hits, open('s2_horloge/t2_tolere.json', 'w'))

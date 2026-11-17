"""chaine.py — additionneur n bits = n copies du module, translatées de V, retards croissants.
Module m : origine m*V ; ses deux germes (S, K) reculés de m*DELAI périodes sur leur voie d'approche.
Module 0 : pas de retenue entrante. Lecture : S_m ↘ -> bit m = 0, ↙ -> 1 ; K_(n-1) ↗ -> bit n = 1, ↘ -> 0."""
import json, fourmis as F, numpy as np, itertools, sys
P = F.P
M = json.load(open('module.json'))
LOUT, AMOD = M['ray_out']           # rayon sortant : x+y = LOUT, (x-y) mod 4 = AMOD
VA = 2402; VX = (LOUT + VA) // 2; VY = LOUT - VX
DELAI = 950                          # périodes de retard par module
CAP = "HDBG"

def germe_chaine(n, a, b, delai=DELAI, va=None):
    vx, vy = (VX, VY) if va is None else ((LOUT + va) // 2, LOUT - (LOUT + va) // 2)
    cells, ants, noms = [], [], []
    for m in range(n):
        am, bm = (a >> m) & 1, (b >> m) & 1
        ox, oy = m * vx, m * vy
        for r in ('S', 'K'):
            R = M[r]; sc, sa = R['seed']
            k = m * delai                                  # recul de k périodes : +k*(2,-2)
            cells += [(x + ox + 2 * k, y + oy - 2 * k) for x, y in sc]
            ants.append((sa[0] + ox + 2 * k, sa[1] + oy - 2 * k, sa[2])); noms.append(f"{r}{m}")
            for nd in R['nodes']:
                cd = nd['cond']
                if 'c' in cd: raise ValueError
                if all({'a': am, 'b': bm}[q] == v for q, v in cd.items()):
                    cells.append((nd['cell'][0] + ox, nd['cell'][1] + oy))
    return cells, ants, noms

def lit(dh, xs, ys, t, i, need=30):
    """direction de l'autoroute de la fourmi i au pas t (périodique sur les need dernières périodes) ou None"""
    d = dh[:t, i]
    if t < need * P + P: return None
    w = d[t - need * P - P:t]
    if not np.array_equal(w[P:], w[:-P]): return None
    dx = int(xs[t - 1, i]) - int(xs[t - 1 - P, i]); dy = int(ys[t - 1, i]) - int(ys[t - 1 - P, i])
    return {(-2, 2): 0, (-2, -2): 1, (2, -2): 2, (2, 2): 3}.get((dx, dy))

def verifie(n, T, Tlec, delai=DELAI, va=None, montre=False):
    bad = 0; res = []
    for a in range(1 << n):
        for b in range(1 << n):
            cells, ants, noms = germe_chaine(n, a, b, delai, va)
            nn, dh, xs, ys = F.simule_tout(cells, ants, T)
            if nn < 0: print("BORD", a, b); bad += 1; continue
            s = a + b; lu = 0; ok = True; txt = []
            for m in range(n):
                d = lit(dh, xs, ys, min(len(dh), m * delai * P + Tlec), 2 * m)
                txt.append(F.FL[d] if d is not None else '?')
                if d == 0: lu |= 1 << m
                elif d != 3: ok = False
            dk = lit(dh, xs, ys, min(len(dh), (n - 1) * delai * P + Tlec + 20000), 2 * n - 1); txt.append('K' + (F.FL[dk] if dk is not None else '?'))
            if dk == 2: lu |= 1 << n
            elif dk != 3: ok = False
            ok = ok and lu == s
            bad += not ok
            res.append((a, b, s, lu, ok, ''.join(txt)))
            if montre or not ok: print(a, '+', b, '=', s, 'lu', lu, ''.join(txt), 'OK' if ok else 'ECHEC', flush=True)
    return bad, res

if __name__ == "__main__":
    n = int(sys.argv[1]); T = int(sys.argv[2]); Tl = int(sys.argv[3])
    bad, res = verifie(n, T, Tl, montre=len(sys.argv) > 4)
    print(f"n={n} : {len(res)} entrées, échecs {bad}")

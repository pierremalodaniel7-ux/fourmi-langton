#!/usr/bin/env python3
"""R-337 Demi-additionneur R2L2 avec UN SEUL vaisseau constant K (au lieu du zigzag K2-K3 de R-325..R-329).
Porte R-327 : B = vaisseau r = 0 en (0,0) (joué en 1er), A = vaisseau r = 2 en (30,−56). Seul, A sort sur sa voie ; seul, B sort sur la
sienne ; ensemble, les deux sont DÉCALÉS (A de 2 voies). On ajoute K (direction rK, départ, phase τ, place dans l'ordre de jeu) et on
demande, pour les 4 cas (a, b), des sorties toutes propres (aucune case restante) avec :
  S = a⊕b : un vaisseau sur la voie de sortie de B seul (direction 0) dans les cas (1,0) et (0,1), aucun dans (0,0) et (1,1) ;
  C = a∧b : un vaisseau dans une (direction, voie) présente SEULEMENT dans le cas (1,1).
Moteur : fourmi_r (lot, 2 cœurs), revérifié ensuite avec hx.py. Usage : python3 demi_add_k.py [T]"""
import sys, json, itertools, collections
from hx import ship, ship_dir, rot, step, PHASES, run as hrun
from outils_r import lot
from exp_osc import hd
T = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2400
OFFS = {}
for r in range(6):
    a, c = ship(r); A = [list(a)]; g = {c: 1}
    for ph in range(8): OFFS[(r, ph)] = (A[0][0] - a[0], A[0][1] - a[1]); step(A, g)
def lane(x, y, r):
    X, Y = rot((x, y), -r % 6); return X + Y
def ships(ants, cells):
    """liste (r, voie) des vaisseaux propres + nb de cases non expliquées"""
    out = []; used = set()
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cells if hd(p[0] - x, p[1] - y) <= 2)
        k = PHASES.get((h, near))
        if not k: return None, None
        r, ph = k; gx, gy = x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1]
        out.append((r, lane(gx, gy, r))); used |= {(x + a, y + b) for a, b in near}
    return sorted(out), len(set(cells) - used)
def fmt(ants, cells):
    return 'H:R2L2|' + ';'.join(f'{a[0]},{a[1]},{a[2]}' for a in ants) + '|' + ';'.join(f'{c[0]},{c[1]}' for c in cells)
def parse_dump(l):
    _, a, c = l.split(' ', 1)[1].split('|')[:3]
    return [tuple(map(int, t.split(','))) for t in a.split(';') if t], [tuple(map(int, t.split(',')[:2])) for t in c.split(';') if t]
def dumps(sits, T):
    out = lot(sits, T, ('-x', '-dump'))       # lot ne garde pas les lignes DUMP : on relance avec un petit wrapper
    return out
import subprocess, threading
def lotdump(lines, T, ncpu=2):
    parts = [lines[i::ncpu] for i in range(ncpu)]; res = [None] * ncpu
    def w(k):
        o = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(parts[k]) + '\n', capture_output=True, text=True).stdout
        res[k] = [l for l in o.splitlines() if l.startswith('DUMP')]
    th = [threading.Thread(target=w, args=(k,)) for k in range(ncpu)]; [t.start() for t in th]; [t.join() for t in th]
    out = [None] * len(lines)
    for k in range(ncpu):
        for j, l in enumerate(res[k]): out[k + j * ncpu] = parse_dump(l)
    return out
B = ship(0, (0, 0)); A = ship(2, (30, -56))
def case_sit(a, b, K, korder):
    ants = []; cells = []
    if b: ants.append(B[0]); cells.append(B[1])
    if a: ants.append(A[0]); cells.append(A[1])
    if K:
        ka, kc = K
        ants.insert(min(korder, len(ants)), ka); cells += kc
    return fmt(ants, cells)
if __name__ == '__main__':
    # sorties de référence sans K
    ref = lotdump([case_sit(1, 0, None, 0), case_sit(0, 1, None, 0), case_sit(1, 1, None, 0)], T)
    S_LANE = ships(*ref[1])[0][0]; print('voie S (= B seul) :', S_LANE, '; A seul :', ships(*ref[0])[0], '; A et B :', ships(*ref[2])[0])
    # trajectoire de A seul (U) : positions aux temps multiples de 8
    Aa = [list(A[0])]; Ag = {A[1]: 1}; U = {}
    for t in range(1, 1200):
        step(Aa, Ag)
        if t % 8 == 0: U[t] = (Aa[0][0], Aa[0][1])
    cand = []
    for rK in range(6):
        if rK == 2: continue
        dK = ship_dir(rK)
        for tm in range(240, 900, 40):
            for i in range(-4, 5):
                for j in range(-4, 5):
                    for tau in range(8):
                        st = (U[tm][0] - tm // 8 * dK[0] + i, U[tm][1] - tm // 8 * dK[1] + j)
                        ka, kc = ship(rK, st); KA = [list(ka)]; KG = {kc: 1}
                        for _ in range(tau): step(KA, KG)
                        K = (tuple(KA[0]), sorted(KG))
                        if any(hd(K[0][0] - p[0], K[0][1] - p[1]) < 8 for p in [(0, 0), (30, -56)]): continue
                        for ko in (0, 1, 2): cand.append((rK, tm, i, j, tau, ko, K))
    print('candidats K :', len(cand))
    # 1er filtre : cas (1,0) (U + K) doit donner un vaisseau sur la voie S, tout propre
    res10 = lotdump([case_sit(1, 0, c[6], c[5]) for c in cand], T)
    keep = []
    for c, r in zip(cand, res10):
        s, deb = ships(*r)
        if s is not None and deb == 0 and S_LANE in s: keep.append(c)
    print('après le cas (1,0) :', len(keep))
    good = []
    if keep:
        res = {ab: lotdump([case_sit(ab[0], ab[1], c[6], c[5]) for c in keep], T) for ab in [(0, 0), (0, 1), (1, 1)]}
        why = collections.Counter()
        for n, c in enumerate(keep):
            out = {}
            ok = True
            for ab in [(0, 0), (0, 1), (1, 1)]:
                s, deb = ships(*res[ab][n])
                if s is None or deb: ok = False; why[(ab, 'sale' if s is None else 'débris')] += 1; break
                out[ab] = s
            if not ok: continue
            why[('S01', S_LANE in out[(0, 1)]), ('S00', S_LANE in out[(0, 0)]), ('S11', S_LANE in out[(1, 1)])] += 1
            s10 = ships(*res10[cand.index(c)])[0]
            if S_LANE not in out[(0, 1)] or S_LANE in out[(0, 0)] or S_LANE in out[(1, 1)]: continue
            # C : une sortie présente dans (1,1) et dans aucun autre cas
            others = set(out[(0, 0)]) | set(out[(0, 1)]) | set(s10)
            Cs = [x for x in out[(1, 1)] if x not in others]
            if not Cs: continue
            good.append({'K': c[:6], 'Ksit': c[6], 'C': Cs[0], 'sorties': {str(k): v for k, v in out.items()} | {'(1, 0)': s10}})
    print('demi-additionneurs (4 cas justes, 0 case) :', len(good)); print('raisons :', dict(why) if keep else '')
    for g in good[:10]: print(' ', g['K'], 'C =', g['C'], g['sorties'])
    json.dump({'S': S_LANE, 'trouves': good}, open('data/demi_add_k.json', 'w'))

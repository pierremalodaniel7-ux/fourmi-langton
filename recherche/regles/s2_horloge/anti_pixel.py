"""S2 R-506 — DEUX PIXELS EN ALTERNANCE sur une même horloge (R-502 n° 0, P = 4 203).
Idée : sur l'arête C0C1, le pixel A (bascule R-341) est mis à 1 par le 1er vaisseau du tiers et remis à 0 par le 2e : sa fenêtre ON est
centrée sur l'instant du croisement t_m. Une bascule TOURNÉE de 180° (mise à 1 par le 2e vaisseau, remise à 0 par le 1er du tiers suivant)
a sa fenêtre ON centrée sur t_m + P/6 : elle est allumée quand A est éteint. On la pose dans l'état R' (allumé) à l'instant t* où A est
allumé ... non : à t* A est ON, donc B doit être OFF (M tourné). On prend l'instantané local de A (M ou R'), on le tourne de k crans, on le
translate (fenêtre autour de A) à toutes les phases ; critère : CYCLE exact (fourmi_r) de toute la machine (10 fourmis).
Usage : python3 s2_horloge/anti_pixel.py k Rmax [etat]   (etat = OFF : B posé éteint à un instant où A est allumé ; ON : l'inverse)"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd

W = json.load(open('s2_horloge/pixel_cycles_150_150_tri.json'))[0]
P = W['P']

def local(A, G, idx, rad=5):
    cx, cy = A[idx[0]][0], A[idx[0]][1]
    ants = [tuple(A[k]) for k in idx]
    cells = [q for q in G if hd(q[0] - cx, q[1] - cy) <= rad and
             not any(hd(q[0] - A[k][0], q[1] - A[k][1]) <= 3 for k in range(len(A)) if k not in idx)]
    return ants, cells

def norm(ants, cells):
    pts = [a[:2] for a in ants] + list(cells)
    mx = min(p[0] for p in pts); my = min(p[1] for p in pts)
    return (frozenset((a[0] - mx, a[1] - my, a[2]) for a in ants), frozenset((c[0] - mx, c[1] - my) for c in cells))

def orbit(ants, cells, n=400):
    A = [list(a) for a in ants]; G = {c: 1 for c in cells}; S = []
    for _ in range(n):
        S.append(norm(*local(A, G, range(len(A))))); step(A, G)
    return set(S)

def timeline(sit, idx, O_off, O_on, T):
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; st = []
    for t in range(T):
        x = norm(*local(A, G, idx)); st.append('0' if x in O_off else ('1' if x in O_on else '?')); step(A, G)
    return ''.join(st)

if __name__ == '__main__':
    k = int(sys.argv[1]); Rmax = int(sys.argv[2]); etat = sys.argv[3] if len(sys.argv) > 3 else 'OFF'
    a, c = parts_of(W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    M = local(A, G, (0, 1)); O_M = orbit(*M)
    # trouver les fenêtres de A
    st = []; snaps = []
    for t in range(P):
        x = norm(*local(A, G, (0, 1))); st.append(x in O_M); snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
    # premier ON stable : instant milieu de la 1re longue plage non-M
    runs = []; t = 0
    while t < P:
        u = t
        while u < P and st[u] == st[t]: u += 1
        runs.append((st[t], t, u)); t = u
    offs = [r for r in runs if not r[0] and r[2] - r[1] > 300]
    on_mid = (offs[0][1] + offs[0][2]) // 2
    Aon = [list(q) for q in snaps[on_mid][0]]; Gon = dict(snaps[on_mid][1])
    Rp = local(Aon, Gon, (0, 1)); O_R = orbit(*Rp)
    print('plages M/non-M :', [(r[0], r[1], r[2]) for r in runs][:8], ' |orbite M|', len(O_M), '|orbite R\'|', len(O_R), flush=True)
    # instant de pose : A allumé (on_mid) -> B éteint (M tourné) ; ou A éteint -> B allumé (R' tourné)
    if etat == 'OFF':
        t0 = on_mid; src = M
    else:
        mids = [(r[1] + r[2]) // 2 for r in runs if r[0] and r[2] - r[1] > 300]; t0 = mids[0]; src = Rp
    base_a, base_g = snaps[t0]
    ox, oy = base_a[0][0], base_a[0][1]
    # objet source centré, tourné de k ; ses phases
    sa, sc = src; cx, cy = sa[0][0], sa[0][1]
    Sa = [(*rot((x - cx, y - cy), k), (h + k) % 6) for x, y, h in sa]; Sc = [rot((x - cx, y - cy), k) for x, y in sc]
    phases = []; Ab = [list(q) for q in Sa]; Gb = {q: 1 for q in Sc}; seen = set()
    for i in range(60):
        n = norm([tuple(q) for q in Ab], list(Gb))
        if n in seen: break
        seen.add(n); phases.append(([tuple(q) for q in Ab], list(Gb))); step(Ab, Gb)
    print('phases de l\'objet B :', len(phases), flush=True)
    jobs = []; info = []
    for dx in range(-Rmax, Rmax + 1):
        for dy in range(-Rmax, Rmax + 1):
            if not (8 <= hd(dx, dy) <= Rmax): continue
            for i, (pa, pc) in enumerate(phases):
                Ba = [(x + ox + dx, y + oy + dy, h) for x, y, h in pa]; Bc = [(x + ox + dx, y + oy + dy) for x, y in pc]
                if min(hd(b[0] - q[0], b[1] - q[1]) for b in Ba for q in base_a) < 8: continue
                if any(q in base_g for q in Bc): continue
                ants = Ba + list(base_a); cells = list(base_g) + Bc
                jobs.append(fmt(ants, cells)); info.append({'k': k, 'etat': etat, 'd': (dx, dy), 'phase': i, 't0': t0})
    print('machines :', len(jobs), flush=True)
    out = lot(jobs, P + 10)
    cnt = collections.Counter(); win = []
    for i, l, s in zip(info, out, jobs):
        f = l.split('|'); cnt[f[3]] += 1
        if f[3] == 'CYCLE' and int(f[5]) == P: i['sit'] = s; win.append(i)
    print(sorted(cnt.items()), 'cycles P :', len(win), flush=True)
    # alternance : timelines de A (fourmis 2,3) et B (0,1) dans la machine posée
    O_Bm = orbit(*phases[0]) if etat == 'OFF' else None
    O_off_B = orbit(Sa, Sc) if etat == 'OFF' else None
    res = []
    for w in win:
        # orbites tournées de M et R' pour B
        def rt(o):
            a_, c_ = o; return ([(*rot((x - cx, y - cy), k), (h + k) % 6) for x, y, h in a_], [rot((x - cx, y - cy), k) for x, y in c_])
        Mb = rt(M); Rb = rt(Rp)
        tA = timeline(w['sit'], (2, 3), O_M, O_R, P); tB = timeline(w['sit'], (0, 1), orbit(*Mb), orbit(*Rb), P)
        opp = sum(1 for x, y in zip(tA, tB) if {x, y} == {'0', '1'}); same = sum(1 for x, y in zip(tA, tB) if x == y and x != '?')
        w['opp'] = opp; w['same'] = same; w['A'] = collections.Counter(tA); w['B'] = collections.Counter(tB)
        w['swB'] = sum(1 for t in range(1, P) if tB[t] != tB[t - 1]); res.append(w)
    res.sort(key=lambda w: (-w['opp'], w['same']))
    for w in res[:8]: print(w['d'], w['phase'], 'opp', w['opp'], 'same', w['same'], dict(w['A']), dict(w['B']), 'chgB', w['swB'])
    json.dump(res, open('s2_horloge/anti_k%d_%s.json' % (k, etat), 'w'))

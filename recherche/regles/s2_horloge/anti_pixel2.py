"""S2 R-506 (suite) — même recherche que anti_pixel.py mais le pixel B est posé sur une AUTRE arête : l'horloge est symétrique
(état(t + P/3) = R(état(t)), R = rotation de 120° + translation, calculée ici exactement) ; l'arête C1C2 voit les mêmes vaisseaux avec
P/3 de retard (= une période de clignotement). B = bascule tournée de 180° puis de 120°·m, fenêtre centrée sur R^m(position de A).
Usage : python3 s2_horloge/anti_pixel2.py m Rmax"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from anti_pixel import W, P, local, norm, orbit, timeline
from hx import rot, step
from fa_lib import parts_of
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
m = int(sys.argv[1]); Rmax = int(sys.argv[2])
a, c = parts_of(W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
snaps = []
for t in range(P + 1):
    snaps.append(([tuple(q) for q in A], dict(G))); step(A, G)
# R : clock(t + P/3) = R(clock(t)) ?
c0 = snaps[0][0][2:]; c1 = set(snaps[P // 3][0][2:]); Rk = None
for kr in range(6):
    r0 = [(*rot(q[:2], kr), (q[2] + kr) % 6) for q in c0]
    for q1 in c1:
        tx, ty = q1[0] - r0[0][0], q1[1] - r0[0][1]
        if {(x + tx, y + ty, h) for x, y, h in r0} == c1: Rk = (kr, tx, ty)
print('R =', Rk, flush=True)
kr, tx, ty = Rk
def Rm(p, n):
    for _ in range(n): p = (rot(p, kr)[0] + tx, rot(p, kr)[1] + ty)
    return p
# temps de pose : milieu d'une plage ON de A
O_M = orbit(*local([list(q) for q in snaps[0][0]], dict(snaps[0][1]), (0, 1)))
st = [norm(*local([list(q) for q in s[0]], dict(s[1]), (0, 1))) in O_M for s in snaps[:P]]
t0 = 776   # milieu de la plage non-M 438–1115 (anti_pixel.py)
M = local([list(q) for q in snaps[0][0]], dict(snaps[0][1]), (0, 1))
base_a, base_g = snaps[t0]
k = (3 + kr * m) % 6
sa, sc = M; cx, cy = sa[0][0], sa[0][1]
Sa = [(*rot((x - cx, y - cy), k), (h + k) % 6) for x, y, h in sa]; Sc = [rot((x - cx, y - cy), k) for x, y in sc]
phases = []; Ab = [list(q) for q in Sa]; Gb = {q: 1 for q in Sc}; seen = set()
for i in range(60):
    n = norm([tuple(q) for q in Ab], list(Gb))
    if n in seen: break
    seen.add(n); phases.append(([tuple(q) for q in Ab], list(Gb))); step(Ab, Gb)
ctr = Rm((base_a[0][0], base_a[0][1]), m)
print('k =', k, 'centre', ctr, 'phases', len(phases), flush=True)
jobs = []; info = []
for dx in range(-Rmax, Rmax + 1):
    for dy in range(-Rmax, Rmax + 1):
        if hd(dx, dy) > Rmax: continue
        for i, (pa, pc) in enumerate(phases):
            Ba = [(x + ctr[0] + dx, y + ctr[1] + dy, h) for x, y, h in pa]; Bc = [(x + ctr[0] + dx, y + ctr[1] + dy) for x, y in pc]
            if min(hd(b[0] - q[0], b[1] - q[1]) for b in Ba for q in base_a) < 8: continue
            if any(q in base_g for q in Bc): continue
            jobs.append(fmt(Ba + list(base_a), list(base_g) + Bc)); info.append({'m': m, 'k': k, 'd': (dx, dy), 'phase': i, 't0': t0})
print('machines :', len(jobs), flush=True)
out = lot(jobs, P + 10); cnt = collections.Counter(); win = []
for i, l, s in zip(info, out, jobs):
    f = l.split('|'); cnt[f[3]] += 1
    if f[3] == 'CYCLE' and int(f[5]) == P: i['sit'] = s; win.append(i)
print(sorted(cnt.items()), 'cycles P :', len(win), flush=True)
Ap = [list(q) for q in snaps[t0][0]]; Rp = local(Ap, dict(snaps[t0][1]), (0, 1)); O_R = orbit(*Rp)
def rt(o):
    a_, c_ = o; x0, y0 = a_[0][0], a_[0][1]
    return [(*rot((x - x0, y - y0), k), (h + k) % 6) for x, y, h in a_], [rot((x - x0, y - y0), k) for x, y in c_]
OBm, OBr = orbit(*rt(M)), orbit(*rt(Rp))
for w in win:
    tA = timeline(w['sit'], (2, 3), O_M, O_R, P); tB = timeline(w['sit'], (0, 1), OBm, OBr, P)
    w['opp'] = sum(1 for x, y in zip(tA, tB) if {x, y} == {'0', '1'}); w['same'] = sum(1 for x, y in zip(tA, tB) if x == y and x != '?')
    w['B'] = dict(collections.Counter(tB))
win.sort(key=lambda w: (-w['opp'], w['same']))
for w in win[:10]: print(w['d'], w['phase'], 'opp', w['opp'], 'same', w['same'], w['B'])
json.dump(win, open('s2_horloge/anti2_m%d.json' % m, 'w'))

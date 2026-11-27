"""S2 — construit les horloges triangle (tri.py) et teste le CYCLE exact avec fourmi_r. Usage : tri_test.py rB Tmax"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from tri import at, R
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
def build(A, B, c, order, t0=-40):
    shA = [A, R(A, c), R(A, c, 2)]; shB = [B, R(B, c), R(B, c, 2)]
    seq = shA + shB if order == 0 else shB + shA
    ants = []; cells = []
    for s in seq:
        a, cs = at(s, t0); ants.append(a); cells += cs
    if len(set(cells)) < len(cells): return None
    if min(hd(a[0]-b[0], a[1]-b[1]) for i, a in enumerate(ants) for b in ants[i+1:]) < 7: return None
    return fmt(ants, cells)
if __name__ == '__main__':
    rB = int(sys.argv[1]); Tmax = int(sys.argv[2])
    F = [f for f in json.load(open('s2_horloge/tri_rB%d.json' % rB)) if f['T'] <= Tmax]
    jobs = []; meta = []
    for f in F:
        s = build(tuple(f.get('A', (0, (0, 0), 0))) if False else (0, (0, 0), 0), tuple([f['B'][0], tuple(f['B'][1]), f['B'][2]]), tuple(f['c']), f['order'])
        if s: jobs.append(s); meta.append(f)
    print('systèmes :', len(jobs), flush=True)
    out = lot(jobs, 3 * Tmax + 50)
    cnt = collections.Counter(); good = []
    for f, s, l in zip(meta, jobs, out):
        p = l.split('|'); iss = p[3]
        P = int(p[5]) if iss == 'CYCLE' else None
        key = iss if iss != 'CYCLE' else ('CYCLE=3T' if P == 3 * f['T'] else 'CYCLE autre')
        cnt[key] += 1
        if iss == 'CYCLE': good.append(dict(f, P=P, sit=s, boite=p[-1]))
    print(sorted(cnt.items()))
    json.dump(good, open('s2_horloge/tri_cycles_rB%d.json' % rB, 'w'))
    byc = collections.defaultdict(list)
    for g in good: byc[(tuple(g['B'][1]), g['B'][2], g['order'])].append((g['T'], g['P']))
    print('chocs donnant au moins un cycle :', len(byc))
    for k, v in sorted(byc.items(), key=lambda kv: -len(kv[1]))[:15]: print(k, len(v), v[:6], v[-3:])

"""T2 (27-11) — analyse des PORTES d'une machine cyclique R2L2 : pour chaque point où des vaisseaux tournent (porte), et chaque
droite d'entrée, la suite (dans le temps, sur une période) des passages : T = le vaisseau sort sur une autre droite, D = il passe tout droit.
But : trouver une porte « bascule T » (diviseur par 2 causal) : une droite c dont les passages sont réguliers et dont la suite alterne
T, D, T, D… (le vaisseau c tourne quand le bit s est là, passe sinon).
Usage : python3 s2_horloge/t2_portes.py fichier.json [P]   (liste de machines {'sit', 'P'}) — ou importé (analyse(sit, P))."""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import step, ship_dir
from fa_lib import parts_of
from tri import virt
from exp_osc import hd
def lane(v):
    r, p, tau = v; d = ship_dir(r); return (r, p[0] * d[1] - p[1] * d[0])
def segments(sit, P, nper=3):
    """simule nper périodes ; renvoie pos[t][k], et pour chaque fourmi la liste des segments libres fusionnés [lane, t0, t1]"""
    a, c = parts_of(sit); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
    pos = []; lan = []
    for t in range(nper * P):
        pos.append([tuple(q[:2]) for q in A]); lan.append([(lambda v: lane(v) if v else None)(virt(q, G, 0)[0]) for q in A]); step(A, G)
    segs = []
    for k in range(len(A)):
        S = []
        for t in range(nper * P):
            l = lan[t][k]
            if l is None: continue
            if S and S[-1][0] == l: S[-1][2] = t
            else: S.append([l, t, t])
        segs.append(S)
    return pos, segs
def analyse(sit, P, rad=4):
    pos, segs = segments(sit, P)
    # portes = lieux où un vaisseau change de droite (fin d'un segment, entre t dans la 2e période)
    turns = []
    for k, S in enumerate(segs):
        for i in range(len(S) - 1):
            if P <= S[i][2] < 2 * P: turns.append((S[i][2], k, S[i][0], S[i + 1][0], pos[S[i][2]][k]))
    gates = []
    for t, k, l1, l2, p in turns:
        for g in gates:
            if hd(g['p'][0] - p[0], g['p'][1] - p[1]) <= 10: g['in'].add(l1); g['n'] += 1; break
        else: gates.append({'p': p, 'in': {l1}, 'n': 1})
    res = []
    for gi, g in enumerate(gates):
        for l in sorted(g['in']):
            seq = []
            for k, S in enumerate(segs):
                for i, (ll, t0, t1) in enumerate(S):
                    if ll != l: continue
                    # instant du plus proche passage du point de porte
                    best = min(range(t0, t1 + 1), key=lambda t: hd(pos[t][k][0] - g['p'][0], pos[t][k][1] - g['p'][1]))
                    dmin = hd(pos[best][k][0] - g['p'][0], pos[best][k][1] - g['p'][1])
                    if dmin > rad + 6 or not (P <= best < 2 * P): continue
                    end_near = hd(pos[t1][k][0] - g['p'][0], pos[t1][k][1] - g['p'][1]) <= 12 and i + 1 < len(S)
                    seq.append((best - P, k, 'T' if end_near else 'D', S[i + 1][0] if end_near else l))
            seq.sort()
            res.append({'gate': gi, 'p': g['p'], 'lane': l, 'seq': seq})
    return gates, res
def alterne(seq):
    s = ''.join(x[2] for x in seq)
    return len(s) >= 4 and len(s) % 2 == 0 and all(s[i] != s[i + 1] for i in range(len(s) - 1)) and s[0] != s[-1]
if __name__ == '__main__':
    L = json.load(open(sys.argv[1]))
    if len(sys.argv) > 2: L = [x for x in L if x['P'] == int(sys.argv[2])]
    tot = collections.Counter()
    for n, m in enumerate(L):
        gates, res = analyse(m['sit'], m['P'])
        for r in res:
            s = ''.join(x[2] for x in r['seq'])
            tot['T' in s and 'D' in s] += 1
            if alterne(r['seq']):
                dt = [b[0] - a[0] for a, b in zip(r['seq'], r['seq'][1:])]
                print('ALTERNE machine', n, 'P', m['P'], 'porte', r['gate'], r['p'], 'droite', r['lane'], s, 'écarts', dt, flush=True)
    print('droites de porte : variables', tot[True], 'constantes', tot[False])

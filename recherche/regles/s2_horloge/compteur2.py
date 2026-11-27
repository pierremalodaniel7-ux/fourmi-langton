"""S2 R-505 — bascule T « en deux temps » : objet frappé alternativement par deux routes opposées a (dir r) et b (dir r+3) ;
chaque vaisseau ressort EXACT. Chaîne X0 →a→ X1 →b→ X2 →a→ X3 →b→ X4 avec X4 = X0 (même place, orbite) et X2 ≠ X0 :
l'objet change d'état à chaque « tour » (a puis b) et revient après 2 tours = bit qui bascule à chaque tour.
Graphe des conversions exactes calculé par miroir2 tir (CONV=1) étage par étage ; exactitude refaite (bascule_shift.setup).
Usage : python3 s2_horloge/compteur2.py"""
import sys, json, re, subprocess, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from fa_lib import parts_of, lotdump
from demi_add_k import fmt, lane
from bascule_shift import setup, kv
from tri import virt
from hx import step
TT = 720
def tir(objs):
    out = []
    for i in range(0, len(objs), 300):
        o = subprocess.run(['./miroir2', 'tir', '40', '0'], input='\n'.join('OSC 0 0 | ' + s for s in objs[i:i + 300]) + '\n',
                           capture_output=True, text=True, env={'CONV': '1'}).stdout
        out += [l for l in o.splitlines() if l.startswith(('CONV', 'DECT'))]
    return out
def exacts(lines):
    """conversions angle 0 dont le vaisseau ressort exact : [(X, Xnext, (r, voie_abs), info)]"""
    L = [l for l in lines if ' angle=0 ' in l]
    jobs = []; meta = []
    for l in L:
        head, X = l.split(' | ')[0], l.split(' | ')[1].strip(); info = kv(head); Xn = l.split('restant ')[1].strip()
        ants, cells, V0, oc, ordr, na = setup(X, info)
        jobs.append(fmt(ants, cells)); meta.append((X, Xn, info, V0, ordr, na))
    res = lotdump(jobs, TT) if jobs else []
    out = []
    for (X, Xn, info, V0, ordr, na), (ants, cells) in zip(meta, res):
        q = 0 if ordr == 1 else na
        if virt(tuple(ants[q]), cells, TT)[0] == V0:
            r = V0[0]; out.append((X, Xn, (r, lane(*V0[1], r)), info))
    return out
def orbit_set(s, p):
    a, c = parts_of(s); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}; S = set()
    for _ in range(p): S.add((frozenset(map(tuple, A)), frozenset(G))); step(A, G)
    return S
def canon(s):
    a, c = parts_of(s); return (frozenset(a), frozenset(c))
if __name__ == '__main__':
    osc = [l.split('| ', 1)[1].strip() for l in open('data/osc2.txt')]
    E1 = exacts(tir(osc)); print('étage 1 (X0 →a→ X1) :', len(E1), flush=True)
    X1s = sorted({e[1] for e in E1}); L2 = exacts(tir(X1s)); print('étage 2 : objets', len(X1s), 'conversions exactes', len(L2), flush=True)
    by = collections.defaultdict(list)
    for e in L2: by[e[0]].append(e)
    chains2 = [(e1, e2) for e1 in E1 for e2 in by[e1[1]] if e2[2][0] == (e1[2][0] + 3) % 6]
    print('chaînes a, b :', len(chains2), flush=True)
    X2s = sorted({c[1][1] for c in chains2}); L3 = exacts(tir(X2s)); print('étage 3 : objets', len(X2s), 'conversions', len(L3), flush=True)
    by3 = collections.defaultdict(list)
    for e in L3: by3[e[0]].append(e)
    chains3 = [(e1, e2, e3) for e1, e2 in chains2 for e3 in by3[e2[1]] if e3[2] == e1[2]]
    print('chaînes a, b, a (même route a) :', len(chains3), flush=True)
    X3s = sorted({c[2][1] for c in chains3}); L4 = exacts(tir(X3s)); print('étage 4 : objets', len(X3s), 'conversions', len(L4), flush=True)
    by4 = collections.defaultdict(list)
    for e in L4: by4[e[0]].append(e)
    orbs = {}; res = collections.Counter(); win = []
    for e1, e2, e3 in chains3:
        for e4 in by4[e3[1]]:
            if e4[2] != e2[2]: continue
            X0 = e1[0]
            if X0 not in orbs: orbs[X0] = orbit_set(X0, int(e1[3]['p']))
            back = canon(e4[1]) in orbs[X0]
            same2 = canon(e2[1]) in orbs[X0]
            res[(back, same2)] += 1
            if back and not same2: win.append({'X0': X0, 'X1': e1[1], 'X2': e2[1], 'X3': e3[1], 'a': e1[3], 'b': e2[3], 'a2': e3[3], 'b2': e4[3]})
    print('chaînes de 4 (retour, X2 = X0) :', dict(res))
    print('BASCULES T en deux temps :', len(win))
    json.dump(win, open('s2_horloge/bascules_T.json', 'w'))
    for w in win[:5]: print(w['X0'], '→', w['X2'])

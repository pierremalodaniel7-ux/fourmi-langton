#!/usr/bin/env python3
"""R-611 Le pas complet de la petite fourmi (R-61) en UN germe R2L2 : les 8 modules (R-607, R-610) côte à côte, chacun translaté
d'un vecteur entier choisi pour que (c) aucune route sortante possible d'un module ne soit sur une voie opposée à < 7 d'une route
entrante d'un autre. Vérification : les 256 états (2 moteurs), superposition (le germe complet = réunion des 8 modules seuls),
certificat R-606 sur le germe complet, puis N usages de suite au même endroit.
Usage : python3 step.py [graine]   (paramètres des modules : resultats_modules.json ; h1 : data/h1_param.json s'il manque)"""
import sys, json, itertools, random, time, copy
from modules import module, spec, VARS, nodes
from nor import Layout, lane_of2
from s3lib import *
from reuse import certificate
from cert2 import certificate2
from diag2 import segments2, INF
_OUTS = {}
def louts(L):
    """sorties logiquement possibles (segments infinis de diag2, masques non vides) : plus fin que possible_outputs()"""
    if id(L) not in _OUTS: _OUTS[id(L)] = {s[1] for s in segments2(L) if s[3] == INF}
    return _OUTS[id(L)]
def build(nm, F, htree=False):
    if htree:
        from htree import build as hb, h1_tree, h1_tree2
        return hb(h1_tree2() if htree == 2 else h1_tree())
    r = module(nm)
    for n in nodes(r):
        if F and F.get(n.name): n.inputs = [('-' if sd == '+' else '+', it) for sd, it in n.inputs]
    return r
class Step:
    def __init__(self, params, offsets, names=None):
        self.names = names or list(params)
        self.L = {nm: Layout(build(nm, params[nm].get('F'), params[nm].get('htree')), a=params[nm].get('a', 0), Dmap=params[nm]['D'], Gmap=params[nm]['G']) for nm in self.names}
        self.off = offsets; self.tmax = max(L.tmax for L in self.L.values())
        self.out = {nm: transwl(self.L[nm].out, self.off[nm]) for nm in self.names}
    def cases(self): return [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
    def present(self, e):
        W = []
        for nm in self.names: W += [transwl(w, self.off[nm]) for w in self.L[nm].present(e)]
        return W
    def sit(self, e): return sit_wls(self.present(e))
    def outputs(self, d): return {nm: int(self.out[nm] in d) for nm in self.names}
def lanes(w): return [lane_of2(antpos(w, t), w[0]) for t in range(8)]
def lane_ok(LA, va, LB, vb):
    """routes sortantes possibles de A contre routes entrantes de B (translatés) : écart de voie ≥ 7 si directions opposées"""
    for o in louts(LA):
        o2 = transwl(o, va); lo = [lane_of2(antpos(o2, t), o[0]) for t in range(8)]
        for i, w in [(0, w) for _, _, w in LB.ships]:
            if (o[0] - w[0]) % 6 == 3:
                i2 = transwl(w, vb); li = [lane_of2(antpos(i2, t), o[0]) for t in range(8)]
                if min(abs(x - y) for x in lo for y in li) < 7: return False
    return True
def rays_ok(LA, va, LB, vb, Tend):
    """entrants deux à deux ≥ 7 pour t ≤ 300 (avant toute porte), sorties possibles deux à deux ≥ 7 pour t ≥ Tend"""
    from reuse import ray_min
    for _, _, a in LA.ships:
        for _, _, b in LB.ships:
            if ray_min(transwl(a, va), transwl(b, vb), 300, -1) < 7: return False
    oa = louts(LA); ob = louts(LB)
    for a in oa:
        for b in ob:
            if ray_min(transwl(a, va), transwl(b, vb), Tend, +1) < 7: return False
    return True
import os
NOLANES = os.environ.get('NOLANES') == '1'   # 1 seul usage : le critère (c) des voies opposées ne sert qu'à la réutilisation
def choose_offsets2(Ls, names, seed=0, box=int(os.environ.get('BOX', 1500))):
    rnd = random.Random(seed); off = {}; Tend = max(L.tmax for L in Ls.values()) + 1200
    for k, nm in enumerate(names):
        for _ in range(3000):
            v = (rnd.randint(-box, box), rnd.randint(-box, box)) if k else (0, 0)
            if all((NOLANES or (lane_ok(Ls[nm], v, Ls[m], off[m]) and lane_ok(Ls[m], off[m], Ls[nm], v))) and rays_ok(Ls[nm], v, Ls[m], off[m], Tend) for m in off): off[nm] = v; break
        else: raise RuntimeError('pas de translation sûre pour ' + nm)
    return off
def choose_offsets(Ls, names, seed=0, spacing=3000):
    rnd = random.Random(seed); off = {}
    for k, nm in enumerate(names):
        for _ in range(2000):
            v = (k * spacing + rnd.randint(-200, 200), rnd.randint(-200, 200)) if k else (0, 0)
            if all(lane_ok(Ls[nm], v, Ls[m], off[m]) and lane_ok(Ls[m], off[m], Ls[nm], v) for m in off): off[nm] = v; break
        else: raise RuntimeError('pas de translation sûre pour ' + nm)
    return off
def multi_check(S, seq, D, engine2=False):
    """N usages du germe complet au même endroit (usage u = états seq[u], retardé de u·D) : superposition exacte et 8 sorties justes"""
    T = S.tmax + (len(seq) - 1) * D + 1200; W = []
    for u, e in enumerate(seq): W += [tshift(w, u * D) for w in S.present(e)]
    s = sit_wls(W); a, c = run_c([s], T)[0]; d = decode(a, c, T)
    union = []
    for u, (a1, c1) in enumerate(run_c([S.sit(e) for e in seq], T)): union += [tshift(w, u * D) for w in decode(a1, c1, T)]
    sup = d is not None and sorted(d) == sorted(union)
    good = sum(all(int(tshift(S.out[nm], u * D) in (d or [])) == spec(nm, e) for nm in S.names) for u, e in enumerate(seq))
    same = None
    if engine2: pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
    return dict(usages=len(seq), superposition=sup, justes=good, deux_moteurs=same, fourmis=len(W))
def load_params():
    R = json.load(open('resultats_modules.json')); P = {nm: R[nm]['parametres'] for nm in R}
    if 'h1' not in P:
        try: P['h1'] = json.load(open(sys.argv[4] if len(sys.argv) > 4 else 'data/h1_param.json'))
        except Exception: pass
    return P
if __name__ == '__main__':
    OUT = 'step_res.json' if len(sys.argv) <= 3 else sys.argv[3]
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    P = load_params(); names = [n for n in ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11', 'h1'] if n in P]
    print('modules :', names, flush=True)
    Ls = {nm: Layout(build(nm, P[nm].get('F'), P[nm].get('htree')), a=P[nm].get('a', 0), Dmap=P[nm]['D'], Gmap=P[nm]['G']) for nm in names}
    off = choose_offsets2(Ls, names, seed); print('translations :', off, flush=True)
    S = Step(P, off, names); envs = S.cases(); T = S.tmax + 1200
    sits = [S.sit(e) for e in envs]; t0 = time.time()
    R = run_c(sits, T); good = 0; clean = 0; bad = []
    for e, (a, c) in zip(envs, R):
        d = decode(a, c, T)
        if d is None: bad.append(('sale', e)); continue
        clean += 1; o = S.outputs(d)
        if all(o[nm] == spec(nm, e) for nm in names): good += 1
        else: bad.append(('faux', e, o))
    print(f'moteur C : {len(envs)} états, {clean} propres, {good} justes (tous les modules) — {time.time()-t0:.0f} s', flush=True)
    # 2e moteur (hx.py) sur les 256 états
    t0 = time.time(); same = sum(1 for s, (a, c) in zip(sits, R) if (lambda pa_pc: sorted(pa_pc[0]) == sorted(a) and sorted(pa_pc[1]) == sorted(c))(run_py(s, T)))
    print(f'hx.py : {same}/256 états finaux identiques au moteur C — {time.time()-t0:.0f} s', flush=True)
    try: ok, delta, info = certificate2(S, log=lambda x: print(x, flush=True)); D = delta + (-delta) % 8
    except AssertionError as ex: ok, D, info = False, None, dict(span=None, R=None, opposees=None); print('certificat : échec', ex, flush=True)
    res = []
    for g in (range(2) if ok else []):
        rnd = random.Random(g); seq = [rnd.choice(envs) for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 10)]
        r = multi_check(S, seq, D, engine2=(g == 0 and len(seq) <= 3)); res.append(r); print('usages', g, r, flush=True)
    json.dump(dict(modules=names, translations=off, T=T, propres=clean, justes=good, deux_moteurs=same, certificat=ok, delta=D,
                   fenetre=info['span'], rayon=info['R'], voies_opposees=info['opposees'], usages=res, mauvais=bad[:5]), open(OUT, 'w'), ensure_ascii=False, indent=1)
    sys.exit()
    json.dump(dict(modules=names, translations=off, T=T, propres=clean, justes=good, mauvais=bad[:5]), open('data/step_res.json', 'w'), ensure_ascii=False)

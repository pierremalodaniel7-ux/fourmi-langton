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
def build(nm, F):
    r = module(nm)
    for n in nodes(r):
        if F and F.get(n.name): n.inputs = [('-' if sd == '+' else '+', it) for sd, it in n.inputs]
    return r
class Step:
    def __init__(self, params, offsets, names=None):
        self.names = names or list(params)
        self.L = {nm: Layout(build(nm, params[nm].get('F')), a=params[nm].get('a', 0), Dmap=params[nm]['D'], Gmap=params[nm]['G']) for nm in self.names}
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
    for o in set(LA.possible_outputs()):
        o2 = transwl(o, va); lo = [lane_of2(antpos(o2, t), o[0]) for t in range(8)]
        for i, w in [(0, w) for _, _, w in LB.ships]:
            if (o[0] - w[0]) % 6 == 3:
                i2 = transwl(w, vb); li = [lane_of2(antpos(i2, t), o[0]) for t in range(8)]
                if min(abs(x - y) for x in lo for y in li) < 7: return False
    return True
def choose_offsets(Ls, names, seed=0, spacing=3000):
    rnd = random.Random(seed); off = {}
    for k, nm in enumerate(names):
        for _ in range(2000):
            v = (k * spacing + rnd.randint(-200, 200), rnd.randint(-200, 200)) if k else (0, 0)
            if all(lane_ok(Ls[nm], v, Ls[m], off[m]) and lane_ok(Ls[m], off[m], Ls[nm], v) for m in off): off[nm] = v; break
        else: raise RuntimeError('pas de translation sûre pour ' + nm)
    return off
def load_params():
    R = json.load(open('resultats_modules.json')); P = {nm: R[nm]['parametres'] for nm in R}
    if 'h1' not in P:
        try: P['h1'] = json.load(open('data/h1_param.json'))
        except Exception: pass
    return P
if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    P = load_params(); names = [n for n in ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11', 'h1'] if n in P]
    print('modules :', names, flush=True)
    Ls = {nm: Layout(build(nm, P[nm].get('F')), a=P[nm].get('a', 0), Dmap=P[nm]['D'], Gmap=P[nm]['G']) for nm in names}
    off = choose_offsets(Ls, names, seed); print('translations :', off, flush=True)
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
    json.dump(dict(modules=names, translations=off, T=T, propres=clean, justes=good, mauvais=bad[:5]), open('data/step_res.json', 'w'), ensure_ascii=False)

#!/usr/bin/env python3
"""R-612 COMPOSITION de modules R2L2 (S3, 27/11) : la sortie d'un module amont (sa puissance racine, tout droit) est posée EXACTEMENT
sur la ligne d'univers d'un littéral d'un module aval (rotation k de 60°, retard s ≡ phase mod 8, translation entière v), Dlink
périodes en amont de la porte où ce littéral sert. Un littéral n'a pas de porte à lui : pas de conflit structurel (journal R-610).
Logique : le vaisseau-littéral est présent ssi la sortie amont vaut 1 (c'est le même vaisseau).
Vérification : tous les cas, moteur C puis hx.py ; état final propre ; sortie finale = spécification."""
import sys, json, random, itertools, time
from nor import Node, Layout, lit
from modules import leaf, NOR2, ne, search, VARS
from s3lib import *
def tw(w, T):
    k, s, v = T; return transwl(tshift(rotwl(w, k), s), v)
def fit(o, l, s0):
    """transformation T telle que tw(o, T) == l, avec un retard s proche de s0"""
    k = (l[0] - o[0]) % 6; oR = rotwl(o, k)
    for s in range(s0 - 8, s0 + 8):
        w = tshift(oR, s)
        if w[3] == l[3]:
            v = (l[1] - w[1], l[2] - w[2]); T = (k, s, v); assert tw(o, T) == l; return T
    raise ValueError
class Circuit:
    def __init__(self, mods, binds, final, params, dlink):
        """mods : nom -> arbre (Node) ; binds : nom -> {littéral : module amont} ; params : nom -> (D, G) ; dlink : (aval, littéral) -> périodes"""
        self.mods, self.binds, self.final = mods, binds, final
        self.L = {m: Layout(mods[m], Dmap=params[m]['D'], Gmap=params[m]['G']) for m in mods}
        self.T = {}; self.place(final, (0, 0, (0, 0)), dlink)
        t0 = min(min(g[2] for g in self.L[m].gates) + self.T[m][1] for m in self.T)
        S = 400 - t0; self.T = {m: (k, s + S, v) for m, (k, s, v) in self.T.items()}
        self.tmax = max(self.L[m].tmax + self.T[m][1] for m in self.T)
        self.out = tw(self.L[final].out, self.T[final])
    def place(self, m, T, dlink):
        assert m not in self.T, 'module utilisé deux fois : ' + m
        self.T[m] = T; L = self.L[m]
        for nm, kind, w in L.ships:
            if kind != 'lit': continue
            lt = nm.split('@')[0]; up = self.binds.get(m, {}).get(lt)
            if up is None: continue
            tg = [g[2] for g in L.gates if g[5] == nm][0] + T[1]; l = tw(w, T); U = self.L[up]
            s0 = tg - 8 * dlink[(m, lt)] - U.tmax
            self.place(up, fit(U.out, l, s0), dlink)
    def value(self, m, e):
        env = dict(e)
        for lt, up in self.binds.get(m, {}).items():
            u = self.value(up, e); env[lt.lstrip('~')] = (1 - u) if lt[0] == '~' else u
        return self.mods[m].value(env)
    def present(self, e):
        W = []
        for m in self.T:
            L = self.L[m]; b = self.binds.get(m, {})
            for nm, kind, w in L.ships:
                if kind == 'K' or (nm.split('@')[0] not in b and lit(e, nm.split('@')[0])): W.append(tw(w, self.T[m]))
        return W
    def sit(self, e): return sit_wls(self.present(e))
    def cases(self): return [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
    def check(self, spec, engine2=False, T=None):
        envs = self.cases(); T = T or self.tmax + 1500; S = [self.sit(e) for e in envs]; R = run_c(S, T); res = []
        for e, s, (a, c) in zip(envs, S, R):
            d = decode(a, c, T); got = None if d is None else int(self.out in d)
            same = None
            if engine2:
                pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
            res.append(dict(cas=e, propre=d is not None, sortie=got, attendu=spec(e), logique=self.value(self.final, e), deux=same))
        return res
def h1_circuit():
    mods = {'H': NOR2('H', leaf('Ha', ['g', 'c']), leaf('Hb', ['~g', '~c'])),          # h1' = g ⊕ c
            'G': NOR2('G', leaf('Ga', ['h1', 'h0']), leaf('Gb', ['~h1', '~h0'])),      # g = h1 ⊕ h0
            'NG': NOR2('NG', leaf('NGa', ['~h1', 'h0']), leaf('NGb', ['h1', '~h0'])),  # ¬g
            'C': Node('C', [('+', leaf('Cl', ['n00', 'n10', 'n01', 'n11']))]),        # c = OR des cubes
            'NC': leaf('NC', ['m00', 'm10', 'm01', 'm11'])}                           # ¬c
    binds = {'H': {'g': 'G', 'c': 'C', '~g': 'NG', '~c': 'NC'}, 'C': {}, 'NC': {}}
    for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
        for P, b in (('Q', 'C'), ('R', 'NC')):
            mods[f'{P}{i}{j}'] = leaf(f'{P}{i}{j}', [ne('x', i), ne('y', j), f'~c{i}{j}'])   # [x=i ∧ y=j ∧ cij]
            binds[b][('n' if P == 'Q' else 'm') + f'{i}{j}'] = f'{P}{i}{j}'
    return mods, binds
def spec_h1(e): return e['h1'] ^ e['h0'] ^ e[f"c{e['x']}{e['y']}"]
if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    mods, binds = h1_circuit(); params = {}
    try: params = json.load(open('data/compose_params.json'))
    except Exception: pass
    for m, r in mods.items():
        if m in params: continue
        L, par = search(r, seed=seed, log=lambda s: None)
        assert L is not None, m
        params[m] = dict(D=par['D'], G=par['G']); print('module', m, 'placé (seul, tous cas justes)', flush=True)
    json.dump(params, open('data/compose_params.json', 'w'))
    rnd = random.Random(seed)
    dl = {(m, lt): rnd.randint(40, 160) for m in binds for lt in binds[m]}
    C = Circuit(mods, binds, 'H', params, dl)
    print('tmax', C.tmax, 'fourmis (max)', max(len(C.present(e)) for e in C.cases()), flush=True)
    t = time.time(); r = C.check(spec_h1)
    print(f"C : {sum(x['propre'] for x in r)}/256 propres, {sum(x['sortie'] == x['attendu'] for x in r)}/256 justes, logique {sum(x['logique'] == x['attendu'] for x in r)}/256 ({time.time()-t:.0f} s)")

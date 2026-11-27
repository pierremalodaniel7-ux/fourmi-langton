#!/usr/bin/env python3
"""R-609 BIBLIOTHÈQUE DE PORTES R2L2 RÉUTILISABLES (S3, 26/11 soir) — format commun, vérification, certificat, 20 usages.
Format d'une porte (bibliotheque_portes.json) :
  vaisseaux : liste ORDONNÉE (ordre de jeu) de [nom, rôle, ligne d'univers] ; rôle = 'K' (constant, toujours là) ou nom d'entrée
              (vaisseau présent ssi l'entrée vaut 1). Ligne d'univers (r, gx, gy, ph) : à t = 0, germe ship(r, (gx,gy)) de hx.py avancé
              de ph pas ; à l'instant t : germe + d_r·((ph+t)//8), phase (ph+t) % 8 (s3lib.at).
  sorties   : nom -> [liste de lignes d'univers, formule] : la sortie vaut 1 ssi un vaisseau suit l'une de ces lignes à la fin.
  horaire   : instants des chocs (pas) ; T = durée de simulation conseillée ; delta = écart (pas) entre usages pour la réutilisation.
Pour poser une porte ailleurs : tourner (rotwl, multiples de 60°), translater (transwl), retarder (tshift) TOUTES ses lignes d'univers.
Usage : python3 portes_lib.py"""
import json, random, itertools, sys
from s3lib import *
from nor import Node, Layout, gate
from reuse import certificate
class Circuit:
    def __init__(self, nom, ships, outputs, gates_t, vars_):
        self.nom, self.ships, self.outputs, self.gates_t, self.vars = nom, ships, outputs, gates_t, vars_
        self.tmax = max(gates_t)
    def cases(self): return [dict(zip(self.vars, b)) for b in itertools.product((0, 1), repeat=len(self.vars))]
    def present(self, e): return [w for nm, role, w in self.ships if role == 'K' or e[role] == 1]
    def sit(self, e): return sit_wls(self.present(e))
    def read(self, d, shift=0):
        S = set(d or [])
        return {o: int(any(tshift(w, shift) in S for w in ws)) for o, (ws, f) in self.outputs.items()}
    def want(self, e): return {o: int(eval(f, {}, dict(e))) for o, (ws, f) in self.outputs.items()}
    def check(self, engine2=True):
        T = self.tmax + 1200; E = self.cases(); S = [self.sit(e) for e in E]; R = run_c(S, T); res = []
        for e, s, (a, c) in zip(E, S, R):
            d = decode(a, c, T); same = None
            if engine2:
                pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
            res.append((e, d is not None, self.read(d) == self.want(e), same))
        return res
    def multi(self, seq, D, engine2=False):
        T = self.tmax + (len(seq) - 1) * D + 1200
        W = []
        for u, e in enumerate(seq): W += [tshift(w, u * D) for w in self.present(e)]
        s = sit_wls(W); a, c = run_c([s], T)[0]; d = decode(a, c, T)
        union = []
        for u, (a1, c1) in enumerate(run_c([self.sit(e) for e in seq], T)):
            union += [tshift(w, u * D) for w in decode(a1, c1, T)]
        sup = d is not None and sorted(d) == sorted(union)
        good = sum(self.read(d, u * D) == self.want(e) for u, e in enumerate(seq))
        same = None
        if engine2:
            pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
        return sup, good, same, len(W)
    def to_json(self, extra):
        return dict(nom=self.nom, entrees=self.vars,
                    vaisseaux=[[n, r, list(w)] for n, r, w in self.ships],
                    sorties={o: [[list(w) for w in ws], f] for o, (ws, f) in self.outputs.items()},
                    horaire=sorted(self.gates_t), **extra)
def from_layout(nom, L, extra_outputs=None, out_name='S', formula=None):
    ships = [(nm, 'K' if k == 'K' else nm.split('@')[0].lstrip('~'), w) for nm, k, w in L.ships]
    assert all(not nm.startswith('~') for nm, k, w in L.ships if k == 'lit'), 'littéral négatif : pas une porte à une seule entrée par variable'
    outs = {out_name: ([L.out], formula)}
    outs.update(extra_outputs or {})
    return Circuit(nom, ships, outs, [g[2] for g in L.gates], L.vars)
def lib():
    P = []
    # NON(x) = 1 constant K ; même germe que COPIE
    L = Layout(Node('K', [('+', 'x')]))
    g = L.gates[0]
    P.append(from_layout('NON', L, formula='1 - x', out_name='non_x'))
    P.append(from_layout('COPIE', L, formula='1 - x', out_name='non_x', extra_outputs={'x_1': ([g[3]], 'x'), 'x_2': ([g[4]], 'x')}))
    # ET direct (sans constant) : x (dir 0) dévie y (dir 1) ; sorties : x∧y sur 2 routes, x∧¬y, ¬x∧y
    P0 = (0, -51, 51, 6); W, oA, oB, tg = gate(P0, '+', 700)
    ships = [('x', 'x', P0), ('y', 'y', W)]
    P.append(Circuit('ET', ships, {'x_et_y': ([oB], 'x * y'), 'x_et_y_bis': ([oA], 'x * y'), 'x_sans_y': ([P0], 'x * (1 - y)'),
                                   'y_sans_x': ([W], 'y * (1 - x)')}, [tg], ['x', 'y']))
    # NOR(x, y) = 1 constant ; OU = NON(NOR) = 2 constants ; ET avec constants = NOR(NON x, NON y) = 3 constants
    P.append(from_layout('NOR', Layout(Node('K', [('+', 'x'), ('-', 'y')]), G=10), formula='int(not (x or y))'))
    P.append(from_layout('OU', Layout(Node('K2', [('+', Node('K1', [('+', 'x'), ('-', 'y')]))]), D=12), formula='int(x or y)'))
    P.append(from_layout('ET_par_NOR', Layout(Node('K3', [('+', Node('K1', [('+', 'x')])), ('-', Node('K2', [('+', 'y')]))]), D=20, G=10),
                         formula='x * y'))
    # XOR : demi-additionneur réutilisable R-337 (classe paire, ../resumes/demi_additionneur_reutilisable.json), ordre K3, K2, B, A
    H = json.load(open(os.path.join(HERE, '..', 'resumes', 'demi_additionneur_reutilisable.json')))
    pieces = [('K3', 'K', H['K3']), ('K2', 'K', H['K2']), ('B', 'b', [[0, 0, 4], [[1, 0]]]), ('A', 'a', [[30, -56, 0], [[29, -55]]])]
    ships = [(n, r, decode([tuple(p[0])], [tuple(c) for c in p[1]], 0)[0]) for n, r, p in pieces]
    X = Circuit('XOR_R337', ships, {}, [400], ['a', 'b'])
    T = 4000; outs = {}
    for e in X.cases():
        a, c = run_c([X.sit(e)], T)[0]; outs[tuple(e.values())] = decode(a, c, T)
    # S : vaisseaux de direction 0 sur la voie 0 (cas (1,0) et (0,1)) ; C : celui présent seulement dans (1,1)
    S = sorted({w for k in [(1, 0), (0, 1)] for w in outs[k] if w[0] == 0 and w[1] + w[2] == 0
                and w not in outs[(0, 0)] and w not in outs[(1, 1)]})
    Cw = sorted(set(outs[(1, 1)]) - set(outs[(1, 0)]) - set(outs[(0, 1)]) - set(outs[(0, 0)]))
    X.outputs = {'S': (S, '(a + b) % 2'), 'C': (Cw[:1], 'a * b')}; X.tmax = 2800
    P.append(X)
    return P
if __name__ == '__main__':
    out = []
    for p in lib():
        r = p.check(engine2=True)
        n_ok = sum(1 for x in r if x[1] and x[2]); n2 = sum(1 for x in r if x[3])
        ok, delta, info = certificate(p, T=p.tmax + 1200, log=lambda s: None)
        D = delta + (-delta) % 8
        res20 = []
        for seed in range(3):
            rnd = random.Random(seed); seq = [rnd.choice(p.cases()) for _ in range(20)]
            sup, good, same, nf = p.multi(seq, D, engine2=(seed == 0))
            res20.append(dict(graine=seed, superposition=sup, justes=good, deux_moteurs=same, fourmis=nf))
        nK = sum(1 for _, r_, _ in p.ships if r_ == 'K')
        print(f"{p.nom:12s} {len(p.ships)} vaisseaux dont {nK} constants ; {n_ok}/{len(r)} cas justes et propres, 2 moteurs {n2}/{len(r)} ; "
              f"certificat {'OK' if ok else 'ÉCHEC'} (routes opposées à ≥ {info['opposees']} voies, Δ = {D} pas) ; 20 usages : "
              + ', '.join(f"{x['justes']}/20{' sup' if x['superposition'] else ''}" for x in res20) + f" ; 2 moteurs (20 usages) {res20[0]['deux_moteurs']}", flush=True)
        out.append(p.to_json(dict(constants=nK, cas_justes=f'{n_ok}/{len(r)}', deux_moteurs=f'{n2}/{len(r)}', certificat=ok, delta=D,
                                  T=p.tmax + 1200, fenetre=info['span'], rayon=info['R'], voies_opposees=info['opposees'], usages20=res20)))
    json.dump(out, open('bibliotheque_portes.json', 'w'), indent=1, ensure_ascii=False)

"""R-605 Compilateur « arbre de NOR » R2L2 (S3, 26/11 soir).
Brique unique : le choc DÉVIANT « vers l'extérieur » de 2 vaisseaux à 60° (catalogue data/chocs_pairs.json, R-600) :
  puissance K (direction a) + partenaire (direction a+1) -> K part en a+2, le partenaire en a−1 ;        (côté +)
  puissance K (direction a) + partenaire (direction a−1) -> K part en a−2, le partenaire en a+1 ;        (côté −)
  (et de face, direction a+3, utilisé seulement comme 1re entrée).  Même issue dans les 2 ordres de jeu, pour τ = 2…6 (marge ±2 pas).
Nœud = une puissance K (vaisseau constant) ; ses entrées (littéraux ou sous-nœuds) la croisent l'une après l'autre ; la 1re entrée
présente la dévie : K continue tout droit ssi AUCUNE entrée n'est présente -> K = NOR(entrées). Sortie d'un nœud = K tout droit.
Convention d'entrée (comme le compilateur LLR R-62) : un vaisseau par littéral VRAI et par usage (« x » si x = 1, « ~x » si x = 0).
Règles de placement (démontrées dans le journal, R-606) : sur une même ligne d'arrivée, des littéraux en train, OU un seul sous-nœud ;
écart ≥ G périodes entre deux portes d'une même puissance (G ≥ 7 : les sorties d'une porte sont alors à ≥ 7 voies des entrées voisines)."""
from s3lib import *
import itertools
# géométries de base (puissance B = direction 0) : A = partenaire ; sorties (A', B') ; choc vers t ≈ 190
BASE = {
    '+': dict(B=(0, -25, 25, 0), A=(1, -25, 0, 4), oA=(5, -2, 25, 2), oB=(2, -1, -23, 6)),
    '-': dict(B=(0, -25, 25, 0), A=(5, 0, 26, 4), oA=(1, -24, 1, 2), oB=(4, 24, 2, 6)),
    'H': dict(B=(0, -25, 25, 0), A=(3, 26, -25, 4), oA=(1, -24, -1, 2), oB=(2, 0, -25, 6)),
}
TC = 190
def gate(P, side, t):
    """partenaire (et sorties) pour que le partenaire heurte la puissance P (ligne d'univers) vers l'instant t, selon BASE[side]"""
    b = BASE[side]; a = P[0]
    B0, A0, oA0, oB0 = (rotwl(b[k], a) for k in ('B', 'A', 'oA', 'oB'))
    for s in range(t - TC - 4, t - TC + 4):
        Bs = tshift(B0, s)
        if Bs[3] == P[3]:
            v = (P[1] - Bs[1], P[2] - Bs[2])
            f = lambda w: transwl(tshift(w, s), v)
            assert f(B0) == P
            return f(A0), f(oA0), f(oB0), s + TC
    raise ValueError
class Node:
    def __init__(self, name, inputs):
        """inputs : liste ordonnée dans le temps (1re = la plus ancienne) de (côté, littéral 'x' / '~x' ou Node)"""
        self.name = name; self.inputs = inputs
    def value(self, env):
        return int(not any(lit(env, it) if isinstance(it, str) else it.value(env) for _, it in self.inputs))
def lit(env, s): return env[s[1:]] == 0 if s[0] == '~' else env[s] == 1
class Layout:
    def __init__(self, root, a=0, G=10, D=12, Dmap=None, Gmap=None):
        """root : Node ; a : direction de la puissance racine ; G : écart (périodes) entre portes d'une puissance ;
        D : écart (périodes) entre la dernière porte d'un sous-nœud et sa porte chez le parent (Dmap / Gmap : valeurs par nœud)"""
        self.root = root; self.ships = []; self.gates = []
        self.G, self.D, self.Dmap, self.Gmap = G, D, Dmap or {}, Gmap or {}
        P = (a, 0, 0, 0)
        self._place(root, P, 0)
        tmin = min(g[2] for g in self.gates)
        self.shift = 400 - tmin
        self.ships = [(nm, kind, tshift(w, self.shift)) for nm, kind, w in self.ships]
        self.gates = [(g[0], g[1], g[2] + self.shift, tshift(g[3], self.shift), tshift(g[4], self.shift)) for g in self.gates]
        self.out = [w for nm, kind, w in self.ships if nm == root.name][0]
        self.vars = sorted({it.lstrip('~') for nm, kind, w in self.ships if kind == 'lit' for it in [nm.split('@')[0]]})
        self.tmax = max(g[2] for g in self.gates)
    def _place(self, node, P, tend):
        self.ships.append((node.name, 'K', P))
        G = self.Gmap.get(node.name, self.G); n = len(node.inputs)
        for i, (side, it) in enumerate(node.inputs):
            t = tend - 8 * G * (n - 1 - i)
            W, oA, oB, tg = gate(P, side, t)
            self.gates.append((node.name, side, tg, oA, oB))
            if isinstance(it, str):
                self.ships.append((f'{it}@{node.name}{i}', 'lit', W))
            else:
                self._place(it, W, tg - 8 * self.Dmap.get(it.name, self.D))
    def cases(self):
        return [dict(zip(self.vars, b)) for b in itertools.product((0, 1), repeat=len(self.vars))]
    def present(self, env):
        return [w for nm, kind, w in self.ships if kind == 'K' or lit(env, nm.split('@')[0])]
    def sit(self, env): return sit_wls(self.present(env))
    def check(self, envs=None, T=None, engine2=False):
        """simule chaque cas : (cas, état propre ?, sortie lue, attendue, 2 moteurs identiques)"""
        envs = envs or self.cases(); T = T or self.tmax + 1200
        S = [self.sit(e) for e in envs]; R = run_c(S, T); out = []
        for e, s, (a, c) in zip(envs, S, R):
            d = decode(a, c, T); got = None if d is None else int(self.out in d)
            same = None
            if engine2:
                pa, pc = run_py(s, T); same = sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
            out.append((e, d is not None, got, self.root.value(e), same))
        return out
    def possible_outputs(self):
        """sur-ensemble des routes sortantes : toutes les entrées (tout droit) et toutes les sorties de portes"""
        return [w for _, _, w in self.ships] + [g[3] for g in self.gates] + [g[4] for g in self.gates]
    def opposed(self):
        """plus petit écart de voie entre une route sortante possible et une route entrante opposée (critère (c) du lemme)"""
        def lanes(w):
            return [lane_of(antpos(w, t), w[0]) for t in range(8)]
        worst, bad = 99, []
        ins = [w for _, _, w in self.ships]
        for o in set(self.possible_outputs()):
            lo = [lane_of2(antpos(o, t), o[0]) for t in range(8)]
            for i in ins:
                if (o[0] - i[0]) % 6 == 3:
                    li = [lane_of2(antpos(i, t), o[0]) for t in range(8)]
                    m = min(abs(x - y) for x in lo for y in li)
                    if m < worst: worst = m
                    if m < 7: bad.append((o, i))
        return worst, bad
def lane_of2(p, r):
    X, Y = rot(p, -r % 6); return X + Y

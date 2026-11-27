#!/usr/bin/env python3
"""R-623 N PAS ENCHAÎNÉS de la petite fourmi en UN germe, à taille LINÉAIRE en N (S3/T1, 27/11).
Architecture : le germe du pas (modules R-607 vérifiés, un par bit d'un sous-système fermé) est répété N fois, l'usage u translaté de
u·V et retardé de u·Δ. L'usage 0 lit les vaisseaux-littéraux de l'état initial (comme R-617) ; l'usage u ≥ 1 n'a AUCUN littéral dans le
germe : chaque littéral w / ¬w est le vaisseau de SORTIE du module w de l'usage u−1, DIFFUSÉ (chaîne de portes COPIE : une porte donne
2 copies + 1 négation) puis AMENÉ sur la ligne du littéral par 2 à 4 virages (route, R-622). Le schéma des routes est le même pour
tous les usages (périodique), donc taille du germe = N × (modules + diffusion + routes) + littéraux initiaux.
Sous-systèmes fermés (sur le tore 2×2, R-619) : 'h0' ; 'pos' = h0, x, y ; '7' = h0, x, y, c00..c11 (tout sauf h1).
Recherche : placement des modules d'un pas, V, Δ, portes de diffusion, choix des routes (glouton sur les conflits du modèle circ.py,
puis descente). Vérification : simulation des 2^k cas (2 moteurs) : état final = modèle, et chaque valeur intermédiaire comparée
à la vraie fourmi (R-61, modules.spec) pas par pas.
Usage : python3 chainN.py SOUS graine secondes  -> data/chainN_<SOUS>_<graine>.json ; python3 chainN.py SOUS verif fichier.json N"""
import sys, os, json, random, time, itertools, math
from circ import *
from modules import module, spec, VARS, nodes
from nor import Layout
SUBS = {'h0': ['h0'], 'pos': ['h0', 'x', 'y'], '7': ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11']}
RES = json.load(open('resultats_modules.json'))
def mod_layout(v):
    p = RES[v]['parametres']; return Layout(module(v), a=p.get('a', 0), Dmap=p['D'], Gmap=p['G'])
def F(e):
    return {v: spec(v, e) for v in VARS}
def xf(w, off, u, V, Dt):
    """ligne d'univers w du module (décalage off = (dx, dy, dt)) à l'usage u"""
    return transwl(tshift(w, off[2] + u * Dt), (off[0] + u * V[0], off[1] + u * V[1]))
class Design:
    def __init__(self, sub, off, V, Dt, fan, choice):
        """off[v] = (dx, dy, dt) ; fan[v] = [(côté, k), ...] portes de diffusion ; choice[(v, j)] = indice de route du j-ième usage de v"""
        self.sub, self.off, self.V, self.Dt, self.fan, self.choice = sub, off, V, Dt, fan, choice
        self.L = {v: mod_layout(v) for v in sub}
        self.lits = {v: [] for v in sub}     # demandes : (module, nom du littéral, ligne à l'usage 0, instant de porte, polarité)
        for m in sub:
            L = self.L[m]; W = {nm: w for nm, k, w in L.ships}
            for node, side, tg, oA, oB, pn in L.gates:
                if '@' in pn:
                    lit = pn.split('@')[0]; v = lit.lstrip('~')
                    self.lits[v].append((m, pn, W[pn], tg, 1 if lit[0] == '~' else 0))
        self.routes = {}
    def ports(self, v, u):
        """sortie du module v à l'usage u, puis chaîne de diffusion : liste de ports (id, ligne, dispo, polarité) + portes"""
        L = self.L[v]; o = self.off[v]; sid = f'u{u}:{L.root.name}'; line = xf(L.out, o, u, self.V, self.Dt)
        tav = L.tmax + o[2] + u * self.Dt + 60
        gates = []; ports = []; trunk = (sid, line, tav, 0)
        for j, (side, k) in enumerate(self.fan[v]):
            i, A, ta, p = trunk; kk = first_k(A, side, ta + 120) + k
            K, oA, oB, tc = turn(A, side, kk); kid = f'u{u}:F{v}{j}'
            gates.append((kid, K, tc, i, A, oA, oB))
            ports.append((i, oA, tc, p)); ports.append((kid, K, tc, 1 - p)); trunk = (kid, oB, tc, p)
        ports.append(trunk)
        return ports, gates
    def targets(self, v, u):
        o = {m: self.off[m] for m in self.sub}
        return [(m, pn, xf(W, o[m], u, self.V, self.Dt), tg + o[m][2] + u * self.Dt, pol) for m, pn, W, tg, pol in self.lits[v]]
    def assign(self, v, ports, tg):
        """port pour chaque demande : polarités d'abord (le 1er port pol 0 libre pour une demande positive, etc.)"""
        free = list(range(len(ports))); out = []
        for m, pn, W, t, pol in tg:
            best = next((i for i in free if ports[i][3] == pol), free[0]); free.remove(best); out.append(best)
        return out
    def assign_ok(self, v, ports, tg):
        """affectation demandes -> ports pour laquelle chaque demande a au moins une route (polarités assorties d'abord)"""
        a0 = self.assign(v, ports, tg)
        order = [a0] + [list(p) for p in itertools.permutations(range(len(ports)), len(tg)) if list(p) != a0]
        for asg in order[:200]:
            if all(self.candidates(v, j, ports[pi], t) for j, (t, pi) in enumerate(zip(tg, asg))): return asg
        return None
    def candidates(self, v, j, port, tgt, maxn=40):
        key = (port[1], port[2], port[3], tgt[2], tgt[3], tgt[4])
        if key not in self.routes:
            sols = route(port[1], port[2], tgt[2], tgt[3], pol=port[3] ^ tgt[4], kr=40, maxsol=300)
            self.routes[key] = sols[:maxn] if len(sols) <= maxn else [sols[int(i * (len(sols) - 1) / (maxn - 1))] for i in range(maxn)]
        return self.routes[key]
    def circuit(self, N, choice=None):
        """circuit complet à N usages (choice : indices de route ; défaut self.choice) ; None si une route manque"""
        choice = self.choice if choice is None else choice
        C = Circ(self.sub); C.lit_of = {}
        arrive = {}   # (u, module, pn) -> (id, ligne) du signal arrivé
        for u in range(1, N):
            for v in self.sub:
                ports, gates = self.ports(v, u - 1); tg = self.targets(v, u); asg = self.assign_ok(v, ports, tg)
                if asg is None: return None
                for (kid, K, tc, i, A, oA, oB) in gates:
                    C.add_ship(K, name=kid); C.add_gate(tc, kid, K, i, A, oA, oB, 'copie')
                for j, (t, pi) in enumerate(zip(tg, asg)):
                    c = self.candidates(v, j, ports[pi], t)
                    if not c: return None
                    _, seq, ks, out = c[choice.get((v, j), 0) % len(c)]
                    cur_id, cur = ports[pi][0], ports[pi][1]
                    for q, ((side, oo), (K, w, sd, tt, oA, oB)) in enumerate(zip(seq, out)):
                        kid = f'u{u}:R{v}{j}_{q}'; C.add_ship(K, name=kid); C.add_gate(tt, kid, K, cur_id, cur, oA, oB, 'virage')
                        if oo == 1: cur = oA
                        elif oo == 2: cur_id, cur = kid, oB
                        else: cur_id, cur = kid, K
                    assert cur == t[2]; arrive[(u, t[0], t[1])] = (cur_id, cur)
        for u in range(N):
            for m in self.sub:
                L = self.L[m]; o = self.off[m]; W = {nm: w for nm, k, w in L.ships}
                for nm, kind, w in L.ships:
                    if kind == 'K': C.add_ship(xf(w, o, u, self.V, self.Dt), name=f'u{u}:{nm}')
                    elif u == 0:
                        lit = nm.split('@')[0]; C.add_ship(xf(w, o, 0, self.V, self.Dt), C.mask_of(lambda e, l=lit: (e[l[1:]] == 0) if l[0] == '~' else (e[l] == 1)), name=f'u0:{nm}')
                for node, side, tg, oA, oB, pn in L.gates:
                    t = tg + o[2] + u * self.Dt; Kl = xf(W[node], o, u, self.V, self.Dt)
                    if '@' in pn and u > 0: pid, pl = arrive[(u, m, pn)]
                    else: pid, pl = f'u{u}:{pn}', xf(W[pn], o, u, self.V, self.Dt)
                    C.add_gate(t, f'u{u}:{node}', Kl, pid, pl, xf(oA, o, u, self.V, self.Dt), xf(oB, o, u, self.V, self.Dt), 'module')
        T = max(g[0] for g in C.gates) + 1500
        C.compile(T); C.N = N; return C
    def outline(self, v, u):
        L = self.L[v]; o = self.off[v]; return f'u{u}:{L.root.name}', xf(L.out, o, u, self.V, self.Dt), L.tmax + o[2] + u * self.Dt + 30
    def logic_ok(self, C):
        """le modèle donne-t-il, à chaque usage u, la sortie v = (F^(u+1)(e))[v] ? (avant la diffusion)"""
        bad = 0
        for b, e in enumerate(C.cases):
            full = {w: 0 for w in VARS}; full.update(e); s = full
            for u in range(C.N):
                s = F(s)
                for v in self.sub:
                    i, w, t = self.outline(v, u)
                    if (C.present(i, w, t) >> b & 1) != s[v]: bad += 1
        return bad
    def size(self, C): return len(C.ships)
    def to_json(self):
        return dict(sub=self.sub, off=self.off, V=self.V, Dt=self.Dt, fan=self.fan, choice={f'{v}|{j}': c for (v, j), c in self.choice.items()})
def from_json(d):
    return Design(d['sub'], {k: tuple(v) for k, v in d['off'].items()}, tuple(d['V']), d['Dt'], {k: [tuple(x) for x in v] for k, v in d['fan'].items()},
                  {(k.split('|')[0], int(k.split('|')[1])): c for k, c in d['choice'].items()})
def nfan(d): return max(0, math.ceil((d - 1) / 2))
def random_design(sub, rnd, box=400):
    off = {}; c0 = cls(mod_layout(sub[0]).out)
    for k, v in enumerate(sub):   # classes de phase alignées (cls − dt identique pour tous les modules) : routes à déviations paires
        dt = 0 if k == 0 else rnd.randint(-200, 200); dt += (cls(mod_layout(v).out) - c0 - dt) % 8
        off[v] = (0, 0, 0) if k == 0 else (rnd.randint(-box, box), rnd.randint(-box, box), dt)
    ang = rnd.random() * 2 * math.pi; R = rnd.randint(600, 1400); V = (int(R * math.cos(ang)), int(R * math.sin(ang)))
    Dt = int(8 * (abs(V[0]) + abs(V[1]) + abs(V[0] + V[1])) / 2 * rnd.uniform(1.3, 2.0)) + 3000; Dt += (4 - Dt) % 8   # Δ ≡ 4 (mod 8)
    D0 = Design(sub, off, V, Dt, {}, {})
    fan = {v: [(rnd.choice('+-H'), rnd.randint(0, 40)) for _ in range(nfan(len(D0.lits[v])))] for v in sub}
    return Design(sub, off, V, Dt, fan, {})
def score(D, N=int(os.environ.get("NS", 4))):
    C = D.circuit(N)
    if C is None: return 10 ** 6, None
    return len(C.conflicts()), C
def greedy(D, N=int(os.environ.get("NS", 4)), rnd=None):
    """choix des routes une par une : pour chaque demande, l'indice qui minimise les conflits (les autres à leur valeur courante)"""
    best, C = score(D, N)
    if C is None: return best, C
    keys = [(v, j) for v in D.sub for j in range(len(D.lits[v]))]
    for key in keys:
        for c in range(0, 40, 3):
            ch = dict(D.choice); ch[key] = c; C2 = D.circuit(N, ch)
            if C2 is None: continue
            s = len(C2.conflicts())
            if s < best: best, D.choice, C = s, ch, C2
        if best == 0: break
    return best, C
if __name__ == '__main__':
    sub = SUBS[sys.argv[1]]
    if sys.argv[2] == 'verif':
        d = json.load(open(sys.argv[3])); D = from_json(d['design']); N = int(sys.argv[4]); e2 = len(sys.argv) > 5
        t0 = time.time(); C = D.circuit(N); cf = C.conflicts()
        print(f'N={N} : {len(C.ships)} vaisseaux dans le germe, {len(C.gates)} portes, T={C.T}, conflits du modèle {len(cf)}, logique fausse {D.logic_ok(C)}', flush=True)
        r = C.check(engine2=e2)
        print(f'   simulation : {sum(x[1] for x in r)}/{len(r)} états finaux = modèle ; 2 moteurs : {sum(1 for x in r if x[2])}/{len(r) if e2 else 0} — {time.time()-t0:.0f} s', flush=True)
        sys.exit()
    seed, secs = int(sys.argv[2]), float(sys.argv[3]); rnd = random.Random(seed); t0 = time.time(); best = None
    log = open(f'data/chainN_{sys.argv[1]}_{seed}.log', 'a')
    while time.time() - t0 < secs:
        D = random_design(sub, rnd); s, C = greedy(D)
        print(f'{time.time()-t0:.0f}s essai : conflits {s} (V {D.V}, Δ {D.Dt})', file=log, flush=True)
        if C is None: continue
        if best is None or s < best[0]:
            best = (s, D); json.dump(dict(conflits=s, design=D.to_json()), open(f'data/chainN_{sys.argv[1]}_{seed}.json', 'w'))
        if s == 0:
            r = C.check(); ok = sum(x[1] for x in r)
            print(f'   N={C.N} simulation : {ok}/{len(r)} = modèle ; logique fausse {D.logic_ok(C)}', file=log, flush=True)
            if ok == len(r): json.dump(dict(conflits=s, design=D.to_json()), open(f'data/chainN_{sys.argv[1]}_{seed}_OK.json', 'w')); break

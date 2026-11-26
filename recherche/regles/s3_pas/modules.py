#!/usr/bin/env python3
"""R-607 Le pas de la petite fourmi RL sur le tore 2×2 (R-61), module par module, en arbres de NOR R2L2 (nor.py).
État 8 bits : c00 c10 c01 c11 x y h1 h0.  h0' = ¬h0 ; x' = x ⊕ ¬h0 ; y' = y ⊕ h0 ; cij' = cij ⊕ [x=i ∧ y=j] ; h1' = h1 ⊕ h0 ⊕ c (case lue).
Chaque module : arbre de NOR -> recherche de longueurs (D, G par nœud) telles que (1) aucun couple de routes opposées à < 7 voies (lemme R-606),
(2) tous les cas justes et propres ; puis 2 moteurs sur tous les cas, certificat, 20 usages au même endroit (2 moteurs).
Usage : python3 modules.py [nom …]   (noms : h0 x y c00 c10 c01 c11 h1)"""
import sys, json, random, time
from nor import *
from reuse import certificate, check_multi
def ne(v, i): return v if i == 0 else '~' + v          # littéral « v ≠ i »
def eq(v, i): return '~' + v if i == 0 else v          # littéral « v = i »
def neg(l): return l[1:] if l[0] == '~' else '~' + l
def NOT(name, child, side='+'): return Node(name, [(side, child)])
def NOR2(name, a, b): return Node(name, [('+', a), ('-', b)])
def leaf(name, lits):
    """NOR de littéraux : en train, alternés sur les 2 côtés"""
    return Node(name, [('+' if k % 2 == 0 else '-', l) for k, l in enumerate(lits)])
def OR4(name, t):            # NOR(t0, t1, t2, t3) = NOR(NOT(NOR(t0,t1)), NOT(NOR(t2,t3)))  (sortie = NOR des 4)
    return NOR2(name, NOT(name + 'a', NOR2(name + 'A', t[0], t[1])), NOT(name + 'b', NOR2(name + 'B', t[2], t[3])))
def module(nm):
    if nm == 'h0': return Node('h0p', [('+', 'h0')])
    if nm == 'x': return NOR2('xp', leaf('xs1', ['~x', 'h0']), leaf('xs2', ['x', '~h0']))
    if nm == 'y': return NOR2('yp', leaf('ys1', ['~y', '~h0']), leaf('ys2', ['y', 'h0']))
    if nm[0] == 'c':
        i, j = int(nm[1]), int(nm[2]); c = f'c{i}{j}'
        t1 = leaf(nm + 't', ['~' + c, ne('x', i), ne('y', j)])
        m = leaf(nm + 'm', [ne('x', i), ne('y', j)])
        u = Node(nm + 'u', [('+', c), ('-', m)])
        return NOR2(nm + 'p', t1, u)
    if nm == 'h1':
        Ng = NOR2('Ng', leaf('g1', ['~h1', 'h0']), leaf('g2', ['h1', '~h0']))            # ¬g
        Pg = NOR2('Pg', leaf('k1', ['~h1', '~h0']), leaf('k2', ['h1', 'h0']))            # g
        Nc = OR4('Nc', [leaf(f'n{i}{j}', [ne('x', i), ne('y', j), f'~c{i}{j}']) for i, j in ((0, 0), (1, 0), (0, 1), (1, 1))])   # ¬c
        Pc = OR4('Pc', [leaf(f'p{i}{j}', [ne('x', i), ne('y', j), f'c{i}{j}']) for i, j in ((0, 0), (1, 0), (0, 1), (1, 1))])    # c
        A = NOR2('A', Ng, Nc); B = NOR2('B', Pg, Pc)
        return NOR2('h1p', A, B)
def spec(nm, e):
    """valeur attendue (R-61) à partir de l'état complet e"""
    if nm == 'h0': return 1 - e['h0']
    if nm == 'x': return e['x'] ^ (1 - e['h0'])
    if nm == 'y': return e['y'] ^ e['h0']
    if nm[0] == 'c':
        i, j = int(nm[1]), int(nm[2]); return e[f'c{i}{j}'] ^ int(e['x'] == i and e['y'] == j)
    if nm == 'h1': return e['h1'] ^ e['h0'] ^ e[f"c{e['x']}{e['y']}"]
def nodes(n):
    yield n
    for _, it in n.inputs:
        if not isinstance(it, str): yield from nodes(it)
def search(root, seed=0, tries=400, log=print, a=0):
    rnd = random.Random(seed); names = [n.name for n in nodes(root)]
    for k in range(tries):
        Dm = {n: rnd.randint(8, 40) for n in names}; Gm = {n: rnd.randint(8, 16) for n in names}
        L = Layout(root, a=a, Dmap=Dm, Gmap=Gm)
        w, bad = L.opposed()
        if w < 7: continue
        r = L.check()
        ok = sum(1 for x in r if x[1] and x[2] == x[3])
        if ok == len(r):
            log(f'  essai {k} : {ok}/{len(r)} justes et propres, routes opposées à ≥ {w} voies'); return L, dict(D=Dm, G=Gm, a=a, essai=k)
    return None, None
ALL = ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11', 'h1']
VARS = ['c00', 'c10', 'c01', 'c11', 'x', 'y', 'h1', 'h0']
if __name__ == '__main__':
    todo = sys.argv[1:] or ALL
    out = {}
    try: out = json.load(open('resultats_modules.json'))
    except Exception: pass
    for nm in todo:
        t0 = time.time(); root = module(nm)
        print(f'== module {nm}\'', flush=True)
        L, par = search(root)
        if L is None: print('  aucun placement trouvé'); continue
        # contrôle avec la spécification R-61 sur les 256 états complets (les variables absentes ne comptent pas)
        full = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
        assert all(root.value(e) == spec(nm, e) for e in full), 'formule fausse'
        r = L.check(engine2=True)
        n_ok = sum(1 for x in r if x[1] and x[2] == x[3] == spec(nm, {**{v: 0 for v in VARS}, **x[0]})); n2 = sum(1 for x in r if x[4])
        print(f'  {len(r)} cas (les 256 états se ramènent à 2^{len(L.vars)} cas) : {n_ok} justes et propres ; 2 moteurs identiques : {n2}/{len(r)}', flush=True)
        ok, delta, info = certificate(L, log=lambda s: print('  ' + s, flush=True))
        D = delta + (-delta) % 8
        res20 = []
        for seed in range(3):
            rnd = random.Random(seed); seq = [rnd.choice(L.cases()) for _ in range(20)]
            sup, good, same, nf = check_multi(L, seq, D, engine2=(seed == 0))
            res20.append(dict(graine=seed, superposition=sup, justes=good, deux_moteurs=same, fourmis=nf))
            print(f'  20 usages (graine {seed}, Δ = {D} pas) : superposition exacte {sup}, {good}/20 justes, 2 moteurs {same}, {nf} fourmis', flush=True)
        nK = sum(1 for _, k, _ in L.ships if k == 'K'); nl = sum(1 for _, k, _ in L.ships if k == 'lit')
        out[nm] = dict(parametres=par, puissances=nK, litteraux=nl, cas=len(r), justes=n_ok, deux_moteurs=n2, certificat=ok, delta=D,
                       fenetre=info['span'], rayon=info['R'], voies_opposees=info['opposees'], usages20=res20,
                       sortie=L.out, vaisseaux=[(n, k, w) for n, k, w in L.ships], tmax=L.tmax, secondes=round(time.time() - t0, 1))
        json.dump(out, open('resultats_modules.json', 'w'), indent=1, ensure_ascii=False)

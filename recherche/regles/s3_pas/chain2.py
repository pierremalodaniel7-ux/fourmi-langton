#!/usr/bin/env python3
"""R-619 Deux pas ENCHAÎNÉS de la petite fourmi (R-61) : les modules du pas 2 lisent les vaisseaux SORTIS des modules du pas 1.
Composition = greffe (R-612) : chaque littéral v' (ou ¬v') d'un arbre du pas 2 est remplacé par un module du pas 1 qui calcule v'
(ou ¬v', en double rail : même taille, littéraux inversés), dont la puissance racine sort tout droit ssi v' = 1 et entre dans la
porte du pas 2. Diffusion (fan-out) : une copie du module du pas 1 par usage du littéral (pas de dédoublement de vaisseau).
Règle des côtés : htree.py (portes de face), sous-nœuds au plus 2 par nœud -> toujours plaçable (1 usage ; réutilisation : à part).
Sous-système (x, y, h0, c00..c11) : il ne dépend pas de h1 (sur le tore 2×2, avancer de ±1 change la même coordonnée).
Arbres abstraits : (nom, [entrées]) ; entrée = littéral 'v' / '~v' (variables de l'état INITIAL) ou sous-arbre."""
import itertools
from htree import build
from modules import spec, VARS, ne
def S(v, p, pol):
    """module du pas 1 calculant v' (pol = 1) ou ¬v' (pol = 0), nœuds préfixés par p"""
    if v == 'h0': return (p, ['h0' if pol else '~h0'])                                   # NOR(h0) = ¬h0 = h0'
    if v == 'x': return (p, [(p + 'a', ['~x', 'h0' if pol else '~h0']), (p + 'b', ['x', '~h0' if pol else 'h0'])])
    if v == 'y': return (p, [(p + 'a', ['~y', '~h0' if pol else 'h0']), (p + 'b', ['y', 'h0' if pol else '~h0'])])
    if v[0] == 'c':
        i, j = int(v[1]), int(v[2]); c = v
        return (p, [(p + 't', [('~' + c) if pol else c, ne('x', i), ne('y', j)]),
                    (p + 'u', [c if pol else '~' + c, (p + 'm', [ne('x', i), ne('y', j)])])])
    raise ValueError(v)
def graft(t, pre):
    """remplace chaque littéral (variable du pas 1) d'un arbre du pas 2 par le module du pas 1 correspondant"""
    name, ins = t; out = []
    for k, it in enumerate(ins):
        if isinstance(it, str):
            v = it.lstrip('~'); out.append(S(v, f'{pre}{name}{k}{v}', 0 if it[0] == '~' else 1))
        else: out.append(graft(it, pre))
    return (pre + name, out)
def step2_formula(nm):
    """arbre du pas 2, écrit sur les variables de l'état après le pas 1"""
    if nm == 'h0': return ('A', ['h0'])
    if nm == 'x': return ('X', [('Xa', ['~x', 'h0']), ('Xb', ['x', '~h0'])])
    if nm == 'y': return ('Y', [('Ya', ['~y', '~h0']), ('Yb', ['y', 'h0'])])
    if nm[0] == 'c':
        i, j = int(nm[1]), int(nm[2]); c = nm
        here = ('Ch', [ne('x', i), ne('y', j)]); nhere = ('Cn', [('Cm', [ne('x', i), ne('y', j)])])
        return ('C', [('Ca', [c, here]), ('Cb', ['~' + c, nhere])])
def tree(nm): return graft(step2_formula(nm), 'z' + nm + '_')
def root(nm): return build(tree(nm))
def F(e):
    """un pas R-61 sur l'état complet"""
    return {**{f'c{i}{j}': spec(f'c{i}{j}', e) for i in (0, 1) for j in (0, 1)}, 'x': spec('x', e), 'y': spec('y', e), 'h1': spec('h1', e), 'h0': spec('h0', e)}
def spec2(nm, e): return F(F(e))[nm if nm[0] in 'c' else nm]
NAMES = ['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11']
if __name__ == '__main__':
    from modules import nodes
    full = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
    for nm in NAMES:
        r = root(nm); ok = all(r.value(e) == spec2(nm, e) for e in full)
        nK = sum(1 for _ in nodes(r)); nl = sum(1 for n in nodes(r) for _, it in n.inputs if isinstance(it, str))
        print(f"{nm}'' : formule {'JUSTE' if ok else 'FAUSSE'} sur les 256 états ; {nK} puissances, {nl} littéraux")

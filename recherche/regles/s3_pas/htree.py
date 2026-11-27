#!/usr/bin/env python3
"""R-614 Arbres NOR avec portes « de face » (H) : règle de côtés qui évite les conflits structurels S1/S2 (journal R-610, R-613).
S2 n'arrive que si un nœud a la direction de son grand-parent : arêtes consécutives (+,−) ou (−,+). Le chemin (H,H) redonne aussi
la direction du grand-parent, mais un nœud ne lâche jamais de débris dans la direction a+3 (côtés ± : a±1, a±2 ; face : a+1, a+2) :
pas de S2. Donc : après une arête « + » (resp. « − ») les sous-nœuds vont sur « + » (resp. « − ») ou en face (1re entrée) ;
après une arête H (ou à la racine) : +, − et H. Un sous-nœud au plus par ligne (S1). Les littéraux : en train sur les côtés libres.
Arbre abstrait : (nom, [entrées]) ; entrée = littéral 'x' / '~x' ou sous-arbre."""
from nor import Node
def build(t, e='R'):
    name, ins = t
    subs = [x for x in ins if not isinstance(x, str)]; lits = [x for x in ins if isinstance(x, str)]
    allowed = ['+', '-', 'H'] if e in ('R', 'H') else [e, 'H']
    assert len(subs) <= len(allowed), (name, 'trop de sous-nœuds')
    if len(subs) == 3: lines = ['H', '+', '-']
    elif len(subs) == 2: lines = ['+', '-'] if e in ('R', 'H') else ['H', e]
    elif len(subs) == 1: lines = ['+' if e in ('R', 'H') else e]
    else: lines = []
    order = []
    sl = dict(zip(range(len(subs)), lines))
    for k, s in enumerate(subs):
        if sl[k] == 'H': order.insert(0, ('H', build(s, 'H')))
    free = [x for x in ('+', '-') if x not in lines]
    if not free: assert not lits, (name, 'littéraux sans côté libre')
    for k, l in enumerate(lits): order.append((free[k % len(free)], l))
    for k, s in enumerate(subs):
        if sl[k] != 'H': order.append((sl[k], build(s, sl[k])))
    return Node(name, order)
def ne(v, i): return v if i == 0 else '~' + v
def h1_tree():
    n = lambda i, j, pos: (f'{"p" if pos else "n"}{i}{j}', [ne('x', i), ne('y', j), (f'c{i}{j}' if pos else f'~c{i}{j}')])
    # n_ij = NOR(x≠i, y≠j, ¬cij) = [x=i ∧ y=j ∧ cij] ; p_ij = [x=i ∧ y=j ∧ ¬cij]
    Nc = ('Nc', [('Ncx', [('NcX', [n(0, 0, 0), n(1, 0, 0)])]), ('Ncy', [('NcY', [n(0, 1, 0), n(1, 1, 0)])])])   # ¬c
    Pc = ('Pc', [('Pcx', [('PcX', [n(0, 0, 1), n(1, 0, 1)])]), ('Pcy', [('PcY', [n(0, 1, 1), n(1, 1, 1)])])])   # c
    Ng = ('Ng', [('g1', ['~h1', 'h0']), ('g2', ['h1', '~h0'])])      # ¬g
    Pg = ('Pg', [('k1', ['~h1', '~h0']), ('k2', ['h1', 'h0'])])      # g
    return ('h1p', [('A', [Ng, Nc]), ('B', [Pg, Pc])])
def h1_tree2():
    """R-616 variante RÉUTILISABLE : un nœud qui a un enfant de face doit être la 1re entrée de son parent (sinon, s'il ressort tout
    droit, il file sur la voie de cet enfant et percute celui de l'usage suivant). Le sous-arbre qui branche passe donc en 1re entrée
    (en face), et l'autre entrée devient NON(NOR(...)) : un seul sous-nœud, pas d'enfant de face."""
    n = lambda i, j, pos: (f'{"p" if pos else "n"}{i}{j}', [ne('x', i), ne('y', j), (f'c{i}{j}' if pos else f'~c{i}{j}')])
    Nc = ('Nc', [('Ncx', [('NcX', [n(0, 0, 0), n(1, 0, 0)])]), ('Ncy', [('NcY', [n(0, 1, 0), n(1, 1, 0)])])])   # ¬c
    Pc = ('Pc', [('Pcx', [('PcX', [n(0, 0, 1), n(1, 0, 1)])]), ('Pcy', [('PcY', [n(0, 1, 1), n(1, 1, 1)])])])   # c
    Ng = ('Ng', [('W', [('k1', ['~h1', '~h0']), ('k2', ['h1', 'h0'])])])       # W = g, Ng = ¬g
    Pg = ('Pg', [('W2', [('g1', ['~h1', 'h0']), ('g2', ['h1', '~h0'])])])     # W2 = ¬g, Pg = g
    return ('h1p', [('A', [Nc, Ng]), ('B', [Pc, Pg])])

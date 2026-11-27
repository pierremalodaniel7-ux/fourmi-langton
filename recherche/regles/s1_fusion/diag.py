"""S1 : diagnostic « qui touche qui » dans un circuit composé : chaque fourmi du circuit complet est comparée à sa trajectoire
dans la simulation de son SEUL module ; on rapporte le premier écart et la fourmi d'un autre module la plus proche à cet instant."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import step
from fa_lib import parts_of
from chocs_exhaustif_lib import hd
def traj(s, T):
    a, c = parts_of(s); A = [list(x) for x in a]; G = {tuple(x[:2]): 1 for x in c}; P = [[tuple(x[:2]) for x in A]]
    for _ in range(T): step(A, G); P.append([tuple(x[:2]) for x in A])
    return P
def diag(modules, T):
    """modules : liste de (nom, situation du module seul) ; la situation complète = concaténation dans cet ordre (ordre de jeu)."""
    ants, cells, owner, sub = [], [], [], []
    for m, s in modules:
        a, c = parts_of(s); sub.append(traj(s, T)); ants += a; cells += c; owner += [(m, i) for i in range(len(a))]
    full = 'H:R2L2|' + ';'.join('%d,%d,%d' % x for x in ants) + '|' + ';'.join('%d,%d' % x[:2] for x in cells)
    P = traj(full, T); out = []
    k = 0; idx = {}
    for mi, (m, s) in enumerate(modules):
        for i in range(len(sub[mi][0])): idx[k] = (mi, i); k += 1
    for j in range(len(ants)):
        mi, i = idx[j]
        for t in range(T + 1):
            if P[t][j] != sub[mi][t][i]:
                others = [(hd(P[t][j][0] - P[t][q][0], P[t][j][1] - P[t][q][1]), owner[q]) for q in range(len(ants)) if idx[q][0] != mi]
                out.append((t, owner[j], min(others) if others else None)); break
    return sorted(out)

"""décodage des vaisseaux (r, phase, gx, gy) — copie de fusion1.decodeg sans lancer la recherche"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from hx import PHASES
from chocs_exhaustif_lib import hd
from demi_add_k import OFFS
def decodeg(ants, cells):
    out = []; used = set(); cs = set(cells)
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cs if hd(p[0] - x, p[1] - y) <= 2)
        k = PHASES.get((h, near))
        if not k: return None
        r, ph = k; out.append((r, ph, x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1])); used |= {(x + a, y + b) for a, b in near}
    if cs - used: return None
    return out

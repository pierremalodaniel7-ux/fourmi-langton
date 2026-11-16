"""fourmis.py — outils Python autour de libmoteur.so (construction de l'ordinateur à fourmis).
Conventions du dépôt : y vers le bas, caps 0=H 1=D 2=B 3=G, RL. Directions d'autoroute :
0=↙ 1=↖ 2=↗ 3=↘ (= nombre de quarts de tour (x,y)->(-y,x) appliqués au germe R-17)."""
import ctypes, numpy as np, os
L = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libmoteur.so"))
L.init(); L.run.restype = ctypes.c_long
P = 104
GX = [-2,-1,0,1,-2,1,-2,0,-1,0,0]; GY = [-2,-2,-1,0,1,1,2,2,3,3,4]
DEP = {0:(-2,2), 1:(-2,-2), 2:(2,-2), 3:(2,2)}
FL = "↙↖↗↘"
def rot(x, y, r):
    for _ in range(r & 3): x, y = -y, x
    return x, y
def germe(px, py, r):
    """germe R-17 tourné r fois, fourmi en (px,py) : autoroute dès le pas 0 dans la direction r"""
    cells = [(px + a, py + b) for a, b in (rot(gx, gy, r) for gx, gy in zip(GX, GY))]
    return cells, (px, py, (1 + r) & 3)

def simule(cells, ants, T, w=0):
    """renvoie (n pas faits, caps, xs, ys, neuf) pour la fourmi w ; n<0 si bord"""
    L.reset()
    c = np.array(cells, dtype=np.int32).ravel() if cells else np.zeros(0, np.int32)
    L.flip(len(cells), c.ctypes.data_as(ctypes.c_void_p))
    a = np.array(ants, dtype=np.int32).ravel()
    L.set_ants(len(ants), a.ctypes.data_as(ctypes.c_void_p))
    dh = np.zeros(T, np.uint8); xs = np.zeros(T, np.int32); ys = np.zeros(T, np.int32); fr = np.zeros(T, np.uint8)
    n = L.run(T, w, dh.ctypes.data_as(ctypes.c_void_p), xs.ctypes.data_as(ctypes.c_void_p),
              ys.ctypes.data_as(ctypes.c_void_p), fr.ctypes.data_as(ctypes.c_void_p))
    m = abs(n) if n < 0 else n
    return n, dh[:m], xs[:m], ys[:m], fr[:m]

# séquences de référence des 4 autoroutes (phase canonique)
REF = {}
for r in range(4):
    c, a = germe(0, 0, r)
    n, dh, xs, ys, fr = simule(c, [a], 50 * P)
    REF[r] = bytes(dh[20 * P:21 * P])
REFD = {r: REF[r] + REF[r] for r in REF}

def autoroute(dh, xs, ys, need=20, tmin=0):
    """Autoroute finale de la fourmi : (t0, dir, cle, pos) ou None.
    t0 = premier pas de la périodicité 104 finale ; cle = invariant de voie+phase :
    ↗/↙ : (x+y, (x-y) mod 4) ; ↖/↘ : (x-y, (x+y) mod 4), pris au pas de phase canonique."""
    n = len(dh)
    if n < (need + 2) * P: return None
    eq = dh[P:] == dh[:-P]
    bad = np.nonzero(~eq)[0]
    t0 = (bad[-1] + 1 + P) if len(bad) else P   # dh[t]==dh[t-P] pour tout t>=t0
    if n - t0 < need * P or t0 < tmin: return None
    s = int(n - 2 * P)
    dx = int(xs[s + P - 1]) - int(xs[s - 1]); dy = int(ys[s + P - 1]) - int(ys[s - 1])
    r = {v: k for k, v in DEP.items()}.get((dx, dy))
    if r is None: return None
    seq = bytes(dh[s:s + P]); k = REFD[r].find(seq)
    if k < 0: return None
    # au pas u = s + (P-k)%P, la séquence recommence comme la référence
    u = s + ((P - k) % P) - 1
    x, y = int(xs[u]), int(ys[u])
    cle = (x + y, (x - y) % 4) if r in (0, 2) else (x - y, (x + y) % 4)
    return int(t0), r, cle, (x, y)

L.ntouched.restype = ctypes.c_long
def touchees():
    """cases touchées (cellules initiales + toutes les fourmis) dans la dernière simulation"""
    n = L.ntouched(); a = np.zeros(2 * n, np.int32)
    L.get_touched(a.ctypes.data_as(ctypes.c_void_p))
    return set(zip(a[0::2].tolist(), a[1::2].tolist()))

def simule_tout(cells, ants, T):
    L.reset()
    c = np.array(cells, dtype=np.int32).ravel() if cells else np.zeros(0, np.int32)
    L.flip(len(cells), c.ctypes.data_as(ctypes.c_void_p))
    a = np.array(ants, dtype=np.int32).ravel(); na = len(ants)
    L.set_ants(na, a.ctypes.data_as(ctypes.c_void_p))
    dh = np.zeros(T * na, np.uint8); xs = np.zeros(T * na, np.int32); ys = np.zeros(T * na, np.int32)
    L.run_all.restype = ctypes.c_long
    n = L.run_all(T, dh.ctypes.data_as(ctypes.c_void_p), xs.ctypes.data_as(ctypes.c_void_p), ys.ctypes.data_as(ctypes.c_void_p))
    m = abs(n) if n < 0 else n
    return n, dh[:m * na].reshape(m, na), xs[:m * na].reshape(m, na), ys[:m * na].reshape(m, na)

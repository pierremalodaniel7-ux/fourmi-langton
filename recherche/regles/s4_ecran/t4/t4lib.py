"""T4 (27/11) — l'écran de la fourmi : outils communs.
Relie le PAS COMPLET réutilisable (R-617, recherche/regles/s3_pas, lignes d'univers (r, gx, gy, ph)) et les PIXELS M/R' de S4
(R-707, étiquettes traj (r, x, y, τ)). Aucune nouvelle règle de simulation : géométrie exacte en entiers + les 2 moteurs déjà là
(fourmi_r_big = fourmi_r avec MAXA 4096, et hx.py)."""
import os, sys, json, itertools
T4 = os.path.dirname(os.path.abspath(__file__)); S4 = os.path.dirname(T4); REG = os.path.dirname(S4); S3 = os.path.join(REG, 's3_pas')
sys.path.insert(0, S4); sys.path.insert(0, S3)
import traj as TR                      # (chdir vers REG à l'import de lib4)
import pixel
import s3lib as S3L
from s3lib import run_c, run_py, decode as decode3, render as render3
_cwd = os.getcwd(); os.chdir(S3)
from step import Step, load_params
from modules import spec, VARS
P = load_params(); P['h1'] = json.load(open('h1R_param_OK.json'))
RES = json.load(open('step_reuse_res.json')); OFF = {k: tuple(v) for k, v in RES['translations'].items()}
os.chdir(_cwd)
STEP = Step(P, OFF); TDEC = STEP.tmax + 1200
CASES = ['c00', 'c10', 'c01', 'c11']
hd = S3L.hd
def wl_to_T(w, t=None):
    """ligne d'univers S3 -> trajectoire traj (même vaisseau) ; t = instant où on le regarde (n'importe lequel, c'est de la géométrie)"""
    t = TDEC if t is None else t
    p = render3(w, t); return TR.of_label(TR.lab_piece((tuple(p[0]), p[1]), t))
def T_pos(T, t): return TR.antpos(TR.to_label(T), t)
def lat_ab(p, r):
    """coordonnées (latérale, abscisse) du point p dans le repère d'un vaisseau de direction r (latérale constante le long du vol,
    abscisse +2 par période de 8 pas) ; distance hex d'un point à la droite = |écart latéral|"""
    X, Y = TR.rot(p, -r % 6); return X + Y, X - Y
def orbit_ordered(osc):
    a, c = pixel.parse(osc); A = [list(x) for x in a]; g = {x: 1 for x in c}; A0 = [list(x) for x in a]; g0 = dict(g); out = []
    while True:
        out.append(([tuple(x) for x in A], sorted(g))); TR.step(A, g)
        if A == A0 and g == g0: return out
ORBO = {0: orbit_ordered(pixel.M), 1: orbit_ordered(pixel.R2)}
PER = {0: len(ORBO[0]), 1: len(ORBO[1])}
def place_ordered(state, phase, rho, c):
    a, g = ORBO[state][phase % PER[state]]
    A = [(TR.rot((x, y), rho)[0] + c[0], TR.rot((x, y), rho)[1] + c[1], (h + rho) % 6) for x, y, h in a]
    return A, [(TR.rot(q, rho)[0] + c[0], TR.rot(q, rho)[1] + c[1]) for q in g]
KITS = {'SET0a': (pixel.M, 0, 1, 16), 'SET0b': (pixel.M, 0, 1, 17), 'SET5': (pixel.M, 5, 1, 4),
        'RST2': (pixel.R2, 2, -2, 2), 'RST3a': (pixel.R2, 3, -2, 10), 'RST3b': (pixel.R2, 3, -2, 11)}
_K = {}
def kit(name):
    if name not in _K:
        osc, r, l, ph = KITS[name]; K = pixel.kit(osc, r, l, ph); K['r'] = r
        K['fin'] = pixel.ORB[1 if name.startswith('SET') else 0].index(K['obj']); _K[name] = K
    return _K[name]
def kit_on(name, O, t_near):
    """place le kit `name` sur la trajectoire O : rotation rho, centre c, instant a où le kit est « à son temps 0 » ; le centre est
    pris le plus près possible du point où passe O à l'instant t_near. Renvoie (rho, c, a) ou None"""
    K = kit(name); rho = (O[0] - K['r']) % 6; Ka = TR.rotT(K['S'], rho); best = None
    for dt in range(0, 32):
        t = t_near + dt; q = T_pos(O, t); q0 = T_pos(Ka, 0); c = (q[0] - q0[0], q[1] - q0[1])
        Kc = TR.movT(Ka, c, 0); dl = TR.to_label(Kc)[2] - TR.to_label(O)[2]
        if TR.same(TR.movT(Kc, (0, 0), dl), O): return rho, c, dl
    return None
def build_sit(e_list, delays, PL, phases=None, clocks=None):
    """situation complète : pixels (M, phases) puis jetons ordonnés : 'GERM' = vaisseaux des usages du pas (usage u retardé de
    delays[u]) et des vaisseaux horloges (trajectoires traj) insérés avant/après selon l'ordre de jeu exigé par leur choc.
    clocks = liste ordonnée de jetons [(nom, T)] déjà placés autour de 'GERM' : ordre = liste de noms (voir boucle_choix.order)"""
    A, G = [], []
    for nm in CASES:
        p = PL[nm]; a, g = place_ordered(0, p['phase0'] if phases is None else phases[nm], p['rho'], tuple(p['c'])); A += a; G += g
    for tok in (clocks or ['GERM']):
        if tok == 'GERM':
            for u, e in enumerate(e_list):
                for w in STEP.present(e):
                    a, cs = render3(S3L.tshift(w, delays[u]), 0); A.append(a); G += cs
        else:
            (x, y, h), cs = TR.piece_at(tok[1], 0); A.append((x, y, h)); G += cs
    assert len(set(G)) == len(G), 'chevauchement à t = 0'
    return S3L.sit(A, G)
def read_screen(ants, cells, PL):
    scr = {nm: pixel.read_state(ants, cells, PL[nm]['rho'], tuple(PL[nm]['c'])) for nm in CASES}
    near = lambda q: any(hd(q[0] - PL[nm]['c'][0], q[1] - PL[nm]['c'][1]) <= 6 for nm in CASES)
    return scr, [a for a in ants if not near(a)], [q for q in cells if not near(q)]
def decode_partiel(ants, cells, t):
    """comme s3lib.decode mais garde ce qui se décode : (lignes d'univers des vaisseaux propres, fourmis non-vaisseaux, cases orphelines)"""
    cs = set(cells); used = set(); out = []; bad = []
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cs if hd(p[0] - x, p[1] - y) <= 2)
        k = S3L.REC.get((h, near))
        if k is None: bad.append((x, y, h)); continue
        r, ph = k; (dx, dy, _), _ = S3L.STATE[(r, ph)]
        out.append(S3L.norm(r, x - dx, y - dy, ph, t)); used |= {(x + a, y + b) for a, b in near}
    return sorted(out), bad, sorted(cs - used)

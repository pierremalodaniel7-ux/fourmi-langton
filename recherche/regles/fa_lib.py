"""Additionneur complet R2L2 (session 26/11 jour) : outils communs.
Demi-additionneur R-337 (germe resumes/demi_additionneur_reutilisable.json), ordre de jeu K3, K2, B, A.
decode() : liste des vaisseaux (r, voie, abscisse, phase) d'un état, ou None s'il reste des cases non expliquées / une fourmi
qui n'est pas un vaisseau. Abscisse : avance de 2 par période (8 pas) le long de la direction r."""
import json, subprocess, threading
from hx import ship, ship_dir, rot, step, PHASES
from demi_add_k import OFFS, lane, parse_dump, fmt
from exp_osc import hd
HA = json.load(open('resumes/demi_additionneur_reutilisable.json'))
def parts_of(s):
    _, a, c = s.split('|')
    return [tuple(map(int, t.split(','))) for t in a.split(';') if t], [tuple(map(int, t.split(','))) for t in c.split(';') if t]
K3 = ((-16, 16, 4), [(-15, 16)]); K2 = ((62, -24, 4), [(62, -23), (63, -23)])
B = ((0, 0, 4), [(1, 0)]); A = ((30, -56, 0), [(29, -55)])
def along(x, y, r):
    X, Y = rot((x, y), -r % 6); return X - Y
def decode(ants, cells):
    out = []; used = set(); cs = set(cells)
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cs if hd(p[0] - x, p[1] - y) <= 2)
        k = PHASES.get((h, near))
        if not k: return None
        r, ph = k; gx, gy = x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1]
        out.append((r, lane(gx, gy, r), along(gx, gy, r), ph)); used |= {(x + a, y + b) for a, b in near}
    if cs - used: return None
    return sorted(out)
def lotdump(lines, T, ncpu=2):
    parts = [lines[i::ncpu] for i in range(ncpu)]; res = [None] * ncpu
    def w(k):
        o = subprocess.run(['./fourmi_r', '-T', str(T), '-x', '-dump', '-lot'], input='\n'.join(parts[k]) + '\n', capture_output=True, text=True).stdout
        res[k] = [l for l in o.splitlines() if l.startswith('DUMP')]
    th = [threading.Thread(target=w, args=(k,)) for k in range(ncpu)]; [t.start() for t in th]; [t.join() for t in th]
    out = [None] * len(lines)
    for k in range(ncpu):
        for j, l in enumerate(res[k]): out[k + j * ncpu] = parse_dump(l)
    return out
def sit(pieces):
    """pieces : liste de (fourmi, cases) dans l'ordre de jeu"""
    return fmt([p[0] for p in pieces], [c for p in pieces for c in p[1]])
def kship(rK, pos, tau):
    """vaisseau de direction rK dont la position « de référence » est pos, avancé de tau pas"""
    ka, kc = ship(rK, pos); KA = [list(ka)]; KG = {kc: 1}
    for _ in range(tau): step(KA, KG)
    return (tuple(KA[0]), sorted(KG))
def back(piece, n):
    """recule une pièce-vaisseau de n périodes sur sa route"""
    (x, y, h), cs = piece
    X_ = [[x, y, h]]; G_ = {c: 1 for c in cs}
    for _ in range(8): step(X_, G_)
    d = (X_[0][0] - x, X_[0][1] - y)
    return ((x - n * d[0], y - n * d[1], h), [(c[0] - n * d[0], c[1] - n * d[1]) for c in cs])
def pyrun(s, T):
    """2e moteur (hx.py, Python pur)"""
    a, c = parts_of(s); A_ = [list(t) for t in a]; G = {tuple(t[:2]): 1 for t in c}
    for _ in range(T): step(A_, G)
    return [tuple(t) for t in A_], sorted(G)

"""S2 R-507 — assemble le compteur 2 bits : horloge 1 (P1) + pixel = bit 0, horloge 2 (P2 = 2 P1) + pixel = bit 1, posées loin l'une de
l'autre. On choisit le déphasage s de l'horloge 2 et l'instant de lecture s0 pour que les lectures aux instants s0 + ⌊n P1 / 6⌋ donnent
00, 01, 10, 11, 00, … (n = 0 … 11 sur une période 2 P1 = P2), avec la plus grande marge (distance d'une lecture à un changement d'état).
Usage : python3 s2_horloge/compteur5.py   (lit compteur4_paires.json, écrit compteur5.json)"""
import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hx import rot, step
from fa_lib import parts_of
from demi_add_k import fmt
import anti_pixel as ap
from compteur4 import reference
a, c = parts_of(ap.W['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
M = ap.local(A, G, (0, 1))
for _ in range(776): step(A, G)
Rp = ap.local(A, G, (0, 1))
def rt(o, k):
    a_, c_ = o; x0, y0 = a_[0][0], a_[0][1]
    return [(*rot((x - x0, y - y0), k), (h + k) % 6) for x, y, h in a_], [rot((x - x0, y - y0), k) for x, y in c_]
OM = set().union(*[ap.orbit(*rt(M, k)) for k in range(6)]); OR = set().union(*[ap.orbit(*rt(Rp, k)) for k in range(6)])
def tl(sit, P): return ap.timeline(sit, (0, 1), OM, OR, P)
def margins(s):
    """pour chaque t : distance (circulaire) au plus proche instant où l'état diffère de s[t] ; 0 si s[t] == '?'"""
    P = len(s); d = [0] * P
    for t in range(P):
        if s[t] == '?': continue
        r = 0
        while r < P // 2 and s[(t + r + 1) % P] == s[t] and s[(t - r - 1) % P] == s[t]: r += 1
        d[t] = r
    return d
if __name__ == '__main__':
    pairs = json.load(open('s2_horloge/compteur4_paires.json')); best = []
    for pr in pairs:
        P1, P2 = pr['P1'], pr['P2']
        T1 = [(w, tl(w['sit'], P1)) for w in pr['m1']]; T2 = [(w, tl(w['sit'], P2)) for w in pr['m2']]
        T1 = [(w, s) for w, s in T1 if s.count('1') > P1 // 10 and s.count('0') > P1 // 10]
        T2 = [(w, s) for w, s in T2 if s.count('1') > P2 // 10 and s.count('0') > P2 // 10]
        T1.sort(key=lambda x: abs(x[1].count('1') - x[1].count('0'))); T2.sort(key=lambda x: abs(x[1].count('1') - x[1].count('0')))
        T1, T2 = T1[:8], T2[:8]
        print(P1, P2, 'pixels qui clignotent :', len(T1), len(T2), flush=True)
        def nb(s):
            q = s.replace('?', ''); return sum(1 for i in range(len(q)) if q[i] == '1' and q[i - 1] == '0')
        for w1, s1 in T1:
            b = nb(s1); NT = 4 * b; ticks = [(n * P1) // (2 * b) for n in range(NT)]
            m1 = margins(s1)
            # s0 : lectures bit0 = n mod 2
            c0 = []
            for s0 in range(P1):
                mm = min((m1[(s0 + ticks[n]) % P1] if s1[(s0 + ticks[n]) % P1] == str(n % 2) else -1) for n in range(NT))
                if mm > 0: c0.append((mm, s0))
            if not c0: continue
            c0.sort(reverse=True)
            for w2, s2 in T2:
                if nb(s2) != b: continue
                m2 = margins(s2)
                for mm0, s0 in c0[:5]:
                    for sh in range(P2):
                        mm = min((m2[(sh + s0 + ticks[n]) % P2] if s2[(sh + s0 + ticks[n]) % P2] == str((n // 2) % 2) else -1) for n in range(NT))
                        if mm > 0: best.append((min(mm, mm0), P1, P2, w1, w2, s0, sh, b))
        print('combinaisons valides :', len(best), flush=True)
    best.sort(key=lambda b: (-b[0], b[1]))
    out = []
    for mg, P1, P2, w1, w2, s0, sh, b in best[:5]:
        a2, c2 = parts_of(w2['sit']); A2 = [list(t) for t in a2]; G2 = {tuple(t): 1 for t in c2}
        for _ in range(sh): step(A2, G2)
        D = 300
        a1, c1 = parts_of(w1['sit'])
        sit = fmt([tuple(q) for q in a1] + [(x + D, y, h) for x, y, h in A2], list(c1) + [(x + D, y) for x, y in G2])
        out.append({'marge': mg, 'P1': P1, 'P2': P2, 's0': s0, 'decal': sh, 'clignotements_par_periode': b, 'lectures': [s0 + (n * P1) // (2 * b) for n in range(4 * b)],
                    'bit0': 'fourmis 0,1', 'bit1': 'fourmis %d,%d' % (len(a1), len(a1) + 1), 'sit': sit, 'm1': w1, 'm2': w2})
        print('marge', mg, P1, P2, 's0', s0, 'décalage', sh)
    json.dump(out, open('s2_horloge/compteur5.json', 'w'))

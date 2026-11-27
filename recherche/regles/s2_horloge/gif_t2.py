"""T2 — GIF d'une machine R2L2 (grille hexa, coordonnées axiales) : à gauche la machine entière, à droite un zoom sur les fourmis 0, 1
(l'objet : bascule / bit M) ; texte : pas, tour, et (option) phase de l'objet au début de chaque tour. Moteur : hx.py.
Usage : python3 s2_horloge/gif_t2.py fichier.json rang sortie.gif [pas_entre_images] [tour] [png]   (tour = durée d'un tour, ex. P0)"""
import sys, json, math
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from PIL import Image, ImageDraw
from hx import step
from fa_lib import parts_of
from exp_osc import hd
H = json.load(open(sys.argv[1])); h = H[int(sys.argv[2])]; out = sys.argv[3]
every = int(sys.argv[4]) if len(sys.argv) > 4 else 12; lap = int(sys.argv[5]) if len(sys.argv) > 5 else h.get('P0', h['P'])
png = len(sys.argv) > 6
P = h['P']; a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
o0 = (a[0][0], a[0][1])
# orbite de l'objet seul (pour lire sa phase)
def obj(A, G): return (tuple(map(tuple, A[:2])), frozenset(q for q in G if hd(q[0] - o0[0], q[1] - o0[1]) <= 5))
st0 = obj(A, G); B = [list(x) for x in st0[0]]; GB = {q: 1 for q in st0[1]}; orb = {}
for k in range(400): orb.setdefault(obj(B, GB), k); step(B, GB)
p0 = len(orb)
# trajectoire complète pour cadrer
frames = []; xs = []; ys = []
S = []
for t in range(P + 1):
    S.append(([tuple(q) for q in A], set(G))); xs += [q[0] + q[1] / 2 for q in A]; ys += [q[1] * 0.866 for q in A]
    step(A, G)
x0, x1, y0, y1 = min(xs) - 3, max(xs) + 3, min(ys) - 3, max(ys) + 3
W1, H1 = 420, int(420 * (y1 - y0) / (x1 - x0)) if x1 > x0 else 420
H1 = max(300, min(H1, 520)); Z = 280
sc = min(W1 / (x1 - x0), H1 / (y1 - y0))
phases = {}
for t in range(0, P + 1, lap):
    phases[t // lap] = orb.get(obj([list(q) for q in S[t][0]], {q: 1 for q in S[t][1]}))
cols = [(220, 60, 60), (220, 60, 60)] + [(40, 90, 200)] * 3 + [(40, 160, 70)] * 3 + [(120, 120, 120)] * 40
def draw(t):
    ants, cells = S[t]
    im = Image.new('RGB', (W1 + Z + 30, max(H1, Z) + 70), 'white'); d = ImageDraw.Draw(im)
    def P1(x, y): return (10 + (x + y / 2 - x0) * sc, 10 + (y * 0.866 - y0) * sc)
    for (x, y) in cells:
        u, v = P1(x, y); r = max(1.2, sc * 0.45); d.ellipse([u - r, v - r, u + r, v + r], fill=(30, 30, 30))
    for i, (x, y, hh) in enumerate(ants):
        u, v = P1(x, y); r = max(2.5, sc * 0.8); d.ellipse([u - r, v - r, u + r, v + r], fill=cols[i])
    # zoom
    zx, zy = o0[0] + o0[1] / 2, o0[1] * 0.866; R = 7; zs = Z / (2 * R)
    ox = W1 + 20
    d.rectangle([ox, 10, ox + Z, 10 + Z], outline=(150, 150, 150))
    def P2(x, y): return (ox + (x + y / 2 - zx + R) * zs, 10 + (y * 0.866 - zy + R) * zs)
    for (x, y) in cells:
        u, v = P2(x, y)
        if ox <= u <= ox + Z and 10 <= v <= 10 + Z: d.regular_polygon((u, v, zs * 0.5), 6, fill=(30, 30, 30))
    for i, (x, y, hh) in enumerate(ants):
        u, v = P2(x, y)
        if ox <= u <= ox + Z and 10 <= v <= 10 + Z: d.ellipse([u - zs * 0.35, v - zs * 0.35, u + zs * 0.35, v + zs * 0.35], fill=cols[i])
    k = t // lap
    d.text((10, max(H1, Z) + 20), 'pas %d / %d   tour %d (%s)' % (t, P, k + 1, 'impair' if k % 2 == 0 else 'pair'), fill='black')
    d.text((10, max(H1, Z) + 40), 'phase du bit M au debut du tour : ' + ', '.join('tour %d = %s' % (j + 1, phases[j]) for j in sorted(phases) if j <= k) + '  (periode de M seul : %d)' % p0, fill='black')
    d.text((ox, Z + 15), 'zoom : le bit M (rouge)', fill='black')
    return im
if png:
    for j, t in enumerate([0, lap]): draw(t + 30).save(out.replace('.gif', '_tour%d.png' % (j + 1)))
ims = [draw(t) for t in range(0, P, every)]
ims[0].save(out, save_all=True, append_images=ims[1:], duration=60, loop=0)
print(out, len(ims), 'images ; phases au début des tours :', phases)

"""S2 R-506 — GIF des deux pixels opposés : machine entière, pixel A (fourmis 2,3) et B (0,1) entourés (jaune = ON, gris = OFF).
Usage : gif_anti.py anti2_m1.json n sortie.gif [pas]"""
import sys, json, math, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from PIL import Image, ImageDraw, ImageFont
import anti_pixel as ap
from hx import step, rot
from fa_lib import parts_of
w = json.load(open(sys.argv[1]))[int(sys.argv[2])]; out = sys.argv[3]; every = int(sys.argv[4]) if len(sys.argv) > 4 else 15
k = w['k']; P = ap.P
a, c = parts_of(ap.W['sit']); A0 = [list(t) for t in a]; G0 = {tuple(t): 1 for t in c}
M = ap.local(A0, G0, (0, 1)); O_M = ap.orbit(*M)
for _ in range(776): step(A0, G0)
Rp = ap.local(A0, G0, (0, 1)); O_R = ap.orbit(*Rp)
def rt(o):
    a_, c_ = o; x0, y0 = a_[0][0], a_[0][1]
    return [(*rot((x - x0, y - y0), k), (h + k) % 6) for x, y, h in a_], [rot((x - x0, y - y0), k) for x, y in c_]
tA = ap.timeline(w['sit'], (2, 3), O_M, O_R, P + 1); tB = ap.timeline(w['sit'], (0, 1), ap.orbit(*rt(M)), ap.orbit(*rt(Rp)), P + 1)
a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
def xy(p): return (p[0] + p[1] / 2, p[1] * math.sqrt(3) / 2)
pts = []; B2 = [list(t) for t in A]; G2 = dict(G)
for t in range(P): pts += [xy(q) for q in B2]; step(B2, G2)
x0 = min(p[0] for p in pts) - 8; x1 = max(p[0] for p in pts) + 8; y0 = min(p[1] for p in pts) - 8; y1 = max(p[1] for p in pts) + 8
S = 560; sc = min(S / (x1 - x0), S / (y1 - y0))
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: font = ImageFont.load_default()
frames = []; lastA = lastB = '0'
for t in range(P + 1):
    if tA[t] != '?': lastA = tA[t]
    if tB[t] != '?': lastB = tB[t]
    if t % every == 0:
        im = Image.new('RGB', (S, S + 40), 'white'); d = ImageDraw.Draw(im)
        for q in G:
            X, Y = xy(q); u, v = (X - x0) * sc, (Y - y0) * sc; d.rectangle([u - 1, v - 1, u + 1, v + 1], fill='black')
        for i, (nm, idx, s) in enumerate((('A', (2, 3), lastA), ('B', (0, 1), lastB))):
            X, Y = xy(A[idx[0]]); u, v = (X - x0) * sc, (Y - y0) * sc
            d.ellipse([u - 16, v - 16, u + 16, v + 16], fill=(255, 210, 0) if s == '1' else (200, 200, 200), outline='black')
            d.text((u + 18, v - 12), nm, fill='black', font=font)
        for q in A:
            X, Y = xy(q); u, v = (X - x0) * sc, (Y - y0) * sc; d.ellipse([u - 3, v - 3, u + 3, v + 3], fill='red')
        d.text((10, S + 8), f't = {t:4d}   A : {"ON " if lastA == "1" else "OFF"}   B : {"ON " if lastB == "1" else "OFF"}   (P = {P})', fill='black', font=font)
        frames.append(im)
    if t < P: step(A, G)
frames[0].save(out, save_all=True, append_images=frames[1:], duration=60, loop=0)
frames[60].save(out.replace('.gif', '_img.png'))
print('images', len(frames), 'A ON', tA.count('1'), 'B ON', tB.count('1'), 'opposés', sum(1 for x, y in zip(tA, tB) if {x, y} == {'0', '1'}), 'identiques', sum(1 for x, y in zip(tA, tB) if x == y != '?'))

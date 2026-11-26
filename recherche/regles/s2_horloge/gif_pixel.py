"""S2 R-502 — GIF du pixel qui clignote : à gauche la machine entière (horloge triangle), à droite le pixel agrandi + ON / OFF.
Usage : gif_pixel.py fichier.json index sortie.gif [pas_entre_images]"""
import sys, json, math
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from PIL import Image, ImageDraw, ImageFont
from hx import step
from fa_lib import parts_of
from pixel_check import timeline
W = json.load(open(sys.argv[1])); w = W[int(sys.argv[2])]; out = sys.argv[3]; every = int(sys.argv[4]) if len(sys.argv) > 4 else 12
Bs = json.load(open('data/bascules_exactes.json'))
st, ch = timeline(w, Bs)
a, c = parts_of(w['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
pos = w['pos']; n = len(A); P = w['P']
def xy(p): return (p[0] + p[1] / 2, p[1] * math.sqrt(3) / 2)
# cadre global
pts = []
B2 = [list(t) for t in A]; G2 = dict(G)
for t in range(P):
    pts += [xy(q) for q in B2]; step(B2, G2)
x0 = min(p[0] for p in pts) - 4; x1 = max(p[0] for p in pts) + 4; y0 = min(p[1] for p in pts) - 4; y1 = max(p[1] for p in pts) + 4
Wd, H = 520, 520; sc = min(Wd / (x1 - x0), H / (y1 - y0))
pc = xy(A[pos]); Z = 18
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: font = fs = ImageFont.load_default()
frames = []
for t in range(P + 1):
    if t % every == 0:
        im = Image.new('RGB', (Wd * 2 + 20, H + 66), 'white'); d = ImageDraw.Draw(im)
        for q in G:
            X, Y = xy(q); u, v = (X - x0) * sc, (Y - y0) * sc; d.rectangle([u - 1, v - 1, u + 1, v + 1], fill='black')
        for k, an in enumerate(A):
            X, Y = xy(an); u, v = (X - x0) * sc, (Y - y0) * sc
            col = 'green' if k in (pos, pos + 1) else ('#1f5fbf' if an[2] % 2 == 0 else '#d0302f')
            d.ellipse([u - 4, v - 4, u + 4, v + 4], fill=col)
        u, v = (pc[0] - x0) * sc, (pc[1] - y0) * sc; d.rectangle([u - 12, v - 12, u + 12, v + 12], outline='green', width=2)
        # zoom
        ox = Wd + 20
        d.rectangle([ox, 0, ox + Wd, H], outline='#888')
        for q in G:
            X, Y = xy(q)
            if abs(X - pc[0]) < 7 and abs(Y - pc[1]) < 7:
                u, v = ox + Wd / 2 + (X - pc[0]) * Z * 2.5, H / 2 + (Y - pc[1]) * Z * 2.5
                d.regular_polygon((u, v, Z * 1.35), 6, rotation=30, fill='black')
        for k, an in enumerate(A):
            X, Y = xy(an)
            if abs(X - pc[0]) < 7 and abs(Y - pc[1]) < 7:
                u, v = ox + Wd / 2 + (X - pc[0]) * Z * 2.5, H / 2 + (Y - pc[1]) * Z * 2.5
                col = 'green' if k in (pos, pos + 1) else ('#1f5fbf' if an[2] % 2 == 0 else '#d0302f')
                d.ellipse([u - 12, v - 12, u + 12, v + 12], fill=col, outline='white', width=2)
        s = st[t]; lab = {'ON': 'PIXEL = 1 (ON)', 'OFF': 'PIXEL = 0 (OFF)', '?': 'écriture en cours'}[s]
        d.rectangle([ox + 10, H + 8, ox + 330, H + 48], fill={'ON': '#ffd84d', 'OFF': '#dddddd', '?': '#ffffff'}[s])
        d.text((ox + 20, H + 14), lab, fill='black', font=font)
        d.text((10, H + 8), f'R2L2 hexa : horloge 6 fourmis + pixel 2 fourmis', fill='black', font=fs); d.text((10, H + 26), f't = {t} / {P} (cycle exact)', fill='black', font=fs)
        d.text((10, H + 44), 'bleu : horaires, rouge : anti-horaires, vert : pixel', fill='#444', font=fs)
        frames.append(im)
    if t < P: step(A, G)
frames[0].save(out, save_all=True, append_images=frames[1:], duration=60, loop=0, optimize=True)
# images fixes ON et OFF
iON = next(i for i, t in enumerate(range(0, P + 1, every)) if st[t] == 'ON'); iOFF = next(i for i, t in enumerate(range(0, P + 1, every)) if st[t] == 'OFF')
frames[iON].save(out.replace('.gif', '_ON.png')); frames[iOFF].save(out.replace('.gif', '_OFF.png'))
print('images :', len(frames), out)

"""S2 R-512 — image d'un hexagramme : traces des 12 fourmis sur une période (A bleu, B orange), chocs A-B en rouge, départ en noir.
Usage : python3 s2_horloge/img_hexa.py P [rang] -> s2_horloge/img/hexagramme_<P>.png"""
import sys, json, math
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from hx import step
from fa_lib import parts_of
from tri import virt
from exp_osc import hd
PP = int(sys.argv[1]); rk = int(sys.argv[2]) if len(sys.argv) > 2 else 0
h = [x for x in json.load(open('s2_horloge/hexagramme_propres.json')) if x['P'] == PP][rk]
a, c = parts_of(h['sit']); A = [list(t) for t in a]; G = {tuple(t): 1 for t in c}
cart = lambda x, y: (x + y / 2, -y * math.sqrt(3) / 2)
tr = [[] for _ in A]; hits = []
for t in range(PP):
    V = [virt(q, G, 0)[0] for q in A]
    for i, q in enumerate(A): tr[i].append(cart(q[0], q[1]))
    for i in range(6):
        for j in range(6, 12):
            if V[i] is None and V[j] is None and hd(A[i][0] - A[j][0], A[i][1] - A[j][1]) <= 6: hits.append(cart((A[i][0] + A[j][0]) / 2, (A[i][1] + A[j][1]) / 2))
    step(A, G)
fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
for i, T in enumerate(tr):
    ax.plot([p[0] for p in T], [p[1] for p in T], '-', lw=0.6, color='#1f5fbf' if i < 6 else '#e07b00', alpha=0.7)
if hits: ax.scatter([p[0] for p in hits], [p[1] for p in hits], s=4, color='red', zorder=3, label='chocs A-B')
x0, y0 = parts_of(h['sit'])[0], None
ax.scatter([cart(q[0], q[1])[0] for q in a], [cart(q[0], q[1])[1] for q in a], s=12, color='k', zorder=4, label='fourmis à t = 0')
ax.set_aspect('equal'); ax.axis('off'); ax.legend(loc='lower right', fontsize=7)
ax.set_title('Hexagramme R2L2 : 2 horloges de %d pas couplées, CYCLE %d (12 fourmis)' % (h['P0'], PP), fontsize=8)
fig.savefig('s2_horloge/img/hexagramme_%d.png' % PP, bbox_inches='tight'); print('img/hexagramme_%d.png' % PP, len(hits), 'points de choc')

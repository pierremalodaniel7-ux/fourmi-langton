#!/usr/bin/env python3
"""graphe_records.py : courbe record(n) du transitoire (pas certifié) pour les boîtes n×n (convention de T(n)).
Entrées : exhaustifs (n = 3, 4 ; n = 5 partiel) et data/colline_<n>.txt (montée de colline = minorants)."""
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, os, re
D = os.path.dirname(os.path.abspath(__file__)) + '/../../../'
ex = {3: 51277, 4: 133984}
best = {}
for n in range(5, 11):
    f = D + f'data/colline_{n}.txt'
    if os.path.exists(f):
        v = [int(l.split()[1]) for l in open(f) if l[0].isdigit() or l.startswith('FIN')]
        if v: best[n] = max(v)
for n in sorted(best):                      # recopie au coin : record(n+1) >= record(n)
    best[n] = max([best[m] for m in best if m <= n] + [209637 if n >= 5 else 0])
part5 = 209637
fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=150)
ax.plot(list(ex), list(ex.values()), 'o-', color='#1f4e79', label='exhaustif (exact)')
ax.plot([5], [part5], 's', color='#1f4e79', mfc='white', label='5×5 exhaustif partiel (6 M / 33,5 M)')
if best: ax.plot(list(best), list(best.values()), '^--', color='#c55a11', label='minorant (montée de colline + recopie au coin)')
for n, v in list(ex.items()) + list(best.items()): ax.annotate(f'{v:,}'.replace(',', ' '), (n, v), textcoords='offset points', xytext=(4, 6), fontsize=7)
ax.set_xlabel('n (boîte n×n, fourmi au coin, cap haut)'); ax.set_ylabel('pas certifié (début d\'autoroute)')
ax.set_title('Transitoire record avant l\'autoroute (RL)'); ax.grid(alpha=.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(D + 'resultats/records_transitoire.png'); print(best)

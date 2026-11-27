"""S2 R-500 — formule explicite du terme j de la famille triangle (aucun calcul de choc : juste des entiers)."""
import sys
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
def horloge(j):
    a = [(1, 6, 5), (-6, j + 19, 1), (-(j + 12), j + 12, 3), (-5, 5, 4), (1, j + 13, 0), (-(j + 13), j + 19, 2)]
    c = [(1, 5), (1, 6), (-6, j + 19), (-5, j + 19), (-(j + 13), j + 13), (-(j + 12), j + 12), (-4, 5), (0, j + 14), (-(j + 13), j + 18)]
    return 'H:R2L2|' + ';'.join('%d,%d,%d' % x for x in a) + '|' + ';'.join('%d,%d' % x for x in c)
def periode(j): return 363 + 24 * j if j % 2 == 0 else 381 + 24 * j
if __name__ == '__main__':
    from famille import terme
    from outils_r import lot
    js = list(range(0, 301))
    assert all(horloge(j) == terme(j)[2] for j in js)
    out = lot([horloge(j) for j in js], periode(300) + 10)
    print('formule = construction :', len(js), '/', len(js), '; CYCLE de période', sum(l.split('|')[3] == 'CYCLE' and int(l.split('|')[5]) == periode(j) for j, l in zip(js, out)), '/', len(js))
    print(horloge(0)); print(horloge(1))

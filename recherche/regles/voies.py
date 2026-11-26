"""voies des vaisseaux d'une paire (écriture Da, effacement Db) de ecran.py : conflit = 2 routes du même axe, sens opposés, voies proches."""
import itertools
from ecran import *
def lane(x, y, r):
    X, Y = rot((x, y), -r % 6); return X + Y
def axe(a, r):
    l = lane(a[0], a[1], r); return (r % 3, l if r < 3 else -l, r)
def routes(da, db):
    Ea, _, fa = film(*da); Eb, kitb, fb = film(*db)
    R = []
    cr = reverse(*fa)
    for a, s in zip(cr[0], ships_of(*cr)): R.append(('écrit-entrée', axe(a, s[0])))
    sa = [a for a in Ea['ants']][-1 if da[0] == 0 else 0]; ra = (da[1] + 3) % 6
    R.append(('écrit-sortie', axe(sa, ra)))
    R.append(('lit-entrée', axe(kitb[0][0], db[1])))
    for a, s in zip(fb[0], ships_of(*fb)): R.append(('lit-sortie', axe(a, s[0])))
    return R
def conflits(R, marge=5):
    c = []
    for (n1, (ax1, l1, r1)), (n2, (ax2, l2, r2)) in itertools.combinations(R, 2):
        if ax1 == ax2 and r1 != r2 and abs(l1 - l2) <= marge: c.append((n1, n2, l1, l2))
    return c
if __name__ == '__main__':
    for da, db in itertools.product(OPTS, OPTS):
        R = routes(da, db); c = conflits(R)
        if not c: print('sans conflit', da, db, R)
    print('fin')

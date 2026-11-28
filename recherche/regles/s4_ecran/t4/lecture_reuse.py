#!/usr/bin/env python3
"""R-722 suite : RÉUTILISATION du port de lecture. Après une lecture OFF, le vaisseau de réécriture repart en direction 1, de face
(écart 1 voie) avec la sonde de la lecture SUIVANTE du même pixel (comme R-709) ⇒ un 4e choc R (horloge posée à t = 0) le dévie juste
après le pixel. Recherche au hasard dans le catalogue complet (virage ≠ 0, 3) + pré-test hx.py : pixel seul, lecture 1 + choc R +
lecture 2, cas OFF et ON : pixel à la phase « sans lecture », lu1 = lu2 = état, reste propre.
Usage : python3 lecture_reuse.py pixel t1 t2 -> t4/lecture_<pixel>_<t1>.json complété (jeton R)"""
import sys, os, json, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
from lect import kits, place
import lecture_port as LP
CAT = TR.catalogue(False)
def run(nm, files, extra, T):
    p = LP.PL[nm]; a1 = p['arrivee']; out = {}
    toks = [tuple(t[1]) for f in files for t in f['toks']] + [x[1] for x in extra]
    for st in (0, 1):
        ph0 = (kit('SET0a')['ph'] - a1) % 21 if st == 0 else 0
        s = LP.pixel_sit(nm, st, ph0, toks); a, c = run_py(s, T)
        got = pixel.read_state(a, c, p['rho'], tuple(p['c'])); want = (st, (ph0 + T) % (21 if st == 0 else 12))
        ra = [x for x in a if hd(x[0] - p['c'][0], x[1] - p['c'][1]) > 6]; rc = [q for q in c if hd(q[0] - p['c'][0], q[1] - p['c'][1]) > 6]
        dp, bd, orph = decode_partiel(ra, rc, T); labs = [TR.of_label(TR.lab_piece(render3(w, T), T)) for w in dp]
        lu = [int(any(TR.same(tuple(f['sonde']), L) for L in labs)) for f in files]
        out[st] = dict(pixel=got == want, propre=not bd and not orph, lu=lu)
    return out
if __name__ == '__main__':
    nm, t1, t2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    F1 = json.load(open(os.path.join(T4, f'lecture_{nm}_{t1}.json'))); F2 = json.load(open(os.path.join(T4, f'lecture_{nm}_{t2}.json')))
    p = LP.PL[nm]; R0 = place(LP.K['reecr']['out'], p, F1['e']); T = F2['e'] + 720 + 400
    base = run(nm, [F1, F2], [], T); print('sans choc R :', base, flush=True)
    rnd = random.Random(1); t0 = time.time(); n = 0
    while time.time() - t0 < float(os.environ.get('TMAX', 400)):
        k = rnd.randrange(len(CAT)); C = CAT[k]; i = rnd.randrange(2)
        if any((C.outs[o][0] - C.ins[i][0]) % 6 in (0, 3) for o in (0, 1)): continue
        n0 = rnd.randrange(15, 120); A = C.align(i, R0, 0); A = C.align(i, R0, (F1['e'] + 720 - A.te) // 8 + n0)
        Kt = A.ins[1 - i]; n += 1
        # ordre : l'horloge R juste avant/après le vaisseau de réécriture = la sonde ou une horloge de la lecture 1 ; on la met en fin
        # de liste si le signal joue en 1er, sinon en tête (les deux sont des vaisseaux isolés à t = 0)
        r = run(nm, [F1, F2], [('R', Kt)], T) if A.first == i else None
        if r is None:
            files_first = None
            p_ = LP.PL[nm]; toks = [tuple(Kt)]  # horloge en tête : on la passe comme 1er jeton
            r = run(nm, [dict(F1, toks=[['R', list(Kt)]] + F1['toks']), F2], [], T)
            r = {st: dict(v, lu=v['lu'][:]) for st, v in r.items()}
            pos = 'tete'
        else: pos = 'fin'
        ok = r[0] == dict(pixel=True, propre=True, lu=[0, 0]) and r[1] == dict(pixel=True, propre=True, lu=[1, 1])
        print(n, k, i, n0, pos, r, flush=True)
        if ok:
            F1['choc_R'] = dict(k=k, i=i, n0=n0, horloge=list(Kt), position=pos, te=A.te)
            if pos == 'fin': F1['toks'] = F1['toks'] + [['R', list(Kt)]]
            else: F1['toks'] = [['R', list(Kt)]] + F1['toks']
            json.dump(F1, open(os.path.join(T4, f'lecture_{nm}_{t1}.json'), 'w'), indent=1); print('RETENU', flush=True); sys.exit()
    print('rien', n)

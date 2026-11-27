#!/usr/bin/env python3
"""R-722 (T4) : PORT DE LECTURE DÉDIÉ par pixel, réutilisable. Sonde R-708 option 2 (dir 4, voie 2 ; M en phase 15 -> X période 9,
la sonde ressort décalée de 2 voies ; R' : traverse, 12 phases). Choisie parce que ni la sonde ni le retour ne sont antiparallèles
(à < 9 voies) à une entrée du germe (risque de choc de face avec l'usage 2, cause de R-719).
OFF : la sonde ressort sur la voie décalée -> choc Q (horloge) la dévie -> chocs B, C -> elle revient sur la droite de réécriture
X -> M (dir 1) avec X en phase 5 : le pixel redevient M, avec EXACTEMENT la phase qu'il aurait eue sans lecture (w ≡ 9 mod 63).
ON : la sonde traverse R' et passe à côté de Q sans le toucher (contrôlé par simulation de la paire) : elle continue tout droit = « lu 1 ».
Lu = présence de la sonde sur sa droite d'origine après le pixel. Recherche affine (comme boucle3) + pré-tests hx.py (pixel seul).
Usage : python3 lecture_port.py pixel t_lecture  -> t4/lecture_<pixel>_<t>.json"""
import sys, os, json, random, time
os.environ.setdefault('SEQ', '4,4,1')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
from lect import kits, place
import boucle3 as B3
OPT = 2; K, ORB = kits(OPT); PL = json.load(open(os.path.join(T4, 'placement.json')))
PERX = len(ORB['X'])
def ports(nm, tr):
    p = PL[nm]; a1 = p['arrivee']
    tr = tr + ((a1 - 1 - tr) % 21)               # M (OFF) en phase 15 à tr
    Xoff = place(K['lire0']['out'], p, tr); Son = place(K['lire0']['S'], p, tr); Krec = place(K['reecr']['S'], p, 0)
    return tr, Son, Xoff, Krec
def search(nm, tr, tri, wres=9, wmod=63):
    tr, Son, Xoff, Krec = ports(nm, tr); tg = B3.lane(Krec)
    ns = []; X = Xoff; t = tr + 720
    for (k, i, o) in tri:
        C0 = B3.CAT[k].align(i, X, 0); n = (t - C0.te) // 8; ns.append(n); C = B3.CAT[k].align(i, X, n); X = C.outs[o]; t = C.te
    def G(d):
        X, ch = B3.chain(Xoff, tri, [b + x for b, x in zip(ns, d)]); return [B3.lane(X), B3.V(Krec) - B3.V(X)] + [C.te for C in ch]
    g0 = G((0, 0, 0)); co = [[g[j] - g0[j] for g in (G(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))] for j in range(5)]
    al, be, ga = co[0]
    for d1 in range(20, 200):
        for d2 in range(20, 200):
            if ga == 0: return None
            q, r = divmod(tg - g0[0] - al * d1 - be * d2, ga)
            if r or q < 20 or q > 400: continue
            d = (d1, d2, q); v = [g0[j] + sum(co[j][x] * d[x] for x in range(3)) for j in range(5)]
            e, tA, tB, tC = v[1:]; w = e - tr - 720
            if w % wmod == wres and tr + 720 + 160 < tA < tB - 160 and tB < tC - 160 and tC < e - 160:
                X, chocs = B3.chain(Xoff, tri, [b + x for b, x in zip(ns, d)])
                assert TR.same(TR.movT(Krec, (0, 0), e), X)
                return dict(tr=tr, d=d, e=e, w=w, chocs=chocs, Son=Son, Xoff=Xoff, X=X)
    return None
def pixel_sit(nm, state, phase, toks, extra_first=()):
    p = PL[nm]; A, G = [], []
    a, g = place_ordered(state, phase, p['rho'], tuple(p['c'])); A += a; G += g
    for T in toks: (x, y, h), cs = TR.piece_at(T, 0); A.append((x, y, h)); G += cs
    return S3L.sit(A, G)
def order(cand, tri):
    """ordre de jeu : la sonde ('S') puis les horloges insérées selon chaque choc (même règle que boucle_choix.order)"""
    toks = [('S', cand['Son'])]; sig = 'S'
    for j, (C, (k, i, o)) in enumerate(zip(cand['chocs'], tri)):
        kap = ('Q%d' % j, C.ins[1 - i]); names = [t[0] for t in toks]; pos = names.index(sig)
        toks.insert(pos + 1 if C.first == i else pos, kap)
        if o != i: sig = kap[0]
    return toks
def pretest(nm, cand, tri):
    """pixel seul (OFF = M, ON = R'), sonde + 3 horloges, hx.py jusqu'à e + 720 + 300 : OFF -> M à la phase « sans lecture », reste
    propre, la sonde n'est PAS sur sa droite d'origine ; ON -> R' à la phase « sans lecture », la sonde EST sur sa droite d'origine"""
    p = PL[nm]; a1 = p['arrivee']; toks = order(cand, tri); T = cand['e'] + 720 + 300; out = {}
    prev = [('P', tuple(t[1])) for f in os.environ.get('PREV', '').split(',') if f for t in json.load(open(os.path.join(T4, f)))['toks']]
    prevS = [tuple(json.load(open(os.path.join(T4, f)))['sonde']) for f in os.environ.get('PREV', '').split(',') if f]
    toks = prev + toks
    for st in (0, 1):
        ph0 = (kit('SET0a')['ph'] - a1) % 21 if st == 0 else 0
        s = pixel_sit(nm, st, ph0, [t[1] for t in toks]); a, c = run_py(s, T)
        got = pixel.read_state(a, c, p['rho'], tuple(p['c'])); want = (st, (ph0 + T) % (21 if st == 0 else 12))
        ra = [x for x in a if hd(x[0] - p['c'][0], x[1] - p['c'][1]) > 6]; rc = [q for q in c if hd(q[0] - p['c'][0], q[1] - p['c'][1]) > 6]
        dp, bd, orph = decode_partiel(ra, rc, T); on_line = S3L.norm(*([0] * 5)) if False else None
        labs = [TR.of_label(TR.lab_piece(render3(w, T), T)) for w in dp] if dp else []
        lu = any(TR.same(TR.movT(cand['Son'], (0, 0), 0), L) for L in labs) and all(any(TR.same(S, L) for L in labs) == bool(st) for S in prevS)
        out[st] = dict(pixel=got == want, propre=not bd and not orph, lu=int(lu))
    return out
if __name__ == '__main__':
    nm = sys.argv[1]; tr0 = int(sys.argv[2]); rnd = random.Random(int(os.environ.get('GRAINE', 1))); t0 = time.time(); n = 0
    while time.time() - t0 < float(os.environ.get('TMAX', 600)):
        tri = [rnd.choice(s) for s in B3.SEQ]; c = search(nm, tr0, tri)
        if not c: continue
        n += 1; r = pretest(nm, c, tri); ok = r[0] == dict(pixel=True, propre=True, lu=0) and r[1] == dict(pixel=True, propre=True, lu=1)
        print(nm, 'w', c['w'], 'd', c['d'], r, flush=True)
        if ok:
            json.dump(dict(pixel=nm, option=OPT, tr=c['tr'], tri=tri, d=c['d'], e=c['e'], w=c['w'], toks=[[t[0], list(t[1])] for t in order(c, tri)],
                           sonde=list(c['Son']), essais=n), open(os.path.join(T4, f'lecture_{nm}_{tr0}.json'), 'w'), indent=1)
            print('RETENU', flush=True); sys.exit()
    print('rien', n)

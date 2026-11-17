# fa.py — additionneur complet : entrées a, b, c = germes ↙ (voies x+y = 0, 128, 256) ; puissance ↘ classe 3.
import sys; sys.path.insert(0,'..')
import portes as Pt, sim, json, itertools
E=list(itertools.product((0,1),repeat=3))
IN=[(0,0),(64,64),(128,128)]
def gin(e): return [Pt.germe(x,y,0) for (x,y),v in zip(IN,e) if v]
def P(w,s=-391): return Pt.germe((w+s)//2,(s-w)//2,3)
def lanes(w,T=90000):
    r=Pt.run([Pt.situ(gin(e)+[P(w)]) for e in E],T)
    return [None if o=='BORD' or o[-1] is None else o[-1][:3] for o in r]
if __name__=='__main__':
    for w in (-121,-281):
        L=lanes(w); base=L[0][2]
        print('P voie',w,':',[(e,sum(e),(l[2]-base) if l else None, l[:2] if l else None) for e,l in zip(E,L)])

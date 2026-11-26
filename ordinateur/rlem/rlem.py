#!/usr/bin/env python3
"""rlem.py FAM K M : recherche d'un élément de mémoire à 2 états avec LECTURE (entrée b non destructive), nuit 26/11.
Pièces : data/rlem/FAM_pieces.json (liste {nom, situation, periode}) ; ce processus traite les pièces d'indice ≡ K mod M,
écrit une ligne JSON par pièce dans data/rlem/FAM_K.jsonl (reprise : saute les pièces déjà faites).
Étape 1 : autoroute 104 neuve (germe R-20, venant du NE) sur la pièce S0 tournée de r×90° (r = 0..3), chaque voie à ≤ 8 de la
  pièce, 4 avancées, phases (≤ 24, régulièrement espacées) → miroir (S0 intact en place, sonde sortie), changée (résidu = petit
  cycle exact près de la pièce, sonde sortie), autre.
Étape 2 : sur les 3 états S1 les plus fréquents (résidus ramenés au repère de base, débris compris), mêmes tirs → miroir S1 /
  retour S0 (orbite S0 en place) / autre.
Bilan : écriture (S0→S1), effacement (S1→S0), lecture (même rotation et voie : S0 intact sortie x, S1 intact sortie y ≠ x ;
  faible = pour au moins une phase de chaque, forte = toutes). Calcul : src/fourmi (-lot -dump -dumpbox) ; T = 15000."""
import sys, json, os, collections, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lecture'))
from lib import charge, pas, situ, parse, lot, destins, voie, G, E
FAM,K,M=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); T=int(os.environ.get('TT',15000)); D=50; LARG=8; NPH=24; NS1=int(os.environ.get('NS1',5))
O=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../data/rlem'); os.makedirs(O,exist_ok=True)
P=json.load(open(f'{O}/{FAM}_pieces.json')); OUT=f'{O}/{FAM}_{K}.jsonl'
fait={json.loads(l)['nom'] for l in open(OUT)} if os.path.exists(OUT) else set()
def rotA(A,r):
    for _ in range(r%4): A=[(-y,x,(d+1)%4) for x,y,d in A]
    return A
def rotC(C,r):
    for _ in range(r%4): C=[(-y,x) for x,y in C]
    return C
def orbit(A,C,p):
    turn,an,no=charge(situ(A,C)); vis=set(); L=[]
    for _ in range(p):
        for a in an: vis.add((a[0],a[1]))
        L.append(([tuple(a) for a in an],sorted(no))); pas(turn,an,no,range(len(an)))
    ring={(x+dx,y+dy) for x,y in vis for dx in (-1,0,1) for dy in (-1,0,1)}-vis
    K={(tuple(a),frozenset(c for c in n if c in vis)) for a,n in L}
    R=frozenset(c for c in L[0][1] if c in ring)       # cases noires de l'anneau (immobiles : jamais visitées)
    return L,vis,(K,ring,R)
def phases(p,n=None):
    n=n or NPH; return list(range(p)) if p<=n else [round(i*p/n) for i in range(n)]
def tirs(A,C,p,r):
    """tirs sur la pièce (A,C) tournée de r ; renvoie meta, lignes, et l'orbite tournée"""
    Ar,Cr=rotA(A,r),rotC(C,r); L,vis,Kk=orbit(Ar,Cr,p)
    zone={(x+dx,y+dy) for x,y in vis for dx in range(-2,3) for dy in range(-2,3)}
    lines=[]; meta=[]
    for tx in range(-2*D-24,-2*D+25):
        for ty in range(2*D-24,2*D+25):
            if not (4*D<=-tx+ty<4*D+4): continue
            if not any(abs((x+y)-(-tx-ty))<=LARG for x,y in zone): continue
            for s in phases(p):
                An,N=L[s]; cells=[(x-tx,y-ty) for x,y in G]+list(N)
                lines.append(f"RL|{-tx},{-ty},B;"+';'.join(f'{x},{y},{d}' for x,y,d in An)+'|'+';'.join(f'{x},{y}' for x,y in cells))
                meta.append((r,f'{tx},{ty}',s))
    return meta,lines,(vis,Kk)
def boite(vis,m): return (min(x for x,y in vis)-m,min(y for x,y in vis)-m,max(x for x,y in vis)+m,max(y for x,y in vis)+m)
def run_shots(A,C,p,tag):
    allm=[];alll=[];orb={}
    for r in range(4):
        m,l,o=tirs(A,C,p,r); allm+=m; alll+=l; orb[r]=o
    vis0=set().union(*[o[0] for o in orb.values()]); b=boite(vis0,10)
    res=lot(alll,T,tag,opts='-dumpbox '+','.join(map(str,b)))
    return allm,res,orb
def canon(A,C,p):
    """clé d'orbite en place (cases visitées seulement), repère de base"""
    L,vis,Kk=orbit(A,C,p); return min((tuple(sorted(a)),tuple(sorted(c for c in n if c in vis))) for a,n in L)
def cycle_check(sits):
    out=lot(sits,4000,'cy') if sits else []
    R=[]
    for o,an,ce in out:
        f=o.split('|'); R.append(int(f[5]) if f[3]=='CYCLE' and int(f[5])<=600 else None)
    return R
def intact(Pp,ce,vis,KK):
    K,ring,R=KK; return (Pp,frozenset(c for c in ce if c in vis)) in K and frozenset(c for c in ce if c in ring)==R
def propre(A,C,p):
    """pièce idéalisée : on ne garde que les cases à distance ≤ 2 des cases visitées"""
    L,vis,_=orbit(A,C,p); z={(x+dx,y+dy) for x,y in vis for dx in range(-2,3) for dy in range(-2,3)}
    return [c for c in C if c in z]
def ex(d,a):
    if d=='-':          # autoroute pas encore confirmée : sonde loin de la pièce → direction par le quadrant
        if max(abs(a[0]),abs(a[1]))<40 or min(abs(a[0]),abs(a[1]))<10: return '-'
        d=f'{2 if a[0]>0 else -2},{2 if a[1]>0 else -2}'
    return f'{d}@{voie(a[0],a[1],d)}'
for idx,pc in enumerate(P):
    if idx%M!=K or pc['nom'] in fait: continue
    t0=time.time(); r_,A0,C0=parse(pc['situation']); p0=pc['periode']; npc=len(A0)
    meta,res,orb=run_shots(A0,C0,p0,'s1')
    mir0=collections.defaultdict(list); cand=[]
    for (r,k,s),(o,an,ce) in zip(meta,res):
        d=destins(o)[0]
        if ex(d,an[0])=='-': continue
        vis,Kk=orb[r]; Pp=tuple(an[1:1+npc])
        if intact(Pp,ce,vis,Kk): mir0[f'{r}:{k}'].append([s,ex(d,an[0])]); continue
        b=boite(vis,6)
        if all(b[0]<=a[0]<=b[2] and b[1]<=a[1]<=b[3] for a in Pp):
            bb=boite(vis,10); cells=sorted(c for c in ce if bb[0]<=c[0]<=bb[2] and bb[1]<=c[1]<=bb[3])
            # ramener au repère de base (rotation inverse)
            Ab=rotA(list(Pp),4-r); Cb=rotC(cells,4-r); cand.append((r,k,s,ex(d,an[0]),situ(Ab,Cb)))
    cyc=cycle_check([c[4] for c in cand])
    S1=collections.OrderedDict()
    for c,pp in zip(cand,cyc):
        if pp is None: continue
        _,A1,C1=parse(c[4]); C1=propre(A1,C1,pp); c=c[:4]+(situ(A1,C1),); key=canon(A1,C1,pp)
        if key==canon(A0,C0,p0): continue
        e=S1.setdefault(str(key),{'situation':c[4],'periode':pp,'ecritures':[]}); e['ecritures'].append(list(c[:4]))
        if len(C1)<len(parse(e['situation'])[2]): e['situation']=c[4]
    top=sorted(S1.values(),key=lambda e:-len(e['ecritures']))[:NS1]
    rec={'nom':pc['nom'],'tirs1':len(res),'miroirs0':sum(len(v) for v in mir0.values()),'nS1':len(S1),'S1':[]}
    for e in top:
        _,A1,C1=parse(e['situation']); p1=e['periode']
        m2,res2,orb2=run_shots(A1,C1,p1,'s2')
        K0r={r:orbit(rotA(A0,r),rotC(C0,r),p0) for r in range(4)}
        mir1=collections.defaultdict(list); ret=[]
        for (r,k,s),(o,an,ce) in zip(m2,res2):
            d=destins(o)[0]
            if ex(d,an[0])=='-': continue
            vis,Kk=orb2[r]; Pp=tuple(an[1:1+npc])
            if intact(Pp,ce,vis,Kk): mir1[f'{r}:{k}'].append([s,ex(d,an[0])]); continue
            _,v0,K0=K0r[r]
            if (Pp,frozenset(c for c in ce if c in v0)) in K0[0]: ret.append([r,k,s,ex(d,an[0]),intact(Pp,ce,v0,K0)])
        lect=[]
        def meme(x,y):
            if x=='-' or y=='-': return x==y
            (dx,lx),(dy,ly)=x.split('@'),y.split('@'); return dx==dy and abs(int(lx)-int(ly))<=4
        for k in set(mir0)&set(mir1):
            X={v for _,v in mir0[k]}; Y={v for _,v in mir1[k]}
            if any(not meme(x,y) for x in X for y in Y):
                forte=len(X)==1 and len(Y)==1 and len(mir0[k])==len(phases(p0)) and len(mir1[k])==len(phases(p1))
                lect.append({'cle':k,'S0':mir0[k],'S1':mir1[k],'forte':forte})
        rec['S1'].append({'situation':e['situation'],'periode':p1,'n_ecritures':len(e['ecritures']),'ecriture':e['ecritures'][0],
                          'tirs2':len(res2),'miroirs1':sum(len(v) for v in mir1.values()),'retours':ret[:20],'n_retours':len(ret),'lectures':lect})
    rec['duree']=round(time.time()-t0,1)
    with open(OUT,'a') as f: f.write(json.dumps(rec)+'\n')
    print(pc['nom'],rec['tirs1'],'tirs ; S1',rec['nS1'],'; retours',[s['n_retours'] for s in rec['S1']],'; lectures',[len(s['lectures']) for s in rec['S1']],f"{rec['duree']} s",flush=True)

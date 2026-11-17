# compilateur.py — Étape 3 : fonctions booléennes → UN germe LLR (sans aucune case), placement automatique, vérification automatique.
# Architecture (règles R-54…R-60) : en LLR une autoroute qui croise une trace TOURNE ; une « puissance » continue tout droit ssi
# elle ne croise AUCUNE trace = NOR de tout ce qu'elle croise.
#  - entrées en double voie : pour chaque variable v, le littéral v OU ¬v est présent (une fourmi par usage) ;
#  - niveau 1 : une porte = une puissance ↘ (cap G) qui traverse une bande de rayons ↙ (cap H) = les littéraux d'UNE clause ;
#    elle continue ssi la clause est fausse (NOR des littéraux) ;
#  - niveau 2 : une sortie = une puissance ↙ (cap H) qui croise les sorties de niveau 1 d'un INTERVALLE de portes : continue ssi
#    toutes les clauses sont vraies = forme CNF. Une sortie peut aussi être lue directement au niveau 1 (NOR d'une clause).
#  - pas de croisement parasite : chaque rayon ne commence qu'à hauteur de sa porte (rayons en « escalier »).
import itertools, subprocess, json, sys, os
sys.path.insert(0,'..')
HERE=os.path.dirname(os.path.abspath(__file__))
def cnf(f,n):
    """clauses (listes de (var, signe)) d'une forme CNF petite : impliqués premiers de ¬f (Quine-McCluskey) + couverture gloutonne."""
    zeros=[m for m in range(2**n) if not f(m)]
    if not zeros: return []
    terms={(m,0) for m in zeros}; primes=set()
    while terms:
        nxt=set(); used=set()
        for (a,ma),(b,mb) in itertools.combinations(terms,2):
            if ma==mb and bin((a^b)&~ma).count('1')==1 and (a&~ma)!=(b&~ma):
                d=(a^b)&~ma; nxt.add((a&~d,ma|d)); used|={(a,ma),(b,mb)}
        primes|=terms-used; terms=nxt
    cover=[]; left=set(zeros)
    while left:
        p=max(primes,key=lambda t:sum(1 for z in left if (z&~t[1])==t[0]))
        cover.append(p); left-={z for z in left if (z&~p[1])==p[0]}
    # implicant de ¬f (valeur v sur les bits non masqués) -> clause : OU des littéraux opposés
    return [[(i,1-((v>>i)&1)) for i in range(n) if not (m>>i)&1] for v,m in cover]
BIN='trapL16'
PAR=dict(DA=200,GAP=1000,POFF=200,SP=40,OY=0)
def ant(w,l,cap):
    if (w+l)%2: l+=1
    return ((w+l)//2,(l-w)//2,cap)
def compile_(sorties,n,noms):
    """sorties : liste de (nom, f) ; f(m) sur m = entier des n bits (bit i = variable i). Renvoie le plan."""
    gates=[]; outs=[]
    for nom,f in sorties:
        cn=cnf(lambda m:not f(m),n)
        if len(cn)==1: outs.append(dict(nom=nom,niv=1,g=[len(gates)])); gates.append(cn[0]); continue
        cl=cnf(f,n)
        outs.append(dict(nom=nom,niv=2,g=list(range(len(gates),len(gates)+len(cl))))); gates+=cl
    A0=0; DA=PAR['DA']; GAP=PAR['GAP']; lam=0; a=A0; G=[]
    for k,o in enumerate(outs):
        gap=0
        if o['niv']==2:
            est=sum(PAR['POFF']+PAR['SP']*len(gates[gi])+30 for gi in o['g']); gap=max(GAP,est+900); a-=gap
        o['gap']=gap
        for gi in o['g']:
            cl=gates[gi]; ls=lam; rays=[ls+PAR['POFF']+PAR['SP']*i for i in range(len(cl))]; top=rays[-1]
            G.append(dict(a=a,ls=ls,rays=rays,clause=cl)); a-=DA; lam=top+PAR['SP']+30
        o['L']=G[o['g'][-1]]['rays'][-1]+PAR['SP']//2+10; o['ws']=G[o['g'][0]]['a']+o['gap']-300
    return dict(gates=G,outs=outs,n=n,noms=noms)
def germe(plan,m):
    """situation LLR pour l'entrée m. Ordre des fourmis : rayons, puissances niv. 1, puissances niv. 2."""
    A=[]
    for g in plan['gates']:
        for (var,sg),lr in zip(g['clause'],g['rays']):
            if ((m>>var)&1)==sg: A.append(ant(g['a']+6,lr-1,'H'))
    idx1=[]
    for g in plan['gates']: idx1.append(len(A)); A.append(ant(g['a'],g['ls'],'G'))
    idx2={}
    for o in plan['outs']:
        if o['niv']==2: idx2[o['nom']]=len(A); A.append(ant(o['ws'],o['L']-1,'H'))
    lect={o['nom']:(idx2[o['nom']],(-1,1),o['L']+PAR['OY']) if o['niv']==2 else (idx1[o['g'][0]],(1,1),plan['gates'][o['g'][0]]['a']-PAR['OY']) for o in plan['outs']}
    return 'LLR|'+';'.join(f'{x},{y+PAR["OY"]},{c}' for x,y,c in A)+'|',lect
def T_of(plan):
    span=max(o['ws'] for o in plan['outs'] if o['niv']==2) - min(g['a'] for g in plan['gates']) if any(o['niv']==2 for o in plan['outs']) else 2000
    return 9*span+8000
def verifie(plan,sorties,moteur='C'):
    n=plan['n']; T=T_of(plan); lines=[];L=[]
    for m in range(2**n):
        s,lect=germe(plan,m); lines.append(s); L.append(lect)
    res=[]
    if moteur=='C':
        out=subprocess.run([os.path.join(HERE,BIN)],input=''.join(f'{s} {T}\n' for s in lines),capture_output=True,text=True).stdout.strip().split('\n')
        for m,(o,lect) in enumerate(zip(out,L)):
            t=[z for z in o.split() if z.startswith('A') or z in('B','X')]
            def lu(i,d,l):
                if len(t)<=i or not t[i].startswith(f'A18:{d[0]},{d[1]},'): return 0
                return int(abs(int(t[i].split(',')[2])-l)<=4)
            res.append({k:lu(i,d,l) for k,(i,d,l) in lect.items()})
    else:
        import sim
        for m,(s,lect) in enumerate(zip(lines,L)):
            _,_,_,pos=sim.run(s,T,trace=True)
            def lu(i,d,l):
                if (pos[-1][i][0]-pos[-19][i][0],pos[-1][i][1]-pos[-19][i][1])!=d: return 0
                v=min((p[i][0]+p[i][1]) if d==(-1,1) else (p[i][0]-p[i][1]) for p in pos[-18:])
                return int(abs(v-l)<=4)
            res.append({k:lu(i,d,l) for k,(i,d,l) in lect.items()})
    ok=sum(all(r[nom]==int(bool(f(m))) for nom,f in sorties) for m,r in enumerate(res))
    return ok,2**n,T,res
def taille(plan,m=None):
    s,_=germe(plan,(2**plan['n'])-1 if m is None else m); return s.count(',')//2

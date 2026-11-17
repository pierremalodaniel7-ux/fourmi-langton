# circuits.py — fabrique les « circuits » (germe de base + interrupteurs d'entrée + lecture + table attendue)
# à partir des modules Python VÉRIFIÉS du dépôt (rien n'est recopié à la main). Sortie : docs/sources/circuits.json
# Format d'un circuit :
#  base   : {fourmis:[[x,y,cap]], points:[[x,y,c]]}     (cap = 'H','D','B','G' ou chiffre)
#  entrees: [{nom, si1:{fourmis,points}, si0:{fourmis,points}}]  ; les fourmis des entrées sont jouées AVANT celles de la base
#  sorties: [{nom, fourmi:'base:k' | 'entree:nom:k' | 'toutes', type:'dir'|'dirvoie'|'compte', pas, fleche?}]
#  table  : [{e:{nom:0/1}, a:{sortie: attendu}}]  attendu : '↙' | '↙ 337' | '≠↗' | nombre (compte)
#  affichage: optionnel, {type:'somme', a:[noms bits poids croissant], b:[...], lecture:{'↙ 781':0,...}}
import sys, os, json, itertools, re
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path[:0]=[os.path.join(R,'ordinateur'),os.path.join(R,'ordinateur','v2'),os.path.join(R,'ordinateur','v3')]
C=[]
def parse_situ(s):
    r,a,c=(s.split('|')+['',''])[:3]
    F=[[int(t.split(',')[0]),int(t.split(',')[1]),t.split(',')[2].strip()] for t in a.split(';') if t.strip()]
    P=[[int(t.split(',')[0]),int(t.split(',')[1]),int(t.split(',')[2]) if len(t.split(','))>2 else 1] for t in c.split(';') if t.strip()]
    return r.strip(),F,P
def diff_entrees(cas,noms):
    """cas : {tuple d'entrées: situation}. Base = tout à 0 ; entrée i = ce qui s'ajoute quand seul le bit i vaut 1."""
    z=tuple(0 for _ in noms); r,F0,P0=parse_situ(cas[z]); E=[]
    for i,nm in enumerate(noms):
        t=tuple(1 if j==i else 0 for j in range(len(noms)))
        if t not in cas: return None
        _,F,P=parse_situ(cas[t])
        addF=[f for f in F if f not in F0]; addP=[p for p in P if p not in P0]
        if any(f not in F for f in F0) or any(p not in P for p in P0): return None
        E.append(dict(nom=nm,si1=dict(fourmis=addF,points=addP),si0=dict(fourmis=[],points=[])))
    return r,dict(fourmis=F0,points=P0),E
def ajoute(**k): C.append(k)
# ---------- A. portes RL R-40 à R-44 (ordinateur/portes_def.py) ----------
import portes_def as D
for nom,p in D.PORTES.items():
    cles=list(p['cas']); n=len(cles[0]); noms=['a','b'][:n] if 'CROISEMENT' not in nom else ['x','y']
    if 'virage' in nom: noms=['case']
    res=diff_entrees(p['cas'],noms)
    if res is None: print('!! diff impossible',nom); continue
    r,base,E=res
    if p['lire']=='tout': sorties=[dict(nom='nb ↙',fourmi='toutes',type='compte',fleche='↙',pas=p['T'])]; conv=lambda v:len(v) if v!=['↘'] else 0
    elif p['lire']=='voie': sorties=[dict(nom='P',fourmi='base:0',type='dirvoie',pas=p['T'])]
    else: sorties=[dict(nom='sortie',fourmi=('base:0' if p['lire']==-1 and base['fourmis'] else 'entree:case:0' if False else 'base:%d'%(len(base['fourmis'])-1) if base['fourmis'] else 'toutes'),type='dir',pas=p['T'])]
    if 'virage' in nom: sorties=[dict(nom='sortie',fourmi='base:0',type='dir',pas=p['T'])]
    if 'OU' in nom: sorties=[dict(nom='sortie',fourmi='base:1',type='dir',pas=p['T'])]
    tab=[]
    for e,w in p['table'].items():
        if p['lire']=='tout': a=len([x for x in w if x=='↙'])
        elif p['lire']=='voie': a=w.split(' (')[0].replace('voie ','')
        else: a=w
        tab.append(dict(e=dict(zip(noms,e)),a={sorties[0]['nom']:a}))
    rid={'fil + virage droite (−90°)':'R-40','fil + virage gauche (+90°)':'R-40','porte NON':'R-41','porte NOR':'R-41','porte ET':'R-41','COPIE (1 entrée, 2 sorties)':'R-43','OU à 2 étages = NON(NOR)':'R-42','CROISEMENT de 2 fils':'R-43','demi-additionneur (S, C) à 1 puissance':'R-43'}[nom]
    ajoute(id='C-'+re.sub(r'[^a-z0-9]+','-',nom.lower()).strip('-'),nom=nom[0].upper()+nom[1:],regle=r,base=base,entrees=E,sorties=sorties,table=tab,
           dossier='Ordinateur/RL/Portes R-40 à R-44',source=rid,date='2026-11-17',statut='VÉRIFIÉ (2 moteurs, temps fini)',note=p['note'],avancement='fait')
# ---------- B. additionneurs en un germe (R-48, R-49, R-53) ----------
import portes as Pt
def g104(x,y,r=0):
    (a,cells)=Pt.germe(x,y,r); return [[a[0],a[1],a[2]]],[[u,v,1] for u,v in sorted(cells)]
def entree_germes(nom,pos):
    F=[];P=[]
    for x,y in pos: f,p=g104(x,y); F+=f; P+=p
    return dict(nom=nom,si1=dict(fourmis=F,points=P),si0=dict(fourmis=[],points=[]))
import fa
Pf,Pc=g104((-121-391)//2,(-391+121)//2,3)
base=dict(fourmis=Pf,points=Pc+[[130,254,1],[231,369,1]])
E=[entree_germes('a',[(0,0)]),entree_germes('b',[(64,64)]),entree_germes('c',[(128,128)])]
att={0:'↘ -126',1:'↙ 337',2:'↙ 369',3:'↙ 597'}
tab=[dict(e=dict(a=a,b=b,c=c),a={'P':att[a+b+c]}) for a,b,c in itertools.product((0,1),repeat=3)]
ajoute(id='C-R48-additionneur-complet',nom='Additionneur complet à 1 puissance (a + b + c)',regle='RL',base=base,entrees=E,
       sorties=[dict(nom='P',fourmi='base:0',type='dirvoie',pas=110000)],table=tab,
       affichage=dict(type='somme',termes=['a','b','c'],lecture={'↘ -126':0,'↙ 337':1,'↙ 369':2,'↙ 597':3}),
       dossier='Ordinateur/RL/Additionneurs en un germe',source='R-48',date='2026-11-17',statut='VÉRIFIÉ (2 moteurs, 8/8)',avancement='fait',
       note="Une puissance P ↘ traverse les traces des entrées ↙ (chaque trace la décale de 4 voies) ; 2 cases trient la somme k par voie de sortie.")
d2=json.load(open(os.path.join(R,'ordinateur','v2','add2.json')))
base=dict(fourmis=Pf,points=Pc+[[x,y,1] for x,y in d2['cases']])
E=[entree_germes('a0',[(0,0)]),entree_germes('a1',[(128,128),(192,192)]),entree_germes('b0',[(64,64)]),entree_germes('b1',[(256,256),(320,320)])]
lec={**{'↙ %d'%(781+160*v):v for v in range(6)},'↘ -150':6}; inv={v:k for k,v in lec.items()}
tab=[dict(e=dict(a0=a0,a1=a1,b0=b0,b1=b1),a={'P':inv[a0+2*a1+b0+2*b1]}) for a0,a1,b0,b1 in itertools.product((0,1),repeat=4)]
ajoute(id='C-R49-additionneur-2-bits',nom='Ordinateur en un germe : additionneur 2 bits + écran',regle='RL',base=base,entrees=E,
       sorties=[dict(nom='P',fourmi='base:0',type='dirvoie',pas=150000)],table=tab,
       affichage=dict(type='somme',a=['a0','a1'],b=['b0','b1'],lecture=lec,ecran=dict(y=1100,pixels={str(v):(-319+160*v if v<6 else 950) for v in range(7)})),
       dossier='Ordinateur/RL/Additionneurs en un germe',source='R-49',date='2026-11-17',statut='VÉRIFIÉ (2 moteurs, 16/16)',avancement='fait',
       note="Bit de poids 2 = deux germes parallèles ; une puissance compte v = a + b ; 6 cases « épluchent » les voies ; écran y = 1 100, un pixel par valeur.")
import add3
base=dict(fourmis=Pf,points=Pc+[[x,y,1] for x,y in add3.CELLS])
slots={'a0':[0],'b0':[1],'a1':[2,3],'b1':[4,5],'a2':[6,7,8,9],'b2':[10,11,12,13]}
E=[entree_germes(k,[(64*i,64*i) for i in v]) for k,v in slots.items()]
lec={**{'↙ %d'%(1805+160*v):v for v in range(14)},'↘ -182':14}; inv={v:k for k,v in lec.items()}
tab=[]
for bits in itertools.product((0,1),repeat=6):
    e=dict(zip(slots,bits)); v=e['a0']+e['b0']+2*(e['a1']+e['b1'])+4*(e['a2']+e['b2']); tab.append(dict(e=e,a={'P':inv[v]}))
ajoute(id='C-R53-additionneur-3-bits',nom='Additionneur 3 bits en un germe (cases prédites)',regle='RL',base=base,entrees=E,
       sorties=[dict(nom='P',fourmi='base:0',type='dirvoie',pas=300000)],table=tab,
       affichage=dict(type='somme',a=['a0','a1','a2'],b=['b0','b1','b2'],lecture=lec),
       dossier='Ordinateur/RL/Additionneurs en un germe',source='R-53',date='2026-11-17',statut='VÉRIFIÉ (2 moteurs, 64/64)',avancement='fait',
       note="Même principe que R-49 avec les poids 1, 2, 4 ; les 14 cases sont prédites par la règle de déplacement (R-50), sans recherche.")
# ---------- C. portes LLR (R-55 à R-59) ----------
A=[[0,0,'H']]; B=[[32,32,'H']]
def llr(id_,nom,entrees,base,sortie,attendu,src,pas,note):
    E=[dict(nom=n,si1=dict(fourmis=f,points=[]),si0=dict(fourmis=[],points=[])) for n,f in entrees]
    noms=[n for n,_ in entrees]; tab=[]
    for bits in itertools.product((0,1),repeat=len(noms)):
        tab.append(dict(e=dict(zip(noms,bits)),a={sortie['nom']:attendu(*bits)}))
    ajoute(id=id_,nom=nom,regle='LLR',base=dict(fourmis=base,points=[]),entrees=E,sorties=[dict(sortie,pas=pas)],table=tab,
           dossier='Ordinateur/LLR',source=src,date='2026-11-17',statut='VÉRIFIÉ (2 moteurs)',avancement='fait',note=note)
llr('C-R55-nor-llr','Porte NOR LLR (3 fourmis, 0 case)',[('a',A),('b',B)],[[-141,-40,'G']],dict(nom='P',fourmi='base:0',type='dir'),
    lambda a,b:'↘' if a==b==0 else '↙','R-55',30000,"P continue ↘ seulement si elle ne croise aucune trace (a = b = 0) ; sinon elle tourne ↙.")
llr('C-R59-copie-llr','COPIE LLR (2 fourmis, 0 case)',[('a',A)],[[-141,-40,'G']],dict(nom='nb ↙',fourmi='toutes',type='compte',fleche='↙'),
    lambda a:2 if a else 0,'R-59',30000,"a = 1 : A continue ↙ et P tourne ↙ (2 copies) ; a = 0 : P continue ↘ (= NON a).")
llr('C-R56-ou-llr','OU LLR à 2 étages (4 fourmis, 0 case)',[('a',A),('b',B)],[[-141,-40,'G'],[-250,450,'B']],dict(nom='P2',fourmi='base:1',type='dir'),
    lambda a,b:'↗' if (a or b) else '≠↗','R-56',40000,"Étage 1 = NOR ; étage 2 (−250,450,B) monte ↗ et lit la sortie de l'étage 1 : continue ↗ ssi a OU b.")
llr('C-R57-3-etages-llr','3 étages LLR : NOR → OU → NOR (5 fourmis)',[('a',A),('b',B)],[[-141,-40,'G'],[-250,450,'B'],[540,560,'D']],dict(nom='P3',fourmi='base:2',type='dir'),
    lambda a,b:'↖' if a==b==0 else '≠↖','R-57',60000,"P3 part ↖ et lit la sortie ↗ de P2 : continue ↖ ssi a = b = 0.")
llr('C-R58-et-llr','Porte ET LLR (5 fourmis, 0 case)',[('a',[[-500,500,'H']]),('b',B)],[[-822,378,'G'],[161,461,'D'],[-840,862,'B']],dict(nom='Q',fourmi='base:2',type='dir'),
    lambda a,b:'↗' if (a and b) else '≠↗','R-58',60000,"ET = NOR(NON a, NON b) ; chaque entrée commence où il faut le long de son axe pour qu'une puissance ne voie que sa trace. Fragile (12/224 placements).")
# ---------- D. compilateur LLR (R-62, R-63, R-67) ----------
import compilateur as CO, pas_llr as PL
def compile_circuit(id_,nom,S,n,noms,src,stat,note,dossier,par):
    CO.PAR.update(par); CO.PAR['OY']=0
    plan=CO.compile_(S,n,noms); T=CO.T_of(plan)
    basef=[]
    for g in plan['gates']: x,y,c=CO.ant(g['a'],g['ls'],'G'); basef.append([x,y,c])
    k2={}
    for o in plan['outs']:
        if o['niv']==2: k2[o['nom']]=len(basef); x,y,c=CO.ant(o['ws'],o['L']-1,'H'); basef.append([x,y,c])
    E=[]
    for v,nm in enumerate(noms):
        s={}
        for val in (1,0):
            F=[]
            for g in plan['gates']:
                for (var,sg),lr in zip(g['clause'],g['rays']):
                    if var==v and sg==val: x,y,c=CO.ant(g['a']+6,lr-1,'H'); F.append([x,y,c])
            s[val]=dict(fourmis=F,points=[])
        E.append(dict(nom=nm,si1=s[1],si0=s[0]))
    sorties=[];att={}
    for o in plan['outs']:
        if o['niv']==2: sorties.append(dict(nom=o['nom'],fourmi='base:%d'%k2[o['nom']],type='dirvoie',pas=T)); att[o['nom']]='↙ %d'%o['L']
        else: gi=o['g'][0]; sorties.append(dict(nom=o['nom'],fourmi='base:%d'%gi,type='dirvoie',pas=T)); att[o['nom']]='↘ %d'%plan['gates'][gi]['a']
    tab=[]
    for m in range(2**n):
        e={nm:(m>>i)&1 for i,nm in enumerate(noms)}; tab.append(dict(e=e,a={nom_:(att[nom_] if f(m) else '≠'+att[nom_]) for nom_,f in S}))
    ajoute(id=id_,nom=nom,regle='LLR',base=dict(fourmis=basef,points=[]),entrees=E,sorties=sorties,table=tab,dossier=dossier,source=src,date='2026-11-17',
           statut=stat,avancement='fait',note=note,tolerance_voie=4)
P0=dict(DA=200,GAP=1000,POFF=200,SP=40)
compile_circuit('C-R62-demi-additionneur-llr','Demi-additionneur LLR compilé (S = XOR, C = ET)',[('S',lambda m:(m&1)^(m>>1&1)),('C',lambda m:(m&1)&(m>>1&1))],2,['a','b'],
    'R-62','VÉRIFIÉ (2 moteurs, 4/4)',"Compilé automatiquement (forme CNF) : niveau 1 = une puissance ↘ par clause, niveau 2 = une puissance ↙ qui lit un intervalle de clauses. Contient le XOR.",'Ordinateur/LLR',P0)
compile_circuit('C-R62-cap-plus-moins-1','Module « cap ± 1 » compilé (h1\', h0\')',[("h1'",lambda m:(m&1)^(m>>1&1)^(m>>2&1)),("h0'",lambda m:1-(m&1))],3,['h0','h1','c'],
    'R-62','VÉRIFIÉ (2 moteurs, 8/8)',"h1' = h1 ⊕ h0 ⊕ c (c = couleur de la case sous la fourmi), h0' = ¬h0.",'Ordinateur/Fourmi dans fourmi',P0)
for k,(nom_,f) in enumerate(PL.S):
    compile_circuit('C-R63-module-'+re.sub(r"[^a-z0-9]","",nom_.lower())+('p' if "'" in nom_ else ''),"Pas de la petite fourmi : module "+nom_,[(nom_,f)],8,PL.NOMS,'R-63',
        'VÉRIFIÉ (moteur C 256/256'+(' ; Python 29/29 échantillon)' if nom_=="h1'" else ' ; Python 256/256)'),
        "Une sortie du pas de la fourmi RL sur le tore 2×2, compilée seule. Entrées c00 c10 c01 c11 x y h1 h0 en double voie.",'Ordinateur/Fourmi dans fourmi/Modules',P0)
compile_circuit('C-R67-pas-complet','Le pas complet de la petite fourmi en UN germe',PL.S,8,PL.NOMS,'R-67','VÉRIFIÉ (256/256 moteur JavaScript v7, R-68 ; 33/33 Python)',
    "Les 8 sorties du pas (cases, position, cap) dans un seul germe LLR sans case : 35 + 7 portes, ≤ 110 fourmis, 238 940 pas.",'Ordinateur/Fourmi dans fourmi',P0)
# ---------- E. R-39 additionneur 4 bits par modules ----------
e=json.load(open(os.path.join(R,'recherche','ordinateur','entrees.json')))
CAP='HDBG'
base=dict(fourmis=[[x,y,CAP[d%4] if isinstance(d,int) else d] for x,y,d in e['fourmis']],points=[[x,y,1] for x,y in e['fixes']])
E=[]
for m in range(e['n']):
    E.append(dict(nom='a%d'%m,si1=dict(fourmis=[],points=[[x,y,1] for x,y in e['si_a1'][m]]),si0=dict(fourmis=[],points=[])))
for m in range(e['n']):
    E.append(dict(nom='b%d'%m,si1=dict(fourmis=[],points=[[x,y,1] for x,y in e['si_b1'][m]]),si0=dict(fourmis=[],points=[[x,y,1] for x,y in e['si_b0'][m]])))
idx={n:i for i,n in enumerate(e['noms'])}
sorties=[dict(nom=s,fourmi='base:%d'%idx[s],type='dir',pas=p) for s,p in e['lecture'].items()]
tab=[]
for a in range(16):
    for b in range(16):
        s=a+b; ee={**{'a%d'%m:(a>>m)&1 for m in range(4)},**{'b%d'%m:(b>>m)&1 for m in range(4)}}
        aa={'S%d'%m:('↙' if (s>>m)&1 else '↘') for m in range(4)}; aa['K3']='↗' if (s>>4)&1 else '↘'
        tab.append(dict(e=ee,a=aa))
ajoute(id='C-R39-additionneur-4-bits',nom='Additionneur 4 bits par modules enchaînés (R-39)',regle='RL',base=base,entrees=E,sorties=sorties,table=tab,
       affichage=dict(type='somme_bits',a=['a0','a1','a2','a3'],b=['b0','b1','b2','b3'],bits=['S0','S1','S2','S3','K3'],un=['↙','↙','↙','↙','↗']),
       dossier='Ordinateur/RL/Enchaînement (R-39)',source='R-39',date='2026-11-16',statut='VÉRIFIÉ (2 moteurs, 256/256, lecture au pas indiqué)',avancement='fait',
       note="4 modules additionneur complet ; la retenue passe d'un module au suivant par une autoroute. Lire chaque fourmi à SON pas (S0 95 000 … K3 411 400).")
# ---------- F. programmes R-36 à R-38 (une fourmi + cases) ----------
d=json.load(open(os.path.join(R,'docs','sources','germes_ordinateur_R36-R38.json')))
from collections import defaultdict
grp=defaultdict(list)
for g in d: grp[g['dossier']].append(g)
FL={'bas-gauche':'↙','haut-gauche':'↖','haut-droite':'↗','bas-droite':'↘'}
for dos,gs in grp.items():
    def vars_of(g):
        m=re.search(r'a=(\d+) b=(\d+)',g['nom'])
        if m: return {'a':int(m.group(1)),'b':int(m.group(2))}
        m=re.search(r' ([01]{3})',g['nom']); return {'x1':int(m.group(1)[0]),'x2':int(m.group(1)[1]),'x3':int(m.group(1)[2])}
    V=[vars_of(g) for g in gs]; mx={k:max(v[k] for v in V) for k in V[0]}
    bits=[(k,j) for k in mx for j in range(max(1,mx[k].bit_length()))]
    def bitvec(v): return tuple((v[k]>>j)&1 for k,j in bits)
    cas={bitvec(v):'RL|'+g['fourmis']+'|'+g['points'] for v,g in zip(V,gs)}
    noms=[f'{k}{j}' if mx[k]>1 else k for k,j in bits]
    res=diff_entrees(cas,noms)
    if res is None: print('!! R-36/38 non décomposable',dos); continue
    r,base,E=res
    ok=True
    for v,g in zip(V,gs):
        _,F,P=parse_situ('RL|'+g['fourmis']+'|'+g['points']); bv=bitvec(v)
        recP=base['points']+[p for i,b_ in enumerate(bv) if b_ for p in E[i]['si1']['points']]
        if sorted(map(tuple,recP))!=sorted(map(tuple,P)): ok=False
    if not ok: print('!! R-36/38 entrées non additives',dos); continue
    lec_ant='base:1' if 'R-38' in dos else 'base:0'
    pas=210000 if 'R-38' in dos else 300000
    tab=[]
    for v,g in zip(V,gs):
        m=re.search(r'(?:Ici|Sortie de la fourmi 2) ?: ?(bas-gauche|haut-gauche|haut-droite|bas-droite)',g['note']) or re.search(r'direction finale (bas-gauche|haut-gauche|haut-droite|bas-droite)',g['note'])
        if not m: ok=False; break
        tab.append(dict(e=dict(zip(noms,bitvec(v))),a={'sortie':FL[m.group(1)]}))
    if not ok: print('!! pas de direction attendue',dos); continue
    titre=dos.split('/',1)[1]
    ajoute(id='C-'+re.sub(r'[^a-z0-9]+','-',titre.lower()).strip('-'),nom='Programme '+titre,regle=r,base=base,entrees=E,
           sorties=[dict(nom='sortie',fourmi=lec_ant,type='dir',pas=pas)],table=tab,dossier='Ordinateur/RL/Additionneurs à une fourmi (R-36 à R-38)',
           source=titre.split(' ')[0],date='2026-11-16',statut='VÉRIFIÉ (rapport R-36 à R-38)',avancement='fait',
           note=gs[0]['note'].split('. Valeur attendue')[0].split(' Sortie')[0][:300])

# ---------- G. programmes R-37 non décomposables : une variante complète par combinaison d'entrées ----------
have={c['id'] for c in C}
def _pf(s_): return [[int(t.split(',')[0]),int(t.split(',')[1]),t.split(',')[2].strip()] for t in s_.split(';') if t.strip()]
def _pp(s_): return [[int(t.split(',')[0]),int(t.split(',')[1]),1] for t in s_.split(';') if t.strip()]
for dos,gs in grp.items():
    titre=dos.split('/',1)[1]; cid='C-'+re.sub(r'[^a-z0-9]+','-',titre.lower()).strip('-')
    if cid in have: continue
    var={}; tab=[]; noms=None
    for g in gs:
        m=re.search(r'a=(\d+) b=(\d+)',g['nom'])
        if m: e={'a1':int(m.group(1))>>1&1,'a0':int(m.group(1))&1,'b1':int(m.group(2))>>1&1,'b0':int(m.group(2))&1}
        else:
            m=re.search(r' ([01]{3})',g['nom']); e={'x1':int(m.group(1)[0]),'x2':int(m.group(1)[1]),'x3':int(m.group(1)[2])}
        noms=list(e); key=','.join(f'{k}={v}' for k,v in sorted(e.items()))
        var[key]=dict(fourmis=_pf(g['fourmis']),points=_pp(g['points']))
        mm=re.search(r'Ici ?: ?(bas-gauche|haut-gauche|haut-droite|bas-droite)',g['note'])
        tab.append(dict(e=e,a={'sortie':FL[mm.group(1)]}))
    ajoute(id=cid,nom='Programme '+titre,regle='RL',variantes=var,entrees=[dict(nom=n) for n in noms],
        sorties=[dict(nom='sortie',fourmi='base:0',type='dir',pas=300000)],table=tab,dossier='Ordinateur/RL/Additionneurs à une fourmi (R-36 à R-38)',
        source='R-37',date='2026-11-16',statut='VÉRIFIÉ (rapport R-37)',avancement='fait',
        note=gs[0]['note'].split('. Valeur attendue')[0][:300]+" Chaque combinaison d'entrées a son propre jeu de cases (taille exponentielle) : les interrupteurs choisissent la variante.")
json.dump(C,open(os.path.join(R,'docs','sources','circuits.json'),'w'),ensure_ascii=False)
print(len(C),'circuits :',[c['id'] for c in C])

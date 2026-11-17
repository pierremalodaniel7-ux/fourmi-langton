# livrables.py — germes (1 par résultat), images, bestiaire PDF (bestiaire 9).
import sys; sys.path.insert(0,'..')
import sim, json, numpy as np, portes as Pt
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ruban, pieges as Pg, fa, add2
R=[]
# 1. ordinateur 2 bits
d=json.load(open('add2.json')); C2=[tuple(c) for c in d['cases']]
e=(1,1,1,0)   # 3 + 2
st_add='RL|'+Pt.situ(add2.gin(e)+[add2.P()],extra=C2)
base='RL|'+Pt.situ([add2.P()],extra=C2)
def germ_str(g): a,c=g; return a,c
inp={k:Pt.germe(*xy,0) for k,xy in {'a0':(0,0),'b0':(64,64),'a1':(128,128),'a1bis':(192,192),'b1':(256,256),'b1bis':(320,320)}.items()}
def txt(g): (x,y,dd),cells=g; return f"fourmi {x},{y},{dd} + cases "+' ; '.join(f'{a},{b}' for a,b in sorted(cells))
note_in=' | '.join(f"{k} : {txt(g)}" for k,g in inp.items())
R.append(dict(dossier='ordinateur/R-49 additionneur 2 bits',nom='Ordinateur en un germe : additionneur 2 bits + écran',regle='RL',
  fourmis=base.split('|')[1].replace(';',' ; '),points=base.split('|')[2].replace(';',' ; '),
  note=("R-49, VÉRIFIÉ 16/16 (2 moteurs, 150 000 pas). Germe ci-dessus = 0+0 (puissance P + 6 cases). Pour mettre une entrée à 1, AJOUTER : "
        "a0 = germe a0 ; b0 = germe b0 ; a1 = germes a1 ET a1bis ; b1 = germes b1 ET b1bis. "+note_in+
        ". Lecture : laisser tourner 150 000 pas ; écran = bande y = 1 100 : un seul pixel allumé, en x = −319 + 160·v pour v = a+b ≤ 5, en x = 950 pour v = 6. Ex. 3+2 : ajouter a0, a1, a1bis, b1, b1bis → pixel x = 481.")))
# 2. additionneur complet
st_fa_base='RL|'+Pt.situ([fa.P(-121)],extra=[(130,254),(231,369)])
inf={k:Pt.germe(*xy,0) for k,xy in {'a':(0,0),'b':(64,64),'c':(128,128)}.items()}
R.append(dict(dossier='ordinateur/R-48 additionneur complet',nom='Additionneur complet à 1 puissance',regle='RL',
  fourmis=st_fa_base.split('|')[1].replace(';',' ; '),points=st_fa_base.split('|')[2].replace(';',' ; '),
  note="R-48, VÉRIFIÉ 8/8 (2 moteurs, 110 000 pas). Germe = entrées à 0. Pour une entrée à 1, AJOUTER : "+' | '.join(f'{k} : {txt(g)}' for k,g in inf.items())+
  ". Sortie : k = a+b+c ; k=0 → P continue ↘ ; k=1 → ↙ voie x+y=337 ; k=2 → ↙ 369 ; k=3 → ↙ 597. Écran y = 900 : pixels x = −563 (k1), −531 (k2), −303 (k3) ; S = k1 ou k3, C = k2 ou k3."))
# 3. réservoir ruban 15
g,c=ruban.ruban(15); st_r='RL|'+Pt.situ(g,extra=c)
R.append(dict(dossier='ordinateur/R-46 réservoir',nom='Réservoir ruban : 15 autoroutes lâchées une à une',regle='RL',
  fourmis=st_r.split('|')[1].replace(';',' ; '),points=st_r.split('|')[2].replace(';',' ; '),
  note="R-46, VÉRIFIÉ 15/15 (2 moteurs, 92 400 pas). 15 germes 104 ↙ parallèles (voies x+y espacées de 20) ; une case par fourmi la lâche vers ↘, de l'extérieur vers l'intérieur, 40 périodes plus loin à chaque fois. Voies des lâchées x−y = −56 − 160k. Enlever la case k : la fourmi k continue ↙."))
# 4. pièges
pv=[x for x in json.load(open('pieges_vrais.json')) if x['type']=='capture']
best=sorted(pv,key=lambda x:x['periode'])[0]; pg=[x for x in pv if x['cycle']=='Petit Grain 8' and x['rot']==0 and x['p']==-1 and x['s']==3][0]
for x,lab in ((best,'le plus court'),(pg,'Petit Grain du chat, corrigé')):
    R.append(dict(dossier='ordinateur/R-47 pièges',nom=f"Piège {x['cycle']} rot {x['rot']} ({lab})",regle='RL',
      fourmis=x['germe'].split('|')[1].replace(';',' ; '),points=x['germe'].split('|')[2].replace(';',' ; '),
      note=f"R-47, VÉRIFIÉ (cycle exact, 2 moteurs). Source 104 ↙ (fourmi 1) + piège à l'origine (−160+p+s, 160+p−s), p={x['p']}, s={x['s']}. Après capture : cycle exact de période {x['periode']} + UNE 104 éjectée ({x['qui']}) déplacement/voie {x['eject']}. 200 000 pas."))
import add3
b3='RL|'+Pt.situ([add3.P],extra=add3.CELLS)
R.insert(1,dict(dossier='ordinateur/R-53 additionneur 3 bits',nom='Additionneur 3 bits en un germe (cases prédites)',regle='RL',
  fourmis=b3.split('|')[1].replace(';',' ; '),points=b3.split('|')[2].replace(';',' ; '),
  note=("R-53, VÉRIFIÉ 64/64 (2 moteurs, 300 000 pas). Germe = 0+0. Entrées : germe 104 tourné ↙ = fourmi (64i,64i,D) + 11 cases du germe "
        "(−2,−2)(−1,−2)(0,−1)(1,0)(−2,1)(1,1)(−2,2)(0,2)(−1,3)(0,3)(0,4) décalées de (64i,64i). Emplacements i : a0 → 0 ; b0 → 1 ; a1 → 2,3 ; b1 → 4,5 ; "
        "a2 → 6,7,8,9 ; b2 → 10,11,12,13. Sortie : valeur v = a+b sort ↙ sur la voie x+y = 1805 + 160v (v ≤ 13), v = 14 reste ↘. "
        "Les 14 cases ont été PRÉDITES par la règle R-50 (cases de R-49 glissées de 256×(2,2)), sans recherche.")))
json.dump(R,open('germes_ordinateur2_2026-11-17.json','w'),ensure_ascii=False,indent=1)
# images
def img(st,T,win,ds):
    _,g,_,_=sim.run(st,T); x0,x1,y0,y1=win; M=np.ones(((y1-y0)//ds+1,(x1-x0)//ds+1))
    for (x,y),v in g.items():
        if v and x0<=x<=x1 and y0<=y<=y1: M[(y-y0)//ds,(x-x0)//ds]=0
    return M
st3='RL|'+Pt.situ(add3.gin((0,1,1,1,0,1))+[add3.P],extra=add3.CELLS)
FIG=[('Ordinateur en un germe : 3 + 2 = 5 (pixel 5 allumé sur la bande y = 1 100)',st_add,150000,(-1300,1100,-500,1300),4,('band',1100)),
     ('Additionneur 3 bits : 3 + 5 = 8 (sortie ↙ voie 3085)',st3,300000,(-2200,2500,-1200,2600),8,None),
     ('Additionneur complet : a=1, b=0, c=1 → k=2 (sortie ↙ voie 369)','RL|'+Pt.situ([inf['a'],inf['c'],fa.P(-121)],extra=[(130,254),(231,369)]),110000,(-900,900,-500,1000),3,('band',900)),
     ('Réservoir ruban N = 8 : 8 lâchers vers ↘','RL|'+Pt.situ(*[ruban.ruban(8)[0]],extra=ruban.ruban(8)[1]),63280,(-1000,1400,-300,1300),4,None),
     (f"Piège : {best['cycle']} (rot {best['rot']}) capture la 104, cycle {best['periode']} + 1 éjectée",best['germe'],60000,(-400,400,-200,500),2,None)]
with PdfPages('bestiaire_9_ordinateur_v2.pdf') as pdf:
    f=plt.figure(figsize=(8.27,11.69)); f.text(0.07,0.93,'Bestiaire 9 — Vers un vrai ordinateur à fourmis (R-45 à R-50)',size=14,weight='bold')
    f.text(0.07,0.89,"RL, y vers le bas, fourmis jouées dans l'ordre. Germe 104 = fourmi + 11 cases.\nPrincipe (R-41) : une puissance P ↘ traverse les TRACES des entrées ↙ ; chaque trace la décale de 4 voies (classe x−y ≡ 3 mod 4) ;\nles décalages s'additionnent (vérifié jusqu'à 6 traces) : voie de P = L − 4·(somme pondérée). Des cases « épluchent » les voies.\nStatut : VÉRIFIÉ = 2 moteurs (C, Python), temps fini ; une simulation finie ne prouve rien sur l'infini.",size=8,va='top')
    pdf.savefig(f); plt.close(f)
    for i,(t,st,T,win,ds,band) in enumerate(FIG):
        M=img(st,T,win,ds); f,ax=plt.subplots(figsize=(8.27,8)); ax.imshow(M,cmap='gray',extent=(win[0],win[1],win[3],win[2]),interpolation='nearest')
        if band: ax.axhline(band[1],color='red',lw=0.6)
        ax.set_title(t,size=10); ax.tick_params(labelsize=6); f.text(0.05,0.02,R[i]['note'][:600],size=6,wrap=True)
        pdf.savefig(f); f.savefig(f'fig{i+1}.png',dpi=90); plt.close(f)
print(len(R),'germes ; PDF ok')

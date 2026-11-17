# livrables3.py — germes (un par résultat) + images + bestiaire 10.
import compilateur as C, pas_llr as PL, json, sys, numpy as np
sys.path.insert(0,'..'); import sim
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
def note_entrees(plan):
    t=[]
    for v,nm in enumerate(plan['noms']):
        for val in (1,0):
            A=[]
            for g in plan['gates']:
                for (var,sg),lr in zip(g['clause'],g['rays']):
                    if var==v and sg==val: x,y,c=C.ant(g['a']+6,lr-1,'H'); A.append(f'{x},{y+C.PAR["OY"]},H')
            if A: t.append(f"{nm}={val} : ajouter {' ; '.join(A)}")
    return ' | '.join(t)
def base(plan):
    A=[]
    for g in plan['gates']: x,y,c=C.ant(g['a'],g['ls'],'G'); A.append(f'{x},{y+C.PAR["OY"]},G')
    for o in plan['outs']:
        if o['niv']==2: x,y,c=C.ant(o['ws'],o['L']-1,'H'); A.append(f'{x},{y+C.PAR["OY"]},H')
    return ' ; '.join(A)
def lecture(plan):
    return ' ; '.join(f"{o['nom']} = 1 ssi la fourmi de sortie part {'↙ sur la voie x+y = '+str(o['L']+C.PAR['OY']) if o['niv']==2 else '↘ sur la voie x−y = '+str(plan['gates'][o['g'][0]]['a']-C.PAR['OY'])}" for o in plan['outs'])
G=[]; FIG=[]
C.PAR.update(DA=200,GAP=1000,POFF=200,SP=40,OY=0)
for nom,n,noms,S,stat in [('Demi-additionneur LLR compilé (S = XOR, C = ET)',2,['a','b'],[('S',lambda m:(m&1)^(m>>1&1)),('C',lambda m:(m&1)&(m>>1&1))],'VÉRIFIÉ 4/4 (2 moteurs)'),
                          ('Module « cap ± 1 » compilé (h1\', h0\')',3,['h0','h1','c'],[("h1'",lambda m:(m&1)^(m>>1&1)^(m>>2&1)),("h0'",lambda m:1-(m&1))],'VÉRIFIÉ 8/8 (2 moteurs)')]:
    p=C.compile_(S,n,noms); T=C.T_of(p)
    G.append(dict(dossier='ordinateur/R-62 compilateur LLR',nom=nom,regle='LLR',fourmis=base(p),points='',
      note=f"R-62, {stat}, {T} pas. Germe = puissances seules ; entrées en DOUBLE VOIE : pour chaque variable, ajouter les fourmis de sa valeur (mettre ces fourmis AVANT les puissances dans la liste). {note_entrees(p)}. Lecture : {lecture(p)}."))
    FIG.append((nom+' — entrées toutes à 1',C.germe(p,2**n-1)[0],T))
C.PAR.update(POFF=80,SP=30,DA=60)
nom,f=PL.S[0]; p=C.compile_([(nom,f)],8,PL.NOMS); T=C.T_of(p)
ymin=min(g['ls']-g['a'] for g in p['gates'])//2; ymax=max(g['rays'][-1]-g['a'] for g in p['gates'])//2; C.PAR['OY']=-(ymax+ymin)//2 - T//36
G.append(dict(dossier='ordinateur/R-63 pas de la petite fourmi',nom="Pas de la petite fourmi : module c00' (mise à jour d'une case)",regle='LLR',fourmis=base(p),points='',
  note=f"R-63, VÉRIFIÉ 256/256 (moteur C), {T} pas. c00' = c00 ⊕ [x=0 ∧ y=0]. Variables c00 c10 c01 c11 x y h1 h0 en double voie. {note_entrees(p)}. Lecture : {lecture(p)}. Les modules c10', c01', c11', x', y', h0' sont produits par le même compilateur (pas_modules.py), 256/256 chacun."))
FIG.append(("Module c00' — état 0x13",C.germe(p,0x13)[0],T))
json.dump(G,open('germes_fourmi_dans_fourmi_2026-11-17.json','w'),ensure_ascii=False,indent=1)
with PdfPages('bestiaire_10_fourmi_dans_fourmi.pdf') as pdf:
    f=plt.figure(figsize=(8.27,11.69)); f.text(0.07,0.93,'Bestiaire 10 — Fourmi dans fourmi : les fondations (R-61 à R-65)',size=14,weight='bold')
    f.text(0.07,0.89,"Circuit d'un pas de la fourmi RL sur le tore 2×2 (R-61) et compilateur LLR (R-62, R-63).\nLLR : une autoroute qui croise une trace TOURNE ; une « puissance » continue ssi elle ne croise aucune trace = NOR.\nNiveau 1 = une puissance ↘ par clause ; niveau 2 = une puissance ↙ lit un intervalle de clauses : forme CNF, sans case.\nVÉRIFIÉ = 2 moteurs (ou moteur C seul, dit), temps fini.",size=8,va='top')
    im=plt.imread('schema_pas.png'); ax=f.add_axes([0.03,0.05,0.94,0.75]); ax.imshow(im); ax.axis('off'); pdf.savefig(f); plt.close(f)
    for t,st,T in FIG:
        _,g,_,_=sim.run(st,T); pts=np.array([k for k,v in g.items() if v])
        f,ax=plt.subplots(figsize=(8.27,8)); ax.scatter(pts[:,0],pts[:,1],s=0.05,c='k'); ax.invert_yaxis(); ax.set_aspect('equal')
        ax.set_title(t,size=10); pdf.savefig(f); f.savefig('fig_'+str(len(t))+'.png',dpi=80); plt.close(f)
print(len(G),'germes ; PDF ok')

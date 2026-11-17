# images.py — une image par cas de chaque porte (grille finale, moteur Python) + bestiaire PDF + germes.json
import sim, portes_def as D, json, numpy as np, re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
bil=json.load(open('verif_bilan.json'))
def img(st,T,win):
    a,g,_,_=sim.run(st,T); x0,x1,y0,y1=win; M=np.ones((y1-y0,x1-x0))
    for (x,y),v in g.items():
        if v and x0<=x<x1 and y0<=y<y1: M[y-y0,x-x0]=0
    return M,a
WIN={'fil':(-120,60,-40,140)}
def fiche(nom,p):
    win=(-130,40,-40,130) if 'virage' in nom else ((-500,700,-450,1100) if 'OU' in nom else (-400,600,-450,1000))
    st0=list(p['cas'].values())[0]; cells=[tuple(map(int,c.split(','))) for c in st0.split('|')[2].split(';') if c]
    ims=[]
    for e,st in p['cas'].items(): ims.append((e,)+img(st,p['T'],win))
    return win,ims
germes=[]; ecr=json.load(open('ecran.json'))
with PdfPages('bestiaire_ordinateur_2026-11-17.pdf') as pdf:
    f=plt.figure(figsize=(8.27,11.69)); f.text(0.08,0.92,"Bestiaire 8 — Ordinateur à fourmis (R-40 à R-43)",size=16,weight='bold')
    txt=("Règle RL, grille carrée, y vers le bas ; fourmis jouées l'une après l'autre. Germe d'autoroute 104 = fourmi + 11 cases, tourné.\n"
         "Bit = une autoroute ↙ est là (1) ou pas (0). Une « puissance » P (↘) part plus loin, arrive APRÈS les entrées et traverse\n"
         "leurs TRACES : chaque trace la décale de 4 voies (classe x−y ≡ 3 mod 4). Voie de P = L − 4·(nb d'entrées à 1) : un compteur.\n"
         "Une case d'aiguillage placée sur une seule voie fait tourner P vers ↙ : c'est la sortie, dans le même sens que les entrées.\n"
         "Les portes ne lisent que des traces : l'ordre d'arrivée compte, pas le retard exact (retard réglable = reculer un germe).\n\n"
         "Statuts : tables de vérité VÉRIFIÉES par 2 moteurs (C : gate.c ; Python : sim.py) sur un temps fini (60 000 à 110 000 pas).\n"
         "Une simulation finie ne prouve pas le comportement infini ; robustesse à ±1 case faible (voies exactes nécessaires).\n\n"
         "Bilan (2e moteur) :\n"+"\n".join(f"  {k} : {v}" for k,v in bil.items())+
         "\n\nÉcran (objectif 3) : bande y = 900 ; pixel S en x = −563, pixel C en x = −531 (sorties du demi-additionneur).\n"
         "Lu sur les 4 entrées : "+", ".join(f"{k} → S{v['S']} C{v['C']}" for k,v in ecr.items())+"  (juste 4/4).")
    f.text(0.08,0.88,txt,size=8,va='top',family='DejaVu Sans'); pdf.savefig(f); plt.close(f)
    for nom,p in D.PORTES.items():
        win,ims=fiche(nom,p); n=len(ims)
        f,axs=plt.subplots(1 if n==2 else 2,2,figsize=(8.27,9.5 if n==4 else 5.8)); axs=np.array(axs).reshape(-1)
        for ax,(e,M,a) in zip(axs,ims):
            ax.imshow(M,cmap='gray',vmin=0,vmax=1,extent=(win[0],win[1],win[3],win[2]),interpolation='nearest')
            ax.set_title(f"entrées {e} → {p['table'][e]}",size=9); ax.tick_params(labelsize=6)
        f.suptitle(f"{nom} — {bil[nom]} juste (2 moteurs)",size=12,weight='bold')
        f.text(0.05,0.01,p['note'],size=8,wrap=True); pdf.savefig(f); f.savefig('img/'+re.sub(r'[^a-zA-Z0-9]+','_',nom)+'.png',dpi=80); plt.close(f)
        for e,st in p['cas'].items():
            r,a,c=st.split('|')
            germes.append(dict(dossier='ordinateur/'+nom,nom=f"{nom} — entrées {e}",regle=r,fourmis=a.replace(';',' ; '),points=c.replace(';',' ; '),
                               note=f"Attendu : {p['table'][e]} (lire la fourmi de sortie après {p['T']} pas). {p['note']} VÉRIFIÉ 2 moteurs, temps fini. R-40 à R-43, 17/11."))
json.dump(germes,open('germes_ordinateur_2026-11-17.json','w'),ensure_ascii=False,indent=1)
print(len(germes),'germes')

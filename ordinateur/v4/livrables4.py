# livrables4.py — images + bestiaire 11 (PDF) + germes_2026-11-18.json + ajouts au catalogue (format docs/sources/catalogue.json)
import sys, json; sys.path.insert(0,'..'); sys.path.insert(0,'../v3'); import sim
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap
import numpy as np
from lemme104 import REF
import lnr
FIG=[]; G=[]; CAT=[]
def grille(ax,g,ants,titre,marge=2,cols=('white','black','#d62728','#1f77b4','#2ca02c','#9467bd','#8c564b','#e377c2')):
    ks=list(g)+[(a[0],a[1]) for a in ants]
    x0=min(k[0] for k in ks)-marge; x1=max(k[0] for k in ks)+marge; y0=min(k[1] for k in ks)-marge; y1=max(k[1] for k in ks)+marge
    M=np.zeros((y1-y0+1,x1-x0+1),int)
    for (x,y),c in g.items(): M[y-y0,x-x0]=c
    q=max(2,M.max()+1); ax.imshow(M,cmap=ListedColormap(list(cols[:q])),interpolation='nearest',extent=(x0-.5,x1+.5,y1+.5,y0-.5))
    for a in ants: ax.plot(a[0],a[1],'o',color='orange',ms=4 if len(ks)<3000 else 2)
    ax.set_title(titre,fontsize=9); ax.set_aspect('equal')
def fiche(titre,texte,dessin,ref):
    fig=plt.figure(figsize=(8.27,11.69)); ax=fig.add_axes([0.08,0.36,0.84,0.55]); dessin(ax)
    fig.text(0.08,0.975,titre.replace(' : ',' :\n',1) if len(titre)>70 else titre,fontsize=12,weight='bold',va='top')
    fig.text(0.08,0.32,texte,fontsize=8.5,va='top',wrap=True,family='DejaVu Sans')
    FIG.append(fig); fig.savefig(f'img_{ref}.png',dpi=110)
def txt(lines): return '\n'.join(lines)
import compilateur as C, pas_llr as PL
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
plan1=C.compile_(PL.S,8,PL.NOMS); T1=C.T_of(plan1); s1,_=C.germe(plan1,0)
import importlib.util
src=open('pas2_creux.py').read().split("k,K=int")[0].replace("from pas256_creux import lit","")
ns={}; exec(src.replace("lines=[];L=[]","lines=[];L=[]\nif False:"),ns) if False else None
# --- plan 2 pas (avec correctif d'ordre)
import pas
def vec(t): return [t['c'][(0,0)],t['c'][(1,0)],t['c'][(0,1)],t['c'][(1,1)],t['x'],t['y'],t['h']>>1,t['h']&1]
S2=[(nm+"''",(lambda k:lambda m: vec(pas.vrai_pas(pas.vrai_pas(PL.etat(m))))[k])(k)) for k,nm in enumerate(PL.NOMS)]
niv1=lambda f: len(C.cnf(lambda m:not f(m),8))==1
S2=[s for s in S2 if not niv1(s[1])]+[s for s in S2 if niv1(s[1])]
plan2=C.compile_(S2,8,PL.NOMS); T2=C.T_of(plan2); s2,_=C.germe(plan2,0)
def fourmis_de(s): return s.split('|')[1]
# 1. R-69
img=plt.imread('../v3/fig_68.png')
fiche("R-69 — Le pas complet de la petite fourmi, un germe LLR : 256/256 (moteur creux)",
 txt(["Situation : germe unique du pas (R-67) : ≤ 110 fourmis LLR, aucune case, T = 238 940 pas. Entrée = état (4 cases, x, y, cap) de la",
      "petite fourmi sur le tore 2×2 ; sortie = 8 autoroutes lues au pas T.",
      "Signature : nouveau moteur à GRILLE CREUSE (ordinateur/v4/creux.c, table de hachage, 7,3 M cases, 1,4 s par état) :",
      "les 8 sorties justes pour les 256 états. Contrôlé = sim.py sur 7/7 situations ; 1er essai faux (bug de clé (−1,−1), corrigé).",
      "Statut : VÉRIFIÉ en temps fini (moteur creux + moteur JS R-68 + Python léger, voir rapport).",
      "Commande : cd ordinateur/v4 ; python3 pas256_creux.py k 4 (k = 0..3).",
      "Image : figure du germe unique (R-68, reprise)."]),
 lambda ax:(ax.imshow(img),ax.axis('off')),'R-69')
G.append(dict(dossier="Ordinateur/R-69 pas complet (moteur creux)",nom="Pas complet de la petite fourmi — germe unique, état 0",regle="LLR",
  fourmis=fourmis_de(s1),points="",statut="VÉRIFIÉ 256/256 (temps fini, moteur creux + JS + Python)",ref="R-69",
  note=f"État d'entrée 0 (tout blanc, x=y=0, cap H). Lecture au pas {T1}. Pour les autres états, regénérer : ordinateur/v4/pas256_creux.py (C.germe(plan, m))."))
# 2. R-70
def lay(ax,s,titre):
    A=[tuple(map(int,t.split(',')[:2])) for t in fourmis_de(s).split(';')]
    ax.scatter([a[0] for a in A],[a[1] for a in A],s=6,c=['#1f77b4' if t.endswith('H') else '#d62728' for t in fourmis_de(s).split(';')])
    ax.invert_yaxis(); ax.set_aspect('equal'); ax.set_title(titre,fontsize=9)
fiche("R-70 — DEUX pas de la petite fourmi en un germe LLR : 256/256",
 txt(["Situation : la fonction pas∘pas (8 bits → 8 bits) compilée par le compilateur v3 : 39 portes + 5, ≤ 119 fourmis, T = 239 120.",
      "Signature : 248/256 au 1er essai (y'' faux) → limite du compilateur : une sortie de niveau 1 est coupée par une puissance de",
      "niveau 2 placée après elle. Sorties de niveau 1 placées en dernier ⇒ 256/256 (moteur creux).",
      "Ce n'est PAS un chaînage physique (pas de croisement) : la composée est compilée d'un coup.",
      "Statut : VÉRIFIÉ 256/256 par 2 moteurs (creux + Python), temps fini.",
      "Commande : cd ordinateur/v4 ; python3 pas2_creux.py k 4.",
      "Image : position des fourmis du germe (état 0) ; bleu = cap H (rayons, sorties ↙), rouge = cap G (puissances)."]),
 lambda ax:lay(ax,s2,"germe 2 pas, état 0"),'R-70')
G.append(dict(dossier="Ordinateur/R-70 deux pas",nom="Deux pas de la petite fourmi — germe unique, état 0",regle="LLR",fourmis=fourmis_de(s2),points="",
  statut="VÉRIFIÉ 256/256 (temps fini, moteur creux + Python)",ref="R-70",note=f"Lecture au pas {T2}. Autres états : ordinateur/v4/pas2_creux.py."))
# 3. R-71
d0,W,R,v=REF[0]
def dess71(ax):
    g={w:(1 if R[w] else 0) for w in W}
    for k in range(1,4):
        for w in W:
            c=(w[0]+k*v[0],w[1]+k*v[1])
            if c not in g: g[c]=0
    grille(ax,{c:(2 if c in W and not R[c] else (1 if c in W else 3)) for c in g},[(0,0,0)],"fenêtre W (43 cases : noir/rouge) et tube devant (bleu, blanc)",cols=('white','black','#f4a3a3','#cfe3ff'))
fiche("R-71 — Lemme de l'autoroute 104 dans le blanc (connu, Gajardo-Moreira-Goles) : bande de 11 diagonales",
 txt(["Énoncé : une fourmi RL qui lit le motif 104 sur sa fenêtre W (43 cases, 11 diagonales x+y ∈ [s−4, s+6]) et dont le tube devant",
      "∪_{k≥1}(W+k·v) est blanc et libre d'autres fourmis reste en autoroute POUR TOUJOURS (récurrence sur les périodes ; 22 cases neuves",
      "par période, blanches). Plusieurs fourmis : demi-bandes disjointes.",
      "Application : R-17 (1 case dans [−5,5]²) : 120/120 VÉRIFIÉS pour toujours ; 2 cases : 100/100 paires tirées VÉRIFIÉES.",
      "Statut : lemme VÉRIFIÉ (preuve + calcul fini de W) ; déjà connu (implicite chez Gajardo-Moreira-Goles 2002), pas nouveau.",
      "Commande : cd ordinateur/v4 ; python3 fen104.py ; python3 lemme104.py ; python3 lemme_r17.py 100.",
      "Image : fenêtre lue pendant une période (rouge = blanche, noir = noire) et le tube devant (bleu clair, doit être blanc)."]),dess71,'R-71')
# 4. R-72
def dess72(ax):
    lu,pos,g=lnr.run(3,24*3+7+3*52)
    x,y,d=pos[-1]; grille(ax,g,[(x,y,d)],"L³R après 24n+7 + 3 périodes (n = 3)",cols=('white','#444','#888','#bbb','black'))
fiche("R-72 — LⁿR : autoroute de période 16n+4 dès le pas 24n+7, pour TOUT n ≥ 3 (preuve symbolique)",
 txt(["Mots des couleurs lues : B = 0⁴1⁴…(n−1)⁴R (n tours d'un carré 2×2), C = 1000 2111 … (n−1)(n−2)³, D = 2010 3121 … ;",
      "transitoire = B³·RRR0R·B²·C·R (24n+7) ; période = RR(n−1)R·B·(n−1)000·RRR1R·B·C·R·D (16n+4), déplacement (−2,+2).",
      "Preuve : simulation symbolique (couleurs a·n+b mod n+1, tours de carré répétés m = min(n−c) fois d'un coup) ; toutes les",
      "décisions valent pour n ≥ 3 ; récurrence au pas 24n+7 / 40n+11 + lemme d'autoroute (fenêtre 15 cases, 10 neuves blanches).",
      "Contre-vérif : état symbolique = simulation concrète pour n = 3…12. Période minimale, départ au plus tôt.",
      "Statut : VÉRIFIÉ (preuve assistée par ordinateur). Périodes connues (Gajardo-Lutfalla-Rao) ; preuve uniforme + 24n+7 : à confirmer.",
      "Commande : cd ordinateur/v4 ; python3 lnr_sym.py"]),dess72,'R-72')
G.append(dict(dossier="Autoroutes/R-72 famille LⁿR",nom="L³R : autoroute 52 dès le pas 31",regle="LLLR",fourmis="0,0,H",points="",statut="VÉRIFIÉ (tout n ≥ 3)",ref="R-72",
  note="Remplacer LLLR par LⁿR (n ≥ 3) : période 16n+4, déplacement (−2,+2), dès le pas 24n+7 (preuve symbolique, lnr_sym.py)."))
# 5. R-73
V=[l.strip() for l in open('vaisseaux.txt')]
def dess73(ax):
    ax.axis('off'); f=ax.figure
    for i,(s,t) in enumerate(zip(V,[350,550,1900,2150])):
        a2=f.add_axes([0.08+0.43*(i%2),0.645-0.265*(i//2),0.38,0.23]); ants,g,_,_=sim.run(s,t+400)
        n=s.split('|')[0].count('L')
        # ne dessiner que la zone autour des fourmis
        cx,cy=(ants[0][0]+ants[1][0])//2,(ants[0][1]+ants[1][1])//2; gg={k:c for k,c in g.items() if abs(k[0]-cx)<=10 and abs(k[1]-cy)<=10}
        grille(a2,gg,ants,f"n = {n} : période {(8*n+2)//3}",cols=['white']+[plt.cm.viridis(j/(n)) for j in range(n)])
fiche("R-73 — Vaisseaux rapides à 2 fourmis en LⁿR (n = 2, 5, …, 23) : période (8n+2)/3, vitesse ×3",
 txt(["Situation : 2 fourmis LⁿR proches (germes ci-dessous). Signature : le groupe avance d'une diagonale tous les (8n+2)/3 tours",
      "(6, 14, 22, 30, 38, 46, 54, 62), 3 fois plus vite qu'une fourmi seule. n ≡ 2 mod 3 ; n = 11 PRÉDIT puis trouvé. Images : n = 2, 5, 8, 11.",
      "Preuve pour toujours : lemme générique (lemme_gen.py) pour les 8 cas n = 2…23 (dès t = 350 à 3 000). Revérifié avec sim.py (LLR).",
      "Germes (n = 2, 5, 8, 11) : " + " ; ".join(V[:4]) + " ; n = 14…23 : voir germes JSON.",
      "Statut : VÉRIFIÉ (8 cas, pour toujours) ; famille pour tout n ≡ 2 mod 3 : OUVERT (conjecture, 8/8).",
      "Littérature : rien trouvé (1 recherche) ; « Ants on the highway » non relu (arXiv inaccessible).",
      "Commande : cd ordinateur/v4 ; python3 lemme_gen.py ; ./src/fourmi \"LLR|3,1,H;1,2,H|\""]),dess73,'R-73')
for s,t in zip(V,[350,550,1900,2150,2500,1500,1500,3000]):
    n=s.split('|')[0].count('L')
    G.append(dict(dossier="Vaisseaux/R-73 vaisseaux rapides LⁿR",nom=f"Vaisseau rapide L{n}R à 2 fourmis (période {(8*n+2)//3})",regle=s.split('|')[0],
      fourmis=s.split('|')[1],points="",statut="VÉRIFIÉ (pour toujours, lemme)",ref="R-73",note=f"Vaisseau formé et prouvé dès le pas {t} ; vitesse 3 fois celle d'une fourmi seule."))
G.append(dict(dossier="Vaisseaux/R-73 vaisseaux rapides LⁿR",nom="Vaisseau LLR à 2 fourmis (germe le plus simple)",regle="LLR",fourmis="3,1,H;1,2,H",points="",
  statut="VÉRIFIÉ (pour toujours, lemme, dès le pas 420)",ref="R-73",note="Période 6, déplacement (−1,+1) ; une fourmi LLR seule : 18."))
with PdfPages('bestiaire_11_2026-11-18.pdf') as pdf:
    for f in FIG: pdf.savefig(f)
json.dump(G,open('germes_2026-11-18.json','w'),ensure_ascii=False,indent=1)
CAT=[dict(id=f"B11-{i+1}",b=11,classe=x['dossier'].split('/')[0],nom=x['nom'],regle=x['regle'],fourmis=x['fourmis'],points=x['points'],
          img=[0,""],situation=x['dossier'],deroulement=x['ref']+", "+x['statut']+". "+x['note']) for i,x in enumerate(G)]
json.dump(CAT,open('catalogue_ajouts_b11.json','w'),ensure_ascii=False,indent=1)
print(len(FIG),'fiches ;',len(G),'germes')

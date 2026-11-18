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
    fig=plt.figure(figsize=(8.27,11.69)); ax=fig.add_axes([0.08,0.36,0.84,0.58]); dessin(ax)
    fig.text(0.08,0.97,titre,fontsize=13,weight='bold',va='top')
    fig.text(0.08,0.33,texte,fontsize=8.5,va='top',wrap=True,family='DejaVu Sans')
    FIG.append(fig); fig.savefig(f'img_{ref}.png',dpi=110)
def txt(lines): return '\n'.join(lines)

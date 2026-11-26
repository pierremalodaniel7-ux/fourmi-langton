#!/usr/bin/env python3
"""ecran4.py : écran 2×2 = 4 bascules T dans UNE simulation (pixels à 6 000 cases les uns des autres) :
A = 185 (chaine_0, 3 impulsions), B = 572 (chaine_2, 4), C = 186 (chaine_1, 3), D = 1020 (chaine_1020, 4 premières impulsions).
Aucun retard calculé : chaque pixel suit sa propre chronologie ; l'IMAGE (motif ON/OFF des 4 pixels) change à chaque bascule.
Chronologie (moteur2.py, toutes les 100 pas), état final contrôlé par src/fourmi ; images PNG avant/après chaque changement.
Écrit ../../data/bascule/ecran4.json et ../../resultats/bascule/ecran4_*.png."""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lecture'))
from lib import *
D=os.path.dirname(os.path.abspath(__file__)); HON=json.load(open(f'{D}/honnetes.json')); BC=json.load(open(f'{D}/bascules_completes.json'))
S1a=json.load(open(f'{D}/cyclesS1.json')); S1b=json.load(open(f'{D}/cyclesS1_c2.json'))
SP=6000
PIX=[('A',185,json.load(open(f'{D}/chaine_0.json'))[-1],HON[0],S1a,(0,0)),
     ('B',572,json.load(open(f'{D}/chaine_2.json'))[-1],HON[2],S1a,(SP,0)),
     ('C',186,json.load(open(f'{D}/chaine_1.json'))[-1],HON[1],S1a,(0,SP)),
     ('D',1020,[x for x in json.load(open(f'{D}/chaine_1020.json')) if x['impulsions']==4][0],BC[11],S1b,(SP,SP))]
ants=[];cells=[];info=[]
for nom,ic,ch,hb,S1,(dx,dy) in PIX:
    r,A,C=parse(ch['situation']); k0=len(ants)
    ants+=[(x+dx,y+dy,d) for x,y,d in A]; cells+=[(x+dx,y+dy) for x,y in C]
    info.append((nom,ic,Bascule({'hit':hb['hit'],'situation':ch['situation'],'T':ch['T']},S1),k0,len(A),dx,dy))
sit=situ(ants,cells); T=int(os.environ.get('TT',66000))
def etats(an,no):
    out={}
    for nom,ic,b,k0,n,dx,dy in info:
        A=[(x-dx,y-dy,d) for x,y,d in an[k0:k0+n]]; Cc={(x-dx,y-dy) for x,y in no if abs(x-dx)<60 and abs(y-dy)<60}
        out[nom]=b.etat(A,Cc)
    return out
turn,a2,no=charge(sit); prev=None; log=[]; snaps={}
for t in range(T+1):
    if t%100==0:
        e=etats([tuple(x) for x in a2],no); img=''.join('1' if e[k]=='S1' else ('0' if e[k]=='S0' else '?') for k in 'ABCD')
        if img!=prev:
            log.append((t,img)); prev=img
            snaps[t]=({(x,y) for x,y in no},[tuple(x) for x in a2])
    if t<T: pas(turn,a2,no,range(len(a2)))
(o,an,ce),=lot([sit],T,'e4'); same=([tuple(x) for x in a2]==an and no==ce)
print('chronologie de l\'image (A B / C D, 1 = ON = S1) :',log); print('src/fourmi = moteur2 au pas',T,':',same)
stable=[(t,img) for (t,img),(t2,_) in zip(log,log[1:]+[(T,None)]) if '?' not in img and t2-t>=300]
print('images stables (≥ 300 pas) :',stable)
json.dump({'situation':sit,'T':T,'chronologie':log,'stables':stable,'moteurs_identiques':same},open(f'{D}/../../data/bascule/ecran4.json','w'))
# images : pour chaque image stable, la grille de chaque pixel (61×61 cases autour de la pièce) + l'écran 2×2
from PIL import Image, ImageDraw, ImageFont
FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
os.makedirs(f'{D}/../../resultats/bascule',exist_ok=True)
Z=4; W=61
def panneau(t,img):
    # on rejoue jusqu'au milieu de l'intervalle stable pour la vue
    pass
turn,a3,n3=charge(sit); cur=0; frames=[]
for k,(t,img) in enumerate(stable):
    tm=t+150
    while cur<tm: pas(turn,a3,n3,range(len(a3))); cur+=1
    im=Image.new('RGB',(2*W*Z+3*20+260, 2*W*Z+3*20+40),'white'); dr=ImageDraw.Draw(im)
    for j,(nom,ic,b,k0,n,dx,dy) in enumerate(info):
        ox=20+(j%2)*(W*Z+20); oy=40+(j//2)*(W*Z+20)
        on=img[j]=='1'
        dr.rectangle([ox-6,oy-6,ox+W*Z+5,oy+W*Z+5],fill=(255,200,60) if on else (90,90,110))
        dr.rectangle([ox,oy,ox+W*Z-1,oy+W*Z-1],fill='white')
        for x,y in n3:
            u,v=x-dx+30,y-dy+30
            if 0<=u<W and 0<=v<W: dr.rectangle([ox+u*Z,oy+v*Z,ox+u*Z+Z-1,oy+v*Z+Z-1],fill='black')
        for x,y,d in a3[k0:k0+n]:
            u,v=x-dx+30,y-dy+30
            if 0<=u<W and 0<=v<W: dr.rectangle([ox+u*Z,oy+v*Z,ox+u*Z+Z-1,oy+v*Z+Z-1],fill='red')
        dr.text((ox,oy-20),f'{nom} = pièce {ic} : {"ON (S1)" if on else "OFF (S0)"}',fill='black',font=FT)
    ex=2*W*Z+3*20; dr.text((ex,40),f'pas {tm}',fill='black',font=FT)
    for j in range(4):
        x0=ex+(j%2)*110; y0=70+(j//2)*110
        dr.rectangle([x0,y0,x0+100,y0+100],fill=(255,200,60) if img[j]=='1' else (90,90,110))
    dr.text((ex,300),f'image {k} : {img[:2]} / {img[2:]}',fill='black',font=FT)
    f=f'{D}/../../resultats/bascule/ecran4_{k}.png'; im.save(f); frames.append(f)
print('images :',frames)

# bande récapitulative : les écrans 2×2 successifs
n=len(stable); im=Image.new('RGB',(n*70+20,150),'white'); dr=ImageDraw.Draw(im)
for k,(t,img) in enumerate(stable):
    x0=10+k*70
    for j in range(4):
        dr.rectangle([x0+(j%2)*30,20+(j//2)*30,x0+(j%2)*30+27,20+(j//2)*30+27],fill=(255,200,60) if img[j]=='1' else (90,90,110))
    dr.text((x0,90),f'{t}',fill='black',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11))
dr.text((10,115),'écran 2×2 (A B / C D), pas où l’image change ; jaune = ON (S1)',fill='black',font=FT)
im.save(f'{D}/../../resultats/bascule/ecran4_bande.png'); print('bande : resultats/bascule/ecran4_bande.png')

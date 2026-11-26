#!/usr/bin/env python3
"""docs_nuit.py B : fiches du bestiaire B (nuit 26/11) ajoutées à docs/sources/catalogue.json (remplace les fiches BA-9… déjà
présentes) + germes resultats/germes_2026-11-26_lecture.json (dossier « Ordinateur/Bascules »)."""
import sys, json, os
from lib import *
B=int(sys.argv[1]); R='../..'
CAP='HDBG'
def lettres(sit):
    r,A,C=parse(sit); return ';'.join(f'{x},{y},{CAP[d]}' for x,y,d in A), ';'.join(f'{x},{y}' for x,y in C)
fiches=[]; germes=[]
def ajoute(id_,nom,sit,img,zoom,situation,deroulement,mesures,statut,interet,deja,source,commande=''):
    f,p=lettres(sit)
    e={'id':id_,'b':B,'classe':'Ordinateur — lecture et durée de vie de la bascule (26/11)','nom':nom,'regle':'RL','fourmis':f,'points':p,
       'img':[img,''],'situation':situation,'deroulement':deroulement,'mesures':mesures,'statut':statut,'interet':interet,'deja':deja,'source':source}
    if zoom: e['zoom']=zoom
    if commande: e['commande']=commande
    fiches.append(e); germes.append({'dossier':'Ordinateur/Bascules','nom':f'{id_} {nom}','regle':'RL','fourmis':f,'points':p,'note':f'{statut} ; {source} ; image au pas {img}'})
# BA-9 rattrapage sans pièce
J,sh,dp=60,0,-7; gx,gy=2*J+sh,-2*J-sh+dp
s9=situ([(gx,gy,2),(0,0,2)],G+[(x+gx,y+gy) for x,y in G])
ajoute('BA-9','Deux autoroutes sur la même ligne : la 2e rattrape la 1re, aller-retour exact (sans pièce)',s9,7200,[-60,-200,200,60],
 'Deux germes R-20 (autoroute 104 vers le SO) ; le 2e en amont, en (120,−127) : voie décalée de 7 (classes opposées).',
 'Le 2e roule sur la trace du 1er, le rattrape vers le pas 7 200 ; les deux repartent en arrière en effaçant tout. Au pas 14 416 chacune est EXACTEMENT dans l’état retourné du départ de l’autre.',
 '12 240 situations (J 20–199, 4 avancées, dp −8…8) : 4 353 retours, tous à dp impair (0/6 120 à dp pair) ; 3 423 parfaits (les 2 en R, 28 cases ≠ départ autour de chaque germe). t* de 4 042 à 39 950.',
 'VÉRIFIÉ (2 moteurs, temps fini) / OBSERVÉ (stats)','Explique la « gomme mutuelle » de la bascule (R-141) : elle ne vient pas de la pièce.','Pas trouvé (2 recherches web).','R-147, ordinateur/lecture/rattrapage.py',
 './fourmi -retour -T 40000 (RETOUR au pas 14 416)')
# BA-10 paire = palindrome
h=json.load(open('../bascule/honnetes.json'))[0]
ajoute('BA-10','Paire ON/OFF de la bascule 185 : au pas 14 008 tout est revenu (pièce exacte), sauf 28 cases à chaque source',h['situation'],14008,[-40,-260,260,40],
 'Bascule T 185 (2 fourmis + 1 case) et 2 germes sur la ligne NE (R-140).',
 'S0 → S1 (5 100) → S0 ; au pas t* = 14 008 la sonde 2 est en R(départ de la sonde 1) et inversement ; la grille est celle du départ sauf 56 cases (28 autour de chaque source), la pièce est EXACTEMENT celle du pas 0.',
 '186 : t* = 18 344, 56 cases, pièce exacte ; 572 : 14 348, 64 (8 près de la pièce) ; 1020 : 15 120, 62 (6).',
 'VÉRIFIÉ (2 moteurs, temps fini)','Avec des sources « à l’infini » (fils idéalisés), la bascule 185/186 repartirait exactement de l’état initial après chaque paire : nombre illimité d’écritures/effacements.','Pas trouvé.','R-148, ordinateur/lecture/palindrome.py','./fourmi -retour -T 60000')
# BA-11 ligne bloquée
r_,A,C=parse(h['situation']); p1=A[1]; a=520; q=(p1[0]+a,p1[1]-a)
s11=situ([(q[0],q[1],2)]+A,C+[(x+q[0],y+q[1]) for x,y in G])
ajoute('BA-11','Ligne bloquée : après la paire ON/OFF, une 3e impulsion n’atteint jamais la pièce',s11,34000,[-60,-700,700,60],
 'Paire honnête de 185 + un 3e germe sur la même ligne, 520 cases plus loin.',
 'La paire fait S0 → S1 → S0 et repart ; la 3e autoroute bute sur les débris des sources (28 cases + départ des autoroutes NO) et ne touche pas la pièce, qui reste en S0.',
 '185, 186, 572, 1020 : 1 640/1 640 essais (40 reculs × 41 voies) sans écriture ; témoins sans la paire : 10, 20, 7, 15 écritures.',
 'VÉRIFIÉ (src/fourmi, temps fini)','Explique pourquoi la 2e paire de 572 n’efface pas sa ligne (R-143) : ce n’est pas une paire.','Pas trouvé.','R-150, ordinateur/lecture/passe2.py')
# BA-12 chaîne 1020
ch=json.load(open('../bascule/chaine_1020.json')); c5=max(ch,key=lambda x:x['impulsions'])
ajoute('BA-12',f"Bascule 1020 : {c5['impulsions']} impulsions sur la même ligne (record dans une seule simulation)",c5['situation'],c5['T'],[-60,-700,700,60],
 'Pièce 1020 (cycle de 2 fourmis, période 28, + 1 case) ; germes ajoutés un à un sur la ligne NE (chaine.py).',
 'Chronologie : '+' → '.join(f'{s} ({t})' for t,s in c5['chronologie'] if s!='…')+'.',
 'Ligne effacée seulement après la 1re paire (lignes.py : 244 cases après 2 impulsions, 1 347 à 1 941 ensuite). Les bascules suivantes sont faites par des sondes recyclées.',
 'VÉRIFIÉ (2 moteurs, temps fini)','Record d’écritures/effacements dans une vraie simulation (572 : 4).','Pas trouvé.','R-150, ordinateur/bascule/chaine_1020.json')
# BA-13 écran 2×2
e4=json.load(open('../../data/bascule/ecran4.json'))
ajoute('BA-13','Écran 2×2 : 4 bascules T, 15 images successives dans une seule simulation',e4['situation'],6250,[-60,-140,160,60],
 'Pixels A = 185, B = 572 (6 000 cases à droite), C = 186 (6 000 en bas), D = 1020 ; chacun avec ses germes sur sa ligne NE. Image : pixel A seul.',
 'Images (A B / C D, 1 = ON) : '+' → '.join(f'{img[:2]}/{img[2:]} ({t})' for t,img in e4['chronologie'])+'.',
 'Jamais d’état intermédiaire aux pas multiples de 100 ; src/fourmi = moteur2 au pas 66 000. Images : resultats/bascule/ecran4_*.png et ecran4_bande.png.',
 'VÉRIFIÉ (2 moteurs, temps fini)','Écran plus grand que R-142 (2 pixels) et sans retard calculé.','Pas trouvé.','R-152, ordinateur/bascule/ecran4.py')
# montage multi-lignes (si trouvé)
import glob
for f in sorted(glob.glob('../../data/lecture/montage_185_*.json')):
    m=json.load(open(f))
    if len(m['ordre'])>=2:
        ajoute('BA-14',f"Bascule 185 : {len(m['ordre'])} paires ON/OFF sur des lignes différentes, chacune efface sa ligne",m['situation'],m['t_retour'][-1],[-300,-300,300,300],
         f"Pièce 185 ; paires n° {m['ordre']} (multi_paires.py) : lignes différentes (directions / voies).",
         'Chronologie : '+' → '.join(f'{s} ({t})' for t,s in m['chronologie'] if s!='…')+'.',
         'Chaque paire finit par un aller-retour exact (ses 2 sondes chacune en R(départ de l’autre)). src/fourmi + moteur2.',
         'VÉRIFIÉ (2 moteurs, temps fini)','Contourne le blocage de la ligne (R-150).','Pas trouvé.','R-151, ordinateur/lecture/montage.py'); break
cat=json.load(open(f'{R}/docs/sources/catalogue.json')); ids={e['id'] for e in fiches}
cat=[e for e in cat if e['id'] not in ids]+fiches; json.dump(cat,open(f'{R}/docs/sources/catalogue.json','w'),ensure_ascii=False,indent=1)
json.dump(germes,open(f'{R}/resultats/germes_2026-11-26_lecture.json','w'),ensure_ascii=False,indent=1)
print(len(fiches),'fiches (b =',B,') ;',len(germes),'germes')

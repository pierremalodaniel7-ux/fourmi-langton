#!/usr/bin/env python3
"""fiches.py : ajoute les fiches du bestiaire 25 (bascule, nuit du 25/11) à docs/sources/catalogue.json et écrit
resultats/germes_2026-11-25_bascule.json (dossier « Ordinateur/Bascules »). Idempotent (remplace les fiches BA-*)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas, gomme
from bascule import germe_sit
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../..'); D=os.path.join(R,'data/bascule'); H=os.path.dirname(os.path.abspath(__file__))
CAPS='HDBG'
def lettres(sit):
    r,a,c=sit.split('|')
    f=';'.join(f"{x},{y},{CAPS[int(d)] if d.lstrip('-').isdigit() else d}" for x,y,d in (t.split(',') for t in a.split(';')))
    return r,f,c
G="0,1;1,2;2,3;2,2;2,1;2,0;3,0;3,-1;2,-2;1,-2;-2,-1"
turn,an,no=charge("RL|0,0,B|"+G)
for _ in range(10400): pas(turn,an,no,[0])
gomme(an); a=an[0]; gom=f"RL|{a[0]},{a[1]},{a[2]}|"+';'.join(f'{x},{y}' for x,y in sorted(no))
os.environ['CY']='cycles4.json'
import importlib, recherche_lib as RL; importlib.reload(RL)
A0,C0,p0=RL.piece0(50,3); ech=germe_sit(101,-100,A0,C0)
ch2=json.load(open(f'{H}/chaine_2.json')); ch0=json.load(open(f'{H}/chaine_0.json')); ch1=json.load(open(f'{H}/chaine_1.json'))
ecr=json.load(open(f'{H}/ecran2.json'))
F=[]
def fiche(id_,nom,sit,img,situation,deroulement,mesures,statut,interet,deja,source,commande='',zoom=None):
    r,f,c=lettres(sit); e={"id":id_,"b":25,"classe":"Ordinateur — gomme et bascule (25/11)","nom":nom,"regle":r,"fourmis":f,"points":c,
      "img":[img,""],"situation":situation,"deroulement":deroulement,"mesures":mesures,"statut":statut,"interet":interet,"deja":deja,"source":source}
    if commande: e["commande"]=commande
    if zoom: e["zoom"]=zoom
    F.append(e)
fiche("BA-1","Gomme d'une autoroute 104",gom,5200,
 "Germe R-20 déroulé 10 400 pas (100 périodes d'autoroute 104), puis la fourmi est « gommée » : (x, cap h) → (x − e_h, cap h + 2).",
 "La fourmi refait tout son chemin à l'envers et efface la trace ; image au pas 5 200 : moitié effacée. Au pas 10 400 il ne reste que le germe (11 cases), fourmi en (0,−1) cap haut.",
 "EFFACE exact au pas 2t pour t = 10 à 10⁶ (départ blanc) et t = 1 040 à 1 040 000 (germe) ; 2 moteurs (src/fourmi -gomme, moteur2.py).",
 "VÉRIFIÉ (preuve en 2 cas blanc/noir + 2 moteurs) — CONNU (réversibilité)",
 "La brique « effacer » : un signal qui revient sur sa trace la défait exactement. Vaut pour RL, LR, NN, UU ; pas pour LLR ; à n fourmis : gommer toutes les fourmis et inverser l'ordre de jeu.",
 "Connu : réversibilité (flipping rotators ; Tsukiji & Hagiwara 2011, Algorithms 4(1)).","R-136, ordinateur/bascule/GOMME.md","./fourmi -gomme t -T 2t \"RL|0,0,H|\"")
fiche("BA-2","Gomme par échange (pièce de 4 fourmis, détruite)",ech,9948,
 "Germe R-20 à ≈ 200 cases d'un petit cycle de 4 fourmis (n° 50 de cycles4.json, phase 3).",
 "Une fourmi de la pièce (classe opposée à la sonde) repart exactement en gomme et efface la trace d'entrée ; la sonde reste dans la pièce, qui éclate ensuite.",
 "Fenêtre x∈[35,75], y∈[−75,−35] entièrement blanche au pas 9 948 (src/fourmi et moteur2.py). Statistique : 15 825 gommes sur 903 776 essais (4 fourmis), 8 152 sur 501 370 (2 fourmis), pièce détruite dans 100 % des cas contrôlés.",
 "VÉRIFIÉ (cet exemple, 2 moteurs, temps fini) ; « pièce toujours détruite » OBSERVÉ",
 "Montre que la gomme par réflexion existe, mais coûte la pièce : une fourmi seule ne peut jamais repartir en gomme (invariant de classe, R-137) et un cycle semble exiger autant de fourmis de chaque classe (R-139).",
 "Pas trouvé.","R-138, R-139","")
fiche("BA-3","Bascule T 572 : ON puis OFF, la ligne est effacée",ch2[0]['situation'],16000,
 "Pièce = 2 fourmis + 1 case (n° 572 de cycles2.json, période 24) ; 2 germes R-20 sur la même ligne venant du NE (voies voisines), le 2e plus loin.",
 "1re autoroute : la pièce passe de S0 (cycle 24) à S1 (cycle 28, dans une tache noire) au pas ≈ 6 100. 2e autoroute : elle roule sur la trace de la 1re, la pièce revient à S0 EN PLACE (pas ≈ 8 400) ; les deux sondes repartent chacune en gomme exacte de la trace de l'autre (8 541 et 5 851 pas) : la ligne entre pièce et sources redevient blanche (image au pas 16 000), puis les 2 autoroutes partent vers le NO depuis les sources.",
 "Chronologie (moteur2.py, tous les 100 pas) : S0 → S1 (6 100) → S0 (8 400) → S0 jusqu'à 42 584. Fenêtre de la ligne : 309 cases noires au pas 6 000, 0 dès 14 000 (2 moteurs).",
 "VÉRIFIÉ (2 moteurs, temps fini)",
 "Une mémoire 1 bit réinscriptible qui nettoie sa ligne d'entrée : la gomme demandée, réalisée par une PAIRE (une fourmi de chaque classe), compatible avec la loi d'équilibre.",
 "Pas trouvé (deja_connu.md, 25/11).","R-140, R-141, ordinateur/bascule/chaine_2.json","")
fiche("BA-4","Bascule T 572 : ON, OFF, ON",ch2[1]['situation'],ch2[1]['T'],
 "Même montage que BA-3 + un 3e germe plus loin sur la même ligne.",
 "S0 → S1 → S0 → S1 : la 3e autoroute rallume le pixel (tache noire autour de la pièce). Image : zoom sur la pièce à la fin.",
 "Chronologie (moteur2.py) : S0, S1 (6 100), S0 (8 400), S1 (21 700) jusqu'à 57 144 ; état final identique avec src/fourmi. 4e impulsion : non trouvée (recul 40 à 220 périodes, voies ±8).",
 "VÉRIFIÉ (2 moteurs, temps fini)","Trois écritures successives sur la même ligne.","Pas trouvé.","R-140, chaine_2.json","",[-8,-8,14,14])
fiche("BA-5","Bascule T 185 : ON puis OFF",ch0[0]['situation'],16000,
 "Pièce n° 185 de cycles2.json (cycle 16 : 0,0,D ; −1,1,B + 1 case) ; 2 germes sur la même ligne.",
 "S0 → S1 (un autre cycle de période 16, 2 fourmis + 4 cases) → S0 en place ; ligne effacée par la paire.",
 "Fenêtre de la ligne : 306 cases au pas 6 000, 0 dès 14 000 (2 moteurs). 3e impulsion : S1 au pas 20 900.",
 "VÉRIFIÉ (2 moteurs, temps fini)","2e bascule indépendante (même famille).","Pas trouvé.","R-140, chaine_0.json","")
fiche("BA-6","Bascule T 186 : ON puis OFF",ch1[0]['situation'],20000,
 "Pièce n° 186 de cycles2.json (cycle 16 + 1 case) ; 2 germes sur la même ligne.",
 "S0 → S1 (cycle 20) → S0 en place ; ligne effacée.",
 "Fenêtre : 311 cases au pas 6 000, 0 au pas 20 000 (2 moteurs). 3e impulsion : S1 au pas 56 800.",
 "VÉRIFIÉ (2 moteurs, temps fini)","3e bascule.","Pas trouvé.","R-140, chaine_1.json","")
fiche("BA-7","Écran de 2 pixels : ON, OFF, ON sur chaque pixel",ecr['situation'],12000,
 "Pixel A = BA-4 en (0,0) ; pixel B = bascule 186 à 3 impulsions en (0,4000), retardée de 3 120 pas : son état de départ est son état « 3 120 pas avant », calculé exactement par réversibilité (gomme, ordre inversé).",
 "A : ON 6 100, OFF 8 400, ON 21 700. B : ON 8 900, OFF 15 900, ON 59 900. Image au pas 12 000 : A éteint, B allumé.",
 "Chronologie moteur2.py ; positions finales des 10 fourmis identiques avec src/fourmi (T = 60 888).",
 "VÉRIFIÉ (2 moteurs, temps fini)","Première démonstration d'un écran réinscriptible (2 pixels, 3 écritures chacun) dans la fourmi RL à plusieurs fourmis.",
 "Pas trouvé.","R-142, ordinateur/bascule/ecran2.py","")
bc=json.load(open(f'{H}/bascules_completes.json'))[11]
fiche("BA-8","Bascule T 1020 : ON puis OFF (4e pièce, couverture complète)",bc['situation'],16000,
 "Pièce n° 1020 de cycles2.json : cycle de 2 fourmis (0,0,D ; −1,−1,B, période 28) + une case noire isolée (3,1) ; 2 germes sur la même ligne (NE).",
 "S0 → S1 (pas 5 400) → S0 en place (10 000) ; la paire efface la ligne puis repart vers le NO depuis les sources.",
 "Chronologie moteur2.py ; fenêtre de la ligne : 199 cases au pas 6 000, 0 aux pas 16 000 et 30 000 (src/fourmi -boite). Couverture complète des 2 049 pièces : 40 bascules idéalisées, 33 honnêtes, 4 pièces seulement (185, 186, 572, 1020), dont 22 variantes pour 1020.",
 "VÉRIFIÉ (2 moteurs, temps fini)","Montre que la famille « cycle de 2 fourmis + 1 case isolée » est la bonne.","Pas trouvé.","R-144, bascules_completes.json","")
cat=json.load(open(f'{R}/docs/sources/catalogue.json')); cat=[e for e in cat if not e['id'].startswith('BA-')]+F
json.dump(cat,open(f'{R}/docs/sources/catalogue.json','w'),ensure_ascii=False,indent=1)
germes=[{"dossier":"Ordinateur/Bascules","nom":e['nom'],"regle":e['regle'],"fourmis":e['fourmis'],"points":e['points'],"note":e['deroulement'][:300]} for e in F]
json.dump(germes,open(f'{R}/resultats/germes_2026-11-25_bascule.json','w'),ensure_ascii=False,indent=1)
print(len(F),'fiches ;',len(cat),'au catalogue')

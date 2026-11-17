# portes_def.py — définition des germes « ordinateur » retenus (R-40 à R-43). Chaque porte : liste de cas (entrées -> situation).
import portes as Pt
c,s,dB=-121,-391,64
PA=lambda: Pt.germe(0,0,0); PB=lambda: Pt.germe(dB,dB,0); PP=lambda: Pt.germe((c+s)//2,(s-c)//2,3)
P2=lambda: Pt.germe(800,1103,1)          # 2e étage (OU), arrive ↖
SEED104='RL|0,0,D|-2,-2;-1,-2;0,-1;1,0;-2,1;1,1;-2,2;0,2;-1,3;0,3;0,4'
def S(g,cells): return 'RL|'+Pt.situ(g,extra=cells)
def ab(cells,useB=True,extra_g=()):
    out={}
    for a in (0,1):
        for b in ((0,1) if useB else (0,)):
            g=([PA()] if a else [])+([PB()] if b else [])+[PP()]+[f() for f in extra_g]
            out[(a,b) if useB else (a,)]=S(g,cells)
    return out
PORTES={
 'fil + virage droite (−90°)': dict(cas={(0,):SEED104,(1,):SEED104+';-26,25'}, lire=0, T=8000,
     table={(0,):'↙',(1,):'↘'}, note="Case seule au contact de l'autoroute 104 ; 565 pas de chaos (le plus court des 40 placements). Entrée = la case est là ou non."),
 'fil + virage gauche (+90°)': dict(cas={(0,):SEED104,(1,):SEED104+';-27,25'}, lire=0, T=14000,
     table={(0,):'↙',(1,):'↖'}, note="5 688 pas de chaos (le plus court des virages à gauche)."),
 'porte NON': dict(cas=ab([(141,260)],useB=False), lire=-1, T=90000, table={(0,):'↙',(1,):'↘'},
     note="P (puissance ↘) traverse la trace de A ; décalée de 4 voies si a=1 ; la case (141,260) ne touche que la voie non décalée."),
 'porte NOR': dict(cas=ab([(141,260)]), lire=-1, T=90000, table={(0,0):'↙',(0,1):'↘',(1,0):'↘',(1,1):'↘'},
     note="Compteur : voie de P = L − 4(a+b). Case (141,260) : P tourne ↙ ssi a=b=0. NOR seul suffit (universel)."),
 'porte ET': dict(cas=ab([(133,267)]), lire=-1, T=90000, table={(0,0):'↘',(0,1):'↘',(1,0):'↘',(1,1):'↙'},
     note="Même compteur ; la case (133,267) ne touche que la voie L − 8."),
 'COPIE (1 entrée, 2 sorties)': dict(cas=ab([(135,265)],useB=False), lire='tout', T=90000,
     table={(0,):['↘'],(1,):['↙','↙']}, note="A continue ↙ (sortie 1) ; P tourne ↙ ssi a=1 (sortie 2, case (135,265)) ; sinon P reste ↘."),
 'OU à 2 étages = NON(NOR)': dict(cas=ab([(141,260),(-41,261)],extra_g=(P2,)), lire=-1, T=110000,
     table={(0,0):'↖',(0,1):'↙',(1,0):'↙',(1,1):'↙'},
     note="Étage 1 = NOR (sortie O1 ↙). Étage 2 = puissance P2 qui arrive ↖ (pour lire O1 avant de croiser A et B) + case (−41,261)."),
 'CROISEMENT de 2 fils': dict(cas={(x,y):S(([PA()] if x else [])+([PP()] if y else []),[(137,264),(148,267)]) for x in (0,1) for y in (0,1)},
     lire='tout', T=60000, table={(0,0):[],(0,1):['↙'],(1,0):['↙'],(1,1):['↙','↙']},
     note="X (↙) passe d'abord ; Y (↘) traverse sa trace puis un collecteur de 2 cases le renvoie ↙ sur la voie 397 : trace de sortie de Y identique case par case pour x=0 et x=1."),
 'demi-additionneur (S, C) à 1 puissance': dict(cas=ab([(130,254),(133,267)]), lire='voie', T=90000,
     table={(0,0):'↘',(0,1):'↙ voie 337 (S)',(1,0):'↙ voie 337 (S)',(1,1):'↙ voie 369 (C)'},
     note="Voie L−4 = XOR, L−8 = ET. Cases (130,254) et (133,267). Lecture par la voie de sortie (= colonne de l'écran)."),
}

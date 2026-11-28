# État du projet (mis à jour le 26-11-2026)

## Démontré
- R-03 périodes de cycle ≡ 0 mod 4 (toute règle L/R, tout nombre de fourmis).
- R-09 toutes les fourmis RL de même classe de parité ⇒ jamais borné (preuve esquissée, À RELIRE).
- R-135 B5 : toute config dans un carré 5×5, fourmi n'importe où, tout cap → autoroute 104 (exhaustif, certificat ; code à relire) ; T(5) = 351 374.
- R-20 bout d'autoroute 104 minimal = 11 cases. R-28 cycle minimal : Tourniquet, période 4.

## Vérifié par calcul exact
Cycles à 2 fourmis (R-02, R-13, record 309 752), à 4 fourmis, composé (1 030 792) ; navettes R-19 / R-21
(portée = 19 797 + 52m) ; nids R-26 ; Rouage 8 (R-29) ; cycles de groupe R-31 (Double Navette sans case) ; 12 cycles symétriques
à 8-12 fourmis, dont quadruple navette 253 760 (R-36).

- R-39 additionneur 2 à 5 bits par modules recopiés (retenue = autoroute), toutes entrées justes au pas de lecture ; germe 4 bits (recherche/ordinateur).

## Observé (simulations finies)
Losanges (R-06) ; autoroutes de groupe 12, 16, 24, 48, 52, 96, 102 ; passagers 100, 108, 12, 10, 388, 688,
142, 20, 2 620 (R-18, R-22, R-32) ; collisions 1 et 2 cases (R-16, R-24) ; chocs de 2 autoroutes (R-25) ;
Lambine (R-33) ; 95 directions d'autoroutes (R-35).

## Ordinateur (17/11, R-40 à R-44)
Autoroute la plus câblable en RL : la 104 à 1 fourmi (les autoroutes à plusieurs fourmis éclatent) ; hors RL : LLR / LⁿR (murs = miroirs, 6 pas de chaos).
Porte « compteur » par traversée de traces : NOR, ET, NON, COPIE, CROISEMENT, OU à 2 étages, demi-additionneur, écran — VÉRIFIÉ (2 moteurs, temps fini). Puits définitif impossible (R-44). Germes : ordinateur/.
17/11 après-midi (R-45 à R-50) : ADDITIONNEUR 2 BITS EN UN GERME + écran, 16/16 (2 moteurs) ; additionneur complet à 1 puissance ; réservoir ruban 15/15 ; 88 pièges exacts, 0 « tout coincé » ; règles de déplacement. Taille encore exponentielle en n bits.

## Ordinateur — mémoire (25/11 nuit, R-136 à R-142, ordinateur/bascule/)
Gomme (R-136, connu). Une fourmi seule ne repart jamais en gomme (R-137, démontré). Loi d'équilibre des classes dans les cycles (R-139, observé).
BASCULE T trouvée : 2 fourmis + 1 case, S0/S1 à chaque autoroute sur la même ligne, ON/OFF/ON (R-140) ; la paire ON/OFF efface sa ligne (R-141) ;
écran 2 pixels ON/OFF/ON (R-142) ; 4e impulsion OK (572), flux nul sur chaque arête des cycles (R-143) ; 4 pièces sur 2 049 (R-144). Ouvert : 5e impulsion, lecture non destructive, élément à 2 entrées (RLEM non dégénéré).

## Ordinateur — règle hexa R2L2 sans case fixe (25-26/11, R-300 à R-350, recherche/regles/)
Vaisseau R2L2 (1 fourmi + 1 case, R-306, connu) ; AUCUN miroir possible (R-330, R-331 démontrés) ; chocs de 2 vaisseaux sans perte (R-333).
Réutilisables au même endroit, certifiés pour tout nombre d'usages : mémoire 1 bit (R-335/R-339), demi-additionneur (R-337/R-338), bascule RS (R-341/R-343),
**additionneur complet a + b + retenue (R-349 : 8/8, 20 usages, 2 moteurs, certificat ; sorties lues sur 3 positions)**.
Calcul → mémoire : a∧b écrit dans une bascule, lu, remis à 0, 20/20 (R-346). Additionneur 2 bits par enchaînement 16/16 mais UN usage (R-345) ;
version réutilisable : échec expliqué (R-350). Boucle : relais immobile qui dévie = 3k états (T3, R-347), 0 trouvé (R-348) ;
HORLOGES à 6 fourmis (triangle de vaisseaux qui se relancent, P = 2 322 + 2 736 n, n ≤ 4, R-349b).
Sessions du 26-27/11 (journaux dans recherche/regles/s1_fusion, s2_horloge, s3_pas, s4_ecran, copiés en fin de journal.md) :
fusion propre et réutilisable de 2 signaux exclusifs à 2 constants (R-403, certificat) ; **additionneur 2 bits RÉUTILISABLE (R-405, 2 moteurs, 20 usages)** ;
famille infinie d'horloges triangle (R-500, démontré) ; **pixel qui clignote pour toujours (R-502, CYCLE exact)** ; **compteur 2 bits (R-507, CYCLE exact)** ;
**hexagramme : 2 horloges couplées par 6 portes, tous les vaisseaux récupérés (R-512, CYCLE exact)** ;
**pas complet de la petite fourmi (tore 2×2) en UN germe, réutilisable (R-616/R-617, 256/256, 2 moteurs, certificat)** ; 2 pas enchaînés 7 bits sur 8 (R-619) ;
**écran 2×2 adressable (R-707) puis écran 4×4 (R-711)**, 2 moteurs, temps fini.

## Simulateur v7 (17/11 soir)
docs/ (GitHub Pages après fusion de la PR n°1) : bibliothèque fusionnée (747 éléments), 37 circuits avec interrupteurs, pas complet de la petite fourmi VÉRIFIÉ 256/256 (R-68, moteur JS + Python).

## Ouvert
R-04 (≤ 2 états blancs par cycle) ; R-14/R-27 conjecture des phases (0 contre-exemple sur ≈ 2,7 M) ;
RL à plusieurs fourmis : seulement les pentes 0, 1, 5/3 ? ; ordinateur R2L2 : additionneur 3 bits réutilisable (R-407 à R-411), lecture non destructive d'un pixel (R-709, R-713), N pas enchaînés de la petite fourmi (T1, R-620+) ; mémoire : bascule T trouvée (R-140), RLEM à 2 entrées ouvert ; 13 à 100 fourmis : aucun cycle ni autoroute nouvelle (R-36, 3 069 situations) ; portée arbitraire des navettes.

## À revérifier
Rail 0,0,H ; 2,6,H ; 8,6,D (R-13 vs R-18) ; LLRRRL autoroute 896 (bord de grille ?).

## Pistes : voir `pistes.md`. Journal complet : `journal.md` (chercher par grep).

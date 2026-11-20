# État du projet (mis à jour le 17-11-2026)

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

## Simulateur v7 (17/11 soir)
docs/ (GitHub Pages après fusion de la PR n°1) : bibliothèque fusionnée (747 éléments), 37 circuits avec interrupteurs, pas complet de la petite fourmi VÉRIFIÉ 256/256 (R-68, moteur JS + Python).

## Ouvert
R-04 (≤ 2 états blancs par cycle) ; R-14/R-27 conjecture des phases (0 contre-exemple sur ≈ 2,7 M) ;
RL à plusieurs fourmis : seulement les pentes 0, 1, 5/3 ? ; ordinateur : mémoire / horloge (R-39) ; 13 à 100 fourmis : aucun cycle ni autoroute nouvelle (R-36, 3 069 situations) ; portée arbitraire des navettes.

## À revérifier
Rail 0,0,H ; 2,6,H ; 8,6,D (R-13 vs R-18) ; LLRRRL autoroute 896 (bord de grille ?).

## Pistes : voir `pistes.md`. Journal complet : `journal.md` (chercher par grep).

# État du projet (mis à jour le 16-11-2026)

## Démontré
- R-03 périodes de cycle ≡ 0 mod 4 (toute règle L/R, tout nombre de fourmis).
- R-09 toutes les fourmis RL de même classe de parité ⇒ jamais borné (preuve esquissée, À RELIRE).
- R-20 bout d'autoroute 104 minimal = 11 cases. R-28 cycle minimal : Tourniquet, période 4.

## Vérifié par calcul exact
Cycles à 2 fourmis (R-02, R-13, record 309 752), à 4 fourmis, composé (1 030 792) ; navettes R-19 / R-21
(portée = 19 797 + 52m) ; nids R-26 ; Rouage 8 (R-29) ; cycles de groupe R-31 (Double Navette sans case) ; 12 cycles symétriques
à 8-12 fourmis, dont quadruple navette 253 760 (R-36).

## Observé (simulations finies)
Losanges (R-06) ; autoroutes de groupe 12, 16, 24, 48, 52, 96, 102 ; passagers 100, 108, 12, 10, 388, 688,
142, 20, 2 620 (R-18, R-22, R-32) ; collisions 1 et 2 cases (R-16, R-24) ; chocs de 2 autoroutes (R-25) ;
Lambine (R-33) ; 95 directions d'autoroutes (R-35).

## Ouvert
R-04 (≤ 2 états blancs par cycle) ; R-14/R-27 conjecture des phases (0 contre-exemple sur ≈ 2,7 M) ;
RL à plusieurs fourmis : seulement les pentes 0, 1, 5/3 ? ; 13 à 100 fourmis : aucun cycle ni autoroute nouvelle (R-36, 3 069 situations) ; portée arbitraire des navettes.

## À revérifier
Rail 0,0,H ; 2,6,H ; 8,6,D (R-13 vs R-18) ; LLRRRL autoroute 896 (bord de grille ?).

## Pistes : voir `pistes.md`. Journal complet : `journal.md` (chercher par grep).

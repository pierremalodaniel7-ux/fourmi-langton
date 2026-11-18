# É0 — Socle et contrôle croisé des deux moteurs (S1, 18-11-2026)

Moteurs : `src/fourmi` (moteur unique, y vers le bas) et `recherche/autoroute/ant_controle.c` (`ant`, y vers le haut).
Pour comparer : dérive (dx,dy) de `ant` = (dx,−dy) de `fourmi`. « Début » = premier pas du régime périodique.

| Contrôle | src/fourmi | ant | Accord |
|---|---|---|---|
| `make -C src test` | 18/18 OK | — | — |
| Départ blanc | A104 (−2,+2) dès 9 977 | (−2,−2) dès 9 977 | oui |
| 512 configs 3×3 (fourmi coin bas-gauche, cap haut) | 512 autoroutes | 512 autoroutes | 512/512 : même dérive, même début |
| 22 collisions 1 case (R-16 / `ant obstf 150`) | 22 durées de chaos | les mêmes 22 durées | 22/22 identiques |
| 4×4 (65 536) | non refait | 65 536 autoroutes, T(4) = 133 984 (masque 32972), 41 s | — |

## Écart « demi-tour » : TRANCHÉ
- `auto2` (R-16) note la **première** autoroute après le choc ; `ant obst` notait la **dernière** : il exige
  que la fourmi soit sortie de la boîte de tout ce qui a été touché, donc une autoroute qui repart en arrière
  (vers le germe initial) n'est jamais acceptée avant d'avoir retraversé le germe.
- Nouveau mode `./ant obstf 150` (première autoroute après le pas d'impact, sans critère de boîte) :
  9 même direction, 7 virages droite, 5 virages gauche, **1 demi-tour** (chaos 51 046, j=−19, k=150) = R-16 exactement.
- Avec `ant obst` le même cas : le demi-tour revient sur la trace, retraverse le germe de départ, et repart
  en virage : chaos total 66 924, dérive finale (−2,+2) (y vers le haut). D'où « 13 virages, 0 demi-tour ».
- Conclusion : les deux moteurs sont d'accord ; R-16 reste juste (première autoroute, trace longue synthétique).

## Correction de l'acquis du chat
T(3) = **51 277** (pas 51 380) et T(4) = **133 984** (pas 134 087) : l'ancienne version comptait le début
une période moins 1 pas trop tard (écart 103 dans les deux cas). Les nouvelles valeurs coïncident avec `src/fourmi` (3×3).

Commandes : `gcc -O2 -o ant ant_controle.c ; ./ant blank ; ./ant box 3 v ; ./ant obst 150 ; ./ant obstf 150 ; ./ant box 4`.

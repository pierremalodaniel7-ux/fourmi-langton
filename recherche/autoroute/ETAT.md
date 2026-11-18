# Autoroute — état (mis à jour à la fin de chaque séance)

PROCHAINE SÉANCE : S1
PROCHAINE TÂCHE : É0 Socle (puis enchaîner É1 dans la même heure)

## Tâches
- [x] É0 Socle + contrôle croisé (écart R-16 « demi-tour ») — S1, R-69, E0_controle.md
- [x] É1 Lemme du certificat (énoncé, preuve, implémentation) — S1, R-70, E1_certificat.md, `fourmi -cert`
- [~] É2 Collisions → théorème « épars » — S1 : T1 une case (R-72 à R-74) et T2 îlot de 2 cases voisines (R-76) DÉMONTRÉS ; 2 cases loin OBSERVÉ (R-75). Reste : automate des sites (plusieurs îlots loin), îlots de rayon ≤ 2
- [ ] É3 Boîtes exhaustives 5×5 (6×6 ?) + T(n)
- [ ] É4 Transitoires extrêmes
- [ ] É5 Observables (boucle gelée, frontière)
- [ ] É6 Germes et bassin à rebours
- [ ] É7 Contre-attaque
- [ ] É8 Synthèse

## Acquis (18-11, chat, ant_controle.c)
- Départ blanc : autoroute dès 9 977, dérive (−2,−2) dans la convention y vers le haut. OBSERVÉ (= connu).
- 3×3 : 512/512 ; 4×4 : 65 536/65 536 → autoroute ; T(3) = 51 277, T(4) = 133 984 (corrigé S1, R-69) (fourmi au coin bas-gauche, cap haut). OBSERVÉ.
- 1 case sur l'autoroute : 22 classes, 22/22 → autoroute finale (9 même direction, 13 virages). OBSERVÉ ; à réconcilier avec R-16.
- Boucle gelée : L ≤ 1 336 pendant le chaos, ≤ 112 sur l'autoroute (départ blanc). OBSERVÉ.

## Séances
(une ligne par séance : S<n>, date, durée, tâches, lien du rapport)

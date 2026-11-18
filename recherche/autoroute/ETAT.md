# Autoroute — état (mis à jour à la fin de chaque séance)

PROCHAINE SÉANCE : S2
PROCHAINE TÂCHE : É2 suite — (1) automate des « sites » pour plusieurs îlots loin (germe + 22 types, transitions
par demi-tour ; partir de `outils/chaine_demitours.py` et R-75), démontrer avec les couplages de E2_epars.md ;
(2) îlots de rayon ≤ 2 (même schéma que T2/T3 : `outils/preuves_loin.py` + `ant pmin/uturn` à n cases ; prendre s à p* ≈ 90). Puis É3 : 5×5 par tranches de 200 000 (`outils/box5_fond.sh`,
reprise automatique ; tranches faites : voir resultats/box5/ ; le script de reprise lit data/box5_*.res : recopier ces fichiers dans data/ avant de reprendre).
Outils de la séance S1 : `fourmi -cert` / `-c0 T` (certificat), `ant obstf`, `ant pmin`, `ant uturn` (preuves par couplage).

## Tâches
- [x] É0 Socle + contrôle croisé (écart R-16 « demi-tour ») — S1, R-69, E0_controle.md
- [x] É1 Lemme du certificat (énoncé, preuve, implémentation) — S1, R-70, E1_certificat.md, `fourmi -cert`
- [~] É2 Collisions → théorème « épars » — S1 : T1 une case (R-72 à R-74) et T2 îlot de 2 cases voisines (R-76) DÉMONTRÉS ; 2 cases loin OBSERVÉ (R-75). Reste : automate des sites (plusieurs îlots loin), îlots de rayon ≤ 2
- [~] É3 Boîtes exhaustives 5×5 (6×6 ?) + T(n) — S1 : 1,2 M/33,5 M certifiées (tranches 0–600 000, 1 600 000–2 200 000)
- [ ] É4 Transitoires extrêmes
- [ ] É5 Observables (boucle gelée, frontière)
- [ ] É6 Germes et bassin à rebours
- [ ] É7 Contre-attaque
- [ ] É8 Synthèse

## Acquis S1 (18-11, voir rapports/S1_2026-11-18.md)
- Certificat d'autoroute (R-70) : DÉMONTRÉ ; départ blanc démontré dès 9 977.
- Boîtes 3×3, 4×4 (coin, cap H) : toutes démontrées (R-71).
- T1 une case noire n'importe où, T2 îlot de 2 cases voisines, T3 îlot de 3 cases en L ou en ligne, n'importe où : DÉMONTRÉS, à faire relire (R-72 à R-78).
- 5×5 (coin, cap H) : tranches [0,600 000) et [1 600 000,2 200 000) certifiées, max 184 622 (data/box5_*.res).
- Seul mécanisme de retour en arrière : le demi-tour (1 classe sur 22), qui roule sur la trace jusqu'au site précédent.

## Acquis (18-11, chat, ant_controle.c)
- Départ blanc : autoroute dès 9 977, dérive (−2,−2) dans la convention y vers le haut. OBSERVÉ (= connu).
- 3×3 : 512/512 ; 4×4 : 65 536/65 536 → autoroute ; T(3) = 51 277, T(4) = 133 984 (corrigé S1, R-69) (fourmi au coin bas-gauche, cap haut). OBSERVÉ.
- 1 case sur l'autoroute : 22 classes, 22/22 → autoroute finale (9 même direction, 13 virages). OBSERVÉ ; à réconcilier avec R-16.
- Boucle gelée : L ≤ 1 336 pendant le chaos, ≤ 112 sur l'autoroute (départ blanc). OBSERVÉ.

## Séances
(une ligne par séance : S<n>, date, durée, tâches, lien du rapport)
- S1, 18-11, 11:18–12:07 UTC : É0 ✓, É1 ✓, É2 (T1, T2, T3 démontrés), É3 5×5 1,2 M/33,5 M — rapports/S1_2026-11-18.md

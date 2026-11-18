# Autoroute — état (mis à jour à la fin de chaque séance)

PROCHAINE SÉANCE : S3
PROCHAINE TÂCHE : (1) relire `ant triple2` / `ant multi` (code neuf de S2) et écrire la preuve du couplage multiple
proprement ; (2) É2 suite : plusieurs îlots éloignés (automate des sites) avec `ant multi` ; (3) É3 5×5 par tranches
(`outils/box5_fond.sh`, recopier resultats/box5/*.res dans data/ avant de reprendre).
Outils : `fourmi -cert`, `ant pmin/uturn/triple2/multi`, `outils/gen_ilots.py`, `preuves_loin.py`, `cherche_s.sh`,
`cherche_triple.sh`, `juge_uturn.py`.

## Tâches
- [x] É0 Socle + contrôle croisé (écart R-16 « demi-tour ») — S1, R-82, E0_controle.md
- [x] É1 Lemme du certificat (énoncé, preuve, implémentation) — S1, R-83, E1_certificat.md, `fourmi -cert`
- [~] É2 Collisions → théorème « épars » — S2 : T4 îlots 3×3 (R-80, R-81, à relire). S1 : T1 une case (R-85 à R-87) et T2 îlot de 2 cases voisines (R-76) DÉMONTRÉS ; 2 cases loin OBSERVÉ (R-75). Reste : automate des sites (plusieurs îlots loin), îlots de rayon ≤ 2
- [~] É3 Boîtes exhaustives 5×5 (6×6 ?) + T(n) — S1+S2 : 2 M/33,5 M certifiées (tranches 0–1 000 000, 1 600 000–2 600 000)
- [ ] É4 Transitoires extrêmes
- [ ] É5 Observables (boucle gelée, frontière)
- [ ] É6 Germes et bassin à rebours
- [ ] É7 Contre-attaque
- [ ] É8 Synthèse

## Acquis S1 (18-11, voir rapports/S1_2026-11-18.md)
- Certificat d'autoroute (R-83) : DÉMONTRÉ ; départ blanc démontré dès 9 977.
- Boîtes 3×3, 4×4 (coin, cap H) : toutes démontrées (R-84).
- T1 une case noire n'importe où, T2 îlot de 2 cases voisines, T3 îlot de 3 cases en L ou en ligne, n'importe où : DÉMONTRÉS, à faire relire (R-85 à R-78).
- 5×5 (coin, cap H) : tranches [0,1 000 000) et [1 600 000,2 600 000) certifiées (2 M), max 188 466 (resultats/box5/).
- S2 : T4 tout îlot dans un carré 3×3 (400 formes), n'importe où : DÉMONTRÉ sous réserve de relecture (R-80, R-81).
- Seul mécanisme de retour en arrière : le demi-tour (1 classe sur 22), qui roule sur la trace jusqu'au site précédent.

## Acquis (18-11, chat, ant_controle.c)
- Départ blanc : autoroute dès 9 977, dérive (−2,−2) dans la convention y vers le haut. OBSERVÉ (= connu).
- 3×3 : 512/512 ; 4×4 : 65 536/65 536 → autoroute ; T(3) = 51 277, T(4) = 133 984 (corrigé S1, R-82) (fourmi au coin bas-gauche, cap haut). OBSERVÉ.
- 1 case sur l'autoroute : 22 classes, 22/22 → autoroute finale (9 même direction, 13 virages). OBSERVÉ ; à réconcilier avec R-16.
- Boucle gelée : L ≤ 1 336 pendant le chaos, ≤ 112 sur l'autoroute (départ blanc). OBSERVÉ.

## Séances
(une ligne par séance : S<n>, date, durée, tâches, lien du rapport)
- S2, 18-11, 12:37–13:29 UTC : T4 (îlots 3×3), vérificateurs à n changements de repère, Δ — rapports/S2_2026-11-18.md
- S1, 18-11, 11:18–12:07 UTC : É0 ✓, É1 ✓, É2 (T1, T2, T3 démontrés), É3 5×5 1,2 M/33,5 M — rapports/S1_2026-11-18.md

# Autoroute — état (mis à jour à la fin de chaque séance)

PROCHAINE SÉANCE : S8
PROCHAINE TÂCHE : É6 (germes et dynamique inverse depuis l'autoroute ; lien avec R-20) ; en fond : 5×5 (`outils/box5_fond.sh`,
recopier resultats/box5/*.res dans data/ ; faites : [0, 6,4 M) et [7,6 M, 8,0 M)). C-L (R-103) : tester les boîtes 5×5 au fil de
l'exhaustif. En attente : relecture humaine (SYNTHESE.md, E2b_couplage.md) ; T7 (trois cases éparses, plan dans E2_epars.md).

## Tâches
- [x] É0 Socle + contrôle croisé (écart R-16 « demi-tour ») — S1, R-82, E0_controle.md
- [x] É1 Lemme du certificat (énoncé, preuve, implémentation) — S1, R-83, E1_certificat.md, `fourmi -cert`
- [~] É2 Collisions → théorème « épars » — S5 : T6 deux cases éparses DÉMONTRÉ (R-95 à R-98, à relire). S2 : T4 îlots 3×3 (R-80, R-81, à relire). S1 : T1 une case (R-85 à R-87) et T2 îlot de 2 cases voisines (R-76) DÉMONTRÉS ; 2 cases loin OBSERVÉ (R-75). Reste : automate des sites (plusieurs îlots loin), îlots de rayon ≤ 2
- [~] É3 Boîtes exhaustives 5×5 (6×6 ?) + T(n) — S1–S5 : [0, 6 000 000) certifié (6 M/33,5 M), max 209 637
- [~] É4 Transitoires extrêmes — S6 : montée de colline, record(8) ≥ 220 334 (R-101), E4_transitoires.md
- [x] É5 Observables (boucle gelée, frontière) — S7 : R-102 à R-104, conjecture C-L, E5_observables.md
- [ ] É6 Germes et bassin à rebours
- [ ] É7 Contre-attaque
- [~] É8 Synthèse — S5 : note intermédiaire recherche/autoroute/SYNTHESE.md (+ PDF)

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
- Boucle gelée : corrigé en S7 (R-102) : sur l'autoroute nue, suite périodique à 34 valeurs, max 152 (172 près du germe).

## Séances
(une ligne par séance : S<n>, date, durée, tâches, lien du rapport)
- S7, 18-11, 21:14–21:41 UTC : É5 boucle gelée, C-L (R-102 à R-104) — rapports/S7_2026-11-18.md
- S6, 18-11, 19:08–19:51 UTC : É4 transitoires (R-101) — rapports/S6_2026-11-18.md
- S5, 18-11, 15:51–16:23 UTC : T6 deux cases éparses, transport, synthèse S1–S5 — rapports/S5_2026-11-18.md
- S4, 18-11, 14:38–15:17 UTC : R-92 (faille corrigée), R-93 (deux cases, 1re fixée), R-94 (récurrence en k₁), 5×5 4 M — rapports/S4_2026-11-18.md
- S3, 18-11, 13:38–14:39 UTC (redémarrage 13:57–14:36) : preuve du couplage, R-88 à R-91, T5 — rapports/S3_2026-11-18.md
- S2, 18-11, 12:37–13:29 UTC : T4 (îlots 3×3), vérificateurs à n changements de repère, Δ — rapports/S2_2026-11-18.md
- S1, 18-11, 11:18–12:07 UTC : É0 ✓, É1 ✓, É2 (T1, T2, T3 démontrés), É3 5×5 1,2 M/33,5 M — rapports/S1_2026-11-18.md

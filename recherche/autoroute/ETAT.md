# Autoroute — état (mis à jour à la fin de chaque séance)

PROCHAINE SÉANCE : S10
PROCHAINE TÂCHE (S10) : T7 (trois cases éparses). Étapes : (1) étendre `outils/t6_refait.sh` à R-96/R-98 (G1, G2, transport dual) pour
que T6 soit entièrement reproductible (R-94/R-95 le sont depuis S9, R-116) ; (2) T7 : mesurer le temps d'une base W₂ = blanc + c₁ + c₂
avec `t1relatif.py`, puis regrouper les 484 bases par « type de sortie » (piste (i) de E2_epars.md) avant de tout lancer. En fond : 5×5 à partir de X5 (voir la
ligne É3 ; `cp resultats/box5/*.res data/` puis `nohup nice -n 10 recherche/autoroute/outils/box5_fond.sh C DEBUT 200000 N &` par cœur,
3 cœurs, 4,5 min par tranche et par cœur).
Pistes ouvertes : théorème « départ blanc + une vieille trace » (plan dans E7_contre_attaque.md) ; germes 8–10 cases dans [−2,2]²
(8 et 9 : voir R-114) ; É4 records.

## Tâches
- [x] É0 Socle + contrôle croisé (écart R-16 « demi-tour ») — S1, R-82, E0_controle.md
- [x] É1 Lemme du certificat (énoncé, preuve, implémentation) — S1, R-83, E1_certificat.md, `fourmi -cert`
- [~] É2 Collisions → théorème « épars » — S9 : R-94/R-95 refaits à l'identique (R-116, `t6_refait.sh`). S5 : T6 deux cases éparses DÉMONTRÉ (R-95 à R-98, à relire). S2 : T4 îlots 3×3 (R-80, R-81, à relire). S1 : T1 une case (R-85 à R-87) et T2 îlot de 2 cases voisines (R-76) DÉMONTRÉS ; 2 cases loin OBSERVÉ (R-75). Reste : automate des sites (plusieurs îlots loin), îlots de rayon ≤ 2
- [~] É3 Boîtes exhaustives 5×5 (6×6 ?) + T(n) — S1–S8 : [0, 9 200 000) certifié (9,2 M/33,5 M), max 252 046 (R-111)
- [~] É4 Transitoires extrêmes — S6 : montée de colline, record(8) ≥ 220 334 (R-101), E4_transitoires.md
- [x] É5 Observables (boucle gelée, frontière) — S7 : R-102 à R-104, conjecture C-L, E5_observables.md
- [~] É6 Germes et bassin à rebours — S9 : 6 et 7 cases dans [−2,2]² toutes démontrées (R-114). S8 : R-107 (inverse = fourmi retournée), R-108/R-110 (toutes les configurations de 4 cases dans [−4,4]² et 5 cases dans [−3,3]² démontrées). S7 : R-105 (transitoire minimal à k cases), R-106 (dynamique inverse), E6_germes.md
- [~] É7 Contre-attaque — S9 : « autoroute × vieille trace », 328 collisions certifiées, aucune boucle (R-112). S8 : pas de construction ; ping-pong le plus court (R-109), E7_contre_attaque.md
- [x] É8 Synthèse — S9 : SYNTHESE.md S1–S8 + nouveauté par résultat + liste de relecture (+ PDF) ; S5 : note intermédiaire

## Acquis S1 (18-11, voir rapports/S1_2026-11-18.md)
- Certificat d'autoroute (R-83) : DÉMONTRÉ ; départ blanc démontré dès 9 977.
- Boîtes 3×3, 4×4 (coin, cap H) : toutes démontrées (R-84).
- T1 une case noire n'importe où, T2 îlot de 2 cases voisines, T3 îlot de 3 cases en L ou en ligne, n'importe où : DÉMONTRÉS, à faire relire (R-85 à R-78).
- 5×5 (coin, cap H) : [0, 9 200 000) certifié, max 252 046 (R-111, resultats/box5/).
- S2 : T4 tout îlot dans un carré 3×3 (400 formes), n'importe où : DÉMONTRÉ sous réserve de relecture (R-80, R-81).
- Seul mécanisme de retour en arrière : le demi-tour (1 classe sur 22), qui roule sur la trace jusqu'au site précédent.

## Acquis (18-11, chat, ant_controle.c)
- Départ blanc : autoroute dès 9 977, dérive (−2,−2) dans la convention y vers le haut. OBSERVÉ (= connu).
- 3×3 : 512/512 ; 4×4 : 65 536/65 536 → autoroute ; T(3) = 51 277, T(4) = 133 984 (corrigé S1, R-82) (fourmi au coin bas-gauche, cap haut). OBSERVÉ.
- 1 case sur l'autoroute : 22 classes, 22/22 → autoroute finale (9 même direction, 13 virages). OBSERVÉ ; à réconcilier avec R-16.
- Boucle gelée : corrigé en S7 (R-102) : sur l'autoroute nue, suite périodique à 34 valeurs, max 152 (172 près du germe).

## Séances
(une ligne par séance : S<n>, date, durée, tâches, lien du rapport)
- S8, 18-11, 23:37–00:10 UTC : R-107 à R-110, É6 germes, É7 — rapports/S8_2026-11-18.md
- S7, 18-11, 21:14–21:47 UTC : É5 boucle gelée, C-L (R-102 à R-104), É6 germes et rebours (R-105, R-106) — rapports/S7_2026-11-18.md
- S6, 18-11, 19:08–19:51 UTC : É4 transitoires (R-101) — rapports/S6_2026-11-18.md
- S5, 18-11, 15:51–16:23 UTC : T6 deux cases éparses, transport, synthèse S1–S5 — rapports/S5_2026-11-18.md
- S4, 18-11, 14:38–15:17 UTC : R-92 (faille corrigée), R-93 (deux cases, 1re fixée), R-94 (récurrence en k₁), 5×5 4 M — rapports/S4_2026-11-18.md
- S3, 18-11, 13:38–14:39 UTC (redémarrage 13:57–14:36) : preuve du couplage, R-88 à R-91, T5 — rapports/S3_2026-11-18.md
- S2, 18-11, 12:37–13:29 UTC : T4 (îlots 3×3), vérificateurs à n changements de repère, Δ — rapports/S2_2026-11-18.md
- S1, 18-11, 11:18–12:07 UTC : É0 ✓, É1 ✓, É2 (T1, T2, T3 démontrés), É3 5×5 1,2 M/33,5 M — rapports/S1_2026-11-18.md

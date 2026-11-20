# Rapport de travail — balayage massif des règles LR (20-11-2026)

**Mission** : toutes les règles L/R d'une fourmi sur la grille carrée, départ blanc, q = 2 à 16 ; réductions prouvées,
classement, certificats d'autoroute, bestiaire ≥ 50 bêtes, germes, rapport.

## Horaires (UTC, horloge de la machine)
| Tranche | Début | Fin | Contenu |
|---|---|---|---|
| Démarrage, moteur `src/balaye.c`, tests (RL, LLR…) | 12:36 | 12:39 | 2 faux positifs (période 2 et 4 le long d'un bord) corrigés : tenue ≥ 30 000 pas + certificat |
| Passe 1 : 65 242 règles × 2·10⁶ pas, 4 cœurs | 12:39:25 | 13:00:54 | 5 052 s de calcul (somme des cœurs) |
| En parallèle : section 1 (preuves, `verif_sec1.py`), analyse, recherche web | 12:39 | 13:00 | recherche web impossible (voir plus bas) |
| Passe 2 : non résolues q ≤ 9 à 10⁸ pas + « croissance linéaire » à 2·10⁷ | 13:00:54 | 13:20:51 | arrêtée volontairement à 13:21 ; 332 + 163 règles, 4 683 s de calcul |
| Analyse, bestiaire 23 (PDF), germes, rapport, dépôt | 13:21 | ~13:40 | |

## Nombres (rien d'inventé : tout sort de `stats.md`, `relations.md`, `famille_LaRb.txt`)
- Règles simulées : **65 242** = tous les mots primitifs de longueur 2 à 16 contenant L et R, un par paire L↔R.
  Cela couvre les 2·65 242 règles à miroir près ; les mots non primitifs (w^k) et L^q / R^q sont réglés par preuve.
- Passe 2 : 317 règles menées à 10⁸ pas (q ≤ 9 ; 98 règles q = 8–9 non relancées ou interrompues à l'arrêt), 163 règles à 2·10⁷ pas.
  **Non fait** : q = 10 à 12 à 2·10⁷ pas (prévu, pas le temps) ; q = 13 à 16 seulement 2·10⁶ pas (sauf 163 « croissance linéaire »).

| Classe | Nombre | Statut |
|---|---|---|
| B cycle exact | **0** | — (aucun retour à l'état initial depuis le blanc) |
| V autoroute certifiée | **6 785** | DÉMONTRÉ (certificat exact, R-136) |
| V? cap périodique, certificat refusé | 9 | OBSERVÉ (longe un bord, probablement) |
| C constructeur (virages réguliers) | 6 167 | OBSERVÉ |
| S symétrique | 470 | OBSERVÉ (théorème connu pour cette famille) |
| X chaotique | 51 811 | OBSERVÉ |
| E sortie de zone ±65 536 | 0 | — |

Répartition par q : `recherche/balayage_lr/stats.md`. Période la plus fréquente : **18** (2 038 règles, celle de LLR).
Records : période **54 280** (LLLLLLLRRLLRLLL, q = 15) ; transitoire **80 669 024** pas (LLRRLLR, q = 7 !).
17 directions d'autoroute (pente réduite) : 1/1 (6 534), 1/3 (121), 0/1 (77), 3/5, 1/2, 2/3, 3/11, 5/7, 1/5, 7/11, 1/7, 3/7, 4/13, 9/11, 3/13, 7/9, 7/17.

## Ce qui a raté / limites
- **Recherche bibliographique impossible** : langtonsant.es, lutfalla.fr et arxiv.org refusés par le réseau de la session (DNS).
  Champ « Déjà connu » rempli d'après `deja_connu.md` et ce que je sais ; aucune bête n'est dite « nouvelle ».
- Classes C / X : seuil heuristique (nombre de 20-grammes distincts dans la suite des virages < 120 000 → C). Frontière floue.
- La classe S n'a qu'un critère (symétrie à ≥ 1/2 des passages par l'origine, ≥ 3 fois).
- Le premier détecteur d'autoroute voyait des périodes 2 / 4 le long d'un bord : corrigé ; le certificat a ensuite refusé
  9 caps périodiques tardifs (dont LRRRRRLLR et LRRRRLLR) : ce ne sont PAS des autoroutes prouvées.
- `src/fourmi` reste INDÉCIS sur la période 54 280 (limite de son détecteur) ; balaye.c la certifie, l'image du PDF la montre.
- Images des bêtes à transitoire > 3·10⁶ : dessinées au pas 3·10⁶ (encore le chaos), le moteur Python du PDF serait trop lent.

## Reproduire
```
gcc -O3 -march=native -o src/balaye src/balaye.c
python3 outils/regles_lr.py 2 16 > data/balayage/regles.txt
cd data/balayage && split -n r/4 regles.txt part_ && for p in part_a?; do ../../src/balaye 2000000 < $p > $p.csv & done; wait
./pass2.sh            # (copie dans recherche/balayage_lr/) passe 2
python3 recherche/balayage_lr/analyse.py data/balayage      # CSV, stats.md, relations.md
python3 recherche/balayage_lr/famille_LaRb.py
python3 recherche/balayage_lr/verif_sec1.py
python3 recherche/balayage_lr/fiches.py 23 2026-11-20 && python3 outils/mkbestiaires.py 23 "Balayage des règles LR, q ≤ 16 (20-11)"
```
Une règle seule : `echo LLRRLLR | src/balaye 100000000` (colonnes en tête de `src/balaye.c`).

## Livrables
1. Tableau complet : `resultats/balayage_lr_2026-11-20.csv.gz` (65 242 lignes : règle, q, classe, pas, période, dx, dy, début,
   instant certifié, boîte, rapport de boîte, 20-grammes, cases non blanches, symétries, statut).
2. Statistiques : `recherche/balayage_lr/stats.md` (par classe et par q, histogramme des périodes, records, directions).
3. Notes et preuves : `recherche/balayage_lr/PREUVES.md` (R1–R7), `relations.md`, `famille_LaRb.txt`.
4. Bestiaire 23 (77 fiches) : `resultats/Bestiaire 23 - Balayage des règles LR, q ≤ 16 (20-11).pdf`.
5. Germes : `resultats/germes_2026-11-20_balayage_lr.json` (+ copie `docs/sources/`), 77 germes.
6. Journal : R-136 à R-141.

## Notes d'observation (ce qui m'a surpris)
- **Zéro cycle** depuis le blanc pour 65 242 règles : toute règle mixte (L et R) semble non bornée.
- **Toutes** les autoroutes détectées en passe 1 (6 768) passent le certificat : le détecteur « cap périodique tenu ≥ max(3P, 30 000) »
  ne s'est trompé qu'en passe 2, sur des transitoires énormes (bords de constructeurs).
- **Transitoires géants à petit q** : LLRRLLR (q = 7) ne part qu'au pas 80,7 millions ; LLRRRL (q = 6) au pas 64,4 millions.
  Il reste sûrement des autoroutes cachées dans les « chaotiques » : ne rien conclure de X.
- **S = paires, exactement** : 470 / 470.
- **LᵃRᵇ** : formule de période 16(a+b) − 20 (ou moitié) pour b impair, rien pour b pair — régularité nette, non prouvée.
- Les familles L^a RR (b = 2) restent minuscules : L¹²RR tient dans 12×12 après 2·10⁶ pas ; LLLRR dans 42×42 après 10⁸ pas
  (croissance très lente ; si l'orbite était bornée elle reviendrait un jour à l'état initial par réversibilité, mais ce retour peut être plus loin que 10⁸ pas : RIEN de prouvé).
- Les relations (a) envers, (b) rotation, (c) complément-envers ne conservent pas le comportement depuis le blanc.

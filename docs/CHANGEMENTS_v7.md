# Ce qui a changé depuis la v6

## Données (bibliotheque.json, séparée du code)
- Tous nos germes fusionnés à partir de 12 sources (v6, Drive 02_Resultats, catalogue des bestiaires 1 à 10, circuits) : **747 éléments**.
  - 277 sont visibles hors archives ;
  - 332 doublons sont **marqués et archivés**, pas effacés (« Archives / doublons ») ;
  - 138 germes détaillés sont en archives (R-36 à R-38, R-39, R-40 à R-44, bestiaires 8 à 10).
- Un germe identique à un autre garde ses autres noms (« aussi appelé ») et ses autres dossiers (↪).
- Pastille littérature sur chaque élément : 506 vertes, 69 rouges, 172 grises. Toucher la pastille montre la source.
- Statut (VÉRIFIÉ, OBSERVÉ…), références R-xx, date et fichier d'origine. Pour l'Ordinateur, l'avancement (fait / en cours / à faire).
- Historique des versions dans bibliotheque.json. `outils/construire_bibliotheque.py` **fusionne** : un élément déjà présent n'est jamais écrasé,
  et un élément ajouté à la main (`modifie_a_la_main`) est gardé.
- Menu en dossiers (système de la v6 gardé) : Une fourmi, Autoroutes, Collisions, Navettes et horloges, Cycles et groupes, Passagers,
  R-20 à R-25, **Ordinateur** (RL, LLR, pièges, fourmi dans fourmi, avancement), Archives.

## Mode circuit (37 circuits)
- Interrupteurs d'entrée, Calculer (✔/✘ et résultat en clair « 3 + 2 = 5 »), Toute la table.
- Les calculs se font dans un **Web Worker** ; si la page est ouverte par double-clic et que le Worker est refusé, ils se font dans la page.
- Couleurs : entrées, puissances, zone de lecture, bande écran.
- Les circuits sont fabriqués par `outils/circuits.py` directement à partir de nos modules Python vérifiés.

## Moteur et affichage
- Jusqu'à **1 000 fourmis** (v6 : 100). Le pas complet de la petite fourmi en a 110.
- Zéro fourmi permis quand on le demande (croisement avec les deux fils à 0). Sinon, même comportement qu'en v6.
- « Aller au pas N », par tranches, avec un bouton Stop.
- Grille classique **tournée de 45°** (mêmes calculs, seul l'affichage tourne).
- Téléphone : zoom et déplacement à deux doigts, gros boutons, grille en haut de la page.

## Atelier « Construire »
- Palette de portes (RL et LLR), pose sur la grille, aimant selon les règles R-50 (RL) et R-60 (LLR), avertissement si une règle est cassée.
- « Brancher » (LLR, gabarit R-56). C'est un premier pas : il faut vérifier le résultat en simulant.
- « Enregistrer comme germe » ajoute le germe à « Mes germes » (dans le navigateur) et le télécharge.

## Tests
- `node test.js` : les 44 tests de la v6, tous verts.
- `node test_v7.js` : 49 contrôles, tous verts :
  - aucun germe v6 perdu ;
  - chaque source entièrement présente ;
  - les 236 bêtes des bestiaires présentes ;
  - aucun identifiant perdu d'une version à l'autre ;
  - 31 résultats attendus redonnés par le moteur (cycles exacts, autoroutes, pièges).
- `node test_circuits.js [rapide|tout]` : les 37 circuits redonnent les tables de nos rapports avec le moteur JavaScript.
  - R-39 : 256/256 ; R-53 : 64/64 ; les 8 modules du pas : 256/256 chacun.
  - Pas complet R-67 : voir resultats_tests_circuits.txt et le journal.

## Pas encore fait / limites
- « Brancher » seulement en LLR, et seulement un gabarit (R-56).
- La famille de navettes R-21 n'a pas de germe enregistré (fabriquée par nav.c avec un paramètre m).
- La feuille de route « fourmi dans fourmi » n'est pas dans le Drive : l'avancement est reconstruit à partir des rapports R-61 à R-67.
- Programmes R-37 : chaque combinaison d'entrées a ses propres cases, donc les interrupteurs choisissent une variante complète.

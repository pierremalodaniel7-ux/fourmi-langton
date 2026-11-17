# Simulateur fourmi de Langton — v7

**En ligne** : https://pierremalodaniel7-ux.github.io/fourmi-langton/ (dossier `docs/` de la branche main, GitHub Pages).
Sans connexion : ouvrir `index.html` (double-clic) ; les calculs de circuits se font alors dans la page au lieu d'un Web Worker.

- Mode d'emploi : `mode_emploi.html` ; nouveautés : `CHANGEMENTS_v7.md`.
- Données (séparées du code) : `bibliotheque.json` (+ `bibliotheque.js` pour le double-clic), reconstruite par
  `python3 outils/construire_bibliotheque.py` (fusion, jamais d'écrasement ; sources dans `sources/`) ; circuits : `python3 outils/circuits.py`.
- Tests : `node test.js` (v6), `node test_v7.js` (bibliothèque), `node test_circuits.js rapide|tout` (circuits).

---

# Fourmi de Langton — simulateur à bidouiller

## Lancer

- **Simulateur** : ouvrir `index.html` dans un navigateur (double-clic). Rien à installer.
  **Il faut d'abord extraire le zip** : ouvrir `index.html` depuis l'intérieur du zip ne marche pas
  (le navigateur ne voit pas `engine.js` et `ui.js`). La page le signale alors par un bandeau rouge.
  Pas à pas :
  1. Windows : clic droit sur `fourmi-langton.zip` → « Extraire tout… » → « Extraire ».
     Mac : double-clic sur le zip (il est extrait à côté). Linux : clic droit → « Extraire ici ».
  2. Ouvrir le dossier `fourmi-langton` obtenu : on doit y voir `index.html`, `engine.js`, `ui.js`.
  3. Clic droit sur `index.html` → « Ouvrir avec » → Firefox (ou glisser le fichier dans une fenêtre Firefox).
     La barre d'adresse commence alors par `file:///`.
  4. Cliquer sur « ▶ Lecture ». Si rien ne bouge, regarder le bandeau rouge en haut de la page, ou la
     console (touche F12 → onglet « Console »).
- **Tests** : `node test.js` (Node seul, aucune dépendance).
- **Expériences en ligne de commande** : `node lancer.js --regle RL --fourmis "0,0,H ; 0,1,H" --pas 1000000`
  (résultat en JSON ; `node lancer.js --aide` pour toutes les options).

| Fichier | Rôle |
|---|---|
| `engine.js` | Le moteur pur, sans DOM : règles, grilles carrée et hexagonale, retour en arrière, détecteurs. |
| `ui.js` | L'interface : dessin sur `<canvas>`, souris, formulaires, cadrage, mesures, partage. |
| `index.html` | La page et sa mise en forme. |
| `test.js` | Les tests du moteur (et de `lancer.js`). |
| `lancer.js` | L'outil en ligne de commande. Il charge `engine.js` : même moteur que la page. |
| `captures/` | Captures d'écran de la page (voir `RAPPORT.md`). |

## Le modèle en 5 lignes

Chaque case porte un compteur `N` ; sa couleur est `N mod q`, où `q` est le nombre de lettres de la règle.
À chaque pas, chaque fourmi (dans l'ordre) : lit la couleur `c` de sa case, tourne selon la lettre
n°`c` de la règle (`cap ← (cap + virage[c]) mod M`), ajoute 1 au compteur, avance d'une case.
Le moteur écrit `N = N₀ + V` : `N₀` est la couleur de départ, `V` le nombre de passages.
Seul `V` est stocké, par blocs de 64 × 64 cases créés à la demande : la grille est donc infinie.
L'axe `y` pointe vers le bas, comme à l'écran.

## Deux grilles

| | Grille carrée (M = 4) | Grille hexagonale (M = 6) |
|---|---|---|
| Règle | lettres `R L N U`, ex. `RL`, `LLRR` | préfixe `H:` puis `N R1 R2 U L2 L1`, ex. `H:L2NNL1L2L1` |
| Virages | `R` +1, `L` −1, `N` 0, `U` 2 (quarts de tour) | `N` 0, `R1` +1, `R2` +2, `U` 3, `L2` −2, `L1` −1 (sixièmes de tour) |
| Coordonnées | `(x, y)`, `y` vers le bas | axiales `(x, y)` |
| Caps | `H` haut, `D` droite, `B` bas, `G` gauche (ou 0..3) | `0`=E(1,0) `1`=SE(0,1) `2`=SO(−1,1) `3`=O(−1,0) `4`=NO(0,−1) `5`=NE(1,−1) (noms ou 0..5) |
| Tore | carré L × L | parallélogramme L × L en coordonnées axiales |

C'est la règle qui choisit la grille : avec le préfixe `H:`, la grille est hexagonale ; sans préfixe,
c'est la grille carrée, inchangée. En hexagonal, `R` et `L` seuls valent `R1` et `L1`.
Le menu « Forme » convertit la règle au plus près (R ↔ R1, L ↔ L1 ; R2 et L2 deviennent R et L).
Les directions sont rangées dans le sens horaire à l'écran. À l'écran, l'hexagone `(x, y)` (pointe en
haut) a pour centre `X = x + y/2`, `Y = y·√3/2`. Ces conventions sont celles de `bestiaire2.c`.

## Les paramètres

| Paramètre | Effet |
|---|---|
| **Règle** | Un mot, une lettre par couleur (voir le tableau ci-dessus). `RL` est la fourmi classique. |
| **Forme / Tore** | Grille carrée ou hexagonale ; tore de côté `L` (entouré de pointillés ; autour, ses copies périodiques). |
| **Motif** | Couleurs de départ : vide, damier, rayures, aléatoire, carré plein (centré sur l'origine). Les formules s'appliquent aux coordonnées de la grille : en hexagonal, le « carré » est un losange. |
| **Taille** | Côté des carreaux, largeur des rayures ou côté du carré. |
| **Densité / graine** | Motif aléatoire : fraction de cases colorées, et graine du tirage. Même graine = même grille. |
| **Fourmis** | Nombre, puis liste `x,y,cap ; …`. |
| **Clic : dessiner** | Fait passer la case à la couleur suivante. Possible en pleine simulation (pratique pour poser un obstacle). |
| **Clic : placer les fourmis** | Clic sur une case = nouvelle fourmi ; clic sur une fourmi = la tourner d'un cran ; clic droit ou Maj + clic = l'enlever. |
| **Vitesse** | De 1 pas/s à 1 000 000 pas/image (environ 60 images par seconde). |
| **Départ / −1 pas / +1 pas** | Retour au pas 0, recul d'un pas, avance d'un pas. Clavier : espace, ← et →. |
| **Mode** | Couleurs des cases, ou carte des visites (couleur selon `V`, échelle logarithmique). |
| **Suivi de la forme** | (coché au départ) Le cadrage s'ajuste tout seul pour que la zone voulue tienne dans l'image. |
| **Cadrer** | « toute la zone visitée », ou « le centre (sans les autoroutes) » : une fourmi partie sur une autoroute ne compte que pour la zone qu'elle occupait quand l'autoroute a été reconnue. Les boutons **Tout voir** et **Centre** de la barre font la même chose une fois, et règlent le mode du suivi. |
| **Suivre la fourmi n°1** | Garde la fourmi au centre de l'écran (coupe le suivi de la forme, et inversement). |
| **Partage** | Un lien (la configuration est après le `#`) ou un fichier JSON. Ils décrivent la situation de départ, pas l'instant courant. |

Changer la règle, la grille, le motif ou les fourmis remet la simulation au pas 0.
Glisser déplace la vue, la molette zoome : cela coupe les suivis automatiques.
On peut dézoomer jusqu'à 1/1024 de pixel par case. Quand une case fait moins d'un pixel, chaque pixel montre
la couleur moyenne de ses cases visitées, mêlée au fond selon la racine carrée de la proportion de cases
visitées, pour qu'une autoroute d'une case de large reste visible de loin.
En hexagonal, à moins de 5 pixels par case, les hexagones sont dessinés comme des losanges de même centre
et de même aire (c'est invisible à cette taille, et beaucoup plus rapide).

## Cases noires et germes

- **Cases noires** : coller `x,y` (couleur 1) ou `x,y,c`, séparés par `;`, espace ou retour à la ligne (`#` = commentaire) ; « Ajouter » / « Remplacer » modifient la situation de départ (`config.dessin`, donc aussi le lien et le JSON) ; une erreur indique la ligne fautive.
- « Relatif à la fourmi 1 » compte les coordonnées depuis la case de départ de la fourmi n°1 (à la lecture comme à l'export).
- « Exporter » écrit les cases non blanches de l'instant présent, « Exporter le départ » le dessin de départ, « Copier » met le texte dans le presse-papiers.
- **Germes** : mettre `germes.json` dans le dossier puis `node outils/germes_vers_js.js` → `germes.js` (lu par une balise `<script>`, car `fetch` ne marche pas en `file://`). Choisir un germe remplit règle, fourmis et cases, et affiche sa note.
- **Autoroute de groupe** : plusieurs fourmis de même période et même déplacement, à moins de 30 cases, sont signalées ensemble.

## Les mesures

- Nombre de pas, cases visitées, boîte englobante des cases visitées, position et cap de chaque fourmi,
  images par seconde pendant la lecture.
- **Cycle exact** : toutes les couleurs et toutes les fourmis (position et cap) sont revenues à l'état initial.
  La dynamique étant réversible, c'est une **preuve** que tout se répétera à l'identique. Sur un tore,
  ça finit toujours par arriver (nombre fini d'états).
- **Détecteur d'autoroute** : pour chaque fourmi, il cherche la plus petite période `P ≤ 20 000` telle
  que la suite (couleur lue, déplacement) se répète à l'identique sur au moins 3 périodes et 100 pas.
  Il affiche `P`, le déplacement par période (en coordonnées axiales en hexagonal) et le pas de début.
  Déplacement nul = « cycle borné ».
- **C'est une détection, pas une preuve.** Le détecteur observe un temps fini. Si la répétition casse,
  l'affichage disparaît.
- Le graphe trace le nombre de cases visitées en fonction du temps.

## 7 expériences

Elles sont dans le menu « Expériences toutes prêtes ». Les chiffres ci-dessous sont ceux du moteur.

1. **`RL` seule.** Environ 10 000 pas de désordre, puis l'autoroute : `P = 104`, déplacement (±2, ±2),
   début au pas 9 977. Regarde la courbe des cases visitées devenir une droite, et compare les cadrages
   « Tout voir » et « Centre ». Pose ensuite un pavé de cases noires sur le chemin de la fourmi : la détection tombe.
2. **`RL` sur damier** (carreaux de côté 1). L'autoroute est immédiate : un escalier de période 2,
   déplacement (+1, −1). Avance pas à pas. Essaie aussi des carreaux de côté 8.
3. **Deux fourmis qui se croisent** (`0,0,H ; 40,0,G`). Elles se gênent pendant près de 200 000 pas
   dans une zone d'environ 120 × 145 cases, puis partent chacune sur une autoroute. Mets une vitesse
   élevée. Le « bonus » du menu (`0,0,H ; 1,0,H`) donne l'inverse : un cycle exact de période 28 sur
   16 cases, pour toujours.
4. **`LLRR`.** Pas d'autoroute, mais un motif qui retrouve sans cesse une symétrie haut-bas exacte
   (axe horizontal entre les lignes y = 0 et y = 1). Monte la vitesse, puis mets en pause et avance pas à
   pas pour tomber sur un instant symétrique. Regarde aussi la carte des visites.
5. **`RLR`.** Une tache irrégulière qui grossit sans régularité visible ; aucune période détectée
   après 1 000 000 de pas. Compare la forme de la courbe à celle de `RL`.
6. **Rosace hexagonale** (`H:L2NNL1L2L1`, fourmi `0,0,E`). Après 200 000 pas : 25 574 cases visitées,
   fourmi en (62, 74), cap 3 (O).
7. **Spirale hexagonale** (`H:L1L2NUL2L1R2`, fourmi `0,0,E`). Après 200 000 pas : 62 472 cases visitées,
   fourmi en (180, 4), cap 2 (SO). Le détecteur y signale par moments une « autoroute » de période 698 dont
   le déplacement change d'une fois sur l'autre (le long du bord) : encore un exemple de détection qui
   n'est pas une preuve.

Pour aller plus loin : `LRRRRRLLR` remplit un carré. Le détecteur y annonce par moments une
« autoroute » de période 58 le long d'un bord, qui finit par casser.
Et `node lancer.js --regle RL --tore 8 --pas 1e8 --arret-cycle` montre que la fourmi classique sur un tore
8 × 8 revient à son état initial au pas 11 502 464.

## L'outil en ligne de commande

```
node lancer.js --regle RL --fourmis "0,0,H ; 0,1,H" --pas 1000000
```

Options : `--regle`, `--fourmis`, `--pas` (`1e6` accepté), `--tore L`, `--motif`, `--taille`, `--densite`,
`--graine`, `--config fichier.json` (le fichier exporté par la page), `--arret-cycle`, `--compact`.
Le JSON donne : `cycle` (`oui`, `periode`), `casesVisitees`, `zone` (bornes, `largeur`, `hauteur`) et,
pour chaque fourmi, sa position, son cap et son `autoroute` (`periode`, `deplacement`, `debut`, `debutExact`,
`bornee` = déplacement nul). Le moteur fait environ 10 millions de pas par seconde.

## Réversibilité

Le bouton « −1 pas » défait exactement un pas : la fourmi recule, le compteur de la case diminue de 1,
et la couleur retrouvée dit de combien elle avait tourné. `test.js` vérifie qu'avancer puis reculer du
même nombre de pas redonne exactement l'état de départ, en carré comme en hexagonal.

## Modifier le code

- Les grilles sont décrites au début de `engine.js` (`GEOMETRIES`) : directions, noms des caps, virages.
  Le reste du moteur ne voit que des numéros de direction modulo `M`.
- Les motifs initiaux sont dans `fabriquerFond`. Un nouveau motif = une formule `(x, y) → couleur`.
- Les réglages du détecteur (`PERIODE_MAX`, `NB_PERIODES`, `LONGUEUR_MIN`, `INTERVALLE_RECHERCHE`) sont
  des constantes en tête de `engine.js`.
- La géométrie de l'écran (centre d'une case, case sous un point) est dans `engine.js`
  (`centreCase`, `caseSousPoint`), pour pouvoir la tester sans navigateur.


## Germes (v6, 16-11-2026)
- 180 germes (49 de la v5 + 24 de la nuit du 16-11 + 95 autoroutes par direction + 12 cycles symétriques).
- Menu en ARBRE : chaque dossier s'ouvre et se ferme (clic sur son nom) ; le nombre de germes est entre parenthèses.
  Case « Filtrer » : tape un mot (nom, règle, dossier) pour ne garder que les germes correspondants.
- Pour ajouter des germes : modifier germes.json (champ « dossier » = « A/B/C » pour les sous-dossiers), puis
  `node outils/germes_vers_js.js`.

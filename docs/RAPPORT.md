# Rapport des modifications

Tous les chiffres de ce rapport ont été mesurés : par `node test.js` (37 tests, tous verts), par
`outils/captures.js` (vérifications dans Chromium sans fenêtre, toutes passées) et par
`outils/mesurer_fps.js` (images par seconde).

## 1. Ce qui a changé, fichier par fichier

### `engine.js` (moteur, toujours sans DOM)

- **Deux grilles.** `GEOMETRIES[4]` (carrée, inchangée) et `GEOMETRIES[6]` (hexagonale, coordonnées
  axiales, directions `0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1)`, sens horaire à l'écran).
  `DIRECTIONS`, `TOURS` et `NOMS_DIRECTIONS` restent exportés (carré) pour compatibilité.
- **Règles.** `analyserRegle` : préfixe `H:` + jetons `N R1 R2 U L2 L1` (virages 0, +1, +2, 3, −2, −1 mod 6),
  sinon règle carrée `R L N U` exactement comme avant. `nettoyerRegle` s'appuie dessus.
  La simulation expose `M`, `geometrie`, `jetons` (une « lettre » par couleur) et `virages`.
- **Caps.** `lireDirection(d, M)`, `lireFourmis(texte, M)`, `ecrireFourmis(fourmis, M)` : `E SE SO O NO NE`
  ou `0..5` en hexagonal (et les alias `SW W NW`). Coordonnées des fourmis bornées à ± 10⁹.
- **Un pas** : lire la couleur, `cap ← (cap + virage[c]) mod M`, compteur + 1, avancer. `reculer()` défait
  les mêmes opérations : il est exact dans les deux grilles (testé sur 200 000 pas).
- **Grille par blocs** (classe `Grille`) à la place du dictionnaire `"x,y" → V` : blocs de 64 × 64 compteurs
  (`Uint32Array`) créés à la demande. Elle garde l'interface d'un `Map` (`size`, `get`, `has`, `keys`,
  `values`, `entries`, `for…of`), si bien que les anciens tests passent sans changement.
  Le moteur est **5 à 7 fois plus rapide** (10 à 14 millions de pas/s au lieu de 2 à 3).
- **Boîte englobante paresseuse** (`get boite()`) : recalculée seulement quand on la lit après un recul
  qui a touché son bord. Elle porte aussi `zmin`/`zmax` (z = 2x + y) pour cadrer exactement les hexagones.
- **Détecteur d'autoroute** : le même, avec le déplacement en coordonnées de la grille (axiales en hexagonal).
  Historique en `Uint16Array` (voir bug n°1). Recherche plus rapide (filtre sur les deux derniers symboles)
  et tous les 4096 pas au lieu de 1000. Le pas de début est inchangé, puisqu'il est daté en remontant
  l'historique : RL → période 104, début au pas 9 977.
- **Nouveau : cycle exact** (`sim.cycle`). Le moteur compte les cases dont la couleur diffère de la couleur
  initiale. Quand ce nombre vaut 0 et que toutes les fourmis sont revenues à leur départ (position et cap),
  l'état initial est retrouvé, ce qui est une preuve de périodicité. Ce compte est invalidé si on dessine
  en cours de route.
- **Nouveau : zone propre à chaque fourmi** (`f.boite`), et `f.noyau` = cette zone au moment où l'autoroute
  est reconnue (pour le cadrage « centre »).
- **Nouveau** : `centreCase` et `caseSousPoint` (géométrie de l'écran, avec l'arrondi cubique pour les
  hexagones), testables sans navigateur ; `bilan()` (le résumé qu'utilise `lancer.js`) ; `b.version` sur
  chaque bloc (l'interface s'en sert pour son cache).

### `ui.js` (interface)

- **Hexagones** : vrais hexagones à pointe en haut (centre `X = x + y/2`, `Y = y·√3/2`) à partir de 5 pixels par
  case, groupés par couleur (un `Path2D` par couleur), contour repassé dans la même couleur pour éviter les
  liserés. Plus petit : image d'un pixel par case posée par une transformation oblique, si bien que
  chaque case devient un losange de même centre et même aire. Clic → case axiale par arrondi cubique.
  Fourmis : triangle orienté selon les 6 caps. Tore hexagonal : contour en parallélogramme, copies
  périodiques.
- **Zoom** de 1/1024 à 80 pixels par case (avant : 0,5 à 80). Quand une case fait moins d'un pixel, un pixel
  = un bloc de k × k cases (k puissance de 2), en couleur moyenne. Pour tenir des millions de cases, chaque
  bloc de 64 × 64 garde un résumé (sommes de couleurs par carrés de 4 × 4), recalculé seulement si le bloc
  a changé.
- **Suivi de la forme** (coché par défaut) et cadrage « toute la zone » / « le centre (sans les autoroutes) » ;
  boutons « Tout voir » et « Centre » dans la barre. Glisser, la molette, + et − coupent le suivi. « Suivre la
  fourmi n°1 » et « Suivi de la forme » s'excluent.
- **Dessin au plus une fois par image**, et pas à chaque image pendant la lecture quand il coûte plus de 8 ms
  (il ne prend alors pas plus de la moitié du temps, le reste allant à la simulation).
- **Mesures** : cycle exact, images par seconde, déplacement « (axial) » en hexagonal.
- **Expériences** : « 6. Rosace hexagonale » (`H:L2NNL1L2L1`, `0,0,E`) et « 7. Spirale hexagonale »
  (`H:L1L2NUL2L1R2`, `0,0,E`). Exemples de règles hexagonales dans le menu « Exemples ».
- Vitesses jusqu'à 1 000 000 pas/image (avant : 100 000).
- **Supprimé** : le damier H/V de Cohen-Kong (`dessinerDamierHV`, `damierHVApplicable`, la note, l'option du
  partage). Un ancien lien ou fichier JSON contenant `affichage.damierHV` se charge toujours : l'option est ignorée.

### `index.html`

- Menu « Forme » (carrée / hexagonale), aide sur les règles `H:` et sur les caps hexagonaux.
- Case « Suivi de la forme » + menu « Cadrer », boutons « Tout voir » et « Centre ».
- Lignes « Cycle exact » et « Images par seconde » dans les mesures.
- Case à cocher et note du damier H/V supprimées.

### `test.js`

Les 20 tests d'origine sont intacts et verts. Il n'y avait **aucun** test du damier H/V (il était
seulement dans `ui.js`), donc aucun test n'a été retiré. 17 tests ajoutés : voir la sortie au §3.
Parmi eux, une **simulation de référence naïve** écrite à part (dictionnaire `"x,y" → V`), comparée au moteur
sur 6 configurations : coordonnées négatives, bords de blocs, tores de 65 et 70 cases (plus grands qu'un bloc),
plusieurs fourmis, carré et hexagone.

### `lancer.js` (nouveau)

`node lancer.js --regle RL --fourmis "0,0,H ; 0,1,H" --pas 1000000` → JSON. Il fait `require('./engine.js')`,
sans aucune copie du moteur. Options : `--tore`, `--motif`, `--taille`, `--densite`, `--graine`, `--config`
(fichier exporté par la page), `--arret-cycle`, `--compact`, `--aide`. Exemple réel :

```json
{"pasDemandes":1000000,"regle":"RL","grille":"carrée","pas":1000000,"cycle":{"oui":false},
 "casesVisitees":1001415,"zone":{"xmin":-706,"xmax":707,"ymin":-706,"ymax":708,"largeur":1414,"hauteur":1415},
 "fourmis":[{"x":152,"y":-554,"cap":2,"nomCap":"B","autoroute":{"periode":2,"deplacement":[1,1],"bornee":false,"debut":999697,"debutExact":true}},
            {"x":-150,"y":557,"cap":0,"nomCap":"H","autoroute":{"periode":2,"deplacement":[-1,-1],"bornee":false,"debut":999699,"debutExact":true}}],
 "fourmisDepart":"0,0,H ; 0,1,H","dureeMs":93}
```

Attention à la lecture : ces deux fourmis longent le bord d'un losange qui grandit. Les « autoroutes » de
période 2 sont des morceaux de bord qui cassent au coin suivant : ce sont des détections, pas des preuves.
Autres résultats trouvés avec l'outil : les fourmis voisines `0,0,H ; 1,0,H` → cycle exact de période 28 ;
`H:R1` → cycle exact de période 6 ; `RL` sur un tore 8 × 8 → retour exact à l'état initial au pas 11 502 464.

### `README.md`

Mis à jour : deux grilles, règles `H:`, caps, tore hexagonal, cadrage et suivi, zoom, cycle exact,
expériences 6 et 7, `lancer.js`. Damier H/V retiré (y compris dans l'expérience 2).

### `outils/` (nouveau, facultatif, nécessite Playwright)

`captures.js` (vérifications dans le navigateur + captures), `mesurer_fps.js` (images par seconde),
`erreurs.js` (erreurs JavaScript de la page).

## 2. Bugs trouvés dans le code existant et corrigés

1. **Reculer devenait extrêmement lent** : `_retrecirBoite` relisait toutes les cases chaque fois qu'une case
   du bord de la boîte disparaissait. Mesuré : avancer puis **reculer 200 000 pas en RL prenait 52 secondes**
   (ancien moteur), contre **28 ms** maintenant (boîte recalculée seulement quand on la lit).
2. **Débordement latent du détecteur** : l'historique était un `Uint8Array` et le symbole vaut `c·M + d`.
   En carré, le maximum (63·4 + 3 = 255) tenait tout juste ; avec M = 6, il atteint 383 et aurait été
   tronqué en silence. Il est passé en `Uint16Array`.
3. **Tore minuscule très dézoomé** : la page dessinait toutes les copies périodiques de chaque fourmi, sans
   limite (des centaines de milliers de triangles pour un tore 2 × 2 dézoomé). Avec le nouveau zoom, la page
   aurait gelé. Au-delà de 400 copies, seule la fourmi elle-même est dessinée.
4. **Flèches du clavier sans effet après un clic sur un bouton** (le bouton gardait le focus et le
   gestionnaire ignorait tous les boutons). Les flèches marchent maintenant ; l'espace sur un bouton reste
   au bouton, pour ne pas agir deux fois.
5. **Coordonnées non bornées** dans une configuration importée (lien ou JSON) : bornées maintenant à ± 10⁹.
6. **Coût caché du détecteur** : sur une règle sans autoroute (RLR, LLRR), la recherche faite tous les
   1000 pas coûtait environ 150 ns par pas, plus que le pas lui-même. Après correction, RLR passe de 2,4 à
   10 millions de pas/s, avec les mêmes résultats.

7. **Zoom à la molette presque inopérant dans Firefox** (déjà dans la version d'origine) : Firefox compte
   la molette en lignes (environ 3 par cran) et non en pixels (environ 100 par cran, comme Chrome) ; le zoom
   y était environ 30 fois trop faible. `deltaMode` est maintenant pris en compte : un cran donne ×0,86
   dans les deux navigateurs (vérifié en simulant un événement de molette « à la Firefox »).
8. **Aucun message quand quelque chose ne va pas** : la page affiche désormais un bandeau rouge pour toute
   erreur JavaScript, et un message explicite si `engine.js` est introuvable (cas typique : `index.html`
   ouvert depuis l'intérieur du zip sans l'avoir extrait). Vérifié en ouvrant `index.html` seul dans un dossier.

Point **non** modifié, à savoir : `maxVisites` (échelle de la carte des visites) ne redescend pas quand on
recule ; il est remis à zéro au « Départ ». C'était déjà le cas avant.

## 3. Sortie complète de `node test.js`

```
Étape 1 — règles de base
  ok    "RL" : les 4 premiers pas à la main
        (cases visitées : 1595, cases noires : 834)
  ok    "RL" : 11 000 pas => chaque case visitée compte bien ses passages
  ok    lettres N et U
  ok    motifs initiaux (damier, rayures, carré, aléatoire reproductible)
  ok    dessin à la main : le clic fait défiler les couleurs
Étape 1 — déterminisme
  ok    même configuration => même résultat
  ok    avancer(5000) = 5000 fois avancer(1)
  ok    export JSON puis import => même simulation
  ok    une configuration abîmée est réparée, pas plantée
  ok    champ texte des fourmis : lecture et écriture
Étape 1 — réversibilité
  ok    avancer 3000 pas puis reculer 3000 pas => état de départ
  ok    reculer pas à pas repasse exactement par les mêmes états
  ok    reculer ne descend pas sous le pas 0
  ok    la boîte englobante suit les allers-retours
Étape 1 — tore
  ok    tore : les fourmis restent dans 0..L-1 et la dynamique reste réversible
Étape 2 — détecteur d'autoroute
        (détecté : période 104, déplacement (-2, 2), début au pas 9977)
  ok    "RL" sur grille vide : période 104, déplacement (±2, ±2), début vers 10 000
  ok    "RL" pas à pas : aucune fausse alerte avant, même résultat après
  ok    reculer avant le début de l'autoroute => la détection disparaît, puis revient
  ok    un obstacle sur l'autoroute fait tomber la détection
  ok    règle "N" : « autoroute » de période 1 ; règle "R" : cycle borné (déplacement nul)
  ok    "RL" : l'autoroute commence exactement au pas 9 977 (non-régression)
  ok    une autoroute détectée déplace vraiment la fourmi de (dx, dy) à chaque période
Étape 3 — grille hexagonale
  ok    lecture des règles : préfixe « H: », jetons, règle carrée inchangée
  ok    caps hexagonaux : E SE SO O NO NE ou 0..5, lecture et écriture
  ok    directions hexagonales : 0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1)
  ok    un pas hexagonal à la main : lire, tourner, compter, avancer
  ok    H:L2NNL1L2L1, 200 000 pas : 25 574 cases, fourmi en (62, 74), cap 3
        (détecté : période 698, déplacement axial (18, -21), début au pas 194378)
  ok    H:L1L2NUL2L1R2, 200 000 pas : 62 472 cases, fourmi en (180, 4), cap 2
  ok    200 000 pas en avant puis 200 000 en arrière => grille blanche, fourmi au départ
  ok    hexagonal : configuration riche, avancer puis reculer pas à pas
  ok    tore hexagonal (parallélogramme L × L en axial) : fourmis dans 0..L-1, réversible
  ok    géométrie de l'écran : centre d'une case -> la même case (arrondi cubique)
Étape 3 — grille par blocs et cycle exact
  ok    le moteur donne exactement le même résultat qu'une simulation naïve
  ok    la grille par blocs se comporte comme un dictionnaire "x,y" -> V
  ok    cycle exact (retour à l'état initial) : trouvé quand il existe, oublié en reculant
        (zone totale 3702 de large, centre 92)
  ok    cadrage « centre » : la zone de la fourmi au moment où l'autoroute est reconnue
Étape 4 — outil en ligne de commande
  ok    lancer.js : RL, fourmis voisines (cycle exact), rosace hexagonale

37 test(s) réussi(s), 0 échec(s).
```

## 4. Captures et vérifications dans le navigateur

Chromium sans fenêtre (Playwright), page ouverte en `file://` comme par un double-clic, fenêtre 1400 × 900.
Commande : `node outils/captures.js . captures` (depuis le dossier du projet). Vérifications automatiques,
toutes passées :

- le damier H/V a disparu ; le suivi de la forme est coché au départ ; aucune erreur JavaScript ;
- **couleur des cases** : pour 25 cases visitées visibles, le pixel au centre de la case a *exactement* la
  couleur que donne le moteur. Vérifié en carré, en hexagones de près et en losanges de loin (25/25 à chaque fois) ;
- **clic** au centre, près du bord est et près de la pointe de l'hexagone (3, −2) → c'est bien la case
  axiale (3, −2) qui change de couleur et qui s'affiche sous la souris ;
- **suivi de la forme** : la zone visitée entière tient dans l'image (RL à 20 000 pas, rosace, spirale,
  autoroute à 300 000 pas, 4 millions de cases) ;
- **bouton « Centre »** sur l'autoroute : zoom 64 fois plus fort, et le suivi continue en mode centre ;
- **dézoom maximal** : 1/1024 de pixel par case ; le zoom à la main coupe le suivi ;
- tore hexagonal : la fourmi reste dans le parallélogramme.

| Fichier (`captures/`) | Ce qu'on voit |
|---|---|
| `00-page-entiere.png` | La page complète (RL, 20 000 pas) : panneau, barre, mesures, autoroute détectée au pas 9 977. |
| `01-rl-20000-pas.png` | RL à 20 000 pas, cadrée automatiquement : la tache et l'autoroute en entier. |
| `02-rosace-hexagonale.png` | Rosace, 200 000 pas (25 574 cases), en losanges (2,35 px/case). |
| `03-hexagones-de-pres.png` | Rosace de près : vrais hexagones à pointe en haut, quadrillage hexagonal. |
| `04-spirale-hexagonale.png` | Spirale, 200 000 pas. |
| `05-autoroute-cadrage-tout.png` | RL à 300 000 pas, cadrage « tout » : la diagonale ; la forme centrale est un point. |
| `06-autoroute-cadrage-centre.png` | La même, cadrage « centre » : la forme centrale et le début de l'autoroute. |
| `07-millions-de-cases.png` | Deux fourmis RL, 4 000 000 de cases (0,24 px/case). L'intérieur du losange est **blanc** : il est visité un nombre pair de fois (vérifié : 5 658 cases noires sur 4 002 829, toutes au bord). |
| `07b-…-carte-des-visites.png` | La même en carte des visites : le losange plein. |
| `08-dezoom-maximal.png` | Dézoom maximal (1/1024 px/case) : la forme n'est plus qu'un point. |
| `09-tore-hexagonal.png` | Tore hexagonal 40 × 40 : parallélogramme en pointillés et ses copies. |
| `10-spirale-carte-des-visites.png` | Spirale en carte des visites. |

### Images par seconde (Chromium sans fenêtre, 1400 × 900, **100 000 pas/image** dans les deux versions)

| Situation | Avant | Après |
|---|---|---|
| RL, 8 px/case | 24 images/s, 2,4 M pas/s | **60** images/s, 6,0 M pas/s |
| RL, 0,5 px/case (ancien zoom minimal) | 12 images/s (48 ms de dessin) | **60** images/s (4 ms de dessin) |
| RLR, 0,5 px/case | 24 images/s | **58** images/s |
| RL, 1/1024 px/case, 7 millions de cases | (impossible) | **60** images/s |
| RL, suivi de la forme | (n'existait pas) | 56 images/s, 35 dessins/s |
| Spirale hexagonale, suivi, ~8 millions de cases | (n'existait pas) | 45 images/s, 15 dessins/s |

« Images/s » = images du navigateur (chacune fait avancer la simulation) ; « dessins/s » = images où la
grille est redessinée (voir la règle du dessin au §1). Le pire cas mesuré est la spirale hexagonale qui
remplit tout l'écran, à 25-30 ms par dessin.

### À vérifier toi-même (ce qu'un navigateur sans fenêtre ne montre pas)

- La **fluidité ressentie** sur ta machine : lance la spirale à 100 000 pas/image et lis « Images par
  seconde » dans les mesures.
- Le **zoom à la molette** et le glisser (simulés ici par les boutons et par du code, pas par une vraie molette).
- Un **écran haute densité** (Retina) : les captures sont faites à 2 pixels par pixel CSS, mais pas sur un vrai écran.
- **Firefox et Safari** : seul Chromium a pu être testé (le téléchargement de Firefox est bloqué dans mon
  environnement). Le code n'utilise aucune syntaxe ni fonction récente propre à un navigateur ; la seule
  différence connue de Firefox (la molette) est corrigée.

## 5. Limites qui restent

- **Tore hexagonal = parallélogramme L × L en axial** (choisi plutôt que désactivé) : c'est un vrai tore,
  mais pas le tore « hexagonal régulier » (où les 6 directions jouent le même rôle). La forme visible est un
  losange à 60°.
- **Motifs de départ** en hexagonal : les formules (damier, rayures, carré) s'appliquent aux coordonnées
  axiales ; le « carré » est un losange, les rayures sont obliques.
- **Losanges en dessous de 5 pixels par case** en hexagonal (même centre, même aire que l'hexagone).
- **De très loin, couleur moyenne** : un pixel montre la moyenne de ses cases (fond mêlé selon √p). Une zone
  visitée un nombre pair de fois redevient du fond (voir capture 07) ; la carte des visites est alors plus parlante.
- **Cadrage « centre »** : il repose sur le détecteur d'autoroute, qui n'est pas une preuve. Après un retour en
  arrière, la zone propre à chaque fourmi repart de la zone totale : le cadrage « centre » peut alors englober
  un bout d'autoroute jusqu'au prochain « Départ ».
- **Pire cas du dessin** : une forme hexagonale de plusieurs millions de cases qui remplit l'écran, en suivi,
  descend à environ 15 dessins/s (la simulation continue à environ 45 images/s).
- **Mémoire** : 16 Ko par bloc de 64 × 64 cases touché, plus le résumé (4 Ko) si on dézoome. Une autoroute
  très longue (des centaines de millions de pas) touche beaucoup de blocs presque vides.
- **Portée** : les fourmis doivent rester à moins d'environ 10⁹ cases de l'origine. Au-delà, le moteur
  s'arrête avec une erreur claire au lieu de se tromper.
- **Cycle exact** : il n'est cherché que comme retour à l'état initial. Pour une dynamique réversible c'est
  la seule forme possible de cycle, mais il peut arriver après un temps astronomique (11,5 millions de pas
  pour RL sur un tore 8 × 8).
- **`--arret-cycle`** s'arrête à la fin de la tranche de 65 536 pas où le cycle est trouvé : le champ `pas`
  peut donc dépasser la période (la période, elle, est exacte).

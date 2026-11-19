# É7 — Contre-attaque : un décor fini peut-il occuper la fourmi indéfiniment ? (S8, 18-11-2026)

Réponse de cette séance : **pas de construction** ; voici ce qui bloque et ce qu'on a mesuré.

## 1. Ce qui est impossible (connu)
- Trajectoire bornée : impossible pour toute configuration finie (Bunimovich–Troubetzkoy 1992). Un décor fini ne peut donc pas
  « enfermer » la fourmi ; il faudrait l'occuper en l'emmenant de plus en plus loin sans autoroute.
- La dynamique inverse n'aide pas : le passé d'une configuration est le futur de la fourmi retournée (R-107) ; « autoroute à
  rebours pour tout décor fini » est équivalent à la conjecture.

## 2. Les seuls mécanismes de retour qu'on ait vus (T1–T6)
Le **demi-tour** : une case sur la bande renvoie l'autoroute sur sa propre trace jusqu'au site précédent (germe ou collision),
qui peut la renvoyer à son tour (classes « aller-retour » de T4 : jusqu'à 4 traversées). Dans tous les cas démontrés, le nombre
de traversées est **fini et fixé par la classe** (pente 52·(NS+1)), et l'autoroute finit par partir en terrain neuf.

## 3. Expérience « ping-pong le plus court » (`outils/pingpong.py`)
À chaque étape, on ajoute la case la plus proche, devant la fourmi au moment du certificat, qui renverse la direction finale.
| étape | case ajoutée | distance (demi-périodes) | certifié | boîte des cases |
|---|---|---|---|---|
| 1 | (−11,−4) | 1 | 15 199 | 11 |
| 2 | (26,−13) | 1 | 18 785 | 26 |
| 3 | (7,28) | 1 | 36 485 | 28 |
| 4 | (47,30) | 1 | 43 678 | 47 |
| 5 | (−13,25) | 1 | 55 755 | 47 |
| 6 | (46,−1) | 1 | 81 382 | 47 |
| 7 | (−18,56) | 2 | 79 188 | 56 |
| 8 | (67,−45) | 25 | 136 818 | 67 |
| 9 | — | aucun demi-tour à < 400 demi-périodes (décalage ±12) | — | — |
Remarque : la case est posée là où était la fourmi au certificat ; elle peut modifier tout le chaos précédent (étape 7 : le
certificat recule). Chaque étape est une nouvelle configuration, toutes certifiées (8 cases : 136 818 pas).
Conclusion : renverser la fourmi coûte une case par renversement et une boîte qui grandit ; la méthode gloutonne s'arrête vite.
Ce n'est pas une preuve d'impossibilité.

## 4. Ce qu'il faudrait pour une vraie construction
Un mécanisme **auto-entretenu** (la fourmi fabrique elle-même les miroirs qui la renvoient, comme le rectangle croissant de
Lutfalla pour LLRRRL). Pour RL, les seules structures auto-construites observées sont l'autoroute et le « rouleur » qui roule sur
sa trace et s'arrête au site précédent (R-74, R-81). Aucune ne se reconstruit plus loin. Piste non explorée : chercher, parmi les
issues de collision « autoroute × trace » (R-25), une issue qui renvoie une autoroute vers un site qu'elle vient elle-même de créer.

## 5. S9 (19-11) : « autoroute × vieille trace » (R-112)
Montage : fourmi = germe R-20 (0,0,B ; certifié dès 0, autoroute (−2,2)). Obstacle = la trace laissée par ce même germe après
200 périodes (2 400 cases environ, sans la fourmi), tournée de 0°, 90°, 180° ou 270° et décalée de (a,b) pour que l'autoroute
la percute à ≈ 100 cases. Outil : `outils/trace_croise.sh 200 A0 A1 B0 B1 ROT` (la trace est construite en Python, seul
`src/fourmi -cert` juge). 328 configurations, **328 certifiées** (autoroute pour toujours, DÉMONTRÉ pour chacune).

| trace | configurations | traverse (−2,2) | longe la trace (−2,−2) | remonte la trace (2,2) | demi-tour (2,−2) | pas certifié max |
|---|---|---|---|---|---|---|
| perpendiculaire, construite vers (−2,−2) | 64 | 32 | 16 | 16 | 0 | 50 486 |
| perpendiculaire, construite vers (2,2) | 64 | 24 | 0 | 32 | 8 | 26 903 |
| de face (pointe vers la fourmi) | 100 | 44 (dont 21 ratées) | 26 | 26 | 4 | 113 648 |
| même sens (la fourmi rattrape le germe de la trace) | 100 | 57 (dont 19 ratées) | 15 | 26 | 2 | 26 787 |

Perpendiculaire : exactement 8 classes (période 4 en a, 2 en b, réseau engendré par (2,2) et (−2,2)), chaque classe vue 8 fois
avec le même résultat (pas certifiés égaux à ±104·k près, ou à quelques pas près quand la fourmi longe la trace jusqu'à son bout).
« Longe la trace » = **relais** : la fourmi rejoint la vieille autoroute, la suit jusqu'à sa pointe et la prolonge.
« Remonte » : elle roule sur la vieille trace jusqu'à son germe, puis repart. Demi-tour : elle revient sur sa propre trace.
Conclusion pour É7 : une vieille trace se comporte comme un « site » de plus (comme une case noire) : 1 traversée de plus, puis
une autoroute en terrain neuf. Aucun croisement n'a donné de boucle. Ce n'est pas une preuve qu'il n'en existe pas.
Contrôle croisé (`ant lot`, 2ᵉ moteur) : même direction finale 328/328, début à ≤ 3 pas du certificat.
Bug corrigé au passage : `src/fourmi` tronquait en silence les lignes de plus de 16 ko (configurations de > ≈ 1 500 cases) ;
tampon porté à 1 Mo, 19/19 tests OK.

### Indépendance vis-à-vis de la longueur et du point de croisement (R-113)
Croisement perpendiculaire (trace construite vers (−2,−2)), point de croisement fixé en (−150,150), s = position du croisement
le long de la trace (0 = germe de la trace, P = sa pointe). Les 8 classes (dans l'ordre a = 0..3, b = 0..1) :

| s (P = 200) | classes 1–8 | pas certifiés |
|---|---|---|
| 10 | (−2,−2) (2,2) (2,2) (2,2) (−2,2) (−2,2) (−2,2) (2,2) | effet du bout (germe de la trace) |
| 20 à 160 | (−2,−2) (−2,2) (−2,−2) (2,2) (−2,2) (−2,2) (−2,2) (2,2) | classe 1 : 22 826 − 4s ; classe 4 : 12 638 + 20s ; les 6 autres constants |
| 180, 190 | changent (effet de la pointe) | |

Et pour s = P/2 : identiques pour P = 120, 200, 300, 400. Lecture : la fourmi qui « longe » (classe 1) roule vers la pointe à
4 pas par case de diagonale, celle qui « remonte » (classe 4) roule vers le germe de la trace à 20 pas par case ; les autres
ne voient que le croisement. C'est la même structure que pour une case noire lointaine (T1) : une preuve par couplage
« trace de longueur quelconque, croisée n'importe où loin des bouts » paraît accessible avec les outils de E2b_couplage.md.

Autres orientations (R-113, suite) :
- perpendiculaire, trace construite vers (2,2) : 8 classes, mêmes résultats pour s = 20 à 190 : 4 « longent » vers la pointe
  ((2,2), 4 pas par case), 3 traversent, 1 demi-tour (26 695, constant). Seul s = 10 (près du germe de la trace) diffère.
- de face (la fourmi arrive sur la pointe) : P = 150, 200, 300 donnent la même issue pour 88/100 décalages ; les 12 autres
  (6 classes, pas certifiés 45 000 à 114 000) sont celles où la fourmi remonte toute la trace jusqu'à son germe : l'issue
  dépend alors de P (rencontre avec le germe de la trace à une autre phase).
- même sens (la fourmi rattrape le germe de la trace) : 100/100 identiques pour P = 150, 200, 300.

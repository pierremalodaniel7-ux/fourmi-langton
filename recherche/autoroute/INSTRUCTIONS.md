# Conjecture de l'autoroute — mode d'emploi pour Claude Code

> Lis ce fichier en entier au début de chaque séance « autoroute », puis `ETAT.md` (même dossier).
> Ce fichier complète `CLAUDE.md` (à la racine), qui reste valable.

## 0. Le but
Conjecture : la fourmi RL classique, partie de **n'importe quelle configuration finie** de cases noires,
finit par construire l'autoroute de période 104 (dérive (±2,±2)). Elle est ouverte depuis les années 1980.
Objectif réaliste : **démontrer la conjecture pour des familles de configurations**, trouver des indices
(ou un contre-exemple), et ne jamais refaire ce qui est déjà connu.
Plan détaillé avec schémas : `plan_18-11.pdf`. État de l'art : section 2 du PDF + `deja_connu.md`.

## 1. Le mot-clé « continue » (séances d'une heure)
Quand Pierre-Malo écrit **continue** (ou lance le prompt de démarrage) :
1. `date` → note l'heure de début. Lis `ETAT.md` : la ligne « PROCHAINE TÂCHE » dit quoi faire.
2. Pas de questions préalables (exception à CLAUDE.md : la séance autoroute est déjà cadrée).
   Si un choix se présente, prends le plus raisonnable et écris-le dans le rapport.
3. Travaille **une heure d'horloge** : enchaîne les tâches de la liste (section 4) dans l'ordre.
   - Vérifie l'heure avec `date` après chaque tâche (et toutes les ~15 min pendant un long calcul).
   - Calculs longs : en tâche de fond par tranches de ≤ 10 min (`nohup … &`), en suivant le fichier de sortie.
     Ne réponds pas à Pierre-Malo tant que l'heure n'est pas finie : quand tu réponds, les calculs s'arrêtent.
   - Après chaque tâche terminée : coche-la dans `ETAT.md`, ajoute l'entrée au journal, commit + push.
4. À **60 min** (au plus 70 min si une tâche est presque finie) : arrête, écris le rapport (section 2),
   mets à jour `ETAT.md` (PROCHAINE TÂCHE = la suivante, avec ce qu'il reste à faire), commit + push.
5. Réponds en **10 lignes max** : ce qui est fait, le résultat le plus important, le statut de chaque résultat,
   la prochaine tâche, le lien du rapport. Puis attends le prochain « continue ».

## 2. Le rapport de chaque heure
Fichier `rapports/S<numéro>_<date>.md` (numéro = séance suivante dans `ETAT.md`). Contenu, court :
- heure de début / fin (sortie de `date`), tâches faites, tâches non finies ;
- **résultats** sous forme de tableau : ID (suite de journal.md : R-69, R-70…), énoncé, statut
  (VÉRIFIÉ / OBSERVÉ / AFFIRMÉ / FAUX / OUVERT / DÉMONTRÉ), commande pour reproduire ;
- chiffres réels uniquement (nombre de configurations, temps de calcul mesuré) — jamais inventés ;
- ce qui a raté, ce qui est douteux ;
- si une trouvaille semble nouvelle : la recherche faite pour vérifier (dans `deja_connu.md` puis 1-2 recherches web).
Ensuite, comme le demande CLAUDE.md : déposer le rapport dans le Drive (05_Methode) et, s'il y en a,
bestiaire + germes ; **dossier Drive de ce projet : `06_Conjecture_autoroute`
(id 19qDWY6UO3ecaLp8j8CfY3eQtto0nIqCa)** — y mettre aussi une copie du rapport.
Si tu n'as pas d'outil Drive dans cette séance, dis-le en une ligne : Claude (chat) fera le dépôt.

## 3. Règles propres à cette recherche
- **Moteur** : `src/fourmi` (et les programmes de `src/`). `ant_controle.c` (ce dossier) est un 2ᵉ moteur
  indépendant, simple, pour les contrôles croisés. Pas de troisième moteur.
- **Simulation ≠ preuve.** Une autoroute détectée reste OBSERVÉE tant que le lemme du certificat (tâche É1)
  n'est pas démontré et appliqué. Après É1, une autoroute certifiée = DÉMONTRÉ pour cette configuration.
- Déjà fait dans ce dépôt (ne pas refaire, s'en servir) : R-16 (1 case sur l'autoroute, 22 issues),
  R-17 (1 à 3 cases autour de la fourmi, tout → 104), R-20 (bout d'autoroute minimal 11 cases),
  R-24 (2 cases, 1 683 paires), R-25 (2 autoroutes qui se croisent). `grep -n "R-16" journal.md` etc.
- Littérature connue : Bunimovich–Troubetzkoy 1992 (trajectoire non bornée), Troubetzkoy 1997 (pas de coin
  visité infiniment), Gale–Propp–Sutherland–Troubetzkoy 1995, Gajardo–Moreira–Goles 2002,
  Gajardo–Lutfalla–Rao 2024 (arXiv 2409.10124), Lutfalla 2025 (2505.05426, 2506.10482),
  temps d'échappement MFCS 2026 (2606.26677), dépôt GitHub evanmack45 (5×5 exhaustif, non relu).
- Économie : ne lis jamais un gros fichier en entier (head, grep, wc) ; résultats > 1 Mo dans `data/`.

## 4. Liste des tâches (dans l'ordre ; une séance en fait une ou plusieurs)
Chaque tâche : but → livrable → critère de fin.

**É0 Socle (≈ 30 min)**
- Compiler `src` + `make test` ; compiler `ant_controle.c` (`gcc -O2 -o ant ant_controle.c`).
- Contrôle croisé des 2 moteurs : départ blanc (9 977, période 104), 512 configs 3×3, 22 collisions 1 case.
- **Écart à expliquer** : R-16 donne « 1 demi-tour » parmi 22 issues, `./ant obst 150` donne 0 demi-tour
  (9 même direction, 13 virages). Hypothèse : R-16 note la *première* autoroute après le choc, `ant`
  la *dernière* (un demi-tour repasse dans le chaos). Trancher et le noter.
- Livrable : `E0_controle.md` + ligne de journal. Fin : les deux moteurs d'accord sur tout (ou écart expliqué).

**É1 Lemme du certificat (≈ 1 h)** — la pièce maîtresse.
- Énoncé visé : « si au pas t la fourmi est dans la phase φ de l'autoroute avec le motif M_φ autour d'elle,
  et que toutes les cases du demi-plan devant elle (au sens de la dérive) sont blanches, alors elle construit
  l'autoroute pour toujours ». Déterminer exactement M_φ (zone lue pendant une période) et la zone à vérifier.
- Démonstration écrite (récurrence sur les périodes), courte, relisible par un étudiant de L1.
- Implémenter `certifie(…)` dans le moteur : renvoie DÉMONTRÉ + pas de début, ou rien.
- Livrable : `E1_certificat.md` (énoncé + preuve + test), journal. Fin : le certificat valide le départ blanc.

**É2 Collisions → théorème « épars »**
- Repartir de R-16/R-24, certifier chaque issue avec É1.
- Définir une configuration ε-éparse (îlots de diamètre ≤ d, distants de ≥ D(d)) et démontrer par récurrence
  la conjecture pour les îlots d'une case, puis de 2 cases ; calculer D minimal.
- Puis îlots quelconques de rayon r ≤ 2 (énumération exhaustive des îlots à symétrie près).
- Livrable : `E2_epars.md` (théorème + tableau des cas), germes JSON des issues remarquables.

**É3 Boîtes exhaustives et T(n)**
- Fixer la convention (fourmi au centre ? dans la boîte ? 4 caps ?) et l'écrire.
- 5×5 (33,5 M configs, symétries pour diviser) en tâche de fond par tranches ; comparer avec le dépôt evanmack45.
- Avec É1 : chaque configuration certifiée = démontrée. Mesurer T(3), T(4), T(5) (transitoire max).
- 6×6 seulement si l'estimation de temps tient en quelques heures.
- Livrable : `E3_boites.md`, records en germes.

**É4 Chasse aux transitoires extrêmes** — montée de colline / génétique sur boîtes 6×6 à 10×10 ;
courbe record(n). Livrable : records + graphe.

**É5 Observables** — boucle gelée L(t) (`./ant frozen`), sorties de la tache (frontière), nombre de cases
noires ; chercher une quantité qui annonce l'autoroute ; essayer une régression simple. Livrable : 1-2
conjectures nettes avec données.

**É6 Germes et bassin à rebours** — dynamique inverse (réversible) depuis l'autoroute ; catalogue des
plus petits germes ; lien avec R-20.

**É7 Contre-attaque** — peut-on fabriquer un décor fini qui occupe la fourmi indéfiniment (portes de
`recherche/ordinateur`, rectangle croissant de Lutfalla pour LLRRRL) ? Résultat attendu : construction
ou explication précise de l'échec.

**É8 Synthèse** — vérifier la nouveauté de chaque résultat, rédiger une note (PDF) pour Pierre-Malo.

# Déjà cherché dans la littérature (lire AVANT toute recherche web)

Vocabulaires : chercheurs (highway, multiple ants, multi-turmite, generalised ant, periodic orbit) ;
amateurs (spaceship, glider, oscillator, puffer, 2c/12…). Conventions : Golly et Fatès-Chevrier sont
SYNCHRONES et, dans Golly, les fourmis qui se rencontrent meurent. Chez nous : l'une après l'autre.

| Sujet | Verdict | Source | Cherché le |
|---|---|---|---|
| Cycles à 2 fourmis (croisement puis chemin défait) | Phénomène connu | Chopard & Droz 1998 | 14/11 |
| Losange à 2 fourmis | Déjà connu (qualitatif) ; nos mesures 2 pas/case, √(2t)+1 : pas trouvées | Chopard 1998, healeycodes | 14/11 |
| Carré 2×2 = vaisseau 2c/12 | Déjà connu | Belgacem & Fatès 2012 ; ConwayLife ~2017 | 15/11 |
| Cycles à 4 fourmis, horloges 16N−4 (N pair, synchrone) | Phénomène connu ; chez nous seul N = 2 | Beuret-Tomassini 1997, Fatès-Chevrier 2010, Belgacem-Fatès 2012 | 15/11 |
| Vaisseaux 4 fourmis, 2c/8, 2c/96, vitesse max c/3 | Probablement connu (forum non lu en entier) | ConwayLife « Langton's Ant Society » | 15/11 |
| Périodes famille LⁿR | Déjà connu | Gajardo-Lutfalla-Rao 2025 | 14/11 |
| Démarrer une autoroute depuis un motif | Notion connue ; bout minimal 11 : pas trouvé | Lutfalla 2025 | 15/11 |
| Autoroutes non diagonales | Déjà connu | Lutfalla 2025 (LLRRRL) | 16/11 |
| Autoroutes hexagonales | Connu des amateurs | Golly HexTurmite | 16/11 |
| Même classe ⇒ pas de cycle (R-09) | Pas trouvé énoncé (implicite chez Chopard / Fatès-Chevrier) | — | 15/11 |
| Conjecture des phases (R-14) | Pas trouvé | — | 15/11 |
| Autoroute 102 à 2 fourmis, rail, suiveuse, tandem, passagers, navettes, relais, convertisseur, nids, catalogue de collisions | Pas trouvé | articles + ConwayLife partiel | 15-16/11 |
| Catalogue des directions d'autoroutes | Pas trouvé (langtonsant.es inaccessible depuis Claude) | — | 16/11 |
| Calcul de circuits booléens par la fourmi (P-difficile, universalité) | Déjà connu (principe) ; additionneur multi-fourmis à retenue par autoroute : pas trouvé | Gajardo, Moreira, Goles 2002 (Discrete Appl. Math. 117) | 16/11 |

À lire un jour (bloquant pour dire « nouveau ») : fil ConwayLife « Langton's Ant Society » en entier ; langtonsant.es.
| Portes logiques par traversée de traces (plusieurs fourmis RL, NOR/ET/COPIE/croisement) | Pas trouvé (le principe « la fourmi calcule » est connu : Gajardo-Moreira-Goles 2002, 1 fourmi) | 2 recherches web (arXiv nlin/0306022, fil ConwayLife Langton's Ant Society = synthèse de vaisseaux) | 17/11 |
| Additionneur à une puissance par comptage de traces (poids = germes doublés), pièges à autoroute réutilisables | Pas trouvé (même recherche que la ligne précédente ; Gajardo-Moreira-Goles = 1 fourmi) | 17/11 |
| Conjecture de l'autoroute pour « départ blanc + 1 case noire quelconque » (T1, R-87) ; certificat d'autoroute (R-83) ; boîtes 3×3/4×4 démontrées | Pas trouvé (conjecture générale ouverte ; seul résultat général : trajectoire non bornée, Cohen-Kong / Bunimovich-Troubetzkoy). Le principe « autoroute + avant blanc ⇒ pour toujours » est sans doute folklore | 2 recherches web (arXiv 2505.05426, Wikipedia) | 18/11 |
| Records de transitoire (plus long chaos avant l'autoroute) pour des boîtes n×n | Pas trouvé ; le plus proche : « How Long Can the Escaping Ant Be Confined? » (arXiv 2606.26677, MFCS 2026), NON LU (arxiv.org inaccessible depuis le conteneur, 18/11) ; résumé lu le 19/11 (S9) : bornes sur le temps d'échappement d'un domaine fini (factorielle pour les carrés), autre question ; 2024 : transitoires 10³–10⁵ pour 1 case près de la fourmi | 1 recherche web | 18/11 |
| Boucle gelée (orbite sans retourner les cases) comme indicateur d'autoroute ; conjecture C-L (R-103) | Pas trouvé (1 recherche web, 18/11) | — | 18/11 |
| Configurations démontrées (certificat) : boîtes 3×3/4×4, ≤ 3 cases dans [−5,5]², 4 dans [−4,4]², 5 dans [−3,3]², 1 case partout (T1), îlots 3×3 (T4), 2 cases éparses (T6) | Pas trouvé comme preuves ; le plus proche : simulations de Gajardo–Lutfalla–Rao 2024 (arXiv 2409.10124 : 1 case noire à distance ≤ 3, transitoires 10³–10⁵, numérique) ; MFCS 2026 (temps d'échappement, non lu) | 2 recherches web (S8) | 19/11 |
| Collision d'une autoroute avec une vieille trace d'autoroute (1 fourmi) : 8 classes perpendiculaires, relais, remontée, demi-tour ; indépendance vis-à-vis de la longueur (R-112, R-113) ; germes 6–7 cases dans [−2,2]² (R-114) | Pas trouvé (le plus proche : nos R-25, 2 fourmis ; articles de Lutfalla sur les autoroutes, autre sujet) | 1 recherche web (S9) | 19/11 |
| Record de transitoire 5×5 (351 374, R-118) ; dépôt « evanmack45 » (5×5 exhaustif) | Dépôt introuvable par recherche web (S9) ; record pas trouvé | 1 recherche web | 19/11 |
| B5 : toutes les configurations dans un carré 5×5, fourmi n'importe où dans le carré, tout cap → autoroute 104 (calcul exhaustif + certificat, arbre de choix) | Pas trouvé. Etse, « How Long Can the Escaping Ant Be Confined? » (MFCS 2026, LIPIcs 386, 49 ; arXiv 2606.26677) : temps d'échappement d'un domaine fini (borne 2^d, borne factorielle pour les carrés), pas l'autoroute — lu : résumé et extraits de recherche seulement (drops.dagstuhl.de et arxiv.org inaccessibles depuis le conteneur) ; Gajardo-Lutfalla-Rao 2024 (arXiv 2409.10124) : simulations, transitoires 10³–10⁵, pas de preuve exhaustive ; aucune vérification exhaustive par ordinateur trouvée | 2 recherches web (requêtes : titre Etse MFCS 2026 ; « Langton's ant highway all finite configurations exhaustive proof computer-assisted ») + 1 essai de lecture des 2 PDF (échec réseau) | 19/11 |
| Gomme : retourner la fourmi (x − e_h, h + 2) et inverser l'ordre de jeu efface tout (R-136) | CONNU : réversibilité ; Tsukiji & Hagiwara, « Recognizing the repeatable configurations of time-reversible generalized Langton's ant is PSPACE-hard », Algorithms 4(1), 2011 (« reverse of a walking course ») ; flipping rotators (Lorentz lattice gas) | 2 recherches web | 25/11 |
| Une fourmi seule ne repart jamais en gomme (R-137) ; loi d'équilibre des classes dans les cycles (R-139) ; gomme par échange ; bascule T et paire qui efface sa ligne (R-140, R-141) ; écran 2 pixels (R-142) | Pas trouvé (recherches : « multiple Langton's ants periodic orbit parity class », « reversible Langton's ant », Hagiwara-Tsukiji) | 3 recherches web | 25/11 |
| RLEM (éléments réversibles à mémoire) : tout RLEM 2 états non dégénéré à k ≥ 3 symboles est universel ; parmi les 2-2, les n° 2-2, 2-3, 2-4 ne sont pas universels | CONNU : Morita, Ogiro, Alhazov, Tanizawa, J. Multiple-Valued Logic and Soft Computing 18 (2012) 37–54 ; Morita, arXiv 1309.1264 ; rotary element (Morita 2001) | 1 recherche web | 25/11 |

## Ajout du 26/11 (jour) : déjà connu — règles (recopie de recherche/regles/deja_connu_regles.md)
# Lignes à AJOUTER à deja_connu.md (nuit du 25/11, session « règles » ; non fusionné pour ne pas toucher aux fichiers communs)

| Sujet | Verdict | Source | Cherché le |
|---|---|---|---|
| Réversibilité de la fourmi généralisée (retour en arrière en retournant la fourmi) | Connu | Gajardo et al., Algorithms 4(1) 2011 (PSPACE, « time-reversible generalized Langton's ant ») ; ci2ma pp11-28 | 25/11 |
| Condition exacte de la gomme : q = 2 et K₁ = −K₀ (carré, hexa, triangle) ; gomme collective (n fourmis, ordre inversé) qui remet à zéro un circuit entier | Pas trouvé énoncé (sans doute folklore pour RL) | 1 recherche web | 25/11 |
| LLLR : autoroutes 52 et 156 | Connu | arXiv 2506.10482 | 25/11 |
| LLRRRL : infinité d'autoroutes (896, 992, 800, 1 088…) | Connu | Lutfalla, « Sideways on the highways », arXiv 2505.05426 | 25/11 |
| Hexa ±120° (H:R2L2) = gaz de Lorentz à « flipping rotators » ±2π/3 sur réseau triangulaire : la particule se propage | Connu (propagation dans une bande) | Kong & Cohen ; Grosfils & Boon (arXiv cond-mat/9905168) ; plusieurs particules : arXiv 1908.06019 (2019) NON LU (arxiv.org inaccessible) | 25/11 |
| Hexa ±60° (H:R1L1) / triangle RL = flipping rotators ±π/3 sur nid d'abeilles : marche auto-évitante entre retours | Connu | Webb & Cohen 2014 (arXiv 1404.3629, 1507.07133) | 25/11 |
| Vaisseau R2L2 à 1 case sans trace ; chocs de 2 vaisseaux (0 perte sur 1 215) ; portes interaction / aiguillage ; circuit à 2 étages réutilisé 30 fois | Pas trouvé — À VÉRIFIER dans arXiv 1908.06019 avant de dire « nouveau » | 4 recherches web | 25/11 |
| Comparaison de règles pour le calcul réutilisable (fil, déviation, croisement, réutilisation, gomme) | Pas trouvé | 1 recherche web | 25/11 |

## Nuit du 26/11 (session hexa) — lecture de arXiv 1908.06019 et des sources voisines
| Sujet | Verdict | Source | Cherché le |
|---|---|---|---|
| Vaisseau R2L2 (R-306) : fourmi ±120° qui se propage dans une bande, 8 pas par case | **Déjà connu** : « la particule se propage dans une direction à travers une bande », pour TOUTE configuration de rotateurs ; vitesse moyenne 1/8 (= notre période 8, 1 case) ; appelé « glider » par Khlabystova. Notre forme exacte (1 seule case portée, aucune trace sur fond blanc) n'est pas écrite telle quelle mais en découle | Grosfils, Boon, Cohen, Bunimovich, J. Stat. Phys. 97 (1999) 575 (arXiv cond-mat/9905168, Thm 2) ; Kong & Cohen ; S. Khlabystova, thèse Georgia Tech 2003 | 26/11 |
| « Une fois dans sa bande, la particule n'en sort jamais » (pour toute configuration) ⇒ AUCUN obstacle fixe ne peut tourner un vaisseau | **Déjà connu** (preuve esquissée par cas, figures 10-12) ; nous le revérifions par un calcul exhaustif (R-330) | Grosfils et al. 1999 ; explique R-307 | 26/11 |
| Plusieurs particules ±2π/3 sur réseau triangulaire (rotateurs partout), orbites périodiques à 2 particules (période 4d, taille 3d+1), « chain reaction », théorème : passé non borné ⇒ futur non borné | **Déjà connu** — mais modèle SYNCHRONE avec hypothèse « jamais 2 particules sur le même site au même instant » ; notre convention (l'une après l'autre) diffère exactement dans ces cas | McGinnis & Webb, arXiv 1908.06019 (2019) | 26/11 |
| Deux particules qui se « diffusent » mutuellement dans de nouvelles bandes (déviation par choc, R-310) | **Probablement connu** (Prop. 4.2 de la thèse Khlabystova, lue seulement en résumé) ; McGinnis-Webb Fig. 3 : « déviation de son mouvement par une autre particule » | Khlabystova 2003 ; 1908.06019 | 26/11 |
| Portes « boule de billard » faites de chocs de vaisseaux R2L2 (interaction, aiguillage R-314), circuit réutilisé 30 fois (R-321) | **Pas trouvé ailleurs** : aucune porte logique ni modèle de billard dans 1908.06019, Grosfils 1999, Khlabystova 2003 ; Bunimovich-Khalbystova 2002 (« LLG and many-dimensional Turing machines », Collision-Based Computing, Springer) non lu : c'est la seule source à risque | 6 recherches web + 3 lectures | 26/11 |
| Turmite hexagonale ±120° (Golly HexTurmite) | Rien de spécifique trouvé (règles hexa générales connues, Turk/Golly) | 1 recherche | 26/11 |
| Invariant Q = (cases noires) − Σ⌊cap/2⌋ mod 3 (R2L2) ⇒ aucun miroir exact ; forme générale pour q = 2 : c·K₀ ≡ 1, c·K₁ ≡ −1, c·M ≡ 0 (mod m) (RL : mod 4, R1L1 : mod 6) | **Pas trouvé** (2 recherches) ; le cas RL est sans doute du folklore (parité « damier » de la fourmi, Gale-Propp « Further travels with my ant ») | 2 recherches | 26/11 |
| « 0 perte » pour tous les chocs de 2 vaisseaux (calcul exhaustif) ; mémoire, écran, bascule RS, demi-additionneur réutilisables (certificats pour tout nombre d'usages) | **Pas trouvé** | idem | 26/11 |
| Capture d'un vaisseau par un objet périodique impossible sans émission | **Déjà connu** sous une autre forme : McGinnis-Webb 2019, Thm 3 (passé non borné ⇒ futur non borné) | 1908.06019 | 26/11 |

### Ajout 26/11 jour (session « additionneur complet + boucle ») — R-344
| Trouvaille | Verdict | Source | Date |
|---|---|---|---|
| Portes par chocs de vaisseaux R2L2, demi-additionneur / additionneur réutilisables | **Pas trouvé** dans Bunimovich & Khlabystova 2002 (« Lorentz Lattice Gases and Many-Dimensional Turing Machines », Collision-Based Computing, Springer, p. 443-467, DOI 10.1007/978-1-4471-0129-1_15) : d'après le résumé Springer (lu) et la thèse Khlabystova 2003 (lue en partie), le calcul y est fait par l'ENVIRONNEMENT (symboles écrits aux sommets = règles de diffusion ; une particule = machine de Turing multi-rubans à une tête, plusieurs particules = plusieurs têtes) ; aucune porte, aucun additionneur, aucune mémoire ni horloge par chocs de plusieurs particules ; la thèse dit seulement que 2 « gliders » sur T2 « peuvent changer de bande » après un choc (cf. notre R-310) et que la dynamique à plusieurs particules est « highly non-trivial », sans résultat rigoureux. Corps du chapitre NON lu (aperçu bloqué) : verdict « pas trouvé », pas « nouveau certain ». | résumé Springer (via unpaywall), Crossref, thèse Khlabystova 2003 (1re partie) ; dblp refusé | 26/11 |
| « Réflecteur » | La thèse (Fig. 26) appelle « reflector » un amas de diffuseurs qui CHANGENT d'état (pas un miroir fixe) ; aucun théorème d'impossibilité de réflexion trouvé ⇒ notre R-330/R-331 reste « pas trouvé ailleurs » | thèse Khlabystova 2003 | 26/11 |
| Références à lire si besoin : Bunimovich 1996 (Int. J. Bif. Chaos 6, « Many-dimensional Lorentz cellular automata and Turing machines »), Bunimovich 2001 (Multiple-Valued Logic) | non lues | références du chapitre | 26/11 |

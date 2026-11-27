# S3 — pas de la petite fourmi en R2L2 (journal propre, R-600+)

Entrées R-600 à R-609 écrites après coup (27/11, 00:45 UTC) à partir des commits du 26/11 soir (19:33–20:09) et des fichiers ;
chiffres repris de resultats_modules.json et bibliotheque_portes.json (rien de recalculé à cette heure, sauf mention).

## R-600 Catalogue des chocs de 2 vaisseaux de classe paire — VÉRIFIÉ (2 ordres de jeu, hx.py)
Dir 0 × dir 2 ou 4, toutes positions relatives : en classe paire, seulement des échanges / transparences (pas de déviation utile).
Code : chocs_pairs.py → data/chocs_pairs.json (non versionné).

## R-601 à R-604 Échanges, portes sélectives, couples (g, h), chaînes NOR en classe paire — OBSERVÉ
Pistes « logique de voie » ; abandonnées au profit des chocs DÉVIANTS à 60° (R-605). Code : swaps.py, selectifs.py, combos.py, chaines.py.

## R-605 Compilateur « arbre de NOR » R2L2 — VÉRIFIÉ (par module, tous les cas, 2 moteurs)
Nœud = une puissance K ; ses entrées la croisent l'une après l'autre (choc déviant à 60°, même issue dans les 2 ordres, τ = 2…6) ;
K continue tout droit ssi aucune entrée → K = NOR(entrées). Un vaisseau par littéral vrai et par usage. Code : nor.py.

## R-606 Réutilisation au même endroit + certificat — DÉMONTRÉ (lemme) / VÉRIFIÉ (20 usages, 2 moteurs)
Usage u = même circuit retardé de u·Δ. Lemme : fenêtre d'interaction bornée, rayons libres avant/après qui ne s'approchent plus à < 7,
routes opposées à ≥ 7 voies → tout nombre d'usages est juste. Code : reuse.py (certificate, check_multi).

## R-607 Pas de la petite fourmi RL sur le tore 2×2 (R-61), module par module — VÉRIFIÉ pour h0', x', y', c00'..c11'
État 8 bits c00 c10 c01 c11 x y h1 h0. h0' = ¬h0 ; x' = x ⊕ ¬h0 ; y' = y ⊕ h0 ; cij' = cij ⊕ [x=i ∧ y=j] ; h1' = h1 ⊕ h0 ⊕ c.
| module | puissances | littéraux | cas | justes | 2 moteurs | certificat | Δ (pas) | 20 usages ×3 |
| h0' | 1 | 1 | 2 | 2 | 2 | oui | 2008 | 20/20 ×3 |
| x'  | 3 | 4 | 4 | 4 | 4 | oui | 3864 | 20/20 ×3 |
| y'  | 3 | 4 | 4 | 4 | 4 | oui | 4472 | 20/20 ×3 |
| cij' (×4) | 4 | 6 | 8 | 8 | 8 | oui | 5368–5880 | 20/20 ×3 |
(cas = 2^(variables utilisées) ; les 256 états s'y ramènent.) Commande : python3 modules.py h0 x y c00 c10 c01 c11 → resultats_modules.json.

## R-608 Diagnostic géométrique et recherche des longueurs — OUTIL
diag.py : segments de lignes d'univers à < seuil hors chocs voulus (sans simulation). opt.py / opt2.py : descente (petites échelles).

## R-609 Bibliothèque de portes R2L2 réutilisables — VÉRIFIÉ
NON, COPIE, ET, NOR, OU, ET par NOR, XOR (R-337) : tous les cas justes, 2 moteurs, certificat, 20 usages. Format : bibliotheque_portes.json,
code : portes_lib.py.

## R-610 Module h1' = h1 ⊕ h0 ⊕ c (27/11, 00:41 →) — EN COURS
Arbre de NOR de modules.py (27 puissances, 32 littéraux, 59 vaisseaux, 256 cas). Recherche aléatoire petites échelles (D 8–40, G 8–16,
400 essais) : aucun placement (00:41). Un placement au hasard : 216/256 faux, 0 voie opposée sûre, 195 conflits (diag, seuil 4).
Nouvelle idée : GRANDES échelles (D ≤ 300, G ≤ 60) et descente sur le nombre de conflits géométriques au seuil 7 (opt3.py).
- 00:47 diag2.py : conflits EXACTS par cas (chaque segment porte le masque des cas où il existe ; x et ~x ne coexistent jamais).
  Contrôle : modules x' → 0 conflit ; c00' → 2 couples à distance 4–5 (inoffensifs : le seuil 7 est prudent).
- 00:48–00:57 descentes opt4/opt5/opt6 (D ≤ 300, G ≤ 60, côtés) : plateau à 17 conflits (h1), 27 (h1f), 362 (h1s). OBSERVÉ.
- 00:58 CONFLITS STRUCTURELS — DÉMONTRÉ (argument ci-dessous, contrôlé sur n00/Nc : distance 520 → 2 en t = 3700–3756) :
  les 17 conflits restants sont TOUS à distance 0 et entre directions à 60°. Raison : si un nœud N a la même direction que son
  grand-parent P (côté + puis côté −), dans le repère qui suit la puissance de P, N est immobile et la sortie du parent avance en ligne
  droite vers P ; un débris de N qui part dans la direction du parent suit EXACTEMENT ce trajet et heurte P, quels que soient D et G.
  Remède : changer les côtés (miroirs) → struct.py (descente sur les côtés, conflits présents à distance 0 pour 3 tirages de D, G).
- Variantes de formule (modules.py, vérifiées sur les 256 états) : h1f (c et ¬c en un nœud à 4 sous-nœuds, 19 puissances),
  h1s (NOR des 16 cubes de ¬h1', profondeur 2, 17 puissances mais 80 littéraux).
## R-611 Pas complet en un germe : 7 modules sur 8 côte à côte — VÉRIFIÉ (moteur C) 00:52
step.py : h0', x', y', c00'..c11' translatés (voies opposées ≥ 7 entre modules), 256/256 états propres et justes (moteur C).
- 01:05 Analyse des conflits structurels (repère de la puissance P, où tous les partenaires d'un même côté suivent la MÊME droite
  relative ℓ± vers P) — DÉMONTRÉ (raisonnement) + OBSERVÉ (conflicts2, distance 0 pour tout D, G) :
  (S1) deux sous-nœuds du même côté : les débris immobiles (dans le repère de P) laissés sur ℓ par le 1er sont heurtés par le 2e
       (c'est la règle R-606 « un seul sous-nœud par côté » ; tout-« + » : 21 à 43 conflits à distance 0) ;
  (S2) un nœud N du côté opposé à celui de son parent M a la direction de son grand-parent P : immobile dans le repère de P, ses
       débris de direction M suivent ℓ et heurtent P. Sauf si N = NON d'une seule entrée… mais alors son enfant retombe dans S2.
  Conséquence : dans UN arbre, tout chemin garde le même côté ⇒ chaque nœud (hors racine) a au plus un sous-nœud ⇒ chaînes
  « liste de décision à clauses », qui ne savent pas faire un XOR (preuve : le 1er test devrait être une clause incluse dans {00, 11}).
  C'est pourquoi h0', x', y', cij' passent (profondeur ≤ 2 ou chaîne même côté) et pas h1'.
  REMÈDE choisi : COMPOSER des petits modules. La sortie d'un module (vaisseau tout droit) est posée EXACTEMENT sur la ligne d'univers
  d'un littéral du module suivant (rotation k, translation v, retard s ≡ phase mod 8), loin en amont. Un littéral n'a pas de porte
  à lui, donc pas de débris sur ℓ. → compose.py (R-612).
## R-612 Composition de modules (compose.py) — OUTIL VÉRIFIÉ sur g = h1⊕h0 ; ÉCHEC pour h1' (01:15)
Sous-circuit G (2 feuilles) : 256/256 justes et propres (3 tirages de Dlink). Circuit h1' en 13 modules (8 cubes, c, ¬c, g, ¬g, XOR) :
logique 256/256 mais au mieux 98/256 physiquement (24 tirages de Dlink 40–400) ; sous-circuits c et ¬c (4 cubes → train de 4) : 80–192/256.
Raison (même argument que R-610) : le module amont roule SUR la ligne du littéral, ses portes sont donc des événements sur ℓ± ;
ses débris immobiles (repère de P) bloquent les littéraux suivants du même côté (S1). Composer = greffer un sous-arbre : rien de neuf.
## R-613 Limite du compilateur NOR à chocs déviants — DÉMONTRÉ (sous les règles S1, S2)
Avec S1 et S2, un module = racine NOR de deux chaînes de même côté, chaque nœud de chaîne = NOR(train de littéraux, nœud suivant).
Une chaîne calcule une fonction « canalisante emboîtée » (NCF : f = l ∨ f' ou f = ¬l ∧ f', récursivement) ; la racine = ET de 2 NCF.
Parité de 3 variables : toute NCF qui contient ses 4 points vrais est une seule clause (preuve : la 1re variable canalisante doit être
disjonctive, puis la fonction restante sur 2 variables contient 2 points opposés → b∨c ou b∨¬c) ; 2 clauses ne peuvent exclure les 4
points faux. Donc h1' = h1 ⊕ h0 ⊕ c n'est PAS calculable par un module (ni par composition, qui est géométriquement la même chose).
Statut : DÉMONTRÉ pour ce jeu de portes (côtés + et −). Issue possible : portes « de face » (H), autre mécanisme (XOR R-337, fusion S1).
## R-614 Issue : portes « de face » (H) — EN COURS (01:12)
S2 n'a lieu que pour deux arêtes consécutives (+,−) ou (−,+). Le chemin (H,H) redonne la direction du grand-parent, mais aucun nœud ne
lâche de débris dans la direction a+3 (côtés : a±1, a±2 ; face : a+1, a+2) → pas de S2. Règle (htree.py) : après « + » : +, H ;
après « − » : −, H ; après H ou à la racine : +, −, H ; H = 1re entrée ; un sous-nœud par ligne. Avec H on peut BRANCHER : la limite
R-613 ne s'applique plus. Arbre h1' (27 puissances, 32 littéraux), formule juste sur les 256 états ; conflits à distance 0 : 7, 5, 3
pour 3 tirages de (D, G), tous différents → aucun conflit structurel commun. Descente opt7.py lancée (2 graines).
- 01:12 opt7 (graine 1, 213 s) : placement à 6 conflits géométriques (seuil 7, inoffensifs) → simulation : 256/256 JUSTES ET PROPRES.
  01:17 2e moteur : 256/256 identiques (hx.py), 49 s. → MODULE h1' (1 usage) VÉRIFIÉ : 27 puissances, 32 littéraux, 59 vaisseaux,
  tmax 12 356 pas. Paramètres : h1_param_simple.json (arbre htree.h1_tree()).
- Réutilisation de h1' : NON (critère (c) faux, 0 voie d'écart). Raison DÉMONTRÉE : une porte de face met l'enfant H sur la voie même de
  la puissance parent ; si le parent ressort tout droit (parent = 1 et sa puissance-parent déjà déviée), il file vers l'infini sur cette
  voie et percutera de face l'enfant H (vaisseau constant) de l'usage suivant. Dans l'arbre : Nc (2e entrée de A) et Pc (2e entrée de B)
  ont un enfant H ; B aussi mais A et B ne valent jamais 1 ensemble. Remède envisagé : n'avoir d'enfant H que pour des 1res entrées,
  ou un « balai » (puissance qui dévie la sortie qui s'échappe).
## R-615 LE PAS COMPLET EN UN GERME (1 usage) — VÉRIFIÉ (01:21)
step.py (NOLANES=1 BOX=6000, graine 1) : les 8 modules h0', x', y', c00'..c11', h1' translatés dans un seul germe R2L2 :
256/256 états propres et justes (les 8 sorties = R-61), moteur C (11 s) ; hx.py 256/256 états finaux identiques (54 s).
Commande : NOLANES=1 BOX=6000 python3 step.py 1 3 step8_simple.json h1_param_simple.json
Sans h1' (7 modules, BOX 1500) : certificat OK (Δ = 74 072 pas), 10 usages de suite au même endroit : superposition exacte,
10/10 justes, 2 moteurs identiques (01:15).
## R-616 h1' réutilisable : arbre htree.h1_tree2 (29 puissances) — EN COURS (01:27 →)
Règle ajoutée : un nœud qui a un enfant de face doit être la 1re entrée de son parent (Nc, Pc passent en face sous A, B ; ¬g et g
deviennent NON(NOR(feuilles))). B garde un enfant de face en 2e entrée de la racine, mais A et B ne valent jamais 1 ensemble.
opt9.py : 2 placements 256/256 justes et propres trouvés (graine 4 vers 01:31, graine 3 vers 01:34) ; certificat (Python) en cours.
- 01:41 Certificat de reuse.py trop lent pour 60 vaisseaux (double boucle Python sur 14 000 pas) → cert2.py (numpy, même lemme ; contrôlé identique sur x'). struct.py renommé structurels.py (il masquait le module standard struct).
- 01:43 h1R_param_3 et h1R_param_4 : 256/256 justes et propres, 2 moteurs 256/256 (tmax 10 540 et 9 804). Certificat en cours.
- 01:45 certificat (cert2) des 2 candidats : voies opposées des sorties RÉELLES à 0 (ÉCHEC) ; opp_real.py : 15 couples, tous
  « génériques » (débris ↔ littéraux ou puissances d'autres branches), aucun de la forme structurelle → réglables par D, G.
  opt10.py : descente sur conflits + 5 × couples opposés logiquement possibles (segments infinis de diag2 avec masques), lancée 01:47.
- 01:59 opt10 (graine 8, poids 1 sur les voies opposées, départ = meilleur de la graine 6) : placement à 0 couple opposé, 256/256 justes
  et propres, CERTIFICAT OK (fenêtre 9 877 pas, rayon 1 740, voies opposées ≥ 7 ⇒ tout nombre d'usages pour Δ ≥ 65 733 pas).
  Paramètres : h1R_param_OK.json. Vérification complète (2 moteurs, 20 usages ×3) : h1R_check.py, en cours.
## R-616 MODULE h1' RÉUTILISABLE — VÉRIFIÉ (02:12)
h1R_param_OK.json (arbre htree.h1_tree2, 29 puissances) : 256/256 justes et propres, 2 moteurs 256/256 ; certificat OK
(Δ ≥ 65 733 pas) ; 20 usages ×3 graines au même endroit : superposition exacte, 20/20 justes (moteur C, 900 fourmis) ;
3 usages avec les 2 moteurs : identiques, 3/3. Commande : python3 h1R_check.py h1R_param_OK.json → h1R_verif_OK.json.
## R-617 Pas complet réutilisable (02:05 →)
Germe 8 modules avec ce h1' (step.py graine 1, BOX 6000, voies opposées entre modules vérifiées) : 256/256 propres et justes (C, 8 s),
hx.py 256/256 identiques (47 s). Le certificat cert2 a manqué de mémoire (positions stockées : 130 fourmis × 14 000 pas × 256 cas)
→ cert3.py (sans mémoire, contrôlé identique sur x' et c00') ; step_reuse.py lancé 02:12.
- 02:14 cert3 sur le germe complet (8 modules, h1' réutilisable) : CERTIFICAT OK — fenêtre active max 9 877 pas, rayon 11 709,
  voies opposées ≥ 7 ⇒ tout nombre d'usages pour Δ ≥ 384 741 pas (Δ pris = 384 744). 115 s.
- 02:15 3 usages au même endroit (états au hasard) : superposition exacte, 3/3 (les 8 bits justes à chaque usage), 2 moteurs identiques.
- 02:18–02:20 5 usages ×2 graines (moteur C ; 10 usages : mémoire du moteur C dépassée) : superposition exacte, 5/5 et 5/5.
  STATUT R-617 : VÉRIFIÉ (2 moteurs, 256/256, usages répétés) ; tout nombre d'usages DÉMONTRÉ (certificat R-606, lemme relu en vague 1).
  Résultats : step_reuse_res.json. Commande : python3 step_reuse.py
## R-618 2 pas enchaînés — OUVERT (non tenté, 02:20)
Brancher les sorties du pas 1 sur les littéraux du pas 2 demande UNE copie de module par littéral utilisé (65 vaisseaux-littéraux
dans le pas 2, en comptant les négations) et, d'après S1, un littéral calculé doit être le DERNIER de son côté dans un train : les
feuilles actuelles (trains de 2 à 5 littéraux) ne le permettent pas. Piste : feuilles à 1 littéral calculé par côté + chocs de face,
ou un module « COPIE » (R-609) pour dupliquer.
- 02:21 Dépôts Drive : bestiaire 30 (5 fiches) + catalogue_s3.json → Bestiaires ; germes → 02_Resultats ; rapport (Google Doc) → 05_Methode ;
  versions de 01:25 déplacées dans 99_Archives. PR #15 (vers main) à jour.
- Fichiers de résultats ajoutés : step_res.json (germe 7 modules réutilisable, R-611/R-615), h1R_verif_3.json et h1R_verif_4.json
  (candidats h1' 256/256 dont le certificat a échoué, voies opposées 0, R-616), step8_simple.json (ESSAI RATÉ : 8 modules avec BOX 1500,
  128/256 propres — h1' trop près des autres ; la version juste est celle de R-615, BOX 6000).
## R-619 DEUX PAS ENCHAÎNÉS, 7 bits sur 8 (h0'', x'', y'', c00''..c11'') EN UN GERME — VÉRIFIÉ (27/11, 05:46–06:06, vague 3)
Choix (noté, Pierre-Malo dort) : chaîner par GREFFE (R-612) : chaque littéral v' / ¬v' d'un arbre du pas 2 est un module du pas 1
(double rail : ¬v' par le même arbre aux littéraux inversés) ; la puissance racine de ce module sort tout droit ssi v' = 1 et entre
dans la porte du pas 2. Diffusion = une copie de module du pas 1 par usage (pas de dédoublement de vaisseau). Les arbres du pas 2 ont
au plus 2 sous-nœuds par nœud, donc la règle de côtés de htree.py (portes de face) s'applique toujours (1 usage).
Sous-système fermé : (x, y, h0, cij) ne dépend pas de h1 (sur le tore 2×2, avancer de +1 ou −1 change la même coordonnée) ; F∘F donne
h0'' = h0, x'' = ¬x, y'' = ¬y — mais le germe les calcule EN PASSANT par les vaisseaux x', y', h0' (pas de raccourci).
| module | puissances | littéraux | cas | justes (= F∘F) | 2 moteurs |
| h0'' | 2 | 1 | 2 | 2 | 2 |
| x'', y'' | 11 | 10 | 4 | 4 | 4 |
| cij'' (×4) | 26 | 28 | 16 | 16 | 16 |
Longueurs : descente optc.py (comme opt7), 0 à 280 s par module (c11 : graine 1 ratée en 280 s, graines 2 et 3 OK en 61–102 s).
Germe : les 7 modules translatés (step.choose_offsets2, NOLANES=1, BOX=8000 ; BOX=3000 : pas de place pour c11) : 256/256 états
propres et justes (moteur C, 13 s) ; hx.py 256/256 identiques (108 s). 128 puissances, 143 littéraux.
Commande : python3 chain2.py (formules sur les 256 états) ; python3 optc.py c00 1 280 ; NOLANES=1 BOX=8000 python3 chain_germ.py 1
Résultats : chain_res.json, chain_params.json. Reste : h1'' (le cap) et la réutilisation.
## R-620 h1'' enchaîné — reprise T1 (27/11, 10:55 UTC →) — EN COURS
Session T1 reprise (la session de 09:09 n'avait fait que le rassemblement des journaux). data/ perdu (nouveau conteneur) : départ de zéro.
- 10:58 chain_h1b (départ au hasard, D ≤ 600) : 1 183 et 1 444 conflits au départ, 865 et 1 044 après 220 s : trop lent.
  Analyse (ancêtre commun des couples en conflit) : la plupart entre grosses branches (niveau 0–1) → problème d'encombrement.
- 11:00 init_h1.py : départ « arbre en H », D[n] = a + b·taille(n), G[n] = g0 + g1·taille(plus gros enfant) :
  (30, 20, 1, 10, 8) 680 conflits ; (30, 80, 1, 12, 30) 184 (tmax 188 532) ; (30, 160, 1, 12, 60) 141 (tmax 363 092). OBSERVÉ.
  chain_h1b.py : option MULT=1 (pas proportionnels à la valeur), DMAX / GMAX réglables. Descentes lancées 11:02 (graines 11, 12).
## R-621 Croissance de l'enchaînement par greffe — DÉMONTRÉ (comptage exact sur les arbres, grow.py)
Module à N pas de v = arbre du pas 1 de v dont chaque littéral est le module à N−1 pas (h1 : h1_tree2 réutilisable, 29 puissances).
| N | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| puissances (8 bits) | 52 | 349 | 1 766 | 7 943 | 33 720 | 139 017 | 564 634 | 2 276 011 |
| littéraux (8 bits) | 65 | 377 | 1 793 | 7 793 | 32 465 | 132 497 | 535 313 | 2 151 953 |
Matrice des usages M (M[v][w] = nombre de littéraux w/¬w dans l'arbre de v) : rayon spectral 4 (h1 s'utilise 4 fois) ; sans h1
(sous-système fermé x, y, h0, cij) : 2 (x utilise x deux fois). Donc taille ≈ C·4^N : EXPONENTIELLE, pas linéaire.
(Les arbres de R-619 pour cij'' (26) et chain_h1 pour h1'' (207) sont un peu différents de ceux comptés ici (24, 229).)
Raison : un arbre ne partage rien ; chaque usage d'un bit du pas N−1 recopie tout son module. Pour une croissance linéaire, il faut
DIFFUSER un vaisseau (porte COPIE R-609 : un choc K × x donne ¬x tout droit et deux copies de x) et l'AMENER sur la ligne voulue.
Commande : python3 grow.py 8

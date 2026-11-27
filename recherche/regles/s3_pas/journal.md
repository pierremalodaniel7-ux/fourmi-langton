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

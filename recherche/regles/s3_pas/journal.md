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

# Journal « quelle règle pour un ordinateur réutilisable ? » (nuit du 25/11, session séparée)
Numéros R-300 et suivants (à fusionner dans journal.md au matin). Moteur : `fourmi_r` = copie de `src/fourmi.c`
+ options `-x` (exactement T pas), `-dump` (état final en format situation), `-z` (arrêt quand la grille est toute blanche),
grille triangulaire `T:` (lettres R L U ; 6 caps, voir l'en-tête de fourmi_r.c). Oracle src/oracle.txt : 13/13 identiques.
Compiler : `gcc -O2 -w -o fourmi_r fourmi_r.c` (dans recherche/regles).

## R-300 La gomme : condition exacte — DÉMONTRÉ (preuve courte ci-dessous) + VÉRIFIÉ (moteur, 78/78 essais) (gomme.py, gomme2.py)
Énoncé. Une fourmi (règle K = (K_0, …, K_{q−1}), virages dans le groupe des caps Z_M, demi-tour = +M/2) a joué T pas.
On la pose sur la case qu'elle vient de quitter, cap retourné, et on la laisse jouer T pas avec la MÊME règle.
La grille revient à son état de départ POUR TOUT T ET TOUT DÉPART ⟺ q = 2 et K_1 ≡ −K_0 (mod M) (ou q = 1, trivial).
Preuve (⇐) : invariant « fourmi sur la case y, cap = inverse du cap avec lequel elle avait quitté y, case y = couleur c+1 ».
Elle lit c+1, tourne de K_{c+1}, la case passe à c+2 = c (q = 2) : la case est remise ; nouveau cap = d + K_c + M/2 + K_{c+1}
= d + M/2 (car K_0 + K_1 ≡ 0) = inverse du cap d d'arrivée sur y ⇒ elle va exactement sur la case précédente. Récurrence.
Preuve (⇒) : q ≥ 3, T = 1 depuis le blanc : la gomme lit 1 et écrit 2 ≠ 0 ⇒ échec. q = 2, K_0 + K_1 = s ≢ 0, T = 2 depuis le blanc :
la gomme efface x_1 mais part vers une case y ≠ x_0 (blanche) qu'elle noircit ⇒ 2 cases noires ⇒ échec.
Règles qui ont la gomme (non triviales) : carré RL (= LR) ; hexa (1,5) = R1L1 et (2,4) = R2L2 (+ miroirs) ; TRIANGLE RL.
Triviales : NN, UU (le mouvement ne dépend pas de la couleur). Précision sur « M pair » : sur un réseau, le demi-tour existe
toujours (on repasse par l'arête d'entrée) ; sur le triangle (3 arêtes) il existe aussi (caps dans Z_6). La vraie condition
est seulement q = 2 et « virage sur noir = inverse du virage sur blanc ».
Balayage (gomme2.py, 6 essais par règle : T au hasard 500–6 000, pairs et impairs, blanc ou 5 cases au hasard) :
q = 2 condition vraie : 13 règles, TOUJOURS ; condition fausse : 48 règles, JAMAIS 33, PARFOIS 15 (toutes à mouvement
quasi indépendant de la couleur : RR, LL, UR, H:R1R1… : coïncidence de parité, échouent pour d'autres T) ; q = 3 : 280 règles,
jamais « toujours » (8 « parfois », même cause). Données : data/gomme2.txt.
Déjà connu : la réversibilité de la fourmi de Langton (et le retour en arrière en retournant la fourmi) est classique
(modèle « flipping rotators » des gaz de Lorentz, Cohen-Wang 1995 ; cf. deja_connu.md) ; l'énoncé général « q = 2 et K_1 = −K_0 »,
hexa et triangle compris : pas cherché plus loin que ces sources (voir R-302).
Commande : `python3 gomme.py 20000 ; python3 gomme2.py`

## R-301 Effacer pour q ≥ 3 ? — DÉMONTRÉ (lemme de comptage) + OBSERVÉ (négatif, 0/9 072 essais) (gomme3.py)
Lemme : la couleur d'une case = couleur de départ + nombre de passages (mod q). Une grille revient à son état ⟺ chaque case
a été visitée un multiple de q fois. Une trace laissée par 1 passage demande donc q − 1 passages de plus SUR CHAQUE CASE.
Pour q ≥ 3 aucune fourmi de la même règle ne peut « défaire un pas » : défaire = décrémenter la couleur, or toutes les fourmis
incrémentent. Le renversé de K est la règle K̃_j = −K_{−j−1} lue avec les couleurs renommées c → −c : c'est la même règle sur la
même grille seulement si q = 2 (renommage = identité) — d'où R-300.
Reste un seul moyen général : la périodicité. Un système borné revient à son état de départ (R-44) ⇒ il efface tout, mais
« globalement » (après un cycle complet), pas à la demande.
Essais (gomme3.py) : après T = 20, 100, 1 000 pas (départ blanc), 1 effaceuse posée sur chaque case à distance ≤ 3 et chaque cap
(196 carré / 294 hexa-triangle), puis gomme + 1 2e fourmi (100 / 150), ≤ 200 000 pas, arrêt dès que la grille est blanche (-z) :
RL : 1/196 (c'est la gomme), 0 paire ; LLR, LLLR, RLLR, LLRRRL, H:R1R2, H:R1L2, H:R1R2L1, T:RLL : 0 partout.
Avec R-66 (3 autoroutes LLR sur la même voie ne lavent rien) : en q ≥ 3, PAS DE GOMME LOCALE connue. OUVERT : gomme à plusieurs fourmis
bien synchronisées (q − 1 passages exacts) — le lemme ne l'interdit pas.
Commande : `python3 gomme3.py`

## R-302 Littérature (1re passe, 25/11 00:40) — voir deja_connu.md (lignes à ajouter au matin)
3 recherches web : (1) « time-reversible generalized Langton's ant » : la réversibilité (le passé est déterminé, fourmi
« symétrique en temps », retour en arrière) est CONNUE (Gajardo et al., Algorithms 4(1) 2011 « Recognizing the repeatable
configurations of time-reversible generalized Langton's ant is PSPACE-hard » ; ci2ma pp11-28) ; condition générale sur la règle
(q = 2, K_1 = −K_0, hexa/triangle) : PAS TROUVÉE énoncée. (2) « generalized ant highways / hexagonal turmite » : LLLR a deux
autoroutes 52 et 156 (arXiv 2506.10482) — retrouvé ici (14/2 626) ; LLRRRL infinité d'autoroutes (arXiv 2505.05426) — retrouvé
(896, 992, 800, 1 088) ; rien sur les périodes hexagonales. (3) « highway collision logic gates » : rien d'autre que Gajardo-Moreira-Goles
(1 fourmi). (4) « hexagonal ant 120° glider no trace » : rien (blog scipython, Wikipedia : mention des virages ±60°/±120°).

## R-303 Départ blanc, 130 règles (carré 8, hexa q=2 et q=3 à miroir près, triangle q=2 et q=3), T = 2^22 — OBSERVÉ (scan_blanc.py)
29 autoroutes, 28 cycles (toutes à U ou triangle à U : mouvement borné), 73 indécises. Données : resumes/scan_blanc.txt.
Autoroutes depuis le blanc : RL 104 (9 977), LLR 18 (39), LLLR 52 (79), L4R 68, L5R 84, L6R 100 ; hexa q=2 : R2L2 A8 (début 2),
R2N A4, UN A3 ; hexa q=3 : R2R1R1 A25, R2L2L2 A98, R2R2L2 A25, R2UL2 A12, R2NR1 A54 (672 364), R2UL1 A1863 dans la direction (11,4) (!),
R2L2R1 A75 (1,5 M), R2R2R1 A1940 (5,1), R2L1R1 A5… Sans autoroute (2^22) : LLRRRL, RLLR, hexa R1L1, R1R2, R1L2, R2R1, R2L1, triangle RL.

## R-304 FIL : petites configurations (fourmi + 0 à 3 cases dans [-2,2]², 2 626 par règle, 2^20 pas) — OBSERVÉ (fil_petits.py)
Part qui donne une autoroute / début médian : RL 100 % / 1 869 ; LLR 100 % / 47 ; LLLR 100 % / 79 (dont 14 en A156) ; L4R 100 % / 103
(105 en A34) ; L5R 100 % / 127 ; L6R 100 % / 151 (3 en A50) ; LLRRRL 4,2 % / 270 955 (A896, A992, A800, A1088) ; RLLR 0 % ;
hexa R2L2 100 % / 2 ; R2N, UN, R2R2L2, R2L1R1 100 % / ≤ 5 ; R2UL2 98 % (48 cycles) ; R2R1R1 100 % / 1 483 ; R2L2L2 100 % / 298 ;
R2UL1 96 % / 62 990 ; R2R2R1 83 % ; R1N 8,6 % ; R2NR1 6,6 % ; R1L1, R1R2, R1L2, R2R1, R2L1 : 0 % ; triangle RL 0 % (6 cycles), RRL 0,15 %.
Résumé : resumes/fil_resume.txt.

## R-305 Germes lanceurs (autoroute dès le départ, début ≤ 2P), glouton = MAJORANT du germe minimal — OBSERVÉ (germe.py)
RL 10 cases (R-20 : 11 avec début 0 ; ici on tolère ≤ 2 périodes de mise en route) ; LLR 2 ; LLLR 4 ; L4R 4 ; L5R 4 ; L6R 3 ; LLRRRL 49 (A896) ;
hexa R2L2 1 ; R2N 1 ; UN 1 ; R2R2L2 1 ; R2UL2 1 ; R2L1R1 1 ; R2R1R1 4 ; R2L2L2 3 ; R2NR1 7 ; R1N 11 ; R2R2R1 10 ; R2UL1 36.
Fichier : resumes/germes_regles.json (fourmi en (0,0), cases, P, D).

## R-306 Le VAISSEAU hexa R2L2 (fourmi + 1 case, période 8, 1 case par période en diagonale) — DÉMONTRÉ (certificat dès t = 0)
H:R2L2 = hexa, blanc → +120°, noir → −120°. Germe : fourmi 0,0 cap 4 + case 1,0. `./fourmi_r -cert "H:R2L2|0,0,4|1,0"` → CERT 0 |V|=4.
Il ne laisse AUCUNE trace : 1 seule case non blanche dans toute la grille après 200 ou 400 périodes (trace.py) ; depuis le blanc,
4 cases au total après 10^5 pas (3 portées + 1 laissée au départ). Même chose pour H:R2UL2 (q=3, période 12, CERT 0, 0 case/période).
Toutes les autres autoroutes laissent une trace : RL 12 cases/période, LLR 2, LⁿR 6, LLRRRL 58, R2UL1 158 (trace.py, resumes/trace.txt).
Déjà connu ? Le vaisseau à 4 fourmis RL (2c/12) est connu ; un vaisseau à UNE fourmi sans trace en hexa ±120° : pas trouvé (R-302 (4)).
Remarque : avec des virages ±120° la fourmi n'utilise que 3 caps sur 6 (classe paire ou impaire) ; c'est le « bon » réseau pour une
fourmi à 3 directions — probablement connu des amateurs (HexTurmite de Golly), à vérifier avant de dire « nouveau ».

## R-307 / R-308 Déviation par obstacles fixes et réutilisation — OBSERVÉ (banc.py, miroirs.py, murs.py)
Protocole commun : germe en (0,0) ; obstacle sur la voie K = 30 périodes plus loin ; 1 case (chaque case visitée dans une période),
2 cases voisines, 1 à 3 cases dans une fenêtre 5×5 (2 625), murs de 5 à 33 cases pleins/pointillés selon chaque axe (144 à 192).
Réutilisation : une 2e autoroute identique, 10 périodes devant (elle touche l'obstacle d'abord) ; on compare la sortie de la 2e à la 1re.
RÉSULTAT PRINCIPAL : pour TOUTES les règles qui laissent une trace (RL, LLR, LⁿR, R2N, …), la 2e autoroute ne ressort JAMAIS sur la même
voie que la 1re : 0 / 2 540 (RL), 0 / 2 383 (LLR), 0 / 1 998 (LLLR), 0 / 2 140 (L4R), 0 / 2 050 (R2N), murs : 0 partout.
(Elle ressort parfois dans la même direction : RL 549, LLR 894, R2N 2 050 sur 2 050 — mais décalée.) Cause : la 2e roule sur la trace de la
1re et est déviée AVANT d'atteindre l'obstacle (LLR : comme R-66). ⇒ en RL et LⁿR un fil n'est pas réutilisable tel quel.
Hexa R2L2 : aucun obstacle fixe ne le dévie (2 625 + 144 murs : il passe toujours dans la même direction ; 272 obstacles le DÉCALENT
d'une voie) ; ces décaleurs sont réutilisables : 272 / 272 avec 10 périodes d'écart (102 / 272 à 3 périodes : les 2 vaisseaux se gênent).
Fichiers : data/banc_*.json, data/miroirs_*.json, data/murs_*.json (non versionnés), résumés dans resumes/.

## R-310 Chocs de 2 vaisseaux R2L2 — OBSERVÉ (collisions.py, 1 215 chocs : 5 angles × 3 instants × 81 décalages)
AUCUN choc ne détruit un vaisseau : 0 / 1 215 « autre » ; transparents 791, décalés 46 (face à face), déviés 337, fusion en
vaisseau double (A8 × 2) 41. Types de déviation (angle d'arrivée r, sortie B, sortie A) : (60°, −120°, +120°) 54, (60°, +120°, −120°) 27,
(60°, 0, +120°) 27 [B continue, A tourne], (120°, ±120°) 54, (240°…) 67, (300°…) 108. C'est la « porte d'interaction » des boules de billard
(Fredkin-Toffoli 1982) : si A et B sont là, ils tournent ; si un seul est là, il continue tout droit.

## R-311 Gomme COLLECTIVE : remise à zéro exacte d'un circuit entier — DÉMONTRÉ (même preuve que R-300) + VÉRIFIÉ (gomme_collective.py)
Avec n fourmis jouées l'une après l'autre : retourner chaque fourmi (case qu'elle vient de quitter, cap inversé) ET inverser l'ordre de jeu.
Preuve : la suite des pas élémentaires est défaite dans l'ordre inverse ; chaque pas défait est un pas de gomme (R-300), la grille étant
exactement celle qui suivait ce pas. VÉRIFIÉ : les 28 portes RL d'ordinateur/germes_ordinateur_2026-11-17.json (NON, NOR, ET, COPIE, OU,
CROISEMENT, demi-additionneur, toutes entrées), 3 000 et 20 000 tours : 56/56 remises à zéro exactes ; l'ADDITIONNEUR 4 BITS
(recherche/ordinateur/germe_ordinateur.json, 8 fourmis, 140 cases) après 420 000 tours (toutes les lectures faites, 383 972 cases changées) :
remis à zéro, 0 case différente. Situations au hasard (2 à 6 fourmis) : RL 40/40, H:R2L2 40/40, T:RL 40/40, H:R1L1 40/40 ; LLR 0/40, H:R1R2 0/40.
⇒ En RL (et R2L2) un ordinateur À USAGE UNIQUE devient RÉUTILISABLE : calculer, lire, tout retourner, attendre le même temps → état initial,
on change les entrées, on recommence. Défaut : le retournement est une intervention extérieure (on retourne les fourmis à la main) ;
en interne, seule la navette (R-19) fait un retour qui efface sa trace. Impossible pour q ≥ 3 (R-301).

## R-312 Objets fixes (cycles exacts à 2 fourmis, [-3,3]² + 0/1 case) — OBSERVÉ (cycles2.py)
H:R2L2 : 772 cycles / 44 928 (périodes 3, 12, 15, 18, 21, 24, 27, 30, 54 ; période 3 : « H:R2L2|0,0,0;-1,0,3|-1,0 ») ; RL : 8 864 / 19 968
(périodes 4 à 64…, cf. R-02/R-28). (LLR : R-52, pas de cycle court.)

## R-313 Miroirs-oscillateurs R2L2 (9 oscillateurs × 49 places) — OBSERVÉ (osc_miroir.py)
Le vaisseau traverse 235 fois, tourne de ±120° 153 fois mais l'oscillateur est alors presque toujours détruit (ses 2 fourmis partent en
vaisseaux) ; 10 déviations propres avec oscillateur intact ; une 2e vaisseau 10, 60 ou 3 780 périodes derrière n'est JAMAIS dévié pareil
(l'oscillateur a changé d'état). ⇒ pas de miroir fixe réutilisable trouvé en R2L2. OUVERT : miroir à 3 fourmis ou plus, « rail » de vaisseaux.

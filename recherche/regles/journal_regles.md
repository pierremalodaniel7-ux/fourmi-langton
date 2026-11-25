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

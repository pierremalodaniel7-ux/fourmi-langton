# La boucle : ce que les théorèmes interdisent et permettent (hexa R2L2, 26/11 jour, R-347)

Cadre : grille hexagonale, R2L2 (blanc → +120°, noir → −120°), fourmis jouées l'une après l'autre, configuration FINIE
(nombre fini de fourmis et de cases noires). Un « vaisseau » = 1 fourmi + 1 case (R-306). Un « objet » = un oscillateur
(paire de fourmis en orbite, etc.). Tout ce qui suit est démontré en quelques lignes ; les statuts sont indiqués.

## Interdit
**T0 — pas de canon (horloge qui émet sans fin).** Le nombre de fourmis ne change jamais et chaque vaisseau EST une fourmi.
Un objet de n fourmis émet au plus n vaisseaux qui partent pour toujours. DÉMONTRÉ (évident).
⇒ « une horloge qui envoie un top toutes les P périodes, indéfiniment » est impossible ; une horloge ne peut que
TOURNER sur place, ou échanger : un vaisseau entre, un vaisseau sort.

**T1 — borné ⇒ périodique (dans les deux sens du temps).** La règle est réversible (gomme collective, R-311). Si tout reste dans une
région bornée pour t ≥ 0, il n'y a qu'un nombre fini d'états, donc l'orbite repasse par un état ; réversible ⇒ l'orbite est un cycle
pur, donc elle était aussi bornée dans le passé. DÉMONTRÉ.

**T2 — pas de capture (McGinnis-Webb 2019, Thm 3 ; notre R-340).** Passé non borné ⇒ futur non borné : un vaisseau venu de l'infini ne
peut pas être retenu pour toujours, il faut que « quelque chose reparte ». Version contraposée de T1. DÉMONTRÉ.
⇒ on ne peut pas « charger » une boucle avec un seul vaisseau sans qu'un vaisseau ressorte (prix : au moins 1 fourmi perdue).

**T3 — un relais qui dévie en restant lui-même est impossible (R-331, généralisé ici).** Soit D un objet borné qui, à chaque passage,
reçoit un vaisseau de direction r et émet un vaisseau de direction r', et qui redevient lui-même (à translation et phase près) après
k passages. Deux quantités se conservent (R-331) : (I1) le nombre de fourmis de chaque classe de caps (pairs / impairs) ; (I2)
Q = (cases noires) − Σ⌊cap/2⌋ mod 3, additive, constante le long d'une orbite, et valant pour un vaisseau Q(r) = 2, 2, 1, 1, 0, 0 (r = 0…5).
Sur k passages, D gagne k·(classe(r) − classe(r')) fourmis d'une classe et k·(Q(r) − Q(r')) en Q ; revenu à lui-même il ne gagne rien, donc
 – classe(r') = classe(r) : déviations de 60°, 180°, 300° IMPOSSIBLES (pour tout k) ;
 – k·(Q(r) − Q(r')) ≡ 0 (mod 3) : pour r' = r ± 2 (déviation ±120°), Q change de ±1, donc **3 divise k**.
DÉMONTRÉ. Cas k = 1 (relais qui reste exactement lui-même, la consigne (a)) : aucune déviation possible — c'est R-331.
Cas k = 2 (relais « bascule » qui alterne deux états) : impossible aussi. Le premier cas permis : un relais à **3 états**
R0 → R1 → R2 → R0 qui dévie de ±120° à chaque passage.

**T4 — circuit fermé (horloge à vaisseau qui tourne).** Un vaisseau qui fait le tour d'un circuit fixe de m relais, indéfiniment,
avec tout borné : par T1 c'est un grand oscillateur ; chaque relais reçoit toujours la même direction, donc T3 s'applique à chacun.
Conséquences (DÉMONTRÉ) : toutes les directions du circuit sont de la même classe ({0, 2, 4} ou {1, 3, 5}) ; chaque virage vaut ±120° ;
pas de « ping-pong » (aller-retour à 180°) ; chaque relais a un nombre d'états multiple de 3 ; le plus petit circuit est un TRIANGLE
de 3 relais à 3 états (directions 0 → 2 → 4 → 0) ; le tout revient à son état de départ au bout de 3 tours (au moins).

## Permis (pas interdit par ces théorèmes) — donc à chercher
- un relais à 3 états (OUVERT : recherche § R-348) ;
- un triangle de 3 relais = horloge (OUVERT) ;
- des virages « payés » par des vaisseaux constants (comme dans le demi-additionneur) : chaque virage coûte 1 fourmi qui part ;
  une boucle de n virages coûte donc n fourmis, d'où « horloge à n tours avec ≈ 3n fourmis » (borne facile, voir R-349) ;
- tout oscillateur est déjà une « boucle » au sens faible (2 fourmis qui tournent : M, période 21) ; ce que T3 interdit, c'est une boucle
  faite de relais IMMOBILES qui renvoient un vaisseau libre.

## Ce que ça veut dire pour l'ordinateur
Sans relais, un signal ne repasse jamais au même endroit sauf si on le « relance » avec un vaisseau neuf à chaque virage :
le calcul R2L2 est « en avant » (les entrées et les constantes viennent de l'infini et repartent à l'infini), comme un circuit
combinatoire déplié dans le temps. La mémoire (R-335, R-341) existe parce qu'un objet peut CHANGER (T3 n'interdit que l'objet qui reste
le même) ; une horloge interne exige un relais à 3 états.

## Résultats de la recherche (26/11 jour, R-348, R-349b)
- **Relais à 3 états : 0** (2 fourmis : 4 398 déviations ±120°, 262 chaînes à 2 pas, 0 retour ; 3 fourmis : 0). OBSERVÉ (négatif).
- **Horloges sans miroir : OUI, avec 6 fourmis.** Six vaisseaux disposés avec une symétrie d'ordre 3 (2 « générateurs » tournés de
  120° et 240°) qui partent loin, se relancent les uns les autres par chocs et reviennent EXACTEMENT à leur état de départ.
  Famille observée : période P = 2 322 + 2 736 n, rayon 22 + 32 n, pour n = 0, 1, 2, 3, 4 (P = 2 322 … 13 266, l'orbite s'éloigne
  jusqu'à 150 cases du centre) ; retour exact VÉRIFIÉ par 2 moteurs (CYCLE de fourmi_r = preuve par réversibilité que c'est périodique
  pour toujours ; hx.py). Vols libres jusqu'à 426 pas (≈ 53 cases) entre deux chocs. 4 vaisseaux (symétrie 2) : au mieux P = 36 ;
  3 vaisseaux (symétries 2, 3, 6, rayon 10) : 0 cycle. Ce n'est pas un circuit de relais fixes (T3 les rend très contraints) mais une
  « boucle dynamique » : chaque vaisseau est relancé par un autre vaisseau qui revient lui aussi. Famille infinie : OUVERT (5 termes).

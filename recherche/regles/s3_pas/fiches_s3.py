#!/usr/bin/env python3
"""Fiches du bestiaire n° 30 (S3) et germes : catalogue À PART (catalogue_s3.json), germes_2026-11-27_s3.json.
Usage : python3 fiches_s3.py   puis   python3 ../../../outils/mkbestiaires.py 30 "…" --catalogue catalogue_s3.json"""
import json
from step import Step, load_params, build
from nor import Layout
from s3lib import parse
E = dict(c00=1, c10=0, c01=1, c11=0, x=1, y=0, h1=1, h0=0)     # un état parmi les 256
def fiche(id_, nom, s, T, zoom, **kw):
    _, a, c = s.split('|')[:3]
    d = dict(id=id_, b=30, classe='Règles/Hexa R2L2/s3_pas', nom=nom, regle='H:R2L2', fourmis=a, points=c, img=[T, zoom])
    d.update(kw); return d
P = load_params(); P['h1'] = json.load(open('h1_param_simple.json'))
off8 = {'h0': (0, 0), 'x': (-3799, 3325), 'y': (-4967, -1821), 'c00': (-4069, 2117), 'c10': (1364, 1737), 'c01': (4675, 219),
        'c11': (-2561, -4463), 'h1': (-801, 3854)}
S8 = Step(P, off8); L1 = S8.L['h1']
fiches = [
 fiche('R-615', "Le pas complet de la petite fourmi (tore 2×2) en UN germe R2L2 : 8 modules, 256/256 états", S8.sit(E), 0, 'zoom -6600,-6000,6600,7000',
       situation="8 modules NOR (h0', x', y', c00'..c11', h1') translatés dans un seul germe ; un vaisseau par littéral vrai de l'état (ici c00=1 c01=1 x=1 h1=1).",
       deroulement="Chaque module calcule un bit du pas suivant par chocs déviants à 60° (et de face pour h1') ; à la fin, une sortie par bit qui vaut 1.",
       mesures="256/256 états propres et justes (moteur C, 11 s) ; hx.py 256/256 états finaux identiques (54 s).",
       statut="VÉRIFIÉ (2 moteurs, tous les états, 1 usage) ; réutilisation : OUVERT (h1' non réutilisable, voir R-614)",
       interet="Premier pas complet d'une fourmi simulé par une autre fourmi (R2L2), en un seul germe, exhaustivement vérifié.",
       deja="Pas trouvé (cf. deja_connu_regles.md : calcul par chocs en R2L2 non décrit).", source='recherche/regles/s3_pas/journal.md (27/11, R-615)',
       commande='NOLANES=1 BOX=6000 python3 recherche/regles/s3_pas/step.py 1 3 step8_simple.json h1_param_simple.json'),
 fiche('R-614', "Module h1' = h1 ⊕ h0 ⊕ c (case lue) : arbre NOR avec chocs DE FACE, 256/256", L1.sit(E), 0, None,
       situation="27 puissances, 32 littéraux (59 vaisseaux) ; règle de côtés : après « + » seulement + ou face, après « − » seulement − ou face.",
       deroulement="Avec les seuls chocs à 60° c'est impossible (R-613, démontré) ; les chocs de face permettent de brancher l'arbre.",
       mesures="256/256 justes et propres, 2 moteurs (49 s) ; tmax 12 356 pas.",
       statut="VÉRIFIÉ (1 usage) ; réutilisable : NON (voie de l'enfant de face = voie du parent)",
       interet="Contourne une limite démontrée du compilateur (pas de XOR à 3 entrées avec les côtés ±).", deja="Pas trouvé.",
       source='recherche/regles/s3_pas/journal.md (R-610, R-613, R-614)', commande='python3 recherche/regles/s3_pas/opt7.py h1H 1 780'),
]
S7 = Step(P, {'h0': (0, 0), 'x': (77, 222), 'y': (-1335, -440), 'c00': (594, 490), 'c10': (1388, 965), 'c01': (-899, -230), 'c11': (-1198, 1301)},
          names=['h0', 'x', 'y', 'c00', 'c10', 'c01', 'c11'])
fiches.append(fiche('R-611', "7 bits sur 8 du pas en un germe RÉUTILISABLE : certificat, 10 usages au même endroit", S7.sit(E), 0, 'zoom -1500,-700,1600,1500',
       situation="Modules h0', x', y', c00'..c11' translatés (voies opposées ≥ 7 entre modules, rayons ≥ 7).",
       deroulement="Usage u = le même germe retardé de u·Δ ; Δ = 74 072 pas (certificat R-606).",
       mesures="256/256 (2 moteurs) ; certificat OK ; 10 usages au hasard : superposition exacte, 10/10 justes, 2 moteurs identiques.",
       statut="VÉRIFIÉ (10 usages) ; tout nombre d'usages DÉMONTRÉ (certificat)", interet="Réutilisation indéfinie du calcul de 7 bits.",
       deja="Pas trouvé.", source='recherche/regles/s3_pas/journal.md (R-615)', commande='python3 recherche/regles/s3_pas/step.py 0 10 (sans h1)'))
for f in fiches:
    if f['img'][1] is None: f['img'] = [0]
json.dump(fiches, open('catalogue_s3.json', 'w'), ensure_ascii=False, indent=1)
json.dump([dict(dossier='Règles/Hexa R2L2/s3_pas', nom=f['nom'], regle=f['regle'], fourmis=f['fourmis'], points=f['points'], note=f['mesures'] + ' — ' + f['statut'])
           for f in fiches], open('germes_2026-11-27_s3.json', 'w'), ensure_ascii=False, indent=1)
print(len(fiches), 'fiches', [len(f['fourmis'].split(';')) for f in fiches], 'fourmis')

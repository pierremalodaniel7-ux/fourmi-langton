#!/usr/bin/env python3
"""S1 : catalogue À PART (s1_fusion/catalogue_s1.json, bestiaire n° 28) et germes (germes_2026-11-27_s1.json) depuis les JSON de résultats.
Puis : python3 ../../outils/mkbestiaires.py 28 "<titre>" --catalogue s1_fusion/catalogue_s1.json --sortie ...
Usage : python3 s1_fusion/mk28.py   (depuis recherche/regles/)"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
def split(s):
    _, a, c = s.split('|'); return a, c
F = json.load(open(os.path.join(HERE, 'fusion_verif.json')))[0]
A = json.load(open(os.path.join(HERE, 'add2_final.json')))
cert = A.get('certificat')
cert_txt = ('certificat fin OK pour %d écarts (distance min entre usages, non libres : %s)' % (len(cert['par_ecart']), ', '.join(str(p[1]) for p in cert['par_ecart']))
            if cert and cert['ok'] else 'certificat : en cours / non conclu')
CL = 'Règles/Hexa R2L2/s1_fusion'
fiches = []
a, c = split(F['un_usage']['(1, 0)'])
fiches.append(dict(id='R-403', b='28', classe=CL, nom='Fusion propre et réutilisable : deux signaux exclusifs ressortent sur LA MÊME route (2 vaisseaux constants)',
    regle='H:R2L2', fourmis=a, points=c, img=[700, ''],
    situation='Constants K « −85,85,4 » et Kp « 91,−7,2 » ; entrée s1 (direction 1) présente, s2 (direction 2) absente. Ordre de jeu Kp, s1, s2, K.',
    deroulement="s1 seul ou s2 seul : il ressort un vaisseau O (direction 2, voie 1) sur EXACTEMENT la même trajectoire ; rien : K et Kp continuent. Image : pendant le choc.",
    mesures='3 cas justes, 2 moteurs ; 2 usages 9/9 ; 20 usages (5 suites) 20/20 en superposition exacte ; certificat : distance entre usages ≥ 7.',
    statut='VÉRIFIÉ (2 moteurs, 20 usages) ; tout nombre d\'usages DÉMONTRÉ (certificat)',
    interet="Un « OU » de signaux exclusifs qui se réutilise : brique pour regrouper des retenues.",
    deja='Pas trouvé (fusions de signaux en automates : Golly / jeu de la vie, autre modèle).',
    source='recherche/regles/s1_fusion/journal.md (R-403)', commande='python3 s1_fusion/fusion_final.py s1_fusion/fusion3_122_0_2.json 0 10'))
for cas, img, nom in (('1111', 900, 'ADDITIONNEUR 2 BITS RÉUTILISABLE (8 pièces) : 3 + 3 = 6'), ('0111', 900, 'Additionneur 2 bits R-405 : 2 + 3 = 5 (routes qui se croisent)')):
    a, c = split(A['un_usage'][cas])
    fiches.append(dict(id='R-405' if cas == '1111' else 'R-406', b='28', classe=CL, nom=nom, regle='H:R2L2', fourmis=a, points=c, img=[img, ''],
        situation='Demi-additionneur R-337 (a0, b0) + additionneur complet R-349 posé pour que sa pièce A suive exactement la retenue c0 (D = 20). Cas a0 b0 a1 b1 = ' + cas + '.',
        deroulement="La retenue c0 entre dans l'étage 1 par l'entrée A (a + b + c est symétrique) ; le bloc HA0 joue au rang de A. Les routes des deux étages se croisent (50 paires à distance ≥ 2).",
        mesures='16/16 justes, 2 moteurs ; 2 usages 256/256 ; 20 usages (graines 0, 1, 2, 20 × 1111, alterné) 20/20, superposition exacte, 2 moteurs ; ' + cert_txt + '.',
        statut='VÉRIFIÉ (2 moteurs, 20 usages)' + ('; tout nombre d\'usages DÉMONTRÉ (certificat fin)' if cert and cert['ok'] else '; tout nombre d\'usages OUVERT'),
        interet='Premier additionneur 2 bits réutilisable au même endroit en R2L2 sans aucune case fixe (R-350 avait échoué).',
        deja='Pas trouvé (circuits à fourmis : Gajardo-Moreira-Goles 2002, autre construction, non réutilisable au même endroit).',
        source='recherche/regles/s1_fusion/journal.md (R-405, R-406)', commande='python3 s1_fusion/add2_final.py 20 5'))
json.dump(fiches, open(os.path.join(HERE, 'catalogue_s1.json'), 'w'), ensure_ascii=False, indent=1)
germes = [dict(dossier=CL, nom=f['id'] + ' — ' + f['nom'], regle=f['regle'], fourmis=f['fourmis'], points=f['points'], note=f['statut'] + ' ; ' + f['commande'])
          for f in fiches]
germes += [dict(dossier=CL, nom='R-405 additionneur 2 bits, cas ' + k, regle='H:R2L2', fourmis=split(s)[0], points=split(s)[1],
                note='a0 b0 a1 b1 = ' + k + ' ; un usage ; sorties : ' + json.dumps(A['sorties'])) for k, s in sorted(A['un_usage'].items())]
json.dump(germes, open(os.path.join(HERE, 'germes_2026-11-27_s1.json'), 'w'), ensure_ascii=False, indent=1)
print(len(fiches), 'fiches,', len(germes), 'germes')

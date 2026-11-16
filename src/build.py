# build.py — bêtes de la nuit du 16/11 : vérifie chaque situation avec les programmes C, fabrique les germes,
# puis écrit catalogue_nuit.json (bestiaire 5), germes_nuit.json (simulateur) et resultats_nuit.csv (tableau trié).
import subprocess, json, re, csv
def sh(*a, t=900): return subprocess.run(list(a), capture_output=True, text=True, timeout=t).stdout
def F(n): return format(n, ',').replace(',', ' ')
def norm(s): return ' ; '.join(x.strip() for x in s.replace(' ', '').split(';') if x.strip())
def analyse(f, c, T=2000000):
    out = sh('./exploreY', 'Y', '1', '1', str(T), f.replace(' ', ''), c.replace(' ', ''))
    a = [l for l in out.splitlines() if l.startswith('ANALYSE')][0]
    d = dict(re.findall(r'(\w+)=([^ []+)', a))
    fa = re.search(r'fourmis_a_cet_instant=(.*?)  noires', a).group(1).strip().rstrip(';').strip()
    na = re.search(r'noires_a_cet_instant=(\S*)', a); na = na.group(1).rstrip(';') if na else ''
    sig = [l for l in out.splitlines() if l.startswith('X|')][0].split('|')[1]
    return {'P': int(d['P']), 'cases': int(d['cases_du_cycle']), 'boite': d['boite'], 'nmin': int(d['noires_min']), 'nmax': int(d['noires_max']),
            'comp': int(d['composantes']), 'germe_f': norm(fa), 'germe_p': norm(na.replace(';', ' ; ')), 'sig': sig}
def cyc_exact(f, c, T=2000000):
    sig = sh('./explore3', 'X', '1', '1', str(T), f.replace(' ', ''), c.replace(' ', '')).split('|')[1]
    m = re.match(r'CYC(\d+) P=(\d+)', sig); return int(m.group(2)) if m else None
B = []; GERMES = []; ROWS = []
def add(**k): B.append(k)
def germe(dossier, nom, f, p, note): GERMES.append({'dossier': 'Nuit du 16-11/' + dossier, 'nom': nom, 'regle': 'RL', 'fourmis': norm(f), 'points': norm(p), 'note': note})
def row(n, k, quoi, P, f, p, statut): ROWS.append([n, k, quoi, P, norm(f), norm(p), statut])

# ---------- 1. Plus petits cycles ----------
CL1 = 'Plus petits cycles (grille préparée)'
f, p = '-1,-1,H ; 0,0,D', '0,0'; a = analyse(f, p); assert a['P'] == 4
o = sh('./explore3', 'X', '1', '1', '200000', '-1,-1,D;2,0,B;-1,0,H').split('|')[1]
add(id='Z-4', classe=CL1, nom='Le Tourniquet', fourmis=f, points=p, img=[4, 'cycle'],
    situation="Deux fourmis dans un carré 2×2 et une seule case noire.",
    deroulement="Les deux fourmis tournent autour du carré en se croisant (elles partagent parfois la même case) et tout revient à l'identique au bout de 4 pas. Il apparaît aussi tout seul : avec 3 fourmis sur grille blanche (-1,-1,D ; 2,0,B ; -1,0,H), une fourmi part en autoroute 104 et les deux autres se figent en Tourniquet vers le pas 49 700.",
    mesures="Cycle exact de période 4 ; 4 cases ; 1 case noire en permanence.",
    interet="Plus petit cycle possible : toutes les périodes sont des multiples de 4 (R-03) et une fourmi seule ne revient jamais (Cohen-Kong). Sur grille blanche, le plus petit cycle à 2 fourmis fait 16 pas.",
    statut='PROUVÉ (cycle exact ; minimalité par R-03)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-28)')
germe('Plus petits cycles', 'Tourniquet (période 4)', f, p, 'Cycle exact 4 pas, 2 fourmis + 1 case. Minimum possible (R-03).')
germe('Plus petits cycles', 'Tourniquet spontané (3 fourmis)', '-1,-1,D ; 2,0,B ; -1,0,H', '', 'Une fourmi part (104), les deux autres forment un Tourniquet (nid de période 4) vers le pas 49 700.')
row(2, 1, 'cycle minimal (Tourniquet)', 4, f, p, 'PROUVÉ'); row(3, 0, 'nid de période 4 (Tourniquet spontané)', 4, '-1,-1,D ; 2,0,B ; -1,0,H', '', 'VÉRIFIÉ')

f, p = '2,-2,H ; 1,-1,D ; 0,-1,B ; 0,-2,H', '1,0 ; 1,-2 ; 1,-1 ; 2,-2 ; 0,0 ; 0,-3 ; 1,-3'; a = analyse(f, p); assert a['P'] == 8
add(id='Z-8', classe=CL1, nom='Le Rouage', fourmis=f, points=p, img=[8, 'cycle'],
    situation="Quatre fourmis serrées dans un carré 4×4 avec 7 cases noires.",
    deroulement="Les quatre fourmis s'engrènent comme des dents de roue (jusqu'à trois sur la même case) et reviennent à l'état de départ tous les 8 pas. Il naît aussi tout seul : 5 fourmis sur grille blanche (1,0,D ; 1,-2,H ; 1,-1,G ; -2,0,B ; -1,2,G) ; la fourmi 4 part en autoroute 104 et les quatre autres sont figées en Rouage.",
    mesures=f"Cycle exact de période 8 ; {a['cases']} cases ; entre {a['nmin']} et {a['nmax']} cases noires.",
    interet="Plus petit cycle à 4 fourmis trouvé ; d'une seule pièce (on ne peut pas le couper en deux cycles de 2 fourmis).",
    statut='VÉRIFIÉ (cycle exact)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-29)')
germe('Plus petits cycles', 'Rouage (période 8)', f, p, 'Cycle exact 8 pas, 4 fourmis + 7 cases.')
germe('Nids', 'Rouage spontané (5 fourmis)', '1,0,D ; 1,-2,H ; 1,-1,G ; -2,0,B ; -1,2,G', '', 'La fourmi 4 part (104) ; les 4 autres forment le Rouage (période 8) — vérifié sans retirer de fourmi.')
row(4, 7, 'cycle 8 (Rouage)', 8, f, p, 'VÉRIFIÉ'); row(5, 0, 'nid à 4 fourmis de période 8 (Rouage spontané)', 8, '1,0,D ; 1,-2,H ; 1,-1,G ; -2,0,B ; -1,2,G', '', 'VÉRIFIÉ')

for (i, nom, f, p) in [('Z-8b', 'Le Petit Grain', '-1,-2,D ; -2,-1,H', '-2,-2'), ('Z-79552', 'Le Grand Grain', '0,-3,B ; 1,2,G', '-1,0')]:
    a = analyse(f, p); P = a['P']
    add(id=i, classe=CL1, nom=nom, fourmis=f, points=p, img=[P, 'cycle'],
        situation="Deux fourmis et une seule case noire.",
        deroulement=f"Les deux fourmis construisent puis défont une figure et reviennent exactement au départ, case noire comprise, au bout de {F(P)} pas. Pendant tout le cycle il reste au moins {a['nmin']} case(s) noire(s) : ce cycle ne passe jamais par une grille blanche, il n'existe donc pas sans la case.",
        mesures=f"Cycle exact de période {F(P)} ; {F(a['cases'])} cases ; boîte {a['boite']} ; de {a['nmin']} à {F(a['nmax'])} cases noires.",
        interet=("Deuxième plus petit cycle à 2 fourmis + 1 case (après le Tourniquet) ; boîte 3×3." if P == 8 else "Record de nos tirages pour 2 fourmis + 1 case : un seul grain de sable suffit à fermer un cycle de près de 80 000 pas.") + " Avec 2 fourmis + 1 seule case, nos tirages ont donné 1 479 périodes de cycle différentes.",
        statut='VÉRIFIÉ (cycle exact)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-30)')
    germe('Cycles 2 fourmis + 1 case', f'{nom} (période {P})', f, p, f'Cycle exact {P} pas ; ne passe jamais par une grille blanche.')
    row(2, 1, f'cycle à 1 case ({nom})', P, f, p, 'VÉRIFIÉ')

# ---------- 2. Nids ----------
CL2 = 'Nids : cycles laissés derrière une autoroute'
for (i, nom, orig, nf, T1, txt) in [
    ('N2-272580', 'Le Grand Nid', '1,0,G ; -1,2,H ; 0,-2,G', 2, 105322, "3 fourmis serrées sur grille blanche. La fourmi 3 part en autoroute 104 au bout d'environ 55 000 pas ; les fourmis 1 et 2 restent et tournent dans les débris."),
    ('N4-332792', 'Le Nid à quatre', '1,-1,G ; 2,2,D ; 0,-1,G ; 0,-2,H ; -2,-2,B', 4, 66918, "5 fourmis sur grille blanche. La fourmi 3 part en autoroute 104 ; les quatre autres restent ensemble."),
    ('N8-15792', 'Le Nid à huit', '-3,1,H ; 3,0,G ; -1,-2,H ; -1,-3,D ; 0,3,H ; 2,-1,D ; 3,-1,B ; -3,0,D ; 1,2,B ; 1,3,G ; 0,-3,B ; -2,1,G', 8, 52108, "12 fourmis placées avec une symétrie d'ordre 4 (rotation d'un quart de tour). Quatre fourmis partent ensemble dans les quatre directions ; les huit autres restent.")]:
    a = analyse(orig, '')
    assert cyc_exact(a['germe_f'], a['germe_p'], 3*a['P']+10) == a['P'], ('germe', i)
    add(id=i, classe=CL2, nom=nom, fourmis=a['germe_f'], points=a['germe_p'], img=[a['P'], 'cycle'],
        situation=txt + f" La situation affichée est un instant du nid ({nf} fourmis + {F(a['nmin'])} cases noires), qui rejoue le cycle dès le pas 0.",
        deroulement=f"Après le départ, les {nf} fourmis restantes reviennent exactement au même état tous les {F(a['P'])} pas. Il reste toujours au moins {F(a['nmin'])} cases noires : le nid a besoin des débris laissés au début, il n'existe pas sur grille blanche.",
        mesures=f"Nid de période {F(a['P'])} ; {F(a['cases'])} cases ; boîte {a['boite']} ; {F(a['nmin'])} à {F(a['nmax'])} cases noires.",
        interet=("Record de nos 400 000 tirages à 3 fourmis. " if nf == 2 else "") + "Les nids sont la règle, pas l'exception : 51 % des situations à 3 fourmis finissent ainsi (R-26). Un nid a toujours autant de fourmis de chaque classe de parité, comme les cycles (R-14) : jamais de nid à 3, 5 ou 7 fourmis.",
        statut='VÉRIFIÉ (retour exact, et revérifié sans retirer la fourmi partie)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-26)')
    germe('Nids', f'{nom} — départ ({len(orig.split(";"))} fourmis)', orig, '', f'Nid de {nf} fourmis, période {a["P"]}.')
    germe('Nids', f'{nom} — le nid seul', a['germe_f'], a['germe_p'], f'Cycle exact {a["P"]} pas dès le pas 0.')
    row(len(orig.split(';')), 0, f'nid de {nf} fourmis ({nom})', a['P'], orig, '', 'VÉRIFIÉ')

# ---------- 3. Cycles de groupe, grille blanche ----------
CL3 = 'Cycles de groupe sur grille blanche'
for (i, nom, f, sit, inter) in [
    ('C4-56296', 'Le Métronome', '-1,-3,D ; 5,3,G ; -1,5,H ; 2,-5,G', "4 fourmis dispersées dans un carré 11×11.", "Cycle très « serré » : plus de 240 pas par case touchée (le Grand Quatuor, 68 000 pas, s'étale bien plus)."),
    ('C4-57924', 'La Double Navette', '-1,-1,D ; 1,2,G ; 2,-1,G ; -2,2,D', "4 fourmis disposées symétriquement (demi-tour autour du centre).", "Navette SANS case noire (question ouverte R-23) : deux paires partent en sens opposés sur une autoroute 104 jusqu'à ~450 cases, la seconde paire les rattrape à grande vitesse sur la trace, et tout revient au centre. Famille : portées de ~150 à ~650 cases trouvées (symétrie de demi-tour)."),
    ('C4-88828', 'La Grande Double Navette', '5,-1,G ; 0,1,D ; -5,2,D ; 0,0,G', "4 fourmis symétriques par demi-tour, plus écartées.", "Plus grande double navette trouvée : la figure s'étend sur ~1 300 cases avant de revenir."),
    ('C6-1848', 'Le Sextuor', '0,1,D ; -1,2,H ; -3,-2,D ; 3,-1,B ; -1,-3,D ; 3,1,G', "6 fourmis au hasard dans un carré 7×7.", "Premier cycle à 6 fourmis d'une seule pièce trouvé par tirage au hasard (13 types sur 55 000 tirages)."),
    ('C8-16', 'La Petite Rosace', '-2,-3,H ; 1,1,H ; 3,-2,D ; -1,1,D ; 2,3,B ; -1,-1,B ; -3,2,G ; 1,-1,G', "8 fourmis avec une symétrie d'ordre 4.", "Cycle à 8 fourmis le plus fréquent (743 tirages) : 16 pas seulement."),
    ('C8-6504', 'La Rosace à huit', '-2,3,D ; -2,2,B ; -3,-2,B ; -2,-2,G ; 2,-3,G ; 2,-2,H ; 3,2,H ; 2,2,D', "8 fourmis avec une symétrie d'ordre 4.", "La symétrie de rotation est conservée tout le long du cycle."),
    ('C12-2112', 'La Rosace à douze', '0,-2,B ; 1,-3,D ; -2,-1,G ; 2,0,G ; 3,1,B ; 1,-2,H ; 0,2,H ; -1,3,G ; 2,1,D ; -2,0,D ; -3,-1,H ; -1,2,B', "12 fourmis avec une symétrie d'ordre 4.", "Plus grand nombre de fourmis dans un cycle exact chez nous.")]:
    P = cyc_exact(f, ''); a = analyse(f, '')
    assert P == a['P'] and a['comp'] == 1, (i, P, a)
    n = len(f.split(';'))
    add(id=i, classe=CL3, nom=nom, fourmis=f, points='', img=[P, 'cycle'], situation=sit,
        deroulement=f"Les {n} fourmis interagissent puis reviennent toutes, en même temps, à leur position et à leur cap de départ sur une grille redevenue blanche, au bout de {F(P)} pas.",
        mesures=f"Cycle exact de période {F(P)} ; {F(a['cases'])} cases ; boîte {a['boite']} ; jusqu'à {F(a['nmax'])} cases noires.",
        interet=inter, statut='VÉRIFIÉ (cycle exact)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-31)')
    germe('Cycles de groupe', f'{nom} (période {P})', f, '', f'Cycle exact {P} pas, {n} fourmis, grille blanche.')
    row(n, 0, f'cycle ({nom})', P, f, '', 'VÉRIFIÉ')

# ---------- 4. Cycles symétriques avec cases ----------
CL4 = 'Cycles symétriques avec cases noires'
for (i, nom, f, p) in [('S4-265776', 'Le Moulin', '0,4,G ; -4,0,H ; 0,-4,D ; 4,0,B', '-1,2 ; 2,2 ; -2,-1 ; -2,2 ; 1,-2 ; -2,-2 ; 2,1 ; 2,-2'),
                       ('S8-287536', 'La Grande Rosace', '0,2,B ; -3,-2,D ; -2,0,G ; 2,-3,B ; 0,-2,H ; 3,2,G ; 2,0,D ; -2,3,H', '1,3 ; -3,1 ; -1,-3 ; 3,-1')]:
    P = cyc_exact(f, p); a = analyse(f, p); n = len(f.split(';'))
    add(id=i, classe=CL4, nom=nom, fourmis=f, points=p, img=[P, 'cycle'],
        situation=f"{n} fourmis et {len(p.split(';'))} cases noires, le tout invariant par quart de tour.",
        deroulement=f"La figure grandit en gardant sa symétrie, puis se défait, et tout revient au départ au bout de {F(P)} pas. Il reste toujours au moins {a['nmin']} cases noires.",
        mesures=f"Cycle exact de période {F(P)} ; {F(a['cases'])} cases ; boîte {a['boite']}.",
        interet="Record de période de nos tirages symétriques " + ("à 4 fourmis." if n == 4 else "à 8 fourmis : la figure couvre 144 000 cases."),
        statut='VÉRIFIÉ (cycle exact)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-31)')
    germe('Cycles symétriques', f'{nom} (période {P})', f, p, f'Cycle exact {P} pas, symétrie d\'ordre 4.')
    row(n, len(p.split(';')), f'cycle symétrique ({nom})', P, f, p, 'VÉRIFIÉ')

# ---------- 5. Passagers ----------
CL5 = 'Passagers sur de nouvelles traces'
f = '1,-1,B ; 1,0,D ; 0,1,H ; -2,0,B ; -1,-1,G'
add(id='P-20', classe=CL5, nom='Le Passager de la Flèche', fourmis=f, points='', img=[4000, ''],
    situation="5 fourmis serrées sur grille blanche.",
    deroulement="Quatre fourmis forment tout de suite la Flèche (vaisseau de période 16, vitesse 1/4). La fourmi 2 reste sur la trace de la Flèche et la suit à la vitesse 1/10 (période 20, déplacement de 2 cases), sans jamais la rattraper.",
    mesures="Passager de période 20, déplacement (+2,0) ; la Flèche : période 16, (+4,0). Tenue sur 400 000 pas (système complet).",
    interet="Premier passager trouvé sur la trace d'un vaisseau de groupe (jusqu'ici : traces 104 et 102 seulement).",
    statut='OBSERVÉ (400 000 pas)', deja='Phénomène connu chez nous (passagers, R-18) ; pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-32)')
germe('Passagers', 'Passager 20 sur la Flèche', f, '', 'La fourmi 2 suit la trace de la Flèche à vitesse 1/10.')
row(5, 0, 'passager 20 sur la trace de la Flèche', 20, f, '', 'OBSERVÉ')
f = '-2,3,H ; -1,0,G ; -2,-2,D ; 1,-1,H ; 3,-2,B ; 2,1,D ; 3,3,G ; 0,2,B'
add(id='P-2620', classe=CL5, nom='Le Paresseux', fourmis=f, points='', img=[300000, ''],
    situation="8 fourmis placées avec une symétrie d'ordre 4.",
    deroulement="Les fourmis 2 et 4 partent en autoroute 102 à deux ; sur leur trace roulent un passager lent de période 388 (fourmi 8) et, encore plus lent, la fourmi 1 : période 2 620 pour 12 cases en x et 20 en y. Les 4 autres fourmis partent en autoroutes 104.",
    mesures="Passager de période 2 620, déplacement (12,20), installé dès le pas 99 651 ; tenu jusqu'à 2 000 000 de pas (≈ 730 périodes).",
    interet="Le plus lent des passagers connus chez nous (vitesse ≈ 0,009 case par pas, 6 fois moins que l'autoroute 102) ; trois vitesses différentes sur la même trace.",
    statut='OBSERVÉ (2 000 000 de pas, système complet)', deja='Phénomène connu chez nous (passagers 388, 688 : R-22) ; période 2 620 pas trouvée ailleurs', source='Claude, nuit du 16/11 (R-32)')
germe('Passagers', 'Paresseux 2620 sur la trace 102', f, '', 'Fourmi 1 : passager de période 2 620 sur la trace de l\'autoroute 102 (fourmis 2-4) ; fourmi 8 : passager 388.')
row(8, 0, 'passager 2620 sur la trace 102', 2620, f, '', 'OBSERVÉ')

# ---------- 6. Une fourmi ----------
CL6 = 'Une fourmi et une case : record de lenteur'
o = sh('./onset', '400000', '0,0,H', '7,-7'); deb = int(re.search(r'debut (\d+)', o).group(1))
add(id='L-106258', classe=CL6, nom='La Lambine', fourmis='0,0,H', points='7,-7', img=[deb + 3000, ''],
    situation="La fourmi classique et une seule case noire en (7,-7).",
    deroulement=f"La case noire relance le chaos : l'autoroute 104 ne démarre qu'au pas {F(deb)}, plus de 10 fois plus tard que sur grille blanche (9 977).",
    mesures=f"Autoroute 104, déplacement (+2,+2), début au pas {F(deb)}. Pire case des 1 680 positions de [-20,20]² (recherche exhaustive). Avec 2 cases dans [-5,5]² : au pire 87 485.",
    interet="Pendant inverse des germes rapides (G-80 à G-310) : une seule case peut multiplier par 10 la durée du chaos.",
    statut='OBSERVÉ (début mesuré par simulation finie ; exhaustif sur [-20,20]²)', deja='Pas trouvé ailleurs', source='Claude, nuit du 16/11 (R-33)')
germe('Une fourmi', 'Lambine (1 case, début 106 258)', '0,0,H', '7,-7', f'Autoroute 104 seulement au pas {deb}.')
row(1, 1, 'record de lenteur (Lambine)', deb, '0,0,H', '7,-7', 'OBSERVÉ')

for b in B: b.update(b=5, regle='RL', fourmis=norm(b['fourmis']), points=norm(b['points']))
json.dump(B, open('catalogue_nuit.json', 'w'), ensure_ascii=False, indent=1)
json.dump(GERMES, open('germes_nuit.json', 'w'), ensure_ascii=False, indent=1)
ROWS.sort(key=lambda r: (r[0], r[1], r[3]))
with open('resultats_nuit.csv', 'w', newline='') as fh:
    w = csv.writer(fh, delimiter=';'); w.writerow(['n_fourmis', 'n_cases', 'quoi', 'periode_ou_debut', 'fourmis', 'cases', 'statut']); w.writerows(ROWS)
print(len(B), 'bêtes,', len(GERMES), 'germes,', len(ROWS), 'lignes')

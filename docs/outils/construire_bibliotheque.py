# construire_bibliotheque.py — fusionne TOUS nos germes dans docs/bibliotheque.json (+ bibliotheque.js pour l'ouverture par double-clic).
# Règles (P10) : rien n'est supprimé ; les doublons sont marqués « doublon de … » et rangés dans « Archives/doublons » ;
# une bibliothèque existante est FUSIONNÉE (un élément déjà présent n'est jamais écrasé ; on ajoute seulement ce qui manque) ;
# chaque reconstruction ajoute une ligne à l'historique des versions.
import json, os, re, sys, datetime
from collections import defaultdict, Counter
ICI=os.path.dirname(os.path.abspath(__file__)); DOCS=os.path.dirname(ICI); SRC=os.path.join(DOCS,'sources')
VERSION='7.0'
def charge(f): return json.load(open(os.path.join(SRC,f),encoding='utf-8'))
CAPS4={'H':0,'D':1,'B':2,'G':3}; CAPS6={'E':0,'SE':1,'SO':2,'SW':2,'O':3,'W':3,'NO':4,'NW':4,'NE':5}
def norm_regle(r): return (r or 'RL').strip().replace(' ','')
def lire_fourmis(s,hexa):
    out=[]
    for t in re.split(r'[;\n]',str(s or '')):
        t=t.strip()
        if not t: continue
        p=[u.strip() for u in t.split(',')]
        if len(p)<3: return None
        try: x,y=int(p[0]),int(p[1])
        except ValueError: return None
        d=p[2].upper(); cap=(CAPS6 if hexa else CAPS4).get(d)
        if cap is None:
            try: cap=int(d)
            except ValueError: return None
        out.append((x,y,cap))
    return out
def lire_points(s):
    out=[]
    for t in re.split(r'[;\n]',str(s or '')):
        t=t.strip()
        if not t: continue
        p=[u.strip() for u in t.split(',')]
        try: out.append((int(p[0]),int(p[1]),int(p[2]) if len(p)>2 else 1))
        except (ValueError,IndexError): return None
    return out
def cle(g):
    """même règle, mêmes fourmis (dans le même ordre), mêmes cases, à une translation près"""
    r=norm_regle(g['regle']); hexa=r.startswith('H:')
    F=lire_fourmis(g['fourmis'],hexa); P=lire_points(g['points'])
    if F is None or P is None or (not F): return None
    xs=[f[0] for f in F]+[p[0] for p in P]; ys=[f[1] for f in F]+[p[1] for p in P]; x0,y0=min(xs),min(ys)
    return (r,tuple((x-x0,y-y0,d) for x,y,d in F),tuple(sorted((x-x0,y-y0,c) for x,y,c in P)))
STAT=re.compile(r'(PROUVÉ|VÉRIFIÉ|CONFIRMÉ|OBSERVÉ|AFFIRMÉ|FAUX|OUVERT)')
def statut_de(*txt):
    for t in txt:
        m=STAT.search(str(t or ''))
        if m: return m.group(1)
    return 'non précisé'
def refs(*txt):
    s=set()
    for t in txt: s|=set(re.findall(r'R-\d+',str(t or '')))
    return sorted(s,key=lambda r:int(r[2:]))
def pastille_de(deja):
    d=(deja or '').strip()
    if not d: return dict(c='gris',t='Pas encore cherché dans la littérature.')
    dl=d.lower()
    if dl.startswith('pas trouvé') or dl.startswith('pas de catalogue') or dl.startswith('pas trouv'): return dict(c='vert',t=d)
    if 'connu' in dl or 'connue' in dl or 'wikipédia' in dl: return dict(c='rouge',t=d)
    return dict(c='gris',t=d)
G=[]           # tous les éléments, dans l'ordre de priorité
INTROUVABLES=[]
def ajoute(src,i,g,dossier,date,**extra):
    e=dict(id=extra.pop('id',None) or f'{src}-{i:03d}',nom=g.get('nom','?'),regle=norm_regle(g.get('regle')),fourmis=str(g.get('fourmis','') or ''),
           points=str(g.get('points','') or ''),note=(g.get('note') or '').strip(),dossier=dossier,dossier_origine=g.get('dossier',''),
           origine=dict(fichier=src,index=i),date=date)
    e.update(extra)
    e.setdefault('statut',statut_de(g.get('statut'),g.get('note'),g.get('nom')))
    e.setdefault('refs',refs(g.get('note'),g.get('dossier'),g.get('nom'),g.get('source')))
    e.setdefault('pastille',pastille_de(g.get('deja')) if 'deja' in g else None)
    G.append(e); return e
# ---- rangement ----
def dossier_v6(d):
    d=d or 'Divers'
    rep=[('Autoroutes par direction (R-35)','Autoroutes/95 directions (R-35)'),('Collisions/1 case noire','Collisions/104 + 1 case (22 cas)'),
         ('Collisions/2 cases noires','Collisions/104 + 2 cases'),('Collisions/2 autoroutes','Collisions/2 autoroutes'),
         ('Cycles/Symétriques 8-12 fourmis (R-36)','Cycles et groupes/10 à 100 fourmis (R-36)'),('Cycles/','Cycles et groupes/'),
         ('Nids (R-26)','Cycles et groupes/Nids (R-26)'),('Navettes','Navettes et horloges'),('Groupes','Autoroutes/Groupes RL'),
         ('Autoroutes/Germes rapides','Une fourmi/Germes rapides'),('Autoroutes/Bouts minimaux','Une fourmi/Bout minimal 11 cases'),
         ('Autoroutes/Lenteur (R-33)','Une fourmi/Lambine (R-33)')]
    for a,b in rep:
        if d.startswith(a): return b+d[len(a):]
    return d
CLASSE={'Voyageurs (autoroutes)':'Autoroutes/Autres règles','Constructeurs (figures qui grandissent)':'Une fourmi/Autres règles (constructeurs)',
 'Symétriques (règles en paires)':'Une fourmi/Autres règles (symétriques)','Chaotiques (aucune autoroute connue)':'Une fourmi/Autres règles (chaotiques)',
 'Bornés (cycles exacts)':'Cycles et groupes/Cycles exacts','Voyageurs (autoroutes de groupe et autoroutes séparées)':'Autoroutes/Groupes RL',
 'Constructeurs (losanges qui grandissent)':'Cycles et groupes/Losanges (R-06)',"Passagers sur la trace d'une autoroute 104":'Passagers',
 "Passagers sur la trace d'une autoroute 102":'Passagers','Navettes (allers-retours)':'Navettes et horloges','Plus petits cycles (grille préparée)':'Cycles et groupes/Plus petits cycles',
 'Nids : cycles laissés derrière une autoroute':'Cycles et groupes/Nids (R-26)','Cycles de groupe sur grille blanche':'Cycles et groupes/Cycles de groupe (R-31)',
 'Cycles symétriques avec cases noires':'Cycles et groupes/Symétriques','Cycles symétriques sans case':'Cycles et groupes/10 à 100 fourmis (R-36)',
 'Passagers sur de nouvelles traces':'Passagers','Une fourmi et une case : record de lenteur':'Une fourmi/Lambine (R-33)',
 "Germes : faire partir l'autoroute vite":'Une fourmi/Germes rapides','Collisions : autoroute + 1 case noire':'Collisions/104 + 1 case (22 cas)',
 'Collisions : autoroute + 2 cases noires':'Collisions/104 + 2 cases','Collisions entre autoroutes':'Collisions/2 autoroutes',
 'Grille hexagonale (règles généralisées)':'Autoroutes/95 directions (R-35)/Hexagonale','Grille carrée, règles généralisées (L, R, N, U)':'Autoroutes/95 directions (R-35)/Carrée',
 'Grille carrée, règle RL (plusieurs fourmis)':'Autoroutes/95 directions (R-35)/Carrée','Ordinateur à fourmis':'Ordinateur/RL/Portes R-40 à R-44',
 'Ordinateur à fourmis (2)':'Ordinateur/RL','Fourmi dans fourmi (compilateur LLR)':'Ordinateur/Fourmi dans fourmi'}
IDDOS={'V-104':'Autoroutes/RL 104','V-18':'Autoroutes/LLR, LLLR, LⁿR','V-LnR':'Autoroutes/LLR, LLLR, LⁿR','V-102':'Autoroutes/RL 102','3V-102':'Autoroutes/RL 102',
 '4V-16':'Autoroutes/RL 16 (la Flèche)','4V-52':'Autoroutes/RL 52 (le Train)','4V-96':'Autoroutes/RL 96 (le Convoi)','4V-12':'Autoroutes/RL 12','P-108':'Autoroutes/RL 108 (la Suiveuse)',
 'P-rail':'Passagers/Rail 12','P-conv10':'Passagers/Convertisseur 10','P-100':'Passagers/100','P-388':'Passagers/388','P-688':'Passagers/688','P-142':'Passagers/142',
 'P-20':'Passagers/20 (la Flèche)','P-2620':'Passagers/2 620','C4-57924':'Navettes et horloges/Double navette (R-31)','C4-88828':'Navettes et horloges/Double navette (R-31)',
 'N-A':'Navettes et horloges/Navette R-19','N-B':'Navettes et horloges/Navette R-19','N-C':'Navettes et horloges/Navette R-19'}
RACINE={'Autoroute 104 nue (11 cases)':'Une fourmi/Bout minimal 11 cases','Germe 1 case':'Une fourmi/Germes rapides','Germe 2 cases':'Une fourmi/Germes rapides',
 'Germe 3 cases':'Une fourmi/Germes rapides','Autoroute 102 à 2 fourmis':'Autoroutes/RL 102','Autoroute 52 à 4 fourmis':'Autoroutes/RL 52 (le Train)',
 'Carré 2x2 (vaisseau 12)':'Autoroutes/RL 12','Flèche 4 fourmis (vitesse 0,25)':'Autoroutes/RL 16 (la Flèche)','Autoroute 96 à 2 fourmis':'Autoroutes/RL 96 (le Convoi)',
 'Suiveuse 108':'Autoroutes/RL 108 (la Suiveuse)','Navette A (période 100)':'Navettes et horloges/Navette R-19','Navette B':'Navettes et horloges/Navette R-19',
 'Navette C':'Navettes et horloges/Navette R-19','Passager 388 sur une 102':'Passagers/388'}
def dossier_nuit(d,nom):
    s=d.split('/',1)[1] if '/' in d else d
    if 'Double Navette' in nom: return 'Navettes et horloges/Double navette (R-31)'
    return {'Plus petits cycles':'Cycles et groupes/Plus petits cycles','Nids':'Cycles et groupes/Nids (R-26)','Cycles 2 fourmis + 1 case':'Cycles et groupes/Plus petits cycles',
            'Cycles de groupe':'Cycles et groupes/Cycles de groupe (R-31)','Cycles symétriques':'Cycles et groupes/Symétriques','Passagers':'Passagers',
            'Une fourmi':'Une fourmi/Lambine (R-33)'}.get(s,'Cycles et groupes')
# ---- 1. v6 ----
for i,g in enumerate(charge('germes_v6.json')): ajoute('v6',i,g,dossier_v6(g.get('dossier')),'2026-11-16')
# ---- 2. germes.json racine (15-11) ----
for i,g in enumerate(charge('germes_racine_15-11.json')): ajoute('racine',i,g,RACINE.get(g['nom'],'Divers'),'2026-11-15')
# ---- 3. R-20 à R-25 : on garde leurs sous-dossiers ----
for i,g in enumerate(charge('germes_r20_dossiers.json')): ajoute('r20',i,g,'R-20 à R-25/'+g['dossier'],'2026-11-15')
# ---- 4. nuit du 16-11 ----
for i,g in enumerate(charge('germes_nuit.json')): ajoute('nuit',i,g,dossier_nuit(g['dossier'],g['nom']),'2026-11-16')
# ---- 5. 95 directions (R-35) ----
for i,g in enumerate(charge('germes_autoroutes.json')):
    ajoute('r35',i,g,'Autoroutes/95 directions (R-35)/'+g['dossier'].split('/',1)[1] if '/' in g['dossier'] else 'Autoroutes/95 directions (R-35)','2026-11-16',refs=['R-35'])
# ---- 6. 10 à 100 fourmis ----
for i,g in enumerate(charge('germes_2026-11-16_10-100fourmis.json')): ajoute('r36cyc',i,g,'Cycles et groupes/10 à 100 fourmis (R-36)','2026-11-16',refs=['R-36'])
# ---- 7. catalogue (bestiaires 1 à 10) ----
for i,b in enumerate(charge('catalogue.json')):
    g=dict(b); dos=IDDOS.get(b['id']) or CLASSE.get(b['classe'],'Divers')
    if b['classe']=='Cycles symétriques avec cases noires' and b['b']==7: dos='Cycles et groupes/10 à 100 fourmis (R-36)'
    if b['b']>=8: dos='Archives/germes détaillés/Bestiaires 8 à 10 (une combinaison d\'entrées)'
    fiche={k:b.get(k) for k in ('situation','deroulement','mesures','interet') if b.get(k)}
    ajoute('cat',i,g,dos,'2026-11-16',id='cat-'+b['id'],bestiaire=b['b'],fiche=fiche,detaille=b['b']>=8,source_texte=b.get('source',''),
           statut=statut_de(b.get('statut')),statut_detail=b.get('statut',''))
# ---- 8. R-36 à R-38 (92 germes détaillés) ----
for i,g in enumerate(charge('germes_ordinateur_R36-R38.json')):
    ajoute('r36ord',i,g,'Archives/germes détaillés/R-36 à R-38/'+g['dossier'].split('/',1)[1],'2026-11-16',detaille=True,avancement='fait')
# ---- 9. R-39 ----
for i,g in enumerate(charge('germe_ordinateur_R39.json')): ajoute('r39',i,g,'Archives/germes détaillés/R-39','2026-11-16',detaille=True,avancement='fait')
# ---- 10. R-40 à R-44 (28 germes : une porte par combinaison d'entrées) ----
for i,g in enumerate(charge('germes_ordinateur_2026-11-17.json')):
    ajoute('r40',i,g,'Archives/germes détaillés/R-40 à R-44/'+g['dossier'].split('/',1)[1],'2026-11-17',detaille=True,avancement='fait')
# ---- 11. R-45 à R-60 ----
D11={'R-49':'Ordinateur/RL/Additionneurs en un germe','R-53':'Ordinateur/RL/Additionneurs en un germe','R-48':'Ordinateur/RL/Additionneurs en un germe',
     'R-46':'Ordinateur/RL/Ruban (R-46)','R-47':'Ordinateur/Pièges à autoroute','R-51':'Ordinateur/Pièges à autoroute','R-55':'Ordinateur/LLR','R-56':'Ordinateur/LLR','R-58':'Ordinateur/LLR'}
for i,g in enumerate(charge('germes_ordinateur2_2026-11-17.json')):
    r=refs(g['dossier'],g['note']); ajoute('r45',i,g,D11.get(r[0] if r else '','Ordinateur'),'2026-11-17',avancement='fait')
# ---- 12. fourmi dans fourmi ----
for i,g in enumerate(charge('germes_fourmi_dans_fourmi_2026-11-17.json')): ajoute('fdf',i,g,'Ordinateur/Fourmi dans fourmi','2026-11-17',avancement='fait')
# ---- 13. circuits (germe mis en avant avec interrupteurs) ----
CIRC=charge('circuits.json')
def ecrireF(F): return ' ; '.join(f'{x},{y},{d}' for x,y,d in F)
def ecrireP(P): return ' ; '.join(f'{x},{y}' if c==1 else f'{x},{y},{c}' for x,y,c in P)
for i,c in enumerate(CIRC):
    if c.get('variantes'):
        z=','.join(f'{e["nom"]}=0' for e in sorted(c['entrees'],key=lambda e:e['nom'])); v=c['variantes'].get(z) or list(c['variantes'].values())[0]
        F,P=v['fourmis'],v['points']
    else:
        F=[f for e in c['entrees'] for f in e['si0']['fourmis']]+c['base']['fourmis']; P=[p for e in c['entrees'] for p in e['si0']['points']]+c['base']['points']
    ajoute('circ',i,dict(nom=c['nom'],regle=c['regle'],fourmis=ecrireF(F),points=ecrireP(P),note=c['note'],source=c['source']),c['dossier'],c['date'],
           id=c['id'],circuit=c['id'],statut=statut_de(c['statut']),statut_detail=c['statut'],avancement=c.get('avancement','fait'),mis_en_avant=True,refs=[c['source']] if c['source'].startswith('R-') else refs(c['nom']))
# ---- 14. germes cités seulement dans les journaux ----
EXTRA=[dict(nom='Convoi 104×3 (3 autoroutes parallèles)',regle='RL',fourmis='0,0,H ; -2,0,B ; -2,2,D',points='',note="R-45 : 3 fourmis, autoroutes 104 parallèles (48 voies d'écart), dès le pas 17 131. Ce n'est pas un vrai convoi groupé. OBSERVÉ.",dossier='Ordinateur/RL/Ruban (R-46)'),
       dict(nom='Mur LLR : miroir (R-64)',regle='LLR',fourmis='0,0,H',points=' ; '.join(f'-60,{y}' for y in range(-300,301)),note="R-40/R-64 : un mur vertical de cases fait tourner l'autoroute LLR ↙ en ↘ (voie −124). OBSERVÉ.",dossier='Autoroutes/LLR, LLLR, LⁿR')]
for i,g in enumerate(EXTRA): ajoute('journal',i,g,g['dossier'],'2026-11-17',avancement='fait')
INTROUVABLES+=[('Famille de navettes R-21 (portée 19 797 + 52 m)',"germe fabriqué par nav.c avec un paramètre m : aucune liste de cases enregistrée (seule la navette R-19 de base est dans la bibliothèque)"),
               ('Piège réutilisable R-51 — autres cas que le germe gardé',"seul 1 germe a été exporté (les 40 cas sont dans ordinateur/v2/miroir_cycle.json, pas mis en germes)")]
# ---- doublons ----
prem={}; nd=0; casses=[]
def archive(e,p):
    e['doublon_de']=p['id']; e['dossier_affiche']=e['dossier']; e['dossier']='Archives/doublons'
    for f in ('fiche','bestiaire','statut_detail','source_texte'):
        if e.get(f) and not p.get(f): p[f]=e[f]
    if (p.get('pastille') is None or p['pastille']['c']=='gris') and e.get('pastille') and e['pastille']['c']!='gris': p['pastille']=e['pastille']
    if p.get('statut')=='non précisé' and e.get('statut')!='non précisé': p['statut']=e['statut']
    if e['dossier_affiche']!=p['dossier']: p.setdefault('aussi',[]).append(e['dossier_affiche'])
    if not p['note'] and e['note']: p['note']=e['note']
    if e['nom']!=p['nom'] and e['nom'] not in p.get('autres_noms',[]): p.setdefault('autres_noms',[]).append(e['nom'])
circs=[e for e in G if e.get('circuit')]
for e in G:
    if e['points'].startswith('germe:'):
        cible=e['points'][6:].strip(); t=[x for x in G if x['nom']==cible and x is not e]
        if t: archive(e,t[0])
        else: casses.append((e['id'],e['nom'],'renvoie à « '+cible+' » introuvable'))
        continue
    if e.get('circuit') or e.get('detaille'): continue          # circuits et germes détaillés : traités à part
    k=cle(e)
    if k is None:
        if not e['fourmis'].strip() and not e['points'].strip(): e['vide']=True; continue
        casses.append((e['id'],e['nom'],'fourmis ou cases illisibles')); continue
    if k in prem: archive(e,prem[k])
    else: prem[k]=e
# un germe ordinaire identique au germe d'un circuit DU MÊME RÉSULTAT (même R-xx) devient « doublon de » ce circuit
for c in circs:
    k=cle(c)
    if k is None: continue
    for e in G:
        if e is c or e.get('circuit') or e.get('doublon_de') or e.get('detaille'): continue
        if cle(e)==k and set(e.get('refs',[]))&set(c.get('refs',[])) and e['origine']['fichier'] not in ('v6',):
            archive(e,c)
# pastilles restantes : par règle simple (dans l'ordre : sources, puis gris)
for e in G:
    if e.get('pastille') is None:
        if e['dossier'].startswith('Ordinateur') or e['origine']['fichier'] in ('circ','r45','fdf','r36ord','r39','r40','journal'):
            e['pastille']=dict(c='vert',t="Pas trouvé ailleurs (recherche R-43, R-58 ; le principe « la fourmi calcule » est connu : Gajardo-Moreira-Goles 2002).")
        else: e['pastille']=dict(c='gris',t='Pas encore cherché dans la littérature (ou recherche non rattachée à ce germe).')
# ---- avancement « fourmi dans fourmi » (feuille de route reconstruite : le doc n'est pas dans le Drive) ----
AV=[('Circuit logique d\'un pas (8 bits → 8 bits)','fait','VÉRIFIÉ 256/256','R-61'),('Portes LLR : NOR, OU, ET, NON, COPIE','fait','VÉRIFIÉ (2 moteurs)','R-55 à R-59'),
    ('XOR LLR','fait (par le compilateur)','VÉRIFIÉ 4/4','R-62'),('Croisement LLR','à faire','croisement direct impossible (OBSERVÉ) ; 3 XOR à construire','R-64'),
    ('Compilateur fonctions → germe LLR','fait (prototype)','VÉRIFIÉ','R-62'),('Les 8 modules du pas','fait','VÉRIFIÉ 2 048/2 048 (C) ; Python 1 792 + 29','R-63'),
    ('Le pas complet en un germe','fait','VÉRIFIÉ 256/256 (JS) ; 33/33 (Python)','R-67, R-68'),('Vérifier le pas complet sur 256 états, 2 moteurs','fait','VÉRIFIÉ 256/256 (moteur JS v7) + 33/33 (Python)','R-68'),
    ('Enchaîner deux pas (sorties → entrées)','à faire','besoin du croisement','—'),('Boucle infinie (horloge + mémoire)','en cours','argument écrit (AFFIRMÉ) ; effacement par 3 passages : négatif','R-65, R-66'),
    ('Porte d\'interaction « propre » (billard)','à faire','—','R-65'),('Mémoire réinscriptible','à faire','pas trouvée','R-51, R-60')]
# ---- fusion avec une bibliothèque existante ----
cible=os.path.join(DOCS,'bibliotheque.json'); hist=[]
if os.path.exists(cible):
    ancienne=json.load(open(cible,encoding='utf-8')); hist=ancienne.get('historique',[])
    ids={e['id'] for e in G}
    for e in ancienne.get('germes',[]):
        if e['id'] not in ids: G.append(e)      # jamais perdu : ce qui existait est gardé tel quel
    anc={e['id']:e for e in ancienne.get('germes',[])}
    for e in G:                                   # ajouts de Pierre-Malo (notes, pastilles posées à la main) conservés
        a=anc.get(e['id'])
        if a and a.get('modifie_a_la_main'): e.update({k:v for k,v in a.items()})
cpt=Counter(e['origine']['fichier'] for e in G)
bilan=dict(par_fichier=dict(cpt),total=len(G),doublons_archives=sum(1 for e in G if e.get('doublon_de')),
           details_archives=sum(1 for e in G if e.get('detaille')),introuvables=[dict(nom=a,raison=b) for a,b in INTROUVABLES],
           casses=[dict(id=a,nom=b,raison=c) for a,b,c in casses],circuits=len(CIRC),
           pastilles=dict(Counter(e['pastille']['c'] for e in G)))
hist.append(dict(version=VERSION,date=datetime.date.today().isoformat(),total=len(G),note='Fusion des 12 sources (v6, Drive 02_Resultats, catalogue, circuits).'))
B=dict(version=VERSION,historique=hist,ordre=['Une fourmi','Autoroutes','Collisions','Navettes et horloges','Cycles et groupes','Passagers','R-20 à R-25','Ordinateur','Archives','Divers'],
       avancement=[dict(etape=a,etat=b,statut=c,ref=d) for a,b,c,d in AV],germes=G,circuits=CIRC,bilan=bilan)
json.dump(B,open(cible,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
open(os.path.join(DOCS,'bibliotheque.js'),'w',encoding='utf-8').write('// généré par outils/construire_bibliotheque.py — ne pas modifier à la main\nwindow.BIBLIOTHEQUE = '+json.dumps(B,ensure_ascii=False)+';\n')
print(json.dumps(bilan,ensure_ascii=False,indent=1)[:2500])

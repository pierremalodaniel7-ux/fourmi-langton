#!/usr/bin/env python3
"""agrege.py : réunit data/B5/jobs/*.res -> recherche/B5/positions/pos_XY.txt, tableau.md, data/B5/ech_arbre.txt.
Contrôle : par position, 64 sous-arbres présents et somme des poids (certifiés + non résolus) = 2^25."""
import glob, os, re
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'..','..')
J=os.path.join(R,'data','B5','jobs'); os.makedirs(os.path.join(D,'positions'),exist_ok=True)
pos={}; ech=[]; nonres=[]
for f in sorted(glob.glob(J+'/*.res')):
    for l in open(f):
        if l.startswith('ECH'): ech.append(l)
        elif l.startswith('NONRES'): nonres.append(l)
        elif l.startswith('RES'):
            d=dict(kv.split('=') for kv in l.split()[1:])
            k=d['pos']; P=pos.setdefault(k,{'jobs':0,'feuilles':0,'poids':0,'nonres':0,'pnr':0,'autre':0,'tmax':-1,'m':0,'sec':0.0,'pas':0,'tmin':10**12,'hist':None})
            P['jobs']+=1; P['feuilles']+=int(d['feuilles']); P['poids']+=int(d['poids']); P['nonres']+=int(d['nonres'])
            P['pnr']+=int(d['poids_nonres']); P['autre']+=int(d['poids_autre_derive']); P['sec']+=float(d['sec']); P['pas']+=int(d['pas'])
            if int(d['tmin'])>=0: P['tmin']=min(P['tmin'],int(d['tmin']))
            if int(d['tmax'])>P['tmax']: P['tmax']=int(d['tmax']); P['m']=int(d['masque_max'])
        elif l.startswith('HIST'):
            h=list(map(int,l.split()[1:])); P['hist']=h if P['hist'] is None else [a+b for a,b in zip(P['hist'],h)]
lig=['| position (x,y) | sous-arbres | feuilles | poids certifié | non résolus | 1er certificat max | masque du record | plus court | temps (s·cœur) |','|---|---|---|---|---|---|---|---|---|']
tot_ok=True; T5=(-1,None)
for y in range(5):
    for x in range(5):
        k=f'{x},{y}'
        if k not in pos: lig.append(f'| {k} | 0/64 | – | – | – | – | – | – | – |'); tot_ok=False; continue
        P=pos[k]; ok=P['jobs']==64 and P['poids']+P['pnr']==1<<25
        tot_ok&=ok and P['nonres']==0 and P['autre']==0
        if P['tmax']>T5[0]: T5=(P['tmax'],(k,P['m']))
        e=lambda n: f'{n:,}'.replace(',',' ')
        lig.append(f"| {k} | {P['jobs']}/64 | {e(P['feuilles'])} | {e(P['poids'])}{' = 2^25' if P['poids']==1<<25 else ''} | {P['nonres']} | {e(P['tmax'])} | {P['m']} | {e(P['tmin'])} | {P['sec']:.0f} |")
        with open(os.path.join(D,'positions',f'pos_{x}{y}.txt'),'w') as o:
            o.write(f"position {k} cap haut : sous-arbres {P['jobs']}/64, feuilles {P['feuilles']}, poids certifié {P['poids']} (2^25 = {1<<25}), "
                    f"non résolus {P['nonres']} (poids {P['pnr']}), dérive ≠ (±2,±2) : {P['autre']}\n1er certificat max {P['tmax']} (masque {P['m']}), "
                    f"min {P['tmin']}, pas simulés {P['pas']}, temps {P['sec']:.1f} s·cœur\nhistogramme log2(t) : {P['hist']}\n")
open(os.path.join(D,'tableau.md'),'w').write('\n'.join(lig)+f"\n\nT(5) = {T5[0]} ; position, masque : {T5[1]} ; tout complet et exact : {tot_ok}\n")
open(os.path.join(R,'data','B5','ech_arbre.txt'),'w').writelines(ech)
open(os.path.join(D,'nonresolus.txt'),'w').writelines(nonres)
print('positions',len(pos),'T5',T5,'complet',tot_ok,'echantillons',len(ech),'nonres',len(nonres))

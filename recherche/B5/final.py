#!/usr/bin/env python3
"""final.py B R-ID : après agrege.py et controles.py. Ajoute les 25 records (une fiche par position) au catalogue
(docs/sources/catalogue.json, bestiaire n° B), écrit resultats/germes_2026-11-19_B5.json et ajoute les germes
(dossier « B5 ») à docs/germes.json sans toucher aux autres. Conversion : y vers le haut (B5) -> y vers le bas (moteurs)."""
import json, os, sys, glob
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(os.path.join(D,'..','..'))
B=int(sys.argv[1]); RID=sys.argv[2]   # ex. R-135
recs=[]
for y in range(5):
    for x in range(5):
        l=open(os.path.join(D,'positions',f'pos_{x}{y}.txt')).read().split('\n')
        w=l[1].split(); t=int(w[3]); m=int(w[5].strip('(),'))
        recs.append((x,y,t,m))
T5=max(r[2] for r in recs)
cat_path=os.path.join(R,'docs','sources','catalogue.json'); cat=json.load(open(cat_path))
cat=[c for c in cat if not c['id'].startswith('B5-')]
germes=[]
for x,y,t,m in recs:
    pts=';'.join(f'{i%5},{-(i//5)}' for i in range(25) if m>>i&1)
    four=f'{x},{-y},H'; n=bin(m).count('1')
    cat.append({"id":f"B5-{x}{y}","b":B,"classe":"Conjecture de l'autoroute (B5, carré 5×5)",
      "nom":f"Record 5×5, fourmi en ({x},{y})"+(" — T(5)" if t==T5 else ""),
      "regle":"RL","fourmis":four,"points":pts,"img":[t+3000,""],
      "situation":f"Carré 5×5 (coin bas-gauche (0,0), y vers le haut), fourmi en ({x},{y}) cap haut, {n} cases noires (masque {m}). Image en y vers le bas.",
      "deroulement":f"Pire des 2^25 coloriages pour cette position : le plus long chaos avant l'autoroute 104.",
      "mesures":f"Premier instant certifié {t:,}".replace(',',' ')+" (arbre, moteur brut, src/fourmi -cert identiques ; ant_controle : début ≤ certificat).",
      "statut":"DÉMONTRÉ pour cette configuration (calcul exact + lemme R-83) ; record de la position = max exhaustif (B5)",
      "interet":"Borne exacte du transitoire pour une fourmi dans un carré 5×5." if t!=T5 else f"T(5) = {t:,}".replace(',',' ')+" : plus long transitoire de tout le carré 5×5 (toutes positions, tous caps).",
      "deja":"Pas trouvé (voir deja_connu.md, B5)","source":"recherche/B5 (19/11), "+RID,
      })
    germes.append({"dossier":"B5","nom":f"Record 5×5 ({x},{y})"+(" T(5)" if t==T5 else ""),"regle":"RL","fourmis":four,"points":pts,
                   "note":f"Pire coloriage du carré 5×5 pour la fourmi en ({x},{y}) cap haut : autoroute 104 certifiée dès {t} (B5, {RID})."})
json.dump(cat,open(cat_path,'w'),ensure_ascii=False,indent=1)
json.dump(germes,open(os.path.join(R,'resultats','germes_2026-11-19_B5.json'),'w'),ensure_ascii=False,indent=1)
gp=os.path.join(R,'docs','germes.json'); G=json.load(open(gp)); G=[g for g in G if g.get('dossier')!='B5']
G+= [{"nom":g["nom"],"regle":"RL","fourmis":g["fourmis"],"points":g["points"].replace(';',' ; '),"note":g["note"],"dossier":"B5"} for g in germes]
open(gp,"w").write(json.dumps(G,ensure_ascii=False,indent=1))
print('fiches',len(recs),'T5',T5,'germes docs',len(G))

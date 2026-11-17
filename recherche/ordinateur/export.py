# export.py — écrit le germe final (4 bits, réglé sur 3+2), la table des entrées et les pas de lecture.
import chaine as Ch, json
N=4; A,B=3,2; P=104
CAP="HDBG"
M=Ch.M
def cases(cond_ok):
    out=[[] for _ in range(N)]
    for m in range(N):
        ox,oy=m*Ch.VX,m*Ch.VY
        for r in ('S','K'):
            for nd in M[r]['nodes']:
                if cond_ok(nd['cond']): out[m].append([nd['cell'][0]+ox,nd['cell'][1]+oy])
    return out
a1=cases(lambda c:c=={'a':1}); b1=cases(lambda c:c=={'b':1}); b0=cases(lambda c:c=={'b':0})
cells0,ants,noms=Ch.germe_chaine(N,0,0)
fixes=[list(c) for c in cells0 if list(c) not in sum(b0,[])]
lect={f"S{m}":m*Ch.DELAI*P+95000 for m in range(N)}; lect[f"K{N-1}"]=(N-1)*Ch.DELAI*P+115000
E={"n":N,"fourmis":[list(a) for a in ants],"noms":noms,"fixes":fixes,"si_a1":a1,"si_b1":b1,"si_b0":b0,
   "lecture":lect,"T_conseille":(N-1)*Ch.DELAI*P+140000,
   "regle_lecture":"S_m : ↘ (bas-droite) = bit m de la somme à 0, ↙ (bas-gauche) = 1 ; K3 : ↗ (haut-droite) = bit 4 à 1, ↘ = 0"}
json.dump(E,open('entrees.json','w'),ensure_ascii=False,indent=1)
cells,ants,noms=Ch.germe_chaine(N,A,B)
fm=" ; ".join(f"{x},{y},{CAP[d]}" for x,y,d in ants)
pts=" ; ".join(f"{x},{y}" for x,y in cells)
g={"dossier":"Ordinateur","nom":"Additionneur 4 bits (réglé sur 3 + 2)","regle":"RL","fourmis":fm,"points":pts,
   "note":("R-39. 4 modules identiques (additionneur complet) ; la retenue passe d'un module au suivant par une autoroute. "
           "Réglé sur a=3, b=2. Lire au pas indiqué la direction de la fourmi : S0 (fourmi 1) pas 95 000, S1 (3) pas 193 800, "
           "S2 (5) pas 292 600, S3 (7) pas 391 400 : ↘ = 0, ↙ = 1 ; K3 (8) pas 411 400 : ↗ = 1, ↘ = 0. "
           "Attendu 3+2=5=00101 : S0 ↙, S1 ↘, S2 ↙, S3 ↘, K3 ↘. Entrées : voir recherche/ordinateur/fiche.md.")}
json.dump([g],open('germe_ordinateur.json','w'),ensure_ascii=False,indent=1)
print(len(cells),"cases ;",len(fixes),"fixes ; a:",[len(x) for x in a1],"b1:",[len(x) for x in b1],"b0:",[len(x) for x in b0])
print(lect)

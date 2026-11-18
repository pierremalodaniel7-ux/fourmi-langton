# R-70 : DEUX pas de la petite fourmi (pas∘pas) compilés en UN germe LLR (compilateur v3), vérifié 256/256 avec le moteur creux.
# Ce n'est PAS un chaînage physique (sorties du pas 1 → entrées du pas 2) : la fonction composée est compilée d'un coup.
import sys, json, subprocess, time
sys.path.insert(0,'../v3'); sys.path.insert(0,'..')
import compilateur as C, pas_llr as PL, pas
from pas256_creux import lit
C.PAR.update(POFF=200,SP=40,DA=200,OY=0)
def vec(t): return [t['c'][(0,0)],t['c'][(1,0)],t['c'][(0,1)],t['c'][(1,1)],t['x'],t['y'],t['h']>>1,t['h']&1]
def sortie2(k): return lambda m: vec(pas.vrai_pas(pas.vrai_pas(PL.etat(m))))[k]
S2=[(n+"''",sortie2(k)) for k,n in enumerate(PL.NOMS)]
# correctif R-70 : sorties de niveau 1 (une seule clause) placées APRÈS celles de niveau 2, sinon une puissance ↙ de niveau 2
# coupe la puissance ↘ d'une sortie de niveau 1 déjà lue (bug vu sur y'' : 248/256)
niv1=lambda f: len(C.cnf(lambda m:not f(m),8))==1
S2=[s for s in S2 if not niv1(s[1])]+[s for s in S2 if niv1(s[1])]
plan=C.compile_(S2,8,PL.NOMS); T=C.T_of(plan)
nb2=sum(1 for o in plan['outs'] if o['niv']==2)
lines=[];L=[]
for m in range(256): s,l=C.germe(plan,m); lines.append(f'{s} {T}\n'); L.append(l)
print('portes niv1',len(plan['gates']),'niv2',nb2,'fourmis max',max(s.count(',')//2 for s in lines),'T',T,flush=True)
k,K=int(sys.argv[1]),int(sys.argv[2]); ok=0; bad=[]
for m in range(k,256,K):
    o=subprocess.run(['./creux'],input=lines[m],capture_output=True,text=True).stdout.strip()
    r=lit(o,L[m]); g=all(r[n]==int(bool(f(m))) for n,f in S2); ok+=g
    if not g: bad.append(m)
print('tranche',k,':',ok,'/',len(range(k,256,K)),'faux',bad,flush=True)

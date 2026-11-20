#!/usr/bin/env python3
"""controles.py : contrôles croisés B5 (à lancer après agrege.py).
(a) échantillons (graine 20261119) : instant de l'arbre vs src/fourmi -cert (instant exact) et ant_controle_b5 (début, dérive)
(b) record de chaque position : b5 brut, src/fourmi -cert, ant_controle_b5
(c) records des 46 tranches de resultats/box5/ : b5 brut"""
import os, subprocess, sys, glob
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(os.path.join(D,'..','..'))
FOU=os.path.join(R,'src','fourmi'); ANT=os.path.join(D,'ant_controle_b5'); B5=os.path.join(D,'b5')
def ligne_fourmi(x,y,m): # src/fourmi : y vers le bas
    return 'RL|%d,%d,H|'%(x,-y)+';'.join('%d,%d'%(i%5,-(i//5)) for i in range(25) if m>>i&1)
def fourmi(cas):
    out=subprocess.run([FOU,'-T','16000000','-cert','-lot'],input='\n'.join(ligne_fourmi(*c) for c in cas)+'\n',capture_output=True,text=True).stdout.splitlines()
    res=[]
    for l in out:
        i=l.find('CERT '); res.append(int(l[i+5:].split()[0]) if i>=0 else -1)
    return res
def ant(cas):
    out=subprocess.run([ANT,'lotpos','5'],input=''.join('%d %d %d\n'%c for c in cas),capture_output=True,text=True).stdout.split('\n')
    return [tuple(map(int,l.split()[3:])) for l in out if l]
mode=sys.argv[1] if len(sys.argv)>1 else 'tout'
if mode in('a','tout'):
    E=[l.split() for l in open(os.path.join(R,'data','B5','ech_arbre.txt'))]
    cas=[(int(e[1]),int(e[2]),int(e[3])) for e in E]; tt=[int(e[4]) for e in E]
    n=len(cas); print('(a) échantillons trouvés dans l\'arbre :',n,'/ 100000 (lignes du fichier, doublons compris)')
    F=[]; A=[]
    for k in range(0,n,5000): F+=fourmi(cas[k:k+5000]); A+=ant(cas[k:k+5000])
    df=sum(1 for a,b in zip(tt,F) if a!=b); okA=sum(1 for t,a in zip(tt,A) if a[0]==1 and a[1]<=t)
    ecart=[t-a[1] for t,a in zip(tt,A) if a[0]==1]
    print('    fourmi -cert : instants différents :',df)
    print('    ant_controle : autoroute détectée et début <= instant certifié :',okA,'/',n,
          '; écart certificat-début : 0 pour',sum(1 for e in ecart if e==0),', max',max(ecart),', min',min(ecart))
    for t,f,a,c in zip(tt,F,A,cas):
        if t!=f or a[0]!=1 or a[1]>t: print('    DESACCORD',c,t,f,a)
if mode in('b','tout'):
    print('(b) records par position')
    for f in sorted(glob.glob(os.path.join(D,'positions','pos_*.txt'))):
        l=open(f).read().split('\n')[1].split(); t=int(l[3]); m=int(l[5].strip('(),'))
        x,y=int(f[-6]),int(f[-5])
        b=int(subprocess.run([B5,'brut','5',str(x),str(y),'5000000',str(m)],capture_output=True,text=True).stdout.split()[1])
        fo=fourmi([(x,y,m)])[0]; a=ant([(x,y,m)])[0]
        print('   ',x,y,'masque',m,'arbre',t,'brut',b,'fourmi',fo,'ant_controle début',a[1],'dérive',a[2:],'OK' if t==b==fo and a[0]==1 and a[1]<=t else 'ECART')
if mode in('c','tout'):
    n=ok=0
    for f in sorted(glob.glob(os.path.join(R,'resultats','box5','*.res'))):
        w=open(f).readline().split(); t=int(w[6])
        m=sum(1<<(int(c.split(',')[0])+5*(-int(c.split(',')[1]))) for c in w[7].strip('()').split(';'))
        b=int(subprocess.run([B5,'brut','5','0','0','5000000',str(m)],capture_output=True,text=True).stdout.split()[1]); n+=1; ok+=b==t
    print('(c) tranches box5 : records identiques',ok,'/',n)

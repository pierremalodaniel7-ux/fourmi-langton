# Lecture "à la fin" : directions de toutes les fourmis S au pas final, pour toutes les entrées
import chaine as Ch, fourmis as F, sys, collections
n=int(sys.argv[1]); T=int(sys.argv[2])
ok=0; mauvais=collections.Counter()
for a in range(1<<n):
  for b in range(1<<n):
    cells,ants,noms=Ch.germe_chaine(n,a,b); nn,dh,xs,ys=F.simule_tout(cells,ants,T)
    s=a+b; good=True
    for m in range(n):
        d=Ch.lit(dh,xs,ys,len(dh),2*m)
        if d!=(0 if (s>>m)&1 else 3): good=False; mauvais[m]+=1
    d=Ch.lit(dh,xs,ys,len(dh),2*n-1)
    if d!=(2 if (s>>n)&1 else 3): good=False; mauvais['K']+=1
    ok+=good
print(f"n={n} T={T} : lecture à la fin correcte pour {ok}/{1<<2*n} ; fausses par fourmi : {dict(mauvais)}")

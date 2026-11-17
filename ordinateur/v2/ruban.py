# ruban.py — RÉSERVOIR = ruban de N autoroutes 104 parallèles (↙), voies x+y espacées de 2s.
# La fourmi k (k = N-1 d'abord) est lâchée vers ↘ par une case, D périodes plus loin que la précédente.
import sys; sys.path.insert(0,'..')
import portes as Pt, sim, json, subprocess
VIR=(-26,25)   # case « virage −90° » (R-43) pour le germe en (0,0) : ↙ -> ↘
def ruban(N,s=10,D=40):
    g=[];cells=[]
    for k in range(N):
        ox,oy=k*s,k*s; g.append(Pt.germe(ox,oy,0))
        n=(N-1-k)*D           # retard du lâcher en périodes
        cells.append((VIR[0]+ox-2*n, VIR[1]+oy+2*n))
    return g,cells
def run_c(st,T):
    p=subprocess.run(['../gate'],input=f'{st} {T}\n',capture_output=True,text=True)
    l=p.stdout.strip()
    return 'BORD' if l.startswith('BORD') else [None if t=='X' else tuple(map(int,t.split(','))) for t in l.split()]
def main():
    res={}
    for N in (2,3,5,8,10,12,15):
        g,cells=ruban(N); st=Pt.situ(g,extra=cells); T=40*104*N+30000
        o=run_c(st,T)
        if o=='BORD': print(N,'BORD'); continue
        ok=sum(1 for a in o if a and (a[0],a[1])==(2,2))
        res[N]=dict(germe='RL|'+st,lachees=ok,detail=o,T=T)
        print(f'N={N:2d} : {ok}/{N} fourmis lâchées en 104 ↘ propres (moteur C, {T} pas) ; voies x-y : {[a[2] for a in o if a]}',flush=True)
    json.dump(res,open('ruban.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()

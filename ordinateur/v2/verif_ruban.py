import sys; sys.path.insert(0,'..')
import ruban, portes as Pt, sim, time
for N in (8,15):
    g,c=ruban.ruban(N); T=40*104*N+30000; t=time.time()
    _,_,_,pos=sim.run('RL|'+Pt.situ(g,extra=c),T,trace=True); ok=0; lanes=[]
    for i in range(N):
        d=(pos[-1][i][0]-pos[-105][i][0],pos[-1][i][1]-pos[-105][i][1])
        st=all((pos[-1-k][i][0]-pos[-105-k][i][0],pos[-1-k][i][1]-pos[-105-k][i][1])==d for k in range(0,2000,13))
        if st and d==(2,2): ok+=1; lanes.append(min(p[i][0]-p[i][1] for p in pos[-104:]))
    print(f'Python : N={N} {ok}/{N} lâchées ↘ stables (2 000 derniers pas) ; voies {lanes} ; {time.time()-t:.1f} s')

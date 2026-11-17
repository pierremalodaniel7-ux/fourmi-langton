import module as Mo, fourmis as F, json, sys
M=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'module.json'))
bad=0
for e in Mo.ENTREES:
    c,a,b=e; s=c^a^b; k=int(c+a+b>=2)
    hS,_=Mo.sim(M,e,'S'); hK,_=Mo.sim(M,e,'K')
    okS = hS and hS[1]==(0 if s else 3); okK = hK and hK[1]==(2 if k else 3)
    bad+= (not okS)+(not okK)
    print(e,"S",F.FL[hS[1]] if hS else None,hS[2] if hS else "", "attendu",F.FL[0 if s else 3],"| K",F.FL[hK[1]] if hK else None,hK[2] if hK else "","t0",hK[0] if hK else "", "attendu",F.FL[2 if k else 3])
print("ECHECS",bad)

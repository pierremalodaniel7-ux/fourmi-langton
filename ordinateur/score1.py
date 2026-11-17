import json,statistics as st,sys
from collections import Counter,defaultdict
rep=json.load(open(sys.argv[1]))
def propre(x): return x['issue']=='AUTOROUTES' and x['nonc']==0 and len(x['dirs'])==1
print('autoroute | cases: n, propres %, tournent ±90 propre %, angles, chaos médian, parasites % | murs miroirs (8/8 même virage propre)')
tab=[]
for nom,r in rep.items():
    cs=[x for x in r['rows'] if x['kind']=='case']
    n=len(cs); pr=sum(propre(x) for x in cs); tu=sum(propre(x) and x['angles'][0] in (90,-90) for x in cs)
    par=sum((len(x['dirs'])>1 or x['nonc']>0) for x in cs)
    ch=[x['chaos'] for x in cs if x['chaos'] is not None]
    angs=Counter(x['angles'][0] if propre(x) else 'sale' for x in cs)
    murs=defaultdict(list)
    for x in r['rows']:
        if x['kind']!='case': murs[x['kind']].append(x)
    good=[]
    for k,v in murs.items():
        a={(x['angles'][0] if propre(x) else 'sale') for x in v}
        if len(a)==1 and list(a)[0] in (90,-90):
            good.append(f"{k}:{list(a)[0]} chaos≤{max((x['chaos'] or 0) for x in v)}")
    score=round(100*tu/n*0.5+ (50 if good else 0) - 100*par/n*0.5)
    tab.append((score,nom))
    print(f"{nom} [{r['base']} P{r['P']} t0={r['t0']}] | n={n} propres {100*pr//n}% virage {100*tu//n}% {dict(angs)} chaos méd {int(st.median(ch)) if ch else '-'} parasites {100*par//n}% | {good}")
print(sorted(tab,reverse=True))

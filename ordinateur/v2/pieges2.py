import pieges as Pg, json
from collections import Counter, defaultdict
PER={'Tourniquet 4':4,'Petit Grain 8':8,'Rouage 8':8,'Petite Rosace 16':16}
T=200000; cas=[(n,r,p,s) for n in Pg.CYC for r in range(4) for p in range(-8,9) for s in range(4)]
lines=[Pg.situ(n,r,-160+p+s,160+p-s) for n,r,p,s in cas]; out=Pg.run(lines,T)
vrai=[]; cnt=Counter(); par=defaultdict(Counter)
for (n,r,p,s),l,o in zip(cas,lines,out):
    if o=='BORD': cnt['BORD']+=1; continue
    t=o.split(); st=[x for x in t if x in('B','X') or x.startswith('A')]; cyc=int(t[t.index('CYC')+1]) if 'CYC' in t else None
    hw=[x for x in st if x.startswith('A')]
    rien = st[0].startswith('A104:-2,2,-5') and cyc==PER[n] and len(hw)==1
    if rien: cnt['pas de contact']+=1; continue
    if 'TOUT' in t: cnt['TOUT COINCÉ']+=1; vrai.append(dict(cycle=n,rot=r,p=p,s=s,o=o,germe=l,type='TOUT')); continue
    if len(hw)==1 and hw[0].startswith('A104') and cyc:
        d=hw[0].split(':')[1]; qui='source' if st[0].startswith('A') else 'fourmi du piège'
        k=f'capture : 1 seule 104 ({qui} éjectée) + cycle exact'; cnt[k]+=1; par[n][d.rsplit(',',1)[0]]+=1
        vrai.append(dict(cycle=n,rot=r,p=p,s=s,periode=cyc,eject=d,qui=qui,o=o,germe=l,type='capture'))
    elif cyc is None and any(x=='B' for x in st): cnt['bornées sans cycle trouvé']+=1
    else: cnt[f'{len(hw)} autoroutes (ou X)']+=1
for k,v in cnt.most_common(): print(v,k)
for n,c in par.items(): print(n,'directions éjectées (dx,dy):',dict(c))
caps=[v for v in vrai if v['type']=='capture']
print('périodes du cycle final :',Counter(v['periode'] for v in caps).most_common(10))
for v in caps:
    if v['cycle']=='Petit Grain 8' and v['rot']==0: print('  PG r0 p',v['p'],'s',v['s'],'cycle',v['periode'],'éjection',v['eject'],v['qui'])
json.dump(vrai,open('pieges_vrais.json','w'),ensure_ascii=False,indent=1)

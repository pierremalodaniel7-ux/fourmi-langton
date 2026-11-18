import re,sys
from collections import defaultdict
cl=defaultdict(list)
for l in open(sys.argv[1]):
    f=l.split('|'); x,y=map(int,f[2].split(',')); k=y; j=x+k
    m=re.search(r'CERT (\d+) \|V\|=\d+ 104,(-?\d+),(-?\d+),',l)
    cl[(j,k%2)].append((k,int(m.group(1)),(int(m.group(2)),int(m.group(3)))))
for key in sorted(cl):
    L=sorted(cl[key]); k0,c0,_=L[0]
    dirs={r[2] for r in L}
    sl={(c-c0)/(k-k0) for k,c,_ in L[1:]}
    print(key,'k0',k0,'cert0',c0,'dir',dirs,'pente',sl)

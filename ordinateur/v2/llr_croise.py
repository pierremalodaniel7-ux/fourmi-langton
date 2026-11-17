# Piste 4 : en LLR, P (↘) traverse les traces de A (↙, λ≈1) et B (↙, λ≈65). Décalage de voie selon (a,b).
import subprocess
from collections import Counter, defaultdict
lines=[];meta=[]
for c in range(-121,-89):
    for k in range(4):
        s=-(abs(c)+80+k)
        if (s-c)%2: s-=1
        px,py=(c+s)//2,(s-c)//2
        for a in (0,1):
            for b in (0,1):
                ants=([f'0,0,H'] if a else [])+([f'32,32,H'] if b else [])+[f'{px},{py},G']
                lines.append('LLR|'+';'.join(ants)+'|'); meta.append((c,k,a,b))
p=subprocess.run(['./trapL'],input=''.join(f'{l} 30000\n' for l in lines),capture_output=True,text=True).stdout.strip().split('\n')
res=defaultdict(dict)
for m,o in zip(meta,p):
    t=o.split(); last=t[len([1 for z in m[2:] if z])] if not o.startswith('BORD') else 'BORD'
    res[(m[0],m[1])][(m[2],m[3])]=last
pat=Counter(); add=0; tot=0
for key,d in res.items():
    try:
        L={e:tuple(map(int,v.split(':')[1].split(','))) for e,v in d.items()}
    except Exception: pat['sale']+=1; continue
    base=L[(0,0)]
    sh=tuple((L[e][0],L[e][1],L[e][2]-base[2]) for e in [(0,1),(1,0),(1,1)])
    pat[sh]+=1; tot+=1
    if all(x[:2]==(1,1) for x in sh) and sh[2][2]==sh[0][2]+sh[1][2]: add+=1
for k,v in pat.most_common(10): print(v,k)
print('additif (même sens, décalage(a,b)=décalage(a)+décalage(b)) :',add,'/',tot)

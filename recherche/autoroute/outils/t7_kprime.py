#!/usr/bin/env python3
"""t7_kprime.py REC_K1_C3FIXE DIRECTIONS : critère de transport (lemme T', E2b §S11) pour les preuves « c₃ fixe » de la récurrence en k₁ :
règle non utilisée, NS = 1, c₂ touchée avant s₁ ; le long de m (f = d₂ ⟂ d) les lectures hors Δ après c₂ et la fenêtre finale s'éloignent de la
partie fixe de Δ₁ ; le long de m₃ (f = d₃ = −d, ou ⟂ d avec le même critère) c₃ est touchée après s₁+104. Sortie : data/t7/kprime.txt. (S11)"""
import re, subprocess, os, sys
from collections import Counter
AD='recherche/autoroute/ant'
D={}
for l in open(sys.argv[2]):
    w=l.split(); D[(w[0],w[1].split(';')[2])]=[(int(a),int(b)) for a,b in re.findall(r'\((-?\d+), (-?\d+)\)',' '.join(w[3:]))]
d=(-2,2); dot=lambda a,b:a[0]*b[0]+a[1]*b[1]
cnt=Counter(); out=open('data/t7/kprime.txt','w')
for l in open(sys.argv[1]):
    if 'deux:COUPLAGE' not in l: continue
    w=l.split(); n,J,K,CE,a,b=w[:6]; c3=w[6][3:]; T0=w[7][3:]; P=re.search(r'OK\[([^\]]*)\]',l).group(1).split()
    d2,d3=D[(n,c3)][0],D[(n,c3)][1]
    o=subprocess.run([AD,'multi',J,K,CE]+P+[a,b],capture_output=True,text=True,env=dict(os.environ,BASE=c3,T0=T0)).stdout.splitlines()[-1]
    g=lambda r: tuple(map(int,re.search(r,o).groups()))
    s1=int(re.search(r's1=(-?\d+)',o).group(1)) if 's1=' in o else -1
    tc2,tb,f0,f1,r0,r1,zl,zd=g(r'tc2=(-?\d+) tbase=(-?\d+) dfix=\[(-?\d+),(-?\d+)\] horsD_apres_c2=\[(-?\d+),(-?\d+)\] zlow=(\d) zd=(\d)')
    A0,A1=g(r'apres base=\[(-?\d+),(-?\d+)\]'); D0,D1=g(r'Delta1=\[(-?\d+),(-?\d+)\]'); rg=int(re.search(r'regle=(\d+)',o).group(1))
    E=1<<30
    def loin(x0,x1,y0,y1,f):          # plage [x0,x1] s'éloigne de [y0,y1] quand on translate de f (diag x+y, y bas : ±4)
        if x0>=E: return True           # plage vide
        s=f[0]+f[1]; return (s>0 and x0>y1) or (s<0 and x1<y0)
    # NB : dans ant, diag = x - y_haut = x + y_bas
    ok=[]
    ok.append(rg==0)
    ok.append(P[0]=='1')
    ok.append(0<=tc2<s1)
    # transport en m (f = d2) : d2 ⟂ d ; lectures hors Δ après c2 loin de la partie fixe ; Z par p (zlow) ou diagonales loin
    m_ok = dot(d2,d)==0 and loin(r0,r1,f0,f1,d2) and (zl==1 or loin(*g(r'diagZ=\[(-?\d+),(-?\d+)\]'),f0,f1,d2))
    # transport en m3 (f = d3) : c3 touchée après s1+104 ; d3 = -d (p diminue, diagonales fixes) ou d3 ⟂ d (lectures après c3 loin de Δ1)
    m3_ok = tb>s1+104 and (dot(d3,d)<0 or (dot(d3,d)==0 and loin(A0,A1,D0,D1,d3) and (zl==1 or loin(*g(r'diagZ=\[(-?\d+),(-?\d+)\]'),D0,D1,d3))))
    v='KP:ok' if all(ok) and m_ok and m3_ok else 'KP:non'
    why='' if v=='KP:ok' else ('regle' if not ok[0] else 'NS' if not ok[1] else 'tc2' if not ok[2] else 'm' if not m_ok else 'm3')
    cnt[(v,why)]+=1; out.write(f'{n} {J} {K} {CE} {a} {b} c3={c3} {v} {why}\n')
for k,v in cnt.most_common(): print(k,v)

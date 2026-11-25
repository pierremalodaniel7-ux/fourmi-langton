#!/usr/bin/env python3
"""honnete.py : pour chaque bascule idéalisée (toggle_hits.json), simulation COMPLÈTE dans un seul système :
fourmis [sonde 2, sonde 1, fourmis de la pièce] (ordre de jeu = celui des deux tirs idéalisés), cases = germe 1 + S0 + germe 2,
germe 2 sur la voie du tir 2, reculé de k périodes (k = K0..K0+K) pour arriver après le tir 1. Après T pas : résidu
près de la pièce = orbite S0 ? (à translation près, et en place). Calcul par src/fourmi (-dump)."""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bascule import orbite, situ_piece, G, E, dans
from moteur2 import charge, pas
os.environ.setdefault('CY','cycles2.json')
import recherche_lib as RL
S1L=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.environ.get('S1F','cyclesS1.json'))))
hits=json.load(open(sys.argv[1])); K0=int(sys.argv[2]); K=int(sys.argv[3]); TMP=f'/tmp/claude-0/h{os.getpid()}.dump'
def norm_frame(sit,p):
    turn,ants,noir=charge(sit); vis=set()
    for _ in range(p):
        for a in ants: vis.add((a[0],a[1]))
        pas(turn,ants,noir,range(len(ants)))
    return min(x for x,y in vis),min(y for x,y in vis)
res=[]
for h in hits:
    ic,s,tx,ty=h['S0'][:4]; A0,C0,p0=RL.piece0(ic,s); g1=(-tx,-ty)
    e=S1L[h['S1']]; mx,my=norm_frame(e['situation'],e['periode'])
    i2,s2,tx2,ty2=h['tir2'][:4]; g2=(-tx2+mx,-ty2+my)
    key0=orbite(A0,C0,p0); key0p=orbite(A0,C0,p0,pos=True)
    for k in range(K0,K0+K):
        G2=(g2[0]+2*k,g2[1]-2*k)
        ants=[(G2[0],G2[1],2),(g1[0],g1[1],2)]+A0
        cells=[(x+g1[0],y+g1[1]) for x,y in G]+C0+[(x+G2[0],y+G2[1]) for x,y in G]
        sit='RL|'+';'.join(f'{x},{y},{d}' for x,y,d in ants)+'|'+';'.join(f'{x},{y}' for x,y in cells)
        T=104*(k+60)+30000
        if os.path.exists(TMP): os.remove(TMP)
        subprocess.run([E,'-T',str(T),'-dump',TMP,sit],capture_output=True)
        d=open(TMP).read().strip().split('|')
        an=[tuple(map(int,a.split(','))) for a in d[-2].split(';')]
        ce={tuple(map(int,c.split(',')[:2])) for c in d[-1].split(';') if c}
        Ar=[a for a in an[2:] if dans(a[0],a[1])]; sorties=[a for a in an if not dans(a[0],a[1])]
        if len(Ar)!=len(A0): continue
        Cr=sorted(c for c in ce if dans(*c))
        o=subprocess.run([E,'-T','300000',situ_piece(Ar,Cr)],capture_output=True,text=True).stdout.split('|')
        if o[3]!='CYCLE': continue
        p=int(o[5])
        if p!=p0: continue
        same=orbite(Ar,Cr,p)==key0; samep=orbite(Ar,Cr,p,pos=True)==key0p
        if same:
            r={'hit':h,'k':k,'en_place':samep,'situation':sit,'T':T,'sondes_finales':[an[0],an[1]]}
            res.append(r); print(r['hit'],r['k'],r['en_place'],flush=True); break
print(len(res),'/',len(hits),'bascules honnêtes')
json.dump(res,open(sys.argv[1].replace('.json','_ok.json'),'w'))

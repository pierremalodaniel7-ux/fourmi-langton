# pas_llr.py — le pas complet de la petite fourmi compilé en UN germe LLR, vérifié sur les 256 états.
import compilateur as C, pas, json, sys, time
C.PAR.update(POFF=80,SP=30,DA=60)
NOMS=['c00','c10','c01','c11','x','y','h1','h0']
def etat(m):
    b=[(m>>i)&1 for i in range(8)]
    return dict(c={(0,0):b[0],(1,0):b[1],(0,1):b[2],(1,1):b[3]},x=b[4],y=b[5],h=2*b[6]+b[7])
def sortie(k):
    def f(m):
        t=pas.vrai_pas(etat(m)); v=[t['c'][(0,0)],t['c'][(1,0)],t['c'][(0,1)],t['c'][(1,1)],t['x'],t['y'],t['h']>>1,t['h']&1]
        return v[k]
    return f
S=[(n+"'",sortie(k)) for k,n in enumerate(NOMS)]
plan=None
if __name__=="__main__":
  plan=C.compile_(S,8,NOMS)
  nb1=len(plan['gates']); nb2=sum(1 for o in plan['outs'] if o['niv']==2); nray=sum(len(g['clause']) for g in plan['gates'])
  print(f'portes niv.1 : {nb1} ; niv.2 : {nb2} ; rayons-littéraux : {nray} ; T = {C.T_of(plan)}')
  for o in plan['outs']: print('  ',o['nom'],'niveau',o['niv'],'clauses',len(o['g']))
  t=time.time(); okc,N,T,res=C.verifie(plan,S,'C'); print('moteur C :',okc,'/',N,f'({time.time()-t:.0f} s)')
  par={n:sum(r[n]==int(bool(f(m))) for m,r in enumerate(res)) for n,f in S}; print('par sortie :',par)
  json.dump(dict(plan=plan,okC=okc,par=par,T=T),open('pas_llr.json','w'),default=str)

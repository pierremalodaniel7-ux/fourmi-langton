import json, sys, module as Mo, fourmis as F
M=json.load(open('module.json')); O=json.load(open('aiguillage_options.json'))
cls=sys.argv[1]; Lstar=int(sys.argv[2])
for br,cond in (("(1, 1)",{'c':1,'a':1}),("(1, 0, 1)",None),("(0, 1, 1)",None)):
    L2,c1,c2,ch,t0,h1,u2=O[br][cls]
    j=(Lstar-L2)//4; assert (Lstar-L2)%4==0 and j>=0, (br,L2)
    c2=[c2[0]+2*j,c2[1]+2*j]
    # cases d'aiguillage : inconditionnelles (posées sur le seul chemin de la feuille)
    M['K']['nodes'].append({'cell':c1,'cond':{},'br':'aig'+br})
    M['K']['nodes'].append({'cell':c2,'cond':{},'br':'aig'+br})
    print(br,"cases",c1,c2,"decalage",j,"periodes")
M['ray_out']=[Lstar,int(cls.strip('()').split(',')[1])]
json.dump(M,open('module.json','w'))

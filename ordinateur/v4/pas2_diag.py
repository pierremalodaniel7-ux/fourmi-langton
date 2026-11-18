import sys,subprocess; sys.argv=['x','0','1']
exec(open('pas2_creux.py').read().split("k,K=int")[0])
for m in [152,153,208,0]:
    o=subprocess.run(['./creux'],input=lines[m],capture_output=True,text=True).stdout.strip()
    r=lit(o,L[m]); t=o.split()[2:]
    print(m,[(n,r[n],int(bool(f(m))),t[L[m][n][0]],L[m][n]) for n,f in S2 if r[n]!=int(bool(f(m)))])
for o in plan['outs']: print(o['nom'],o['niv'],len(o['g']),o.get('L'),o.get('ws'))

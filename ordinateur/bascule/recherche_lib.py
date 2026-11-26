import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moteur2 import charge, pas
C2=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.environ.get('CY','cycles2.json'))))
def piece0(ic,s):
    c=C2[ic]; turn,ants,noir=charge(c['situation']); p=c['periode']; vis=set(); et=None
    for t in range(p):
        if t==s: et=([tuple(a) for a in ants],sorted(noir))
        for a in ants: vis.add((a[0],a[1]))
        pas(turn,ants,noir,range(len(ants)))
    mx=min(x for x,y in vis); my=min(y for x,y in vis)
    return [(x-mx,y-my,d) for x,y,d in et[0]],[(x-mx,y-my) for x,y in et[1]],p

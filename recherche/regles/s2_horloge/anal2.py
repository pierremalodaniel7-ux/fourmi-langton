import sys, json
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from anal import segs
H = json.load(open('resumes/horloges_6_fourmis.json'))
for h in H:
    o = segs(h['situation'], h['P'])
    print('n', h['n'], 'P', h['P'])
    for i in (0, 3):
        print('  ', i, [(k[0][0], k[1], k[2]-k[1]) for k in o[i] if k[2]-k[1] >= 16 and k[1] < h['P']//3 + 100])

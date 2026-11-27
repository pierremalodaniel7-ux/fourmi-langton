"""T2 — tri des étoiles décalées cycliques avec interaction (etoile180_*.json) : étendues, chocs A-B, « propres » (seuls événements
mixtes = chocs de 2 vaisseaux, un de A et un de B), portes à issue variable (t2_portes). Usage : python3 s2_horloge/e180_anal.py fichier.json"""
import sys, json, collections
sys.path.insert(0, '.'); sys.path.insert(0, 's2_horloge')
from hexa_anal import events
from t2_portes import analyse
H = json.load(open(sys.argv[1])); stats = collections.Counter(); keep = []
for h in H:
    k, box = events(h['sit'], h['P'])
    mixte = sum(v for (na, nb), v in k.items() if na and nb)
    propre = mixte > 0 and all((na + nb) <= 2 or not (na and nb) for (na, nb) in k)
    var = 0
    if propre:
        g, res = analyse(h['sit'], h['P'])
        var = sum(1 for r in res if len({x[2] for x in r['seq']}) == 2)
    stats[(mixte > 0, propre, var > 0)] += 1
    if propre: keep.append({**h, 'evenements': {'%d+%d' % kk: v for kk, v in k.items()}, 'boite': box, 'droites_variables': var})
print('(chocs A-B, propre, porte variable) :', dict(stats))
keep.sort(key=lambda h: (-h['droites_variables'] > 0, h['P']))
for h in keep[:12]: print(h['P0'], '->', h['P'], 's', h['s'], 'O2', h['O2'], 'boite', h['boite'], 'var', h['droites_variables'], h['evenements'])
json.dump(keep, open(sys.argv[1].replace('.json', '_propres.json'), 'w'))

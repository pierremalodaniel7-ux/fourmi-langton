import sys,json
sys.argv=['montage.py','185','0,5']
src=open('montage.py').read().split("choix=[(0,0)]")[0]
exec(src)
for a,dl in [(232,2),(240,-6),(236,4)]:
    print(a,dl,chrono(construit([(0,0),(a,dl)]),40000))

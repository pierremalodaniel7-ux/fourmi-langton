import sys; sys.path.insert(0,'.')
from moteur2 import *
turn,ants,noir=charge("RL|2,1,B;3,-5,H;5,2,B|")
for t in range(1,2133521):
    pas(turn,ants,noir,[0,1,2])
    if t%100000==0 or t in (1000,5000,20000,50000): print(t,[tuple(a) for a in ants],len(noir),flush=True)

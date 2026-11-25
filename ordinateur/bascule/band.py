import sys; sys.path.insert(0,'.')
from moteur2 import *
G="0,1;1,2;2,3;2,2;2,1;2,0;3,0;3,-1;2,-2;1,-2;-2,-1"
turn,ants,noir=charge("RL|0,0,B|"+G)
for t in range(1,104*60+1):
    pas(turn,ants,noir,[0])
    if t%1040==0: print(t,ants[0])

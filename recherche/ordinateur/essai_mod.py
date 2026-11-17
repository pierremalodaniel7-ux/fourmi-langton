import module as Mo, fourmis as F
for lane,At in ((-200,0),(-120,600)):
    b=Mo.approche(lane,At,(1,3))
    print(lane,At,"chaos",b[0],"seed",b[1][1],"virage",b[2],"h",b[3][1],b[3][2])

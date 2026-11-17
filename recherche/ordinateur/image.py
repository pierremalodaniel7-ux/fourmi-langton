# image.py N a b T sortie.png : image de l'état au pas T (vue d'ensemble réduite + zooms sur les modules)
import chaine as Ch, fourmis as F, numpy as np, ctypes, sys
from PIL import Image, ImageDraw
n,a,b,T=map(int,sys.argv[1:5]); out=sys.argv[5]
cells,ants,noms=Ch.germe_chaine(n,a,b)
nn,dh,xs,ys=F.simule_tout(cells,ants,T)
x0,y0,w,h=-1500,-11500,13500,4500+11500-3000
buf=np.zeros(w*h,np.uint8); F.L.region(x0,y0,w,h,buf.ctypes.data_as(ctypes.c_void_p)); g=buf.reshape(h,w)
k=12; hh,ww=h//k,w//k; red=g[:hh*k,:ww*k].reshape(hh,k,ww,k).max(axis=(1,3))
img=np.full((hh,ww,3),255,np.uint8); img[red>=1]=(120,120,120)
im=Image.fromarray(img); d=ImageDraw.Draw(im)
for m in range(n):
    ox,oy=m*Ch.VX,m*Ch.VY; px,py=(ox-x0)//k,(oy-y0)//k
    d.rectangle([px-60,py-60,px+60,py+40],outline=(200,0,0)); d.text((px-58,py-58),f"module {m}",fill=(200,0,0))
for i,(x,y) in enumerate(zip(xs[-1],ys[-1])):
    px,py=(x-x0)//k,(y-y0)//k; d.ellipse([px-4,py-4,px+4,py+4],fill=(0,0,220)); d.text((px+5,py),noms[i],fill=(0,0,220))
im.save(out); print("ok",out,im.size)

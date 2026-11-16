// auto2.c — autoroute RL synthétique (trace longue) + 1 case noire sur l'une des 22 cases neuves.
// Sortie : une ligne JSON par case. Directions 0=H 1=D 2=B 3=G, y vers le bas.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 8192
#define OFF 4096
#define P 104
#define RUN (P*200)
#define TRAIL 3000
static unsigned char S[W*W], G[W*W], R0[W*W], V[W*W], B0[W*W];
static const int dx[4]={0,1,0,-1}, dy[4]={-1,0,1,0};
typedef struct {int x,y,d;} Ant;
#define K(x,y) ((long)((y)+OFF)*W+((x)+OFF))
static int step(unsigned char*g, Ant*a){ long k=K(a->x,a->y); int c=g[k];
  a->d=(a->d+(c?3:1))&3; g[k]^=1; a->x+=dx[a->d]; a->y+=dy[a->d]; return c; }
static int out(Ant*a){return a->x<-OFF+3||a->x>OFF-4||a->y<-OFF+3||a->y>OFF-4;}
int main(int argc,char**argv){
  long LONG=argc>1?atol(argv[1]):3000000;
  // graine : bande u in [-300,4] de l'état T=40000, recentrée ; puis prolongée par périodicité
  Ant a={0,0,0}; for(long t=0;t<40000;t++) step(G,&a);
  for(int y=-400;y<=400;y++) for(int x=-400;x<=400;x++){ int X=a.x+x,Y=a.y+y; if(!G[K(X,Y)]) continue;
    int u=-x+y; if(u>=-300&&u<=4) S[K(x,y)]=1; }
  for(int y=-TRAIL-100;y<=100;y++) for(int x=-100;x<=TRAIL+100;x++){ int u=-x+y; if(u>=-200||u<-2*TRAIL) continue;
    int k=(-200-u)/4+1; int X=x-2*k, Y=y+2*k; if(S[K(X,Y)]) S[K(x,y)]=1; }
  Ant s0={0,0,a.d};
  memset(G,0,sizeof G); memcpy(G,S,sizeof S); Ant b=s0; long bad=-1; static unsigned char cs[1<<20];
  for(long t=0;t<200000;t++){cs[t&((1<<20)-1)]=step(G,&b); if(t>=P&&cs[t]!=cs[t-P]&&bad<0) bad=t;}
  fprintf(stderr,"validation 200000 pas : %s\n",bad<0?"autoroute parfaite":"CASSEE");
  memcpy(R0,S,sizeof S); Ant r=s0; for(int y=-TRAIL-100;y<=100;y++) for(int x=-100;x<=TRAIL+100;x++) if(S[K(x,y)]) V[K(x,y)]=1;
  for(int i=0;i<20*P;i++){V[K(r.x,r.y)]=1; step(R0,&r);}
  Ant w0=r; memcpy(B0,R0,sizeof R0);
  int rx[P],ry[P],rc[P],cx[P],cy[P],ct[P],nc=0;
  for(int i=0;i<P;i++){ long k=K(r.x,r.y); rx[i]=r.x; ry[i]=r.y; if(!V[k]){cx[nc]=r.x;cy[nc]=r.y;ct[nc]=i;nc++;} V[k]=1; rc[i]=step(R0,&r);}
  fprintf(stderr,"%d cases neuves ; fourmi en debut de fenetre (%d,%d) cap %d\n",nc,w0.x,w0.y,w0.d);
  for(int j=0;j<nc;j++){
    memcpy(G,B0,sizeof G); Ant e=w0; G[K(cx[j],cy[j])]=1;
    long t,run=0,hs=-1; int bx0,bx1,by0,by1;
    for(t=0;t<20000000;t++){ cs[t&((1<<20)-1)]=step(G,&e); if(out(&e)) break;
      if(t>=P&&cs[t&((1<<20)-1)]==cs[(t-P)&((1<<20)-1)]) run++; else run=0;
      if(run>=RUN){hs=t-run-P+1; t++; break;} }
    memcpy(G,B0,sizeof G); Ant f=w0; G[K(cx[j],cy[j])]=1; bx0=by0=1<<30; bx1=by1=-(1<<30);
    for(long u=0;u<t;u++){ if(u>=ct[j]&&u<=hs){ if(f.x<bx0)bx0=f.x; if(f.x>bx1)bx1=f.x; if(f.y<by0)by0=f.y; if(f.y>by1)by1=f.y; } step(G,&f);}
    Ant e2=e; static unsigned char T2[W*W]; memcpy(T2,G,sizeof G); int cc[P];
    for(int i=0;i<P;i++) cc[i]=step(T2,&e2);
    int Dx=e2.x-e.x, Dy=e2.y-e.y; long retard=0; int lat=0, phase=-1;
    if(Dx==-2&&Dy==2) for(int dl=0;dl<P;dl++){int ok=1; for(int i=0;i<P;i++) if(cc[i]!=rc[(i+dl)%P]){ok=0;break;}
      if(ok){phase=dl; int vx=e.x-rx[dl], vy=e.y-ry[dl]; lat=(vx+vy);
        long n=(-vx+vy)/4; retard=t-(dl+n*P); break;}}
    long tl, brk=-1;
    for(tl=0;tl<LONG;tl++){ cs[(t+tl)&((1<<20)-1)]=step(G,&e); if(out(&e)) break;
      if(cs[(t+tl)&((1<<20)-1)]!=cs[(t+tl-P)&((1<<20)-1)]){brk=t+tl;break;} }
    const char*fam = hs<0?"non_tranche": (Dx==-2&&Dy==2)?(lat==0?"meme_ligne":"ligne_decalee"):
                     (Dx==2&&Dy==2)?"virage_gauche":(Dx==-2&&Dy==-2)?"virage_droite":"demi_tour";
    printf("{\"n\":%d,\"dx\":%d,\"dy\":%d,\"pas_impact\":%d,\"famille\":\"%s\",\"debut_autoroute\":%ld,\"duree_chaos\":%ld,"
           "\"dir\":[%d,%d],\"retard\":%ld,\"decalage\":%d,\"boite\":[%d,%d],\"suivi\":%ld,\"cassure\":%ld}\n",
      j+1,cx[j]-w0.x,cy[j]-w0.y,ct[j],fam,hs,hs-ct[j],Dx,Dy,(phase>=0&&lat==0)?retard:0,lat,bx1-bx0+1,by1-by0+1,tl,brk);
    fflush(stdout);
  }
  return 0;
}

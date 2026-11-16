// two.c — autoroute (germe 11 cases, autoroute dès le pas 0) + 1 ou 2 cases noires sur les cases neuves.
// ./two 1        : les 22 cas à 1 case (contrôle R-16)
// ./two 2 DMAX   : paires (case i bloc J, case j bloc J+δ), δ=0..DMAX (δ=0 : i<j)
// Issue = (période, déplacement) final + pas de récupération (première détection stable après le choc).
#include "ant.h"
static int TIP[11][2]={{0,1},{1,2},{2,3},{2,2},{2,1},{2,0},{3,0},{3,-1},{2,-2},{1,-2},{-2,-1}};
static int NX[22],NY[22];
static Grid g;
static void run(int k,int*cx,int*cy,char*out){ g_clear(&g); for(int i=0;i<11;i++) g_set(&g,TIP[i][0],TIP[i][1],1);
  for(int i=0;i<k;i++) g_set(&g,cx[i],cy[i],1);
  Ant a; memset(&a,0,sizeof a); a.d=2; long tc=100*104; int lp=-1,ldx=0,ldy=0; long since=0;
  for(long t=1;t<=6000000;t++){ a_step(&g,&a);
    if(t>tc&&t%4096==0){ int dx,dy,p=a_period(&a,700,20,&dx,&dy);
      if(p&&p==lp&&dx==ldx&&dy==ldy){ if(t-since>60000){ sprintf(out,"%d (%d,%d) voie %d recup %ld",p,dx,dy,(a.x*dy-a.y*dx)/2,since-tc); return; } }
      else { lp=p; ldx=dx; ldy=dy; since=t; } } }
  sprintf(out,"indecis (%d)",lp); }
int main(int c,char**v){ g_init(&g,1<<22); int mode=atoi(v[1]);
  // cases neuves du bloc 30 (pas 3120..3223) : jamais visitées avant
  { g_clear(&g); for(int i=0;i<11;i++) g_set(&g,TIP[i][0],TIP[i][1],1); Grid vis; g_init(&vis,1<<16); Ant a; memset(&a,0,sizeof a); a.d=2; int n=0;
    for(long t=0;t<31*104;t++){ uint8_t*f=g_slot(&vis,KEY(a.x,a.y)); if(!*f&&t>=30*104){ NX[n]=a.x+2*(-70); NY[n]=a.y-2*(-70); n++; } *f=1; a_step(&g,&a); }
    if(n!=22){ printf("erreur : %d cases neuves\n",n); return 1; } } // décalées de 70 blocs : bloc 100, choc vers le pas 10 400
  char out[200];
  if(mode==1){ for(int i=0;i<22;i++){ int x[1]={NX[i]},y[1]={NY[i]}; run(1,x,y,out); printf("case %2d (%d,%d) : %s\n",i+1,NX[i],NY[i],out);} return 0; }
  int DM=atoi(v[2]);
  for(int d=0;d<=DM;d++) for(int i=0;i<22;i++) for(int j=(d?0:i+1);j<22;j++){ int x[2]={NX[i],NX[j]-2*d},y[2]={NY[i],NY[j]+2*d}; run(2,x,y,out);
    printf("d=%d i=%d j=%d : %s | points \"%d,%d;%d,%d\"\n",d,i+1,j+1,out,x[0],y[0],x[1],y[1]); fflush(stdout); }
}

// trap.c — pièges à autoroute (RL ou toute règle L/R, grille 8192², fourmis dans l'ordre).
// Entrée : "REGLE|fourmis|cases T" par ligne. Sortie : pour chaque fourmi "A dx,dy,voie" (autoroute de période P tenue 8 P)
// ou "B" (bornée : reste dans une boîte < 64 sur les 20 000 derniers pas) ; puis "CYC p" si l'état EXACT des fourmis bornées
// + couleurs de leur boîte (marge 3) revient en p ≤ 40000 pas (les autres fourmis sont loin), "NOCYC" sinon, "TOUT" si aucune autoroute.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 32768
#define O 16384
#define M(s) ((((s)%H)+H)%H)
static unsigned char G[W*W];
static int DX[4]={0,1,0,-1},DY[4]={-1,0,1,0};
static int n,ax[128],ay[128],ad[128],q,K[16];
static int *hx,*hy; static long H=200000;   // historique circulaire des positions
static void step(long t){ for(int i=0;i<n;i++){ int k=(ay[i]+O)*W+ax[i]+O; int c=G[k]; ad[i]=(ad[i]+K[c])&3; G[k]=(c+1)%q;
  ax[i]+=DX[ad[i]]; ay[i]+=DY[ad[i]]; hx[M(t)*128+i]=ax[i]; hy[M(t)*128+i]=ay[i]; } }
int main(){
  static char line[1<<20]; hx=malloc(sizeof(int)*128*H); hy=malloc(sizeof(int)*128*H);
  while(fgets(line,sizeof line,stdin)){
    char *p1=strchr(line,'|'); if(!p1) continue; *p1=0; char *p2=strchr(p1+1,'|'); *p2=0;
    char *sp=strrchr(p2+1,' '); long T=atol(sp+1); *sp=0;
    q=strlen(line); for(int i=0;i<q;i++) K[i]= line[i]=='R'?1: line[i]=='L'?3: line[i]=='U'?2:0;
    n=0; for(char *t=strtok(p1+1,";");t;t=strtok(NULL,";")){char c; if(sscanf(t," %d,%d,%c",&ax[n],&ay[n],&c)==3){ad[n]=c=='H'?0:c=='D'?1:c=='B'?2:3;n++;}}
    memset(G,0,sizeof G);
    for(char *t=strtok(p2+1,";");t;t=strtok(NULL,";")){int x,y; if(sscanf(t," %d,%d",&x,&y)==2) G[(y+O)*W+x+O]=1;}
    int bord=0; long t;
    for(t=0;t<T;t++){ step(t); for(int i=0;i<n;i++) if(ax[i]<-O+4||ax[i]>O-5||ay[i]<-O+4||ay[i]>O-5) bord=1; if(bord) break; }
    if(bord){ printf("BORD\n"); fflush(stdout); continue; }
    long e=T-1; int nb=0, bi[128], minx=1<<30,maxx=-(1<<30),miny=1<<30,maxy=-(1<<30), nhw=0;
    for(int i=0;i<n;i++){
      int x0=1<<30,x1=-(1<<30),y0=1<<30,y1=-(1<<30);
      for(long s=e;s>e-100000;s--){int x=hx[M(s)*128+i],y=hy[M(s)*128+i]; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y;}
      if(x1-x0<400&&y1-y0<400){ printf("B "); bi[nb++]=i; if(x0<minx)minx=x0; if(x1>maxx)maxx=x1; if(y0<miny)miny=y0; if(y1>maxy)maxy=y1; continue; }
      int P=0;
      for(int pp=1;pp<=2000&&!P;pp++){ int dx=hx[M(e)*128+i]-hx[M(e-pp)*128+i], dy=hy[M(e)*128+i]-hy[M(e-pp)*128+i]; if(!dx&&!dy) continue;
        int ok=1; for(long s=e;s>e-8*pp&&ok;s--) if(hx[M(s)*128+i]-hx[M(s-pp)*128+i]!=dx||hy[M(s)*128+i]-hy[M(s-pp)*128+i]!=dy) ok=0; if(ok) P=pp; }
      if(P){ int dx=hx[M(e)*128+i]-hx[M(e-P)*128+i], dy=hy[M(e)*128+i]-hy[M(e-P)*128+i];
        int u=1<<30; for(long r=e-P+1;r<=e;r++){int uu=(dx*dy>0)? hx[M(r)*128+i]-hy[M(r)*128+i] : hx[M(r)*128+i]+hy[M(r)*128+i]; if(uu<u)u=uu;}
        printf("A%d:%d,%d,%d ",P,dx,dy,u); nhw++; }
      else printf("X ");
    }
    if(nb){ minx-=3;maxx+=3;miny-=3;maxy+=3; int w=maxx-minx+1,h=maxy-miny+1;
      unsigned char *snap=malloc(w*h); int sx[128],sy[128],sd[128];
      for(int y=0;y<h;y++) for(int x=0;x<w;x++) snap[y*w+x]=G[(y+miny+O)*W+x+minx+O];
      for(int j=0;j<nb;j++){sx[j]=ax[bi[j]];sy[j]=ay[bi[j]];sd[j]=ad[bi[j]];}
      long per=0;
      for(long k=1;k<=150000&&!per;k++){ step(T+k); int same=1; int out=0; for(int i=0;i<n;i++) if(ax[i]<-O+4||ax[i]>O-5||ay[i]<-O+4||ay[i]>O-5) out=1; if(out){per=-1;break;}
        for(int j=0;j<nb&&same;j++) if(ax[bi[j]]!=sx[j]||ay[bi[j]]!=sy[j]||ad[bi[j]]!=sd[j]) same=0;
        if(same){ for(int y=0;y<h&&same;y++) for(int x=0;x<w;x++) if(G[(y+miny+O)*W+x+minx+O]!=snap[y*w+x]){same=0;break;} }
        if(same) per=k; }
      if(per>0) printf("CYC %ld boite %dx%d",per,w,h); else if(per<0) printf("BORDCYC"); else printf("NOCYC");
      if(per>0&&nhw==0) printf(" TOUT"); free(snap); }
    printf("\n"); fflush(stdout);
  }
}

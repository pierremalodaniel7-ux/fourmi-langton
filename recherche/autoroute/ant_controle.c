/* Fourmi de Langton classique (RL), code exact en entiers.
   Convention : blanc(0) -> tourne à droite, noir(1) -> tourne à gauche, on inverse la case, on avance.
   Détection d'autoroute (pratique) : la trace (couleurs lues) est périodique de période 104
   pendant NPER périodes, déplacement (±2,±2) par période, et la fourmi est à > MARGE cases
   (dans le sens de la dérive) de la boîte englobant tout ce qui a été touché avant le début
   de la phase périodique + le support initial.
   Usage :
     ./ant blank                      -> début d'autoroute depuis le blanc
     ./ant box N                      -> exhaustif : toutes les configs N×N (fourmi au coin bas-gauche, vers le haut)
     ./ant obst DIST                  -> collisions autoroute × 1 case noire isolée
     ./ant frozen                     -> longueur de la "boucle gelée" au cours du temps (CSV)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 4096
#define C (W/2)
#define P 104
#define NPER 20
#define MARGE 20
static unsigned char g[W*W];
static int dx[4]={0,1,0,-1}, dy[4]={1,0,-1,0}; /* 0=haut,1=droite,2=bas,3=gauche */
static short *px,*py; static unsigned char *tr;
typedef struct {long onset; int ddx,ddy; int ok; long steps;} Res;

static Res run(long maxs, int x0,int y0,int bx0,int by0,int bx1,int by1){
  /* bx0..bx1 : boîte du support initial (coordonnées relatives au centre) */
  Res r={-1,0,0,0,0}; int x=x0,y=y0,h=0; long t, runlen=0;
  for(t=0;t<maxs;t++){
    if(x<-C+2||x>C-3||y<-C+2||y>C-3){ r.steps=t; return r; }
    px[t]=x; py[t]=y;
    unsigned char *c=&g[(y+C)*W+(x+C)]; int col=*c; tr[t]=col;
    h = col? (h+3)&3 : (h+1)&3;   /* blanc: droite ; noir: gauche */
    *c^=1; x+=dx[h]; y+=dy[h];
    if(t>=P){ if(tr[t]==tr[t-P]) runlen++; else runlen=0; }
    if(runlen>=P*NPER && (t%P)==0){
      int ddx=x-px[t+1-P], ddy=y-py[t+1-P];
      if(abs(ddx)==2&&abs(ddy)==2){
        long on=t-runlen+1-P; int mx0=bx0,mx1=bx1,my0=by0,my1=by1;
        for(long s=0;s<=on;s++){ if(px[s]<mx0)mx0=px[s]; if(px[s]>mx1)mx1=px[s]; if(py[s]<my0)my0=py[s]; if(py[s]>my1)my1=py[s]; }
        int okx = ddx>0 ? x>mx1+MARGE : x<mx0-MARGE;
        int oky = ddy>0 ? y>my1+MARGE : y<my0-MARGE;
        if(okx&&oky){ r.onset=on; r.ddx=ddx; r.ddy=ddy; r.ok=1; r.steps=t; return r; }
      }
    }
  }
  r.steps=t; return r;
}
static void clear_box(int r){ for(int y=-r;y<=r;y++) memset(&g[(y+C)*W+(C-r)],0,2*r+1); }

int main(int argc,char**argv){
  long MAXS=4000000; px=malloc(MAXS*2); py=malloc(MAXS*2); tr=malloc(MAXS);
  if(!strcmp(argv[1],"blank")){
    Res r=run(MAXS,0,0,0,0,0,0);
    printf("blanc: autoroute=%d debut=%ld derive=(%d,%d) detectee_au_pas=%ld\n",r.ok,r.onset,r.ddx,r.ddy,r.steps);
  } else if(!strcmp(argv[1],"box")){
    int N=atoi(argv[2]); long tot=1L<<(N*N), nok=0, mx=0, argmx=0; long hist[64]={0};
    for(long m=0;m<tot;m++){
      for(int i=0;i<N*N;i++) g[(i/N+C)*W+(i%N+C)]=(m>>i)&1;
      Res r=run(MAXS,0,0,0,0,N-1,N-1);
      if(r.ok){ nok++; if(r.onset>mx){mx=r.onset;argmx=m;} int b=0; long v=r.onset; while(v>1){v>>=1;b++;} hist[b]++; }
      else printf("PAS D'AUTOROUTE detectee: masque=%ld (pas=%ld)\n",m,r.steps);
      clear_box(1500);
    }
    printf("box %dx%d: %ld/%ld autoroutes ; transitoire max=%ld (masque %ld)\n",N,N,nok,tot,mx,argmx);
    for(int b=0;b<64;b++) if(hist[b]) printf("  debut in [2^%d,2^%d): %ld\n",b,b+1,hist[b]);
  } else if(!strcmp(argv[1],"obst")){
    /* autoroute depuis le blanc : dérive d=(ddx,ddy). On place UNE case noire en p = d/2*k + décalage
       perpendiculaire j, avec k grand (loin du germe). Classes : j (x-y) et k mod 2 (x+y mod 4). */
    int D=atoi(argv[2]); Res r0=run(MAXS,0,0,0,0,0,0); clear_box(1500);
    int ux=r0.ddx/2, uy=r0.ddy/2; long n=0,nok=0;
    for(int j=-30;j<=30;j++) for(int k=D;k<D+2;k++){
      int ox=ux*k + j, oy=uy*k;   /* décalage perpendiculaire le long de x */
      g[(oy+C)*W+(ox+C)]=1;
      Res r=run(MAXS,0,0,ox<0?ox:0,oy<0?oy:0,ox>0?ox:0,oy>0?oy:0);
      n++; if(r.ok) nok++;
      printf("obst j=%d k=%d : autoroute=%d debut=%ld derive=(%d,%d)%s\n",j,k,r.ok,r.onset,r.ddx,r.ddy,
        (r.ok && (r.ddx!=r0.ddx||r.ddy!=r0.ddy))?"  <- direction changee":"");
      clear_box(1500);
    }
    printf("collisions: %ld/%ld se terminent par une autoroute\n",nok,n);
  } else if(!strcmp(argv[1],"frozen")){
    int x=0,y=0,h=0; printf("t,L\n");
    for(long t=0;t<14000;t++){
      if(t%20==0){ /* orbite gelée : même règle de virage, sans inverser les cases */
        int fx=x,fy=y,fh=h; long L=0;
        do{ int col=g[(fy+C)*W+(fx+C)]; fh= col?(fh+3)&3:(fh+1)&3; fx+=dx[fh]; fy+=dy[fh]; L++; }
        while(!(fx==x&&fy==y&&fh==h) && L<10000000);
        printf("%ld,%ld\n",t,L);
      }
      unsigned char *c=&g[(y+C)*W+(x+C)]; int col=*c; h= col?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
    }
  }
  return 0;
}

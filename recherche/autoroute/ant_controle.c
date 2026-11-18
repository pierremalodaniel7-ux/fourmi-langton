/* Fourmi de Langton classique (RL), code exact en entiers.
   Convention : blanc(0) -> tourne à droite, noir(1) -> tourne à gauche, on inverse la case, on avance.
   Détection d'autoroute (pratique) : la trace (couleurs lues) est périodique de période 104
   pendant NPER périodes, déplacement (±2,±2) par période, et la fourmi est à > MARGE cases
   (dans le sens de la dérive) de la boîte englobant tout ce qui a été touché avant le début
   de la phase périodique + le support initial.
   Usage :
     ./ant blank                      -> début d'autoroute depuis le blanc
     ./ant box N                      -> exhaustif : toutes les configs N×N (fourmi au coin bas-gauche, vers le haut)
     ./ant obst DIST                  -> collisions autoroute × 1 case noire isolée (DERNIERE autoroute : hors boite)
     ./ant obstf DIST                 -> idem, PREMIERE autoroute (sans critere de boite) + pas d'impact
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

static int NOBOX=0; static long IMPACT=-1; static int OBX=1<<30,OBY=0;
static Res run(long maxs, int x0,int y0,int bx0,int by0,int bx1,int by1){
  /* bx0..bx1 : boîte du support initial (coordonnées relatives au centre) */
  Res r={-1,0,0,0,0}; int x=x0,y=y0,h=0; long t, runlen=0;
  for(t=0;t<maxs;t++){
    if(x<-C+2||x>C-3||y<-C+2||y>C-3){ r.steps=t; return r; }
    px[t]=x; py[t]=y; if(IMPACT<0&&x==OBX&&y==OBY) IMPACT=t;
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
        if(NOBOX?(IMPACT>=0&&on>IMPACT):(okx&&oky)){ r.onset=on; r.ddx=ddx; r.ddy=ddy; r.ok=1; r.steps=t; return r; }
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
      if(argc>3) printf("m %ld %d %ld %d %d\n",m,r.ok,r.onset,r.ddx,r.ddy);
      if(r.ok){ nok++; if(r.onset>mx){mx=r.onset;argmx=m;} int b=0; long v=r.onset; while(v>1){v>>=1;b++;} hist[b]++; }
      else printf("PAS D'AUTOROUTE detectee: masque=%ld (pas=%ld)\n",m,r.steps);
      clear_box(1500);
    }
    printf("box %dx%d: %ld/%ld autoroutes ; transitoire max=%ld (masque %ld)\n",N,N,nok,tot,mx,argmx);
    for(int b=0;b<64;b++) if(hist[b]) printf("  debut in [2^%d,2^%d): %ld\n",b,b+1,hist[b]);
  } else if(!strcmp(argv[1],"obst")||!strcmp(argv[1],"obstf")){
    /* obstf : PREMIERE autoroute (pas de critere de boite), avec pas d'impact. */
    /* autoroute depuis le blanc : dérive d=(ddx,ddy). On place UNE case noire en p = d/2*k + décalage
       perpendiculaire j, avec k grand (loin du germe). Classes : j (x-y) et k mod 2 (x+y mod 4). */
    int D=atoi(argv[2]); Res r0=run(MAXS,0,0,0,0,0,0); clear_box(1500); NOBOX=!strcmp(argv[1],"obstf");
    int ux=r0.ddx/2, uy=r0.ddy/2; long n=0,nok=0;
    for(int j=-30;j<=30;j++) for(int k=D;k<D+2;k++){
      int ox=ux*k + j, oy=uy*k;   /* décalage perpendiculaire le long de x */
      g[(oy+C)*W+(ox+C)]=1; OBX=ox; OBY=oy; IMPACT=-1;
      Res r=run(MAXS,0,0,ox<0?ox:0,oy<0?oy:0,ox>0?ox:0,oy>0?oy:0);
      n++; if(r.ok) nok++;
      printf("obst j=%d k=%d : autoroute=%d debut=%ld derive=(%d,%d) impact=%ld chaos=%ld%s\n",j,k,r.ok,r.onset,r.ddx,r.ddy,IMPACT,IMPACT>=0?r.onset-IMPACT:-1,
        (r.ok && (r.ddx!=r0.ddx||r.ddy!=r0.ddy))?"  <- direction changee":"");
      clear_box(1500);
    }
    printf("collisions: %ld/%ld se terminent par une autoroute\n",nok,n);
  } else if(!strcmp(argv[1],"pmin")){
    /* pmin J K T : case noire en (J-K, K) (y vers le BAS, = (J-K,-K) ici). p = -x + y_bas = -x - y.
       maxpD : borne de p sur D ⊂ A1 ∪ (A0+d), A0 = cases touchées avant 9977, A1 = avant 9977+104 (départ blanc).
       minp : min de p sur les positions de la fourmi entre l'impact et T. Condition de récurrence : minp > maxpD - 4. */
    int J=atoi(argv[2]), K=atoi(argv[3]); long TT=atol(argv[4]);
    int x=0,y=0,h=0, mA0=-1000000, mA1=-1000000;
    for(long t=0;t<9977+104;t++){ int p=-x-y; if(t<9977&&p>mA0)mA0=p; if(p>mA1)mA1=p;
      unsigned char *c=&g[(y+C)*W+(x+C)]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h]; }
    int maxpD = mA1 > mA0+4 ? mA1 : mA0+4; clear_box(1500);
    int ox=J-K, oy=-K; g[(oy+C)*W+(ox+C)]=1; x=y=h=0; long imp=-1; int minp=1<<30;
    int ne=0, EXs[16], EYs[16];   /* cases en plus, décalages (EX,EY) en y vers le bas : argv[5..] par paires */
    for(int a=5;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); g[(oy-EYs[ne]+C)*W+(ox+EXs[ne]+C)]=1; ne++; }
    for(long t=0;t<=TT;t++){ int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1;
      if(hit&&imp<0) imp=t; if(imp>=0){int p=-x-y; if(p<minp)minp=p;}
      unsigned char *c=&g[(y+C)*W+(x+C)]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h]; }
    printf("pmin J=%d K=%d impact=%ld T=%ld maxpD=%d minp=%d %s\n",J,K,imp,TT,maxpD,minp, minp>maxpD-4?"OK":"ECHEC");
    clear_box(1500);
  } else if(!strcmp(argv[1],"uturn")){
    /* uturn J K PSTAR CERT : classe du demi-tour, case (J-K,K) en y vers le bas. p = -x - y (ici y vers le haut).
       s = premier instant après l'impact où p <= PSTAR. Vérifie U1..U4 (voir E2_epars.md). */
    int J=atoi(argv[2]), K=atoi(argv[3]), PS=atoi(argv[4]); long CE=atol(argv[5]);
    static unsigned char wr[W*W]; static int ws[P]; static unsigned char wc[P]; int nw=0;
    int ox=J-K, oy=-K; g[(oy+C)*W+(ox+C)]=1; int x=0,y=0,h=0; long imp=-1, s=-1;
    int ne=0, EXs[16], EYs[16];
    for(int a=6;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); g[(oy-EYs[ne]+C)*W+(ox+EXs[ne]+C)]=1; ne++; }
    int qa0=1<<30,qa1=-(1<<30),qz0=1<<30,qz1=-(1<<30); int L=1<<30, minS=1<<30, minU1=1<<30, sx=0,sy=0,sh=0, okFR=1, maxZ=-(1<<30), nfr=0; long badt=-1;
    for(long t=0;t<=CE+P;t++){
      int p=-x-y; long k=(long)(y+C)*W+(x+C);
      { int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1; if(hit&&imp<0) imp=t; }
      if(imp>=0&&s<0&&t>imp+P&&p<=PS){ s=t; sx=x; sy=y; sh=h; }
      if(imp>=0&&(s<0||t<s)&&p<L) L=p;                       /* L = min p sur [impact, s) */
      if(imp>=0&&(s<0||t<=s+P)&&p<minU1) minU1=p;              /* U1 */
      if(s>=0&&t>=s&&t<s+P){ if(p<minS)minS=p; if(!wr[k]){ int dej=0; for(int i=0;i<nw;i++) if(ws[i]==k){dej=1;break;} if(!dej){ wc[nw]=g[k]; ws[nw++]=(int)k; } } }
      if(s>=0&&t>=s+P&&!wr[k]){ int inW=0; for(int i=0;i<nw;i++) if(ws[i]==k){inW=1;break;}
        nfr++; if(!inW && p>=L){ okFR=0; if(badt<0) badt=t; } }   /* U4 lectures neuves */
      if(t>=CE&&p>maxZ) maxZ=p;
      { int qq=x-y; if(imp>=0&&(s<0||t<=s+P)){ if(qq<qa0)qa0=qq; if(qq>qa1)qa1=qq; } if(t>=CE){ if(qq<qz0)qz0=qq; if(qq>qz1)qz1=qq; } }
      if(s>=0&&t>=s) wr[k]=1;
      if(s>=0&&t==s+P){ /* U2 : position, cap */
        long sh_=(long)(y-sy)*W+(x-sx); int okW=1; for(int i=0;i<nw;i++) if(g[ws[i]+sh_]!=wc[i]) okW=0;
        printf("U2 : a(s+P)-a(s)=(%d,%d) cap %d->%d, fenetre |W|=%d recopiee : %s\n",x-sx,y-sy,sh,h,nw,okW?"OK":"ECHEC"); }
      unsigned char *c=&g[k]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
    }
    printf("uturn J=%d K=%d impact=%ld s=%ld L=%d minU1=%d (U1 %s) min[s,s+P]=%d (U3 %s) lectures_neuves=%d (U4 %s, 1er echec t=%ld) maxpZ=%d (Z %s) diag x+y : site [%d,%d] bande finale [%d,%d] %s\n",
      J,K,imp,s,L,minU1,minU1>21?"OK":"ECHEC",minS,minS>=L-4?"OK":"ECHEC",nfr,okFR?"OK":"ECHEC",badt,maxZ,maxZ<L?"OK":"ECHEC",-qa1,-qa0,-qz1,-qz0,(qz1<qa0||qz0>qa1)?"disjointes":"CHEVAUCHENT");
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

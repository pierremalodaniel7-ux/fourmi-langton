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

static int RH=0; /* cap initial de run (mode lot) */
static int NOBOX=0; static long IMPACT=-1; static int OBX=1<<30,OBY=0;
static Res run(long maxs, int x0,int y0,int bx0,int by0,int bx1,int by1){
  /* bx0..bx1 : boîte du support initial (coordonnées relatives au centre) */
  Res r={-1,0,0,0,0}; int x=x0,y=y0,h=RH; long t, runlen=0;
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


/* Configuration de base (S3) : BASE="x,y;x,y" (y vers le BAS) et T0 = instant où son autoroute (dérive (-2,+2) en y vers
   le bas) est certifiée. Par défaut : départ blanc, T0 = 9977. MPD = borne de p sur D (écart de translation de la base). */
static int NB=0, BXs[4096], BYs[4096]; static long T0=9977; static int MPD=25; static unsigned char DGD[2*W]; /* diagonales x-y(haut) de D */ static int H0=0; /* cap initial (0 H,1 D,2 B,3 G) */
static void place_base(void){ for(int i=0;i<NB;i++) g[(long)(BYs[i]+C)*W+(BXs[i]+C)]=1; }
static void setup_base(void){
  char *b=getenv("BASE"), *t=getenv("T0"), *hh=getenv("H0"); if(b&&*b&&t) T0=atol(t); if(hh) H0=atoi(hh)&3;
  if(b&&*b){ char buf[65536]; strncpy(buf,b,sizeof buf-1); buf[sizeof buf-1]=0;
    for(char *q=strtok(buf,";"); q&&NB<4096; q=strtok(NULL,";")){ char *c=strchr(q,','); if(!c) continue; BXs[NB]=atoi(q); BYs[NB]=-atoi(c+1); NB++; } }
  int mx=-(1<<30); for(int i=0;i<NB;i++){ int p=-BXs[i]-BYs[i]; if(p+4>mx) mx=p+4; DGD[BXs[i]-BYs[i]+W]=1; }
  place_base(); int x=0,y=0,h=H0;
  for(long u=0;u<T0+104;u++){ int p=-x-y; if(u<T0&&p+4>mx) mx=p+4; if(p>mx) mx=p; DGD[x-y+W]=1;
    unsigned char *c=&g[(long)(y+C)*W+(x+C)]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h]; }
  clear_box(2000); MPD=mx; if(NB) fprintf(stderr,"base : %d cases, T0=%ld, borne p sur D = %d\n",NB,T0,MPD);
}

int main(int argc,char**argv){
  long MAXS=4000000; px=malloc(MAXS*2); py=malloc(MAXS*2); tr=malloc(MAXS); setup_base();
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
    int qa0=1<<30,qa1=-(1<<30),qz0=1<<30,qz1=-(1<<30); static unsigned char DG[2*W]; memset(DG,0,sizeof DG); int zinD=0, frD=0;
    DG[ox-oy+W]=1; for(int e=0;e<ne;e++) DG[ox+EXs[e]-(oy-EYs[e])+W]=1;   /* Δ : diagonales x+y(bas) = x-y(haut) touchées */ int L=1<<30, minS=1<<30, minU1=1<<30, sx=0,sy=0,sh=0, okFR=1, maxZ=-(1<<30), nfr=0; long badt=-1;
    for(long t=0;t<=CE+P;t++){
      int p=-x-y; long k=(long)(y+C)*W+(x+C);
      { int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1; if(hit&&imp<0) imp=t; }
      if(imp>=0&&s<0&&t>imp+P&&p<=PS){ s=t; sx=x; sy=y; sh=h; }
      if(imp>=0&&(s<0||t<s)&&p<L) L=p;                       /* L = min p sur [impact, s) */
      if(imp>=0&&(s<0||t<=s+P)&&p<minU1) minU1=p;              /* U1 */
      if(s>=0&&t>=s&&t<s+P){ if(p<minS)minS=p; if(!wr[k]){ int dej=0; for(int i=0;i<nw;i++) if(ws[i]==k){dej=1;break;} if(!dej){ wc[nw]=g[k]; ws[nw++]=(int)k; } } }
      if(s>=0&&t>=s+P&&!wr[k]){ int inW=0; for(int i=0;i<nw;i++) if(ws[i]==k){inW=1;break;}
        nfr++; if(!inW && p>=L){ if(DG[x-y+W]){ okFR=0; if(badt<0) badt=t; } else frD++; } }   /* U4 lectures neuves */
      if(t>=CE&&p>maxZ) maxZ=p;
      if(t>=9977&&(s<0||t<=s+P)) DG[x-y+W]=1;
      if(t>=CE&&DG[x-y+W]) zinD=1;
      { int qq=x-y; if(imp>=0&&(s<0||t<=s+P)){ if(qq<qa0)qa0=qq; if(qq>qa1)qa1=qq; } if(t>=CE){ if(qq<qz0)qz0=qq; if(qq>qz1)qz1=qq; } }
      if(s>=0&&t>=s) wr[k]=1;
      if(s>=0&&t==s+P){ /* U2 : position, cap */
        long sh_=(long)(y-sy)*W+(x-sx); int okW=1; for(int i=0;i<nw;i++) if(g[ws[i]+sh_]!=wc[i]) okW=0;
        printf("U2 : a(s+P)-a(s)=(%d,%d) cap %d->%d, fenetre |W|=%d recopiee : %s\n",x-sx,y-sy,sh,h,nw,okW?"OK":"ECHEC"); }
      unsigned char *c=&g[k]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
    }
    printf("uturn J=%d K=%d impact=%ld s=%ld L=%d minU1=%d (U1 %s) min[s,s+P]=%d (U3 %s) lectures_neuves=%d (U4 %s, 1er echec t=%ld) maxpZ=%d (Z %s) diag x+y : site [%d,%d] bande finale [%d,%d] %s | fenetre finale hors Δ : %s, lectures p>=L hors Δ : %d\n",
      J,K,imp,s,L,minU1,minU1>21?"OK":"ECHEC",minS,minS>=L-4?"OK":"ECHEC",nfr,okFR?"OK":"ECHEC",badt,maxZ,maxZ<L?"OK":"ECHEC",-qa1,-qa0,-qz1,-qz0,(qz1<qa0||qz0>qa1)?"disjointes":"CHEVAUCHENT", zinD?"NON":"OUI", frD);
  } else if(!strcmp(argv[1],"triple")){
    /* triple J K CE P1 T1 P2 T2 L [EX EY ...] : site -> germe -> site (classes de pente 156). y vers le BAS pour J,K,EX,EY.
       s1 = 1er instant après impact+P où p <= P1 (rouleur vers le germe) ; s2 = 1er instant après s1 où p >= P2
       (rouleur qui revient). Conditions C1..C8 : voir E2_epars.md (triple couplage). */
    int J=atoi(argv[2]), K=atoi(argv[3]); long CE=atol(argv[4]); int P1=atoi(argv[5]); long T1=atol(argv[6]); int P2=atoi(argv[7]); long T2=atol(argv[8]); int LL=atoi(argv[9]); /* L imposé, validé en fin (C3) */
    int ne=0, EXs[16], EYs[16]; int ox=J-K, oy=-K; g[(oy+C)*W+(ox+C)]=1;
    for(int a=10;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); g[(oy-EYs[ne]+C)*W+(ox+EXs[ne]+C)]=1; ne++; }
    static unsigned char w1[W*W], w2[W*W], D1[2*W], D2[2*W]; static int ws1[P], ws2[P]; static unsigned char wc1[P], wc2[P];
    memset(D1,0,sizeof D1); memset(D2,0,sizeof D2);
    D1[ox-oy+W]=D2[ox-oy+W]=1; for(int e=0;e<ne;e++) D1[ox+EXs[e]-(oy-EYs[e])+W]=D2[ox+EXs[e]-(oy-EYs[e])+W]=1;
    int x=0,y=0,h=0, n1=0,n2=0, sx1=0,sy1=0,sh1=0,sx2=0,sy2=0,sh2=0; long imp=-1,s1=-1,s2=-1;
    int L=1<<30, minS1=1<<30, minC1=1<<30, Hm=-(1<<30), ok2=-1, ok5=-1, ok4=1, ok7=1, zA=1, zmin=1<<30, zoffD=1; long b4=-1,b7=-1;
    for(long t=0;t<=CE+P;t++){
      int p=-x-y; long k=(long)(y+C)*W+(x+C); int dg=x-y+W;
      { int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1; if(hit&&imp<0) imp=t; }
      if(imp>=0&&s1<0&&t>imp+P&&t>=T1&&p<=P1){ s1=t; sx1=x; sy1=y; sh1=h; }
      if(s1>=0&&s2<0&&t>s1+P&&t>=T2&&p>=P2){ s2=t; sx2=x; sy2=y; sh2=h; }
      if(t>=9977&&(s1<0||t<=s1+P)) D1[dg]=1;
      if(t>=9977&&(s2<0||t<=s2+P)) D2[dg]=1;
      if(imp>=0&&s1<0&&p<L) L=p;
      if(imp>=0&&(s1<0||t<=s1+P)&&p<minC1) minC1=p;
      if(s1>=0&&t>=s1&&t<=s1+P&&p<minS1) minS1=p;
      if(s1>=0&&t>=s1&&(s2<0||t<=s2+P)&&p>Hm) Hm=p;
      /* fenetre 1 */
      if(s1>=0&&t>=s1&&t<s1+P&&!w1[k]){ int dej=0; for(int i=0;i<n1;i++) if(ws1[i]==k){dej=1;break;} if(!dej){wc1[n1]=g[k]; ws1[n1++]=(int)k;} }
      /* C4 : lectures neuves (depuis s1) sur [s1+P, s2+2P] */
      if(s1>=0&&t>=s1+P&&(s2<0||t<=s2+2*P)&&!w1[k]){ int inW=0; for(int i=0;i<n1;i++) if(ws1[i]==k){inW=1;break;}
        if(!inW&&p>=LL&&D1[dg]){ ok4=0; if(b4<0)b4=t; } }
      /* fenetre 2 */
      if(s2>=0&&t>=s2&&t<s2+P&&!w2[k]){ int dej=0; for(int i=0;i<n2;i++) if(ws2[i]==k){dej=1;break;} if(!dej){wc2[n2]=g[k]; ws2[n2++]=(int)k;} }
      /* C7 : lectures neuves (depuis s2) après s2+P ; Hm complet seulement après s2+P */
      if(s2>=0&&t>=s2+P&&!w2[k]){ int inW=0; for(int i=0;i<n2;i++) if(ws2[i]==k){inW=1;break;}
        if(!inW&&p<=Hm+4-4&&D2[dg]){ ok7=0; if(b7<0)b7=t; } }
      if(t>=CE){ if(p<zmin)zmin=p; if(D2[dg]) zoffD=0; }
      if(s1>=0&&t>=s1) w1[k]=1;
      if(s2>=0&&t>=s2) w2[k]=1;
      if(s1>=0&&t==s1+P){ long sh_=(long)(y-sy1)*W+(x-sx1); ok2=(x-sx1==2&&y-sy1==2&&h==sh1); for(int i=0;i<n1;i++) if(g[ws1[i]+sh_]!=wc1[i]) ok2=0; }
      if(s2>=0&&t==s2+P){ long sh_=(long)(y-sy2)*W+(x-sx2); ok5=(x-sx2==-2&&y-sy2==-2&&h==sh2); for(int i=0;i<n2;i++) if(g[ws2[i]+sh_]!=wc2[i]) ok5=0; }
      unsigned char *c=&g[k]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
    }
    int Hs=Hm+4; int c1=minC1>21, c3=(L>=LL)&&(minS1+4>=LL);   /* L imposé = P1-8 doit être <= min p sur [impact,s1) et <= min[s1,s1+P]+4 */
    printf("triple J=%d K=%d impact=%ld s1=%ld s2=%ld L=%d(min %d, min[s1,s1+P]+4 %d) H*=%d C1 %s C2 %s C3 %s C4 %s(%ld) C5 %s C7 %s(%ld) Zmin=%d Zhorsdelta=%s\n",
      J,K,imp,s1,s2,LL,L,minS1+4,Hs,c1?"OK":"ECHEC",ok2==1?"OK":"ECHEC",c3?"OK":"ECHEC",ok4?"OK":"ECHEC",b4,ok5==1?"OK":"ECHEC",ok7?"OK":"ECHEC",b7,zmin,zoffD?"OUI":"NON");
    memset(w1,0,sizeof w1); memset(w2,0,sizeof w2);
  } else if(!strcmp(argv[1],"triple2")){
    /* triple2 J K CE P1 T1 P2 T2 L [EX EY ...] : triple couplage avec ensembles d'accord étendus par la règle
       « un pas de translation » + fermeture par chaînes (E2_epars.md, S2). y vers le BAS pour J,K,EX,EY.
       Ici (y vers le haut) d = (-2,-2), p = -x-y, p(d) = 4. */
    int J=atoi(argv[2]), K=atoi(argv[3]); long CE=atol(argv[4]); int P1=atoi(argv[5]); long T1=atol(argv[6]);
    int P2=atoi(argv[7]); long T2=atol(argv[8]); int LL=atoi(argv[9]);
    int ne=0, EXs[16], EYs[16]; int ox=J-K, oy=-K; g[(oy+C)*W+(ox+C)]=1;
    for(int a=10;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); g[(oy-EYs[ne]+C)*W+(ox+EXs[ne]+C)]=1; ne++; }
    static unsigned char sn1[W*W], sn2[W*W], to1[W*W], to2[W*W], tS[W*W], ws1m[W*W], ws2m[W*W], rd1[W*W], rd2[W*W];
    static unsigned char D1[2*W], D2[2*W]; static int ws1[P], ws2[P]; static unsigned char wc1[P], wc2[P];
    memset(D1,0,sizeof D1); memset(D2,0,sizeof D2);
    D1[ox-oy+W]=D2[ox-oy+W]=1; for(int e=0;e<ne;e++) D1[ox+EXs[e]-(oy-EYs[e])+W]=D2[ox+EXs[e]-(oy-EYs[e])+W]=1;
    long DD=-2L*W-2;   /* indice de c+d (d=(-2,-2)) : k + DD ; c-d : k - DD */
    int x=0,y=0,h=0,n1=0,n2=0,sx1=0,sy1=0,sh1=0,sx2=0,sy2=0,sh2=0; long imp=-1,s1=-1,s2=-1;
    int L=1<<30,minS1=1<<30,minC1=1<<30,Hm=-(1<<30),ok2=-1,ok5=-1,ok4=1,ok7=1,okZ=1; long b4=-1,b7=-1,bz=-1; int zx0=0,zy0=0,zx1=0,zy1=0,zp=1,zd=1,germ=0;
    #define PK(kk) ((int)(-( ((kk)%W) - C ) - ( ((kk)/W) - C )))
    #define DGK(kk) ((int)((((kk)%W)-C) - (((kk)/W)-C) + W))
    for(long t=0;t<=CE+P;t++){
      int p=-x-y; long k=(long)(y+C)*W+(x+C);
      { int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1; if(hit&&imp<0) imp=t; }
      if(imp>=0&&s1<0&&t>imp+P&&t>=T1&&p<=P1){ s1=t; sx1=x; sy1=y; sh1=h; memcpy(sn1,g,sizeof sn1); }
      if(s1>=0&&p<=25) germ=1;   /* s2 seulement après passage au germe */
      if(s1>=0&&s2<0&&germ&&t>s1+P&&t>=T2&&p>=P2){ s2=t; sx2=x; sy2=y; sh2=h; memcpy(sn2,g,sizeof sn2); }
      if(t>=9977&&(s1<0||t<=s1+P)) D1[x-y+W]=1;
      if(t>=9977&&(s2<0||t<=s2+P)) D2[x-y+W]=1;
      if(imp>=0&&s1<0&&p<L) L=p;
      if(imp>=0&&(s1<0||t<=s1+P)&&p<minC1) minC1=p;
      if(s1>=0&&t>=s1&&t<=s1+P&&p<minS1) minS1=p;
      if(s1>=0&&t>=s1&&(s2<0||t<=s2+P)&&p>Hm) Hm=p;
      if(s1>=0&&t>=s1&&t<s1+P){ to1[k]=1; if(!rd1[k]){ if(!ws1m[k]){ ws1m[k]=1; wc1[n1]=g[k]; ws1[n1++]=(int)k; } } }
      if(s2>=0&&t>=s2&&t<s2+P){ to2[k]=1; if(!rd2[k]){ if(!ws2m[k]){ ws2m[k]=1; wc2[n2]=g[k]; ws2[n2++]=(int)k; } } }
      /* C4 : lectures neuves depuis s1, sur [s1+P, s2+2P], dans l'ensemble d'accord G */
      if(s1>=0&&t>=s1+P&&(s2<0||t<=s2+2*P)&&!rd1[k]){
        long c=k; int in=0; for(int it=0;it<100000;it++){ int pc=PK(c);
          if(pc<LL||ws1m[c]||!D1[DGK(c)]){in=1;break;}
          if(pc<=25) break; long cm=c-DD; if(to1[cm]) break; if(sn1[cm]!=sn1[c]) break; c=cm; }
        if(!in){ ok4=0; if(b4<0)b4=t; } }
      /* C7 : lectures neuves depuis s2, après s2+P, dans l'ensemble d'accord A2 */
      if(s2>=0&&t>=s2+P&&!rd2[k]){
        long c=k; int in=0; for(int it=0;it<100000;it++){ int pc=PK(c);
          if(pc>Hm||ws2m[c]||!D2[DGK(c)]){in=1;break;}
          long cp=c+DD; if(PK(cp)<=25) break; if(to2[cp]) break; if(sn2[cp]!=sn2[c]) break;
          /* c et c+d dans GA = (accord G) ou touchées sur [s1,s2] */
          int gaok=1; long q2[2]={c,cp}; for(int u=0;u<2&&gaok;u++){ long z=q2[u]; if(tS[z]) continue; int inz=0;
            for(int it2=0;it2<100000;it2++){ int pz=PK(z); if(pz<LL||ws1m[z]||!D1[DGK(z)]){inz=1;break;}
              if(pz<=25) break; long zm=z-DD; if(to1[zm]) break; if(sn1[zm]!=sn1[z]) break; z=zm; }
            if(!inz) gaok=0; }
          if(!gaok) break; c=cp; }
        if(!in){ ok7=0; if(b7<0)b7=t; } }
      if(t==CE){ zx0=x; zy0=y; } if(t==CE+P){ zx1=x; zy1=y; }
      if(t>=CE){ /* Z : fenêtre finale ; règle selon la direction finale (décidée en fin) */
        int pc=PK(k); if(!(pc>Hm)) zp=0; if(D2[DGK(k)]) zd=0; }
      if(s1>=0&&t>=s1) rd1[k]=1;
      if(s2>=0&&t>=s2) rd2[k]=1;
      if(s1>=0&&t>=s1&&(s2<0||t<=s2)) tS[k]=1;
      if(s1>=0&&t==s1+P){ long sh_=(long)(y-sy1)*W+(x-sx1); ok2=(x-sx1==2&&y-sy1==2&&h==sh1); for(int i=0;i<n1;i++) if(g[ws1[i]+sh_]!=wc1[i]) ok2=0; }
      if(s2>=0&&t==s2+P){ long sh_=(long)(y-sy2)*W+(x-sx2); ok5=(x-sx2==-2&&y-sy2==-2&&h==sh2); for(int i=0;i<n2;i++) if(g[ws2[i]+sh_]!=wc2[i]) ok5=0; }
      unsigned char *cc=&g[k]; h=*cc?(h+3)&3:(h+1)&3; *cc^=1; x+=dx[h]; y+=dy[h];
    }
    int c1=minC1>21, c3=(L>=LL)&&(minS1+4>=LL);
    { int fx=zx1-zx0, fy=zy1-zy0;   /* déplacement sur [CE, CE+P+1) ~ direction finale ; ici d=(-2,-2) */
      int moinsd=(fx==2&&fy==2), plusd=(fx==-2&&fy==-2);
      /* p ne décroît pas (perp. ou +d) : toutes les cases de Z ont p >= min fenêtre -> zp suffit ;
         -d : p décroît, x-y conservé -> il faut zd (diagonales hors Δ2) ; +d : zd suffit aussi */
      okZ = moinsd ? zd : (zp || (plusd && zd)); bz = fx*100+fy; }
    printf("triple2 J=%d K=%d s1=%ld s2=%ld L=%d Hm=%d C1 %s C2 %s C3 %s C4 %s(%ld) C5 %s C7 %s(%ld) Z %s(dep %ld)\n",J,K,s1,s2,LL,Hm,
      c1?"OK":"ECHEC",ok2==1?"OK":"ECHEC",c3?"OK":"ECHEC",ok4?"OK":"ECHEC",b4,ok5==1?"OK":"ECHEC",ok7?"OK":"ECHEC",b7,okZ?"OK":"ECHEC",bz);
  } else if(!strcmp(argv[1],"multi")){
    /* multi J K CE NS P1..PNS [EX EY ...] : NS changements de repère alternés (impair : vers le germe, repère identité ;
       pair : vers le site, repère translation). Généralise triple2 (NS=2). Voir E2_epars.md (S2). y vers le BAS. */
    int J=atoi(argv[2]), K=atoi(argv[3]); long CE=atol(argv[4]); int NS=atoi(argv[5]); int PT[8];
    for(int i=1;i<=NS;i++) PT[i]=atoi(argv[5+i]);
    int ne=0, EXs[16], EYs[16]; int ox=J-K, oy=-K; place_base(); g[(oy+C)*W+(ox+C)]=1;
    for(int a=6+NS;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); g[(oy-EYs[ne]+C)*W+(ox+EXs[ne]+C)]=1; ne++; }
    unsigned char *SN[8],*TO[8],*TP[8],*WM[8],*RD[8],*DGs[8]; static int ws[8][P]; static unsigned char wc[8][P]; int nw[8]={0};
    for(int i=1;i<=NS;i++){ SN[i]=calloc(W*W,1); TO[i]=calloc(W*W,1); TP[i]=calloc(W*W,1); WM[i]=calloc(W*W,1); RD[i]=calloc(W*W,1); DGs[i]=calloc(2*W,1); if(i%2==0) memcpy(DGs[i],DGD,2*W);   /* repère translation (i pair) : Δ_i contient aussi les diagonales de D (germe/base) */
      DGs[i][ox-oy+W]=1; for(int e=0;e<ne;e++) DGs[i][ox+EXs[e]-(oy-EYs[e])+W]=1; }
    long DD=-2L*W-2; long sT[8]; int sx[8],sy[8],sh[8],LV[8],HV[8],minS[8],okR[8],okC[8]; long bC[8];
    /* S10 (R-122) : en repère identité, l'accord « p < L » suppose que les cases de l'îlot ont p ≥ L (dans les deux mondes) ;
       sinon (case de l'îlot à petit p, ex. c3 sur une autre bande) l'accord est faux. pI = plus petit p des cases de l'îlot. */
    int pI = -ox-oy; for(int e=0;e<ne;e++){ int pe = -(ox+EXs[e])-(oy-EYs[e]); if(pe<pI) pI=pe; }
    for(int i=0;i<8;i++){ sT[i]=-1; LV[i]=1<<30; HV[i]=-(1<<30); minS[i]=1<<30; okR[i]=-1; okC[i]=1; bC[i]=-1; }
    int x=0,y=0,h=H0,minC1=1<<30,reachG=0,reachS=0,cur=0; long imp=-1; int zx0=0,zy0=0,zx1=0,zy1=0,zlow=1,zhigh=1,zd=1,zd0=1,zq0=1<<30,zq1=-(1<<30);
    #define PKm(kk) ((int)(-( ((kk)%W) - C ) - ( ((kk)/W) - C )))
    #define DGm(kk) ((int)((((kk)%W)-C) - (((kk)/W)-C) + W))
    /* appartenance à l'ensemble d'accord du changement i (récursif sur i, chaînes) */
    long nacc[5]={0,0,0,0,0}; int lastwhy=0, hq0=1<<30, hq1=-(1<<30), gq0=1<<30, gq1=-(1<<30); long tbase=-1; long tc2=-1, tlast=-1; int fx0=1<<30,fx1=-(1<<30),ra0=1<<30,ra1=-(1<<30),rl0=1<<30,rl1=-(1<<30); /* S11 : tc2 = 1er contact avec la 2e case de l'îlot, dfix = diagonales des positions avant tc2, lectures hors Δ après tc2 */ /* 1er contact avec une case de la base */   /* 1 fenêtre, 2 hors Δ, 3 base p, 4 règle */
    auto int agree(int i,long c);
    int touchedphase(int i,long c){ return i>=1 && TP[i][c]; }
    int A(int j,long c){ return agree(j,c)||touchedphase(j,c); }
    int agree(int i,long c){
      for(int it=0;it<200000;it++){
        int pc=PKm(c);
        if(WM[i][c]){ if(!lastwhy) lastwhy=it?4:1; return 1; }
        if(!DGs[i][DGm(c)]){ if(!lastwhy) lastwhy=it?4:2; return 1; }
        if(i%2){ if(pc<LV[i] && (i==1 || A(i-2,c))){ if(!lastwhy) lastwhy=it?4:3; return 1; }
                 if(pc<=MPD) return 0; long n=c-DD; if(TO[i][n]) return 0; if(SN[i][n]!=SN[i][c]) return 0;
                 if(i>1){ if(!A(i-1,n)) return 0; if(!A(i-1,c)) return 0; }
                 c=n; }
        else { if(pc>HV[i] && (i==2 ? PKm(c+DD)>MPD : A(i-2,c))){ if(!lastwhy) lastwhy=it?4:3; return 1; }
               long n=c+DD; if(TO[i][n]) return 0; if(SN[i][n]!=SN[i][c]) return 0;
               if(!A(i-1,n)) return 0; if(!A(i-1,c)) return 0;
               c=n; }
      } return 0; }
    for(long t=0;t<=CE+P;t++){
      int p=-x-y; long k=(long)(y+C)*W+(x+C);
      { int hit=(x==ox&&y==oy); for(int e=0;e<ne;e++) if(x==ox+EXs[e]&&y==oy-EYs[e]) hit=1; if(hit&&imp<0) imp=t; }
      if(tbase<0) for(int b=0;b<NB;b++) if(x==BXs[b]&&y==BYs[b]) tbase=t;
      if(ne>0 && tc2<0 && x==ox+EXs[0] && y==oy-EYs[0]) tc2=t;
      if(NB>0 && tlast<0 && x==BXs[NB-1] && y==BYs[NB-1]) tlast=t;
      if(t>=T0 && tc2<0){ int q=x-y; if(q<fx0)fx0=q; if(q>fx1)fx1=q; }
      if(imp>=0 && cur<NS){ int i=cur+1;
        if(p<=MPD) reachG=1; if(p>=PT[i>1?i-1:1]+60) reachS=1;
        long prev = cur? sT[cur] : imp;
        int trig = (i%2) ? (p<=PT[i] && (i==1 || reachS)) : (p>=PT[i] && reachG);
        if(t>prev+P && trig){ cur=i; sT[i]=t; sx[i]=x; sy[i]=y; sh[i]=h; memcpy(SN[i],g,(size_t)W*W); reachG=reachS=0; } }
      for(int i=1;i<=NS;i++) if(t>=T0 && (sT[i]<0 || t<=sT[i]+P)) DGs[i][x-y+W]=1;
      if(imp>=0 && cur==0 && p<minC1) minC1=p;
      if(cur>=1 && t<=sT[1]+P && p<minC1) minC1=p;
      /* L_i, H_i */
      for(int i=1;i<=NS;i++){ long a0 = (i==1? imp : sT[i-1]); if(a0<0) continue;
        if(i%2){ if(t>=a0 && (sT[i]<0||t<sT[i]) && p<LV[i]) LV[i]=p; if(sT[i]>=0&&t>=sT[i]&&t<=sT[i]+P&&p<minS[i]) minS[i]=p; }
        else { if(t>=a0 && (sT[i]<0 || t<=sT[i]+P) && p>HV[i]) HV[i]=p; } }
      /* fenêtres, touchées */
      for(int i=1;i<=NS;i++) if(sT[i]>=0){
        if(t>=sT[i]&&t<sT[i]+P){ TO[i][k]=1; if(!RD[i][k]&&!WM[i][k]){ WM[i][k]=1; wc[i][nw[i]]=g[k]; ws[i][nw[i]++]=(int)k; } }
        long fin = (i<NS && sT[i+1]>=0) ? sT[i+1] : -1;
        if(t>=sT[i] && (fin<0 || t<=fin)) { }
      }
      /* lectures neuves de la phase cur (après s_cur+P), jusqu'à s_{cur+1}+2P */
      for(int i=1;i<=NS;i++) if(sT[i]>=0 && t>=sT[i]+P && !RD[i][k]){
        long lim = (i<NS) ? (sT[i+1]>=0 ? sT[i+1]+2*P : -2) : CE+P; if(lim!=-2 && t>lim) continue;
        if(i%2){ if(LV[i]>minS[i]+4) LV[i]=minS[i]+4; if(LV[i]>pI) LV[i]=pI; }
        lastwhy=0; if(!agree(i,k)){ okC[i]=0; if(bC[i]<0)bC[i]=t; } else { nacc[lastwhy]++; if(lastwhy==2){ int q=DGm(k)-W; if(tc2>=0){ if(q<ra0)ra0=q; if(q>ra1)ra1=q; } if(tlast>=0){ if(q<rl0)rl0=q; if(q>rl1)rl1=q; } if(tbase>=0){ if(q<gq0)gq0=q; if(q>gq1)gq1=q; } else { if(q<hq0)hq0=q; if(q>hq1)hq1=q; } } } }
      if(t==CE){ zx0=x; zy0=y; } if(t==CE+P){ zx1=x; zy1=y; }
      if(t>=CE){ int pc=PKm(k); if(NS==0){ if(!(pc>MPD-4)) zhigh=0; } else if(NS%2){ if(!(pc<LV[NS] && (NS==1 || pc<LV[NS-2]))) zlow=0; } else { if(!(pc>HV[NS] && (NS==2 || pc>HV[NS-2]))) zhigh=0; } if(NS>0 && DGs[NS][DGm(k)]) zd=0; if(DGD[DGm(k)]) zd0=0; { int q=DGm(k)-W; if(q<zq0)zq0=q; if(q>zq1)zq1=q; } }
      for(int i=1;i<=NS;i++) if(sT[i]>=0 && t>=sT[i]){ RD[i][k]=1; long fin=(i<NS)?sT[i+1]:-1; if(fin<0 || t<=fin) TP[i][k]=1; }
      for(int i=1;i<=NS;i++) if(sT[i]>=0 && t==sT[i]+P){ int ex=(i%2)?2:-2; long sh_=(long)(y-sy[i])*W+(x-sx[i]);
        okR[i]=(x-sx[i]==ex&&y-sy[i]==ex&&h==sh[i]); for(int q=0;q<nw[i];q++) if(g[ws[i][q]+sh_]!=wc[i][q]) okR[i]=0; }
      unsigned char *cc=&g[k]; h=*cc?(h+3)&3:(h+1)&3; *cc^=1; x+=dx[h]; y+=dy[h];
    }
    int fx=zx1-zx0, fy=zy1-zy0; int moinsd=(fx==2&&fy==2), plusd=(fx==-2&&fy==-2); int okZ;
    if(NS%2) okZ = plusd ? zd : (zlow || (moinsd && zd));   /* repère identité (germe) : p ne croît pas -> p<L suffit */
    else if(NS==0) okZ = moinsd ? zd0 : zhigh;   /* phase 0 : -d -> diagonales de Z hors de celles de D ; sinon p > MPD-4 */
    else okZ = moinsd ? zd : (zhigh || (plusd && zd));
    int all = (minC1>MPD-4) && okZ; printf("multi J=%d K=%d NS=%d C1 %s",J,K,NS,minC1>MPD-4?"OK":"ECHEC");
    for(int i=1;i<=NS;i++){ int c3 = (i%2)? 1 : 1; all = all && okR[i]==1 && okC[i];
      printf(" | s%d=%ld %s R %s lect %s(%ld)",i,sT[i],(i%2)?"L":"H",okR[i]==1?"OK":"ECHEC",okC[i]?"OK":"ECHEC",bC[i]); (void)c3; }
    { int d0=1<<30,d1=-(1<<30); for(int q=0;q<2*W;q++) if(DGD[q]){ if(q-W<d0)d0=q-W; if(q-W>d1)d1=q-W; }
      { int q1=ox-oy; if(q1<fx0)fx0=q1; if(q1>fx1)fx1=q1; } printf(" | DEV tc2=%ld tbase=%ld dfix=[%d,%d] horsD_apres_c2=[%d,%d] zlow=%d zd=%d tlast=%ld horsD_apres_last=[%d,%d]",tc2,tbase,fx0,fx1,ra0,ra1,zlow,zd,tlast,rl0,rl1);
      printf(" | acc fen=%ld horsD=%ld p=%ld regle=%ld",nacc[1],nacc[2],nacc[3],nacc[4]); { int a0=1<<30,a1=-(1<<30); if(NS>=1) for(int q=0;q<2*W;q++) if(DGs[1][q]){ if(q-W<a0)a0=q-W; if(q-W>a1)a1=q-W; } printf(" | horsD diag avant base=[%d,%d] apres base=[%d,%d] Delta1=[%d,%d]",hq0,hq1,gq0,gq1,a0,a1); } printf(" | L1=%d L3=%d | dir=(%d,%d) diagZ=[%d,%d] diagD=[%d,%d] | Z %s => %s\n", LV[1], NS>=3?LV[3]:0, fx,fy, zq0,zq1,d0,d1, okZ?"OK":"ECHEC", all?"TOUT OK":"ECHEC"); }
  } else if(!strcmp(argv[1],"deux")){
    /* deux J K CE NS s1..sNS [EX EY ...] : contrôle DIRECT des couplages de `multi` entre X_k et X_{k+2}.
       Phase i (s_i <= t < s_{i+1}, s_0 = 9977) : X_{k+2} au temps t + 104(i+1) doit avoir la fourmi en a_k(t) + (i pair ? d : 0),
       même cap, et lire la même couleur. Vérifié pour t de 9977 à CE+P. y vers le BAS pour J,K,EX,EY ; ici d = (-2,-2). */
    int J=atoi(argv[2]), K=atoi(argv[3]); long CE=atol(argv[4]); int NS=atoi(argv[5]); long sw[10]; sw[0]=T0;
    for(int i=1;i<=NS;i++) sw[i]=atol(argv[5+i]);
    int ne=0, EXs[16], EYs[16]; for(int a=6+NS;a+1<argc&&ne<16;a+=2){ EXs[ne]=atoi(argv[a]); EYs[ne]=atoi(argv[a+1]); ne++; }
    long TB = CE + P + 104L*(NS+1) + 1; int *bx=malloc(TB*sizeof(int)), *by=malloc(TB*sizeof(int)); unsigned char *bh=malloc(TB), *bc=malloc(TB);
    for(int w=0; w<2; w++){
      int ox=J-K-(w?0:2), oy=-K-(w?0:2); place_base(); g[(oy+C)*W+(ox+C)]=1; for(int e=0;e<ne;e++) g[(oy-EYs[e]+C)*W+(ox+EXs[e]+C)]=1;
      int x=0,y=0,h=H0; long bad=-1, nchk=0;
      long TT = w==0 ? TB : CE+P+1;
      for(long t=0;t<TT;t++){
        unsigned char *c=&g[(long)(y+C)*W+(x+C)]; int col=*c;
        if(w==0){ bx[t]=x; by[t]=y; bh[t]=h; bc[t]=col; }
        else if(t>=T0){ int i=0; while(i<NS && t>=sw[i+1]) i++; long tb=t+104L*(i+1); int ex=(i%2==0)?-2:0;
          nchk++; if(!(bx[tb]==x+ex && by[tb]==y+ex && bh[tb]==h && bc[tb]==col) && bad<0) bad=t; }
        h=col?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
      }
      clear_box(2000);
      if(w==1) printf("deux J=%d K=%d NS=%d : %ld pas comparés, %s (1er écart t=%ld)\n",J,K,NS,nchk,bad<0?"COUPLAGE EXACT":"ECART",bad);
    }
    free(bx); free(by); free(bh); free(bc);
  } else if(!strcmp(argv[1],"lot")){
    /* lot : lignes « RL|0,0,CAP|x,y;x,y… » (format de src/fourmi, y vers le BAS, fourmi en 0,0) -> dernière autoroute (S9) */
    static char L[1<<20]; long MX=argc>2?atol(argv[2]):3900000;
    if(MX>MAXS){ free(px); free(py); free(tr); px=malloc(MX*2); py=malloc(MX*2); tr=malloc(MX); }
    while(fgets(L,sizeof L,stdin)){
      char *f1=strchr(L,'|'); if(!f1) continue; f1++; char *f2=strchr(f1,'|'); if(!f2) continue; f2++;
      f2[-1]=0; char *cp=strrchr(f1,','); char cc=cp?cp[1]:'H'; int h0=cc=='D'?1:cc=='B'?2:cc=='G'?3:0;
      clear_box(1800); int bx0=0,bx1=0,by0=0,by1=0;
      for(char *q=strtok(f2,";\n"); q; q=strtok(NULL,";\n")){ char *c=strchr(q,','); if(!c) continue; int x=atoi(q), y=-atoi(c+1);
        if(x<-1700||x>1700||y<-1700||y>1700) continue; g[(long)(y+C)*W+(x+C)]^=1;
        if(x<bx0)bx0=x; if(x>bx1)bx1=x; if(y<by0)by0=y; if(y>by1)by1=y; }
      RH=h0; IMPACT=-1; Res r=run(MX,0,0,bx0,by0,bx1,by1);
      printf("autoroute=%d debut=%ld derive=(%d,%d) pas=%ld\n",r.ok,r.onset,r.ddx,-r.ddy,r.steps); fflush(stdout);
    }
  } else if(!strcmp(argv[1],"une")){
    /* une N MASQUE : une boîte N×N (même convention que box : cases (i%N, i/N) en y vers le haut, fourmi (0,0) cap haut) */
    int N=atoi(argv[2]); unsigned long long m=strtoull(argv[3],0,10); long MX=atol(argc>4?argv[4]:"3900000");
    if(MX>MAXS){ free(px); free(py); free(tr); px=malloc(MX*2); py=malloc(MX*2); tr=malloc(MX); }
    for(int i=0;i<N*N;i++) g[(i/N+C)*W+(i%N+C)]=(m>>i)&1;
    Res r=run(MX,0,0,0,0,N-1,N-1);
    printf("une N=%d masque=%llu : autoroute=%d debut=%ld derive=(%d,%d) pas=%ld\n",N,m,r.ok,r.onset,r.ddx,r.ddy,r.steps);
  } else if(!strcmp(argv[1],"obs")){
    /* obs N MASQUE ONSET TFIN PAS : boîte N×N (convention de box). Pour t multiple de PAS (et à chaque pas près du début
       d'autoroute ONSET, ±1000) : L(t) = longueur de la boucle gelée, nb de cases noires, largeur de la boîte visitée.
       Résumé : min L sur le chaos [0,ONSET), max L sur l'autoroute [ONSET,TFIN]. */
    int N=atoi(argv[2]); unsigned long long m=strtoull(argv[3],0,10); long ON=atol(argv[4]), TF=atol(argv[5]); int PS=atoi(argv[6]);
    for(int i=0;i<N*N;i++) g[(i/N+C)*W+(i%N+C)]=(m>>i)&1;
    long nb=0; for(int i=0;i<N*N;i++) nb+=(m>>i)&1;
    int x=0,y=0,h=0,x0=0,x1=0,y0=0,y1=0; long minC=1L<<60, maxH=0, tminC=-1, lastbig=-1;
    for(long t=0;t<=TF;t++){
      if(t%PS==0 || (t>ON-1000 && t<ON+1000)){
        int fx=x,fy=y,fh=h; long L=0;
        do{ int col=g[(fy+C)*W+(fx+C)]; fh= col?(fh+3)&3:(fh+1)&3; fx+=dx[fh]; fy+=dy[fh]; L++; }
        while(!(fx==x&&fy==y&&fh==h) && L<100000000);
        if(t<ON){ if(L<minC){minC=L;tminC=t;} }
        else { if(L>maxH) maxH=L; }
        if(L>172) lastbig=t;
        if(argc>7) printf("%ld,%ld,%ld,%d\n",t,L,nb,(x1-x0+1)>(y1-y0+1)?(x1-x0+1):(y1-y0+1));
      }
      unsigned char *c=&g[(y+C)*W+(x+C)]; int col=*c; h= col?(h+3)&3:(h+1)&3; nb+= col? -1:1; *c^=1; x+=dx[h]; y+=dy[h];
      if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y;
    }
    printf("obs N=%d m=%llu debut=%ld : minL(chaos)=%ld (t=%ld) maxL(autoroute)=%ld dernier L>172 : t=%ld\n",N,m,ON,minC,tminC,maxH,lastbig);
    clear_box(1500);
  } else if(!strcmp(argv[1],"imite")){
    /* imite N MASQUE ONSET : L(t) à chaque pas jusqu'à ONSET+3000 ; plus longue suite de pas consécutifs où L(t) égale la
       suite périodique de l'autoroute nue (calée sur une phase φ) : pendant le chaos (t < ONSET) et instant de calage final. */
    static long BARE[P]; { int x=0,y=0,h=0; for(long t=0;t<20000+P;t++){ if(t>=20000){ int fx=x,fy=y,fh=h; long L=0;
        do{ int col=g[(fy+C)*W+(fx+C)]; fh=col?(fh+3)&3:(fh+1)&3; fx+=dx[fh]; fy+=dy[fh]; L++; } while(!(fx==x&&fy==y&&fh==h));
        BARE[t-20000]=L; } unsigned char *c=&g[(y+C)*W+(x+C)]; h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h]; } clear_box(1500); }
    int N=atoi(argv[2]); unsigned long long m=strtoull(argv[3],0,10); long ON=atol(argv[4]), TF=ON+3000;
    for(int i=0;i<N*N;i++) g[(i/N+C)*W+(i%N+C)]=(m>>i)&1;
    place_base();   /* configuration quelconque via BASE="x,y;..." (y vers le bas) */
    static long run[P]; for(int k=0;k<P;k++) run[k]=0; long bestC=0, tbest=-1, settle=-1, rtr=0, horsA=0, thors=-1; int x=0,y=0,h=0;
    static unsigned char trc[1<<22]; static int rm[1<<22]; static unsigned char inseg[1<<22];
    for(long t=0;t<=TF;t++){
      int fx=x,fy=y,fh=h; long L=0;
      do{ int col=g[(fy+C)*W+(fx+C)]; fh=col?(fh+3)&3:(fh+1)&3; fx+=dx[fh]; fy+=dy[fh]; L++; } while(!(fx==x&&fy==y&&fh==h)&&L<100000000);
      long rmax=0; for(int k=0;k<P;k++){ if(BARE[(t+k)%P]==L) run[k]++; else run[k]=0; if(run[k]>rmax) rmax=run[k]; }
      if(t<ON && rmax>bestC){ bestC=rmax; tbest=t; }
      if(t<(1<<22)) rm[t]=(int)rmax;
      if(rmax==0) settle=-1; else if(settle<0) settle=t;   /* début de la dernière suite d'imitation (approx. : n'importe quelle phase) */
      unsigned char *c=&g[(y+C)*W+(x+C)]; trc[t&((1<<22)-1)]=*c; if(t>=104 && trc[t&((1<<22)-1)]==trc[(t-104)&((1<<22)-1)]) rtr++; else rtr=0;
      h=*c?(h+3)&3:(h+1)&3; *c^=1; x+=dx[h]; y+=dy[h];
    }
    { long T2 = TF < (1<<22)-1 ? TF : (1<<22)-1;   /* 2e passe : plages d'autoroute = runs tr[t]==tr[t-104] de longueur >= 104, première période comprise */
      for(long t=0;t<=T2;t++) inseg[t]=0;
      long a=-1; for(long t=104;t<=T2+1;t++){ int eq = (t<=T2) && trc[t]==trc[t-104];
        if(eq){ if(a<0) a=t; } else { if(a>=0 && t-1-a+1>=104){ for(long u=a-104; u<t; u++) if(u>=0) inseg[u]=1; } a=-1; } }
      long last=-1; for(long t=0;t<=T2;t++){ if(inseg[t]){ last=t; continue; } long v=rm[t]; if(last>=0 && v>t-last) v=t-last; if(v>horsA){ horsA=v; thors=t; } } }
    printf("imite N=%d m=%llu debut=%ld : plus longue imitation pendant le chaos = %ld pas (fin t=%ld) ; imitation finale depuis t=%ld (debut%+ld) ; HORS AUTOROUTE max %ld (t=%ld)\n",N,m,ON,bestC,tbest,settle,settle-ON,horsA,thors);
    clear_box(1500);
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

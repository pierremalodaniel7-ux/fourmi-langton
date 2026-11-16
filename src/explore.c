// explore.c — recherche massive de situations de départ (règle RL, fourmis l'une après l'autre).
// Conventions du projet : caps 0=H(0,-1) 1=D(+1,0) 2=B(0,+1) 3=G(-1,0), y vers le bas ; case blanche -> droite.
// Usage : ./explore FAMILLE ESSAIS GRAINE T [params...]
//   A n R          : n fourmis au hasard dans [-R,R]², grille blanche
//   B n k R        : n fourmis + k cases noires au hasard dans [-R,R]²
//   F n forme a b  : n fourmis près d'une forme (0 segment H, 1 segment diag, 2 rectangle plein, 3 rectangle creux,
//                    4 damier, 5 croix, 6 anneau diag) de dimensions a,b (a,b tirés dans [1,a]x[1,b])
//   S m k ordre R  : m fourmis + k cases, recopiées par rotation (ordre 2 ou 4) autour d'un centre au hasard
// Sortie : une ligne par essai :  FAM|SIGNATURE|fourmis|cases|infos
// Cycle EXACT : la dynamique est réversible, donc un cycle repasse par l'état de départ ; on le détecte
// exactement avec un compteur de cases différentes de la grille initiale (aucun hachage).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define W 2048
#define OFF 1024
#define RESC 950
#define HW 16384
#define NMAX 12
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static uint8_t G[W*W];           // bit0 couleur actuelle, bit1 couleur initiale, bit2 visitée
static int touched[W*W]; static long nt;
typedef struct { int x,y,d,alive; long t; uint8_t h[HW]; } Ant;
static Ant A[NMAX]; static int n;
static int X0[NMAX],Y0[NMAX],D0[NMAX];
static int PX[1<<20],PY[1<<20],np;
static uint64_t rs;
static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline int ri(int a,int b){ return a+(int)(rnd()%(uint64_t)(b-a+1)); }
static long ndiff; static int RX[NMAX],RY[NMAX],RD[NMAX];
static void reset(void){ for(long i=0;i<nt;i++) G[touched[i]]=0; nt=0; ndiff=0; }
static inline void touch(long k){ if(!(G[k]&4)){ G[k]|=4; touched[nt++]=k; } }
static int addcell(int x,int y){ if(abs(x)>940||abs(y)>940) return 0; long k=(long)(y+OFF)*W+x+OFF; if(G[k]&1) return 1; touch(k); G[k]|=3; PX[np]=x; PY[np]=y; np++; return 1; }
static int DUPOK=0; static int addant(int x,int y,int d){ if(!DUPOK) for(int i=0;i<n;i++) if(X0[i]==x&&Y0[i]==y) return 0; X0[n]=x;Y0[n]=y;D0[n]=d&3; n++; return 1; }
static int period(Ant*a,int pmax,int rep,int*dx,int*dy){
  long L=a->t<HW?a->t:HW;
  for(int p=1;p<=pmax;p++){ if((long)p*(rep+1)>L) break; int ok=1;
    for(long i=0;i<(long)p*rep;i++) if(a->h[(a->t-1-i)%HW]!=a->h[(a->t-1-i-p)%HW]){ok=0;break;}
    if(ok){ int X=0,Y=0; for(int i=0;i<p;i++){int d=a->h[(a->t-1-i)%HW]; X+=DX[d]; Y+=DY[d];} *dx=X;*dy=Y; return p; } }
  return 0; }
static void canon(int*dx,int*dy){ for(int r=0;r<4;r++){ if((*dx>0&&*dy>=0)||(*dx==0&&*dy==0)) return; int t=*dx; *dx=-*dy; *dy=t; } }
typedef struct { int p,dx,dy,x,y; long te; int g,id; } Esc;
static Esc E[NMAX]; static int ne;
static char sig[1024], info[512];
static int cmpstr(const void*a,const void*b){ return strcmp(*(char**)a,*(char**)b); }
static int ANALYZE; static void analyze(long P);
static void run(long T){
  for(int i=0;i<n;i++){ A[i].x=X0[i]; A[i].y=Y0[i]; A[i].d=D0[i]; A[i].alive=1; A[i].t=0; }
  ne=0; int alive=n; long tcyc=0; int anyesc=0; long tfin=T; int mx2=0; int resnap=0; long tref=0;
  for(int i=0;i<n;i++){RX[i]=X0[i];RY[i]=Y0[i];RD[i]=D0[i];}
  for(long t=1;t<=T;t++){
    for(int i=0;i<n;i++){ Ant*a=&A[i]; if(!a->alive) continue;
      long k=(long)(a->y+OFF)*W+a->x+OFF; uint8_t c=G[k]; touch(k);
      int col=c&1; a->d=(a->d+(col?3:1))&3;
      if(((c>>1)&1)==col) ndiff++; else ndiff--;
      G[k]^=1; a->x+=DX[a->d]; a->y+=DY[a->d]; a->h[a->t%HW]=a->d; a->t++;
      if(abs(a->x)>RESC||abs(a->y)>RESC){ int ax=a->x,ay=a->y;
        for(int j=0;j<n;j++){ Ant*b=&A[j]; if(!b->alive||abs(b->x-ax)+abs(b->y-ay)>120) continue;
          int dx=0,dy=0,p=period(b,3000,4,&dx,&dy);
          E[ne].p=p;E[ne].dx=dx;E[ne].dy=dy;E[ne].x=b->x;E[ne].y=b->y;E[ne].te=t;E[ne].g=-1;E[ne].id=j;ne++; b->alive=0; alive--; } anyesc=1; resnap=1; } }
    if(resnap){ resnap=0; tref=t; for(long q=0;q<nt;q++){ long k=touched[q]; G[k]=(G[k]&~2)|((G[k]&1)<<1); } ndiff=0;
      for(int i=0;i<n;i++){RX[i]=A[i].x;RY[i]=A[i].y;RD[i]=A[i].d;} }
    if(ndiff==0 && alive>0 && t>tref){ int ok=1; for(int i=0;i<n;i++) if(A[i].alive&&(A[i].x!=RX[i]||A[i].y!=RY[i]||A[i].d!=RD[i])){ok=0;break;}
      if(ok){ tcyc=t-tref; if(ANALYZE) analyze(tcyc); break; } }
    if(alive==0){ tfin=t; break; }
    if(t==T/2){ for(int i=0;i<n;i++) if(A[i].alive){ int m=abs(A[i].x)>abs(A[i].y)?abs(A[i].x):abs(A[i].y); if(m>mx2) mx2=m; } }
  }
  if(tcyc&&!anyesc){ sprintf(sig,"CYC%d P=%ld",n,tcyc); sprintf(info,"cases_touchees=%ld",nt); return; }
  // groupes parmi les évadées
  int ng=0; for(int i=0;i<ne;i++) if(E[i].g<0){ E[i].g=ng;
      for(int j=i+1;j<ne;j++) if(E[j].g<0&&E[j].p&&E[i].p&&(long)E[j].dx*E[i].p==(long)E[i].dx*E[j].p&&(long)E[j].dy*E[i].p==(long)E[i].dy*E[j].p&&abs(E[j].x-E[i].x)+abs(E[j].y-E[i].y)<120) E[j].g=ng;
      ng++; }
  char *tok[64]; int nk=0; static char buf[64][48];
  for(int g=0;g<ng;g++){ int k=0,p=0,dx=0,dy=0; for(int i=0;i<ne;i++) if(E[i].g==g){k++; if(!p){p=E[i].p;dx=E[i].dx;dy=E[i].dy;} else if(E[i].p){ long a=p,b=E[i].p; while(b){long t=a%b;a=b;b=t;} long l=(long)p/a*E[i].p; dx=(int)(dx*(l/p)); dy=(int)(dy*(l/p)); p=(int)l; } }
    canon(&dx,&dy); sprintf(buf[nk],"%s%dp%d(%d,%d)",k>1?"G":"",k,p,dx,dy); tok[nk]=buf[nk]; nk++; }
  int mx=0;
  if(tcyc){ sprintf(buf[nk],"NID%d:P=%ld",n-ne,tcyc); tok[nk]=buf[nk]; nk++; }
  else for(int i=0;i<n;i++) if(A[i].alive){ int dx=0,dy=0,p=period(&A[i],3000,4,&dx,&dy);
      int m=abs(A[i].x)>abs(A[i].y)?abs(A[i].x):abs(A[i].y); if(m>mx) mx=m;
      if(p&&(dx||dy)){ canon(&dx,&dy); sprintf(buf[nk],"s:h%d(%d,%d)",p,dx,dy); }
      else if(p) sprintf(buf[nk],"s:loc%d",p);
      else sprintf(buf[nk],"s:?");
      tok[nk]=buf[nk]; nk++; }
  qsort(tok,nk,sizeof(char*),cmpstr); sig[0]=0; for(int i=0;i<nk;i++){ strcat(sig,tok[i]); strcat(sig," "); }
  if(n-ne>0&&!tcyc){ strcat(sig, mx<=mx2+3? "[borne]":"[grandit]"); }
  sprintf(info,"tfin=%ld tref=%ld r=%d/%d esc=",tfin,tref,mx2,mx); for(int i=0;i<ne;i++){ char s[32]; sprintf(s,"%ld,",E[i].te); strcat(info,s);} strcat(info," ids="); for(int i=0;i<ne;i++){ char s[16]; sprintf(s,"%d,",E[i].id+1); strcat(info,s);} }

static int ANALYZE=0;
static void stepall(void){ for(int i=0;i<n;i++){ Ant*a=&A[i]; if(!a->alive) continue; long k=(long)(a->y+OFF)*W+a->x+OFF; touch(k);
    int col=G[k]&1; a->d=(a->d+(col?3:1))&3; G[k]^=1; a->x+=DX[a->d]; a->y+=DY[a->d]; } }
static void analyze(long P){ // état courant = début du cycle. Passe 1 : marque (bit3) les cases touchées pendant le cycle.
  for(long t=0;t<P;t++){ for(int i=0;i<n;i++){ Ant*a=&A[i]; if(!a->alive) continue; long k=(long)(a->y+OFF)*W+a->x+OFF; touch(k); G[k]|=8; } stepall(); }
  long nb=0,nm=0; for(long q=0;q<nt;q++){ long k=touched[q]; if(G[k]&8){ nm++; if(G[k]&1) nb++; } }
  long mn=nb,tm=0,mxb=nb,gmn=nb; int okd=1; { for(int i=0;i<n&&okd;i++) for(int j=i+1;j<n;j++) if(A[i].alive&&A[j].alive&&A[i].x==A[j].x&&A[i].y==A[j].y){okd=0;break;} } int bx[NMAX],by[NMAX],bd[NMAX]; for(int i=0;i<n;i++){bx[i]=A[i].x;by[i]=A[i].y;bd[i]=A[i].d;}
  for(long t=1;t<=P;t++){ for(int i=0;i<n;i++){ Ant*a=&A[i]; if(!a->alive) continue; long k=(long)(a->y+OFF)*W+a->x+OFF;
      int col=G[k]&1; a->d=(a->d+(col?3:1))&3; if(G[k]&8){ if(col) nb--; else nb++; } G[k]^=1; a->x+=DX[a->d]; a->y+=DY[a->d]; }
    int dist=1; for(int i=0;i<n&&dist;i++) for(int j=i+1;j<n;j++) if(A[i].alive&&A[j].alive&&A[i].x==A[j].x&&A[i].y==A[j].y){dist=0;break;}
    if(nb<gmn) gmn=nb;
    if(dist&&(nb<mn||!okd)){ okd=1; mn=nb; tm=t; for(int i=0;i<n;i++){bx[i]=A[i].x;by[i]=A[i].y;bd[i]=A[i].d;} } if(nb>mxb) mxb=nb; }
  int mnx=1<<30,mny=1<<30,Mx=-(1<<30),My=-(1<<30); for(long q=0;q<nt;q++){ long k=touched[q]; if(G[k]&8){ int x=k%W-OFF,y=k/W-OFF; if(x<mnx)mnx=x; if(y<mny)mny=y; if(x>Mx)Mx=x; if(y>My)My=y; } }
  // composantes connexes (8-voisinage) des cases du cycle, et fourmis par composante
  static int stk[W*W/2]; int ncomp=0; char comps[256]=""; 
  for(long q=0;q<nt;q++){ long k0=touched[q]; if(!(G[k0]&8)||(G[k0]&16)) continue; ncomp++; int sp=0; stk[sp++]=k0; G[k0]|=16; long sz=0; int na=0;
    while(sp){ long k=stk[--sp]; sz++; for(int i=0;i<n;i++) if(A[i].alive&&(long)(A[i].y+OFF)*W+A[i].x+OFF==k) na++;
      for(int a=-1;a<=1;a++) for(int b=-1;b<=1;b++){ long k2=k+a+(long)b*W; if((G[k2]&8)&&!(G[k2]&16)){ G[k2]|=16; stk[sp++]=k2; } } }
    if(strlen(comps)<200){ char t[32]; sprintf(t,"%ldc/%df,",sz,na); strcat(comps,t);} }
  printf("ANALYSE composantes=%d [%s] ",ncomp,comps);
  printf("P=%ld cases_du_cycle=%ld boite=%dx%d noires_min=%ld noires_max=%ld instant_min=%ld fourmis_a_cet_instant=",P,nm,Mx-mnx+1,My-mny+1,gmn,mxb,tm);
  for(int i=0;i<n;i++) if(A[i].alive) printf("%d,%d,%c ; ",bx[i],by[i],"HDBG"[bd[i]]);
  if(1){ printf(" noires_a_cet_instant="); // rejouer jusqu'à tm pour lister
    for(long t=0;t<tm;t++) stepall(); for(long q=0;q<nt;q++){ long k=touched[q]; if((G[k]&8)&&(G[k]&1)) printf("%ld,%ld;",k%W-OFF,k/W-OFF); } }
  printf("\n"); }
static const char CAP[]="HDBG";
static void out(const char*fam){ printf("%s|%s|",fam,sig); for(int i=0;i<n;i++) printf("%s%d,%d,%c",i?" ; ":"",X0[i],Y0[i],CAP[D0[i]]);
  printf("|"); for(int i=0;i<np;i++) printf("%s%d,%d",i?" ; ":"",PX[i],PY[i]); printf("|%s\n",info); }
// formes
static void shape(int s,int a,int b,int ox,int oy){
  switch(s){
  case 0: for(int i=0;i<a;i++) addcell(ox+i,oy); break;
  case 1: for(int i=0;i<a;i++) addcell(ox+i,oy+i); break;
  case 2: for(int i=0;i<a;i++) for(int j=0;j<b;j++) addcell(ox+i,oy+j); break;
  case 3: for(int i=0;i<a;i++) for(int j=0;j<b;j++) if(i==0||j==0||i==a-1||j==b-1) addcell(ox+i,oy+j); break;
  case 4: for(int i=0;i<a;i++) for(int j=0;j<b;j++) if((i+j)%2==0) addcell(ox+i,oy+j); break;
  case 5: for(int i=-a;i<=a;i++) addcell(ox+i,oy); for(int j=-b;j<=b;j++) if(j) addcell(ox,oy+j); break;
  case 6: for(int i=0;i<=a;i++){ addcell(ox+i,oy-a+i); addcell(ox+a-i,oy+i); addcell(ox-i,oy+a-i); addcell(ox-a+i,oy-i);} break; } }
int main(int c,char**v){
  char fam=v[1][0]; long E_=atol(v[2]); rs=atol(v[3])*0x9E3779B97F4A7C15ULL+12345; long T=atol(v[4]);
  for(int i=0;i<20;i++) rnd();
  char tag[64];
  for(long e=0;e<E_;e++){ reset(); n=0; np=0; int ok=1;
    if(fam=='A'){ int nn=atoi(v[5]),R=atoi(v[6]); while(n<nn) addant(ri(-R,R),ri(-R,R),ri(0,3)); sprintf(tag,"A%d.%d",nn,R); }
    else if(fam=='B'){ int nn=atoi(v[5]),k=atoi(v[6]),R=atoi(v[7]); int kk=ri(1,k); while(n<nn) addant(ri(-R,R),ri(-R,R),ri(0,3));
      for(int j=0;j<kk;j++) addcell(ri(-R,R),ri(-R,R)); sprintf(tag,"B%d.%d.%d",nn,k,R); }
    else if(fam=='F'){ int nn=atoi(v[5]),s=atoi(v[6]); if(s<0) s=ri(0,6); int a=ri(1,atoi(v[7])),b=ri(1,atoi(v[8]));
      shape(s,a,b,0,0); int bx=(s==5||s==6)?a+3:a+3, by=(s==5||s==6)?b+3:b+3;
      while(n<nn) addant(ri(-3-(s>=5?a:0),bx),ri(-3-(s>=5?b:0),by),ri(0,3)); sprintf(tag,"F%d.s%d.%dx%d",nn,s,a,b); }
    else if(fam=='S'){ int m=atoi(v[5]),k=atoi(v[6]),ord=atoi(v[7]),R=atoi(v[8]);
      int cx2=ri(0,1),cy2=ri(0,1); if(ord==4) cy2=cx2; // centre (en demi-cases) : case, sommet, (milieu d'arête si ordre 2)
      int bx[8],by[8],bd[8],cxs[64],cys[64]; int kk=ri(0,k);
      for(int i=0;i<m;i++){bx[i]=ri(-R,R);by[i]=ri(-R,R);bd[i]=ri(0,3);} for(int j=0;j<kk;j++){cxs[j]=ri(-R,R);cys[j]=ri(-R,R);}
      for(int r=0;r<ord&&ok;r++){ int st=ord==2?2*r:r; // nombre de quarts de tour
        for(int i=0;i<m&&ok;i++){ int u=2*bx[i]-cx2,w=2*by[i]-cy2; for(int q=0;q<st;q++){int t=u;u=-w;w=t;} if(!addant((u+cx2)/2,(w+cy2)/2,bd[i]+st)) ok=0; }
        for(int j=0;j<kk;j++){ int u=2*cxs[j]-cx2,w=2*cys[j]-cy2; for(int q=0;q<st;q++){int t=u;u=-w;w=t;} addcell((u+cx2)/2,(w+cy2)/2); } }
      sprintf(tag,"S%d.%d.o%d.c%d%d",m,k,ord,cx2,cy2); }
    else if(fam=='X'||fam=='Y'){ ANALYZE=(fam=='Y'); DUPOK=1; char*p=strdup(v[5]),*tk; for(tk=strtok(p,";");tk;tk=strtok(NULL,";")){int x,y; char d[4]; if(sscanf(tk," %d,%d,%1s",&x,&y,d)==3) addant(x,y,d[0]=='H'?0:d[0]=='D'?1:d[0]=='B'?2:3);}
      if(c>6){ p=strdup(v[6]); for(tk=strtok(p,";");tk;tk=strtok(NULL,";")){int x,y; if(sscanf(tk," %d,%d",&x,&y)==2) addcell(x,y);} } sprintf(tag,"X"); }
    if(!ok||n==0) continue;
    run(T); out(tag); }
  return 0; }

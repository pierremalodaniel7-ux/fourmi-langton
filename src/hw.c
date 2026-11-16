// hw.c — recherche d'autoroutes et de leur DIRECTION. Règle généralisée : grille carrée (lettres R L N U, q = longueur)
// ou hexagonale (préfixe H: puis jetons N R1 R2 U L2 L1). Plusieurs fourmis jouées l'une après l'autre. Cases de départ
// de couleur au hasard dans 1..q-1. Une fourmi (ou un groupe) qui sort du carré de rayon 950 est mesurée puis retirée.
// Usage : ./hw REGLE ESSAIS GRAINE T n R k Rc
//   REGLE : mot (ex. RL, LLRR), H:... (hexagonale), ou "rand4:q" / "rand6:q" = règle tirée au hasard à chaque essai (q couleurs).
//   n fourmis au hasard dans [-R,R]² ; k cases (nombre tiré dans 0..k) au hasard dans [-Rc,Rc]².
// Sortie : une ligne par groupe sorti :  E|regle|k_fourmis|periode|dx|dy|t_sortie|fourmis|cases
//   (dx,dy) = déplacement par période (coordonnées de la grille ; hexagonale : axiales q,r).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define W 2048
#define OFF 1024
#define RESC 950
#define HW 65536
#define NMAX 16
static int M=4,q=2,turn[32],DX[6],DY[6];
static const int sqx[4]={0,1,0,-1}, sqy[4]={-1,0,1,0}, hxx[6]={1,0,-1,-1,0,1}, hxy[6]={0,1,1,0,-1,-1};
static uint8_t G[W*W]; static int *tl; static long nt;
typedef struct { int x,y,d,alive; long t; uint8_t h[HW]; } Ant;
static Ant A[NMAX]; static int n,X0[NMAX],Y0[NMAX],D0[NMAX]; static int PX[4096],PY[4096],PC[4096],np;
static uint64_t rs; static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline int ri(int a,int b){ return a+(int)(rnd()%(uint64_t)(b-a+1)); }
static char rule[64];
static void setrule(const char*r){ strcpy(rule,r);
  if(!strncmp(r,"H:",2)){ M=6; q=0; const char*p=r+2; while(*p){ if(*p=='N'){turn[q++]=0;p++;} else if(*p=='U'){turn[q++]=3;p++;}
      else if(*p=='R'){turn[q++]=p[1]-'0';p+=2;} else {turn[q++]=6-(p[1]-'0');p+=2;} } memcpy(DX,hxx,sizeof hxx); memcpy(DY,hxy,sizeof hxy); }
  else { M=4; q=strlen(r); for(int i=0;i<q;i++) turn[i]=r[i]=='R'?1:r[i]=='L'?3:r[i]=='U'?2:0; memcpy(DX,sqx,sizeof sqx); memcpy(DY,sqy,sizeof sqy); } }
static int LRONLY=0; static void randrule(int m,int qq){ char r[64]; int ok;
  do { ok=0; if(m==4){ for(int i=0;i<qq;i++){ int u=LRONLY?rnd()%8:rnd()%10; r[i]=u<4?'L':u<8?'R':u<9?'N':'U'; } r[qq]=0; for(int i=0;i<qq;i++) if(r[i]=='L'||r[i]=='R') ok=1; }
       else { const char*tk[6]={"N","R1","R2","U","L2","L1"}; r[0]='H'; r[1]=':'; r[2]=0; for(int i=0;i<qq;i++){ int u=rnd()%6; strcat(r,tk[u]); if(u&&u!=3) ok=1; } } } while(!ok);
  setrule(r); }
static int period(Ant*a,int pmax,int rep,int*dx,int*dy){ long L=a->t<HW?a->t:HW;
  for(int p=1;p<=pmax;p++){ if((long)p*(rep+1)>L) break; int ok=1;
    for(long i=0;i<(long)p*rep;i++) if(a->h[(a->t-1-i)%HW]!=a->h[(a->t-1-i-p)%HW]){ok=0;break;}
    if(ok){ int X=0,Y=0; for(int i=0;i<p;i++){int d=a->h[(a->t-1-i)%HW]; X+=DX[d]; Y+=DY[d];} *dx=X;*dy=Y; return p; } }
  return 0; }
static const char *C4="HDBG", *C6[6]={"E","SE","SO","O","NO","NE"};
int main(int c,char**v){ long E_=atol(v[2]); rs=atol(v[3])*0x9E3779B97F4A7C15ULL+99; long T=atol(v[4]); int nn=atoi(v[5]),R=atoi(v[6]),K=atoi(v[7]),Rc=atoi(v[8]);
  tl=malloc(sizeof(int)*W*W); for(int i=0;i<20;i++) rnd();
  int rr=0,rm=4,rq=2; if(!strncmp(v[1],"randLR",6)){ rr=1; rm=4; rq=atoi(v[1]+7); LRONLY=1; } else if(!strncmp(v[1],"rand",4)){ rr=1; rm=v[1][4]-'0'; rq=atoi(v[1]+6); } else setrule(v[1]);
  for(long e=0;e<E_;e++){ for(long i=0;i<nt;i++) G[tl[i]]=0; nt=0; n=0; np=0; if(rr) randrule(rm,rq);
    if(R<0){ int u,w; do{u=ri(R,-R);w=ri(R,-R);}while(!u&&!w); int pl=ri(1,2),pd[2]={ri(0,M-1),ri(0,M-1)}; for(int i=0;i<nn;i++){X0[i]=i*u;Y0[i]=i*w;D0[i]=pd[i%pl];} n=nn; }
    while(n<nn){ int x=ri(-R,R),y=ri(-R,R),d=ri(0,M-1),dup=0; for(int i=0;i<n;i++) if(X0[i]==x&&Y0[i]==y) dup=1; if(dup) continue; X0[n]=x;Y0[n]=y;D0[n]=d; n++; }
    int kk=K?ri(0,K):0; for(int j=0;j<kk;j++){ int x=ri(-Rc,Rc),y=ri(-Rc,Rc); long k=(long)(y+OFF)*W+x+OFF; if(G[k]) continue; G[k]=ri(1,q-1); tl[nt++]=k; PX[np]=x;PY[np]=y;PC[np]=G[k];np++; }
    for(int i=0;i<n;i++){ A[i].x=X0[i];A[i].y=Y0[i];A[i].d=D0[i];A[i].alive=1;A[i].t=0; } int alive=n;
    for(long t=1;t<=T&&alive;t++){
      for(int i=0;i<n;i++){ Ant*a=&A[i]; if(!a->alive) continue; long k=(long)(a->y+OFF)*W+a->x+OFF; uint8_t cc=G[k];
        if(!(cc&0x80)){ if(!cc) tl[nt++]=k; } int col=cc&0x7f; a->d=(a->d+turn[col])%M; int nc=col+1; if(nc==q) nc=0; G[k]=nc|0x80;
        a->x+=DX[a->d]; a->y+=DY[a->d]; a->h[a->t%HW]=a->d; a->t++;
        if(abs(a->x)>RESC||abs(a->y)>RESC){ int ax=a->x,ay=a->y; int gp[NMAX],gdx[NMAX],gdy[NMAX],gi[NMAX],ng=0;
          for(int j=0;j<n;j++){ Ant*b=&A[j]; if(!b->alive||abs(b->x-ax)+abs(b->y-ay)>150) continue; int dx=0,dy=0,p=period(b,16000,3,&dx,&dy); gp[ng]=p;gdx[ng]=dx;gdy[ng]=dy;gi[ng]=j;ng++; b->alive=0; alive--; }
          // une ligne : la fourmi qui sort ; les autres du groupe sont comptées si même vitesse
          int k2=0; for(int j=0;j<ng;j++) if(gp[j]&&gp[0]&&(long)gdx[j]*gp[0]==(long)gdx[0]*gp[j]&&(long)gdy[j]*gp[0]==(long)gdy[0]*gp[j]) k2++;
          for(int j=0;j<ng;j++){ if(!gp[j]) continue; int same=0; for(int u=0;u<j;u++) if(gp[u]&&(long)gdx[j]*gp[u]==(long)gdx[u]*gp[j]&&(long)gdy[j]*gp[u]==(long)gdy[u]*gp[j]) same=1; if(same) continue;
            int kg=0; for(int u=0;u<ng;u++) if(gp[u]&&(long)gdx[j]*gp[u]==(long)gdx[u]*gp[j]&&(long)gdy[j]*gp[u]==(long)gdy[u]*gp[j]) kg++;
            printf("E|%s|%d|%d|%d|%d|%ld|",rule,kg,gp[j],gdx[j],gdy[j],t);
            for(int u=0;u<n;u++) printf("%s%d,%d,%s",u?" ; ":"",X0[u],Y0[u],M==4?(char[]){C4[D0[u]],0}:C6[D0[u]]);
            printf("|"); for(int u=0;u<np;u++) printf("%s%d,%d%s",u?" ; ":"",PX[u],PY[u],q>2?(char[]){':',(char)('0'+PC[u]),0}:""); printf("\n"); }
          (void)k2; } } } }
  return 0; }

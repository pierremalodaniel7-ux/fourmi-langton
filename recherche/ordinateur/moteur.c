/* moteur.c — moteur RL minimal pour la construction de l'ordinateur (bibliothèque ctypes).
   Grille carrée W x W centrée, y vers le bas, caps 0=H 1=D 2=B 3=G, RL (blanc -> droite).
   Fourmis jouées l'une après l'autre. Octet de case : bit0 = couleur, bit1 = déjà touchée.
   Positions entières. Sortie de grille -> arrêt signalé (jamais de bord silencieux). */
#include <stdlib.h>
#include <string.h>
#define LW 15
#define W (1<<LW)
#define OFF (W/2)
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static unsigned char *G; static long *TL; static long nt, cap;
static int NA; static int AX[256],AY[256],AD[256];
static inline long id(int x,int y){return ((long)(y+OFF)<<LW)+(x+OFF);}
static inline void touch(long k){ if(!(G[k]&2)){ G[k]|=2; if(nt==cap){cap*=2;TL=realloc(TL,cap*sizeof(long));} TL[nt++]=k; } }
int init(void){ if(!G){ G=calloc((size_t)W*W,1); cap=1<<20; TL=malloc(cap*sizeof(long)); } return W; }
void reset(void){ for(long i=0;i<nt;i++) G[TL[i]]=0; nt=0; }
/* cellules : bascule la couleur (XOR) */
void flip(int n,const int *xy){ for(int i=0;i<n;i++){ long k=id(xy[2*i],xy[2*i+1]); touch(k); G[k]^=1; } }
void set_ants(int n,const int *xyd){ NA=n; for(int i=0;i<n;i++){AX[i]=xyd[3*i];AY[i]=xyd[3*i+1];AD[i]=xyd[3*i+2];} }
void get_ants(int *xyd){ for(int i=0;i<NA;i++){xyd[3*i]=AX[i];xyd[3*i+1]=AY[i];xyd[3*i+2]=AD[i];} }
int color(int x,int y){ return G[id(x,y)]&1; }
/* T tours (chaque tour : chaque fourmi joue un pas, dans l'ordre).
   Pour la fourmi w : dh[t]=cap après le pas, xs/ys = position après le pas, fr[t]=1 si la case quittée était neuve.
   Arrêt si une fourmi approche du bord : renvoie -(t+1). Sinon T. */
long run(long T,int w,unsigned char *dh,int *xs,int *ys,unsigned char *fr){
  int lim=OFF-4;
  for(long t=0;t<T;t++){
    for(int i=0;i<NA;i++){
      long k=id(AX[i],AY[i]); unsigned char c=G[k]; int neuf=!(c&2);
      if(neuf){ G[k]|=2; if(nt==cap){cap*=2;TL=realloc(TL,cap*sizeof(long));} TL[nt++]=k; }
      int d=(AD[i]+((c&1)?3:1))&3; AD[i]=d; G[k]=c^1|2; AX[i]+=DX[d]; AY[i]+=DY[d];
      if(i==w){ if(dh)dh[t]=d; if(xs){xs[t]=AX[i];ys[t]=AY[i];} if(fr)fr[t]=neuf; }
      if(AX[i]<-lim||AX[i]>lim||AY[i]<-lim||AY[i]>lim) return -(t+1);
    }
  }
  return T;
}
long ntouched(void){ return nt; }
void get_touched(int *xy){ for(long i=0;i<nt;i++){ long k=TL[i]; xy[2*i]=(int)(k&(W-1))-OFF; xy[2*i+1]=(int)(k>>LW)-OFF; } }
/* toutes les fourmis : dh[t*NA+i], xs/ys idem ; arrêt au bord -> -(t+1) */
long run_all(long T,unsigned char *dh,int *xs,int *ys){
  int lim=OFF-4;
  for(long t=0;t<T;t++){
    for(int i=0;i<NA;i++){
      long k=id(AX[i],AY[i]); unsigned char c=G[k];
      if(!(c&2)){ if(nt==cap){cap*=2;TL=realloc(TL,cap*sizeof(long));} TL[nt++]=k; }
      int d=(AD[i]+((c&1)?3:1))&3; AD[i]=d; G[k]=c^1|2; AX[i]+=DX[d]; AY[i]+=DY[d];
      long j=t*NA+i; dh[j]=d; xs[j]=AX[i]; ys[j]=AY[i];
      if(AX[i]<-lim||AX[i]>lim||AY[i]<-lim||AY[i]>lim) return -(t+1);
    }
  }
  return T;
}
/* région [x0,x0+w) x [y0,y0+h) : 0 jamais touchée, 1 touchée blanche, 2 noire */
void region(int x0,int y0,int w,int h,unsigned char *out){
  for(int j=0;j<h;j++) for(int i=0;i<w;i++){ unsigned char c=G[id(x0+i,y0+j)]; out[(long)j*w+i]=(c&1)?2:((c&2)?1:0); }
}

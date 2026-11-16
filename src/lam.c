// lam.c — « la Lambine » : 1 fourmi RL en 0,0,H + k cases noires dans [-R,R]², recherche locale qui MAXIMISE
// le temps avant l'autoroute (mesuré par le temps de sortie du disque de rayon 950, moins 49 400 ≈ trajet sur l'autoroute).
// ./lam K R ITER GRAINE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define W 2048
#define OFF 1024
static uint8_t G[W*W]; static int tl[1<<22]; static long nt;
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static uint64_t rs; static inline uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static long ev(int k,int*cx,int*cy){ for(long i=0;i<nt;i++) G[tl[i]]=0; nt=0;
  for(int i=0;i<k;i++){ long q=(long)(cy[i]+OFF)*W+cx[i]+OFF; if(!G[q]){tl[nt++]=q;} G[q]=1|2; }
  int x=0,y=0,d=0; for(long t=1;t<=3000000;t++){ long q=(long)(y+OFF)*W+x+OFF; if(!(G[q]&2)){G[q]|=2; tl[nt++]=q;}
    int c=G[q]&1; d=(d+(c?3:1))&3; G[q]^=1; x+=DX[d]; y+=DY[d]; if(abs(x)>950||abs(y)>950) return t; }
  return 3000000; }
int main(int c,char**v){ int K=atoi(v[1]),R=atoi(v[2]); long IT=atol(v[3]); rs=atol(v[4])*0x9E3779B97F4A7C15ULL+7;
  int cx[64],cy[64],bx[64],by[64]; long best=0;
  if(IT==0){ long N=0; int S=2*R+1; long M=1; for(int i=0;i<K;i++) M*=S*S;
    for(long code=0;code<M;code++){ long c2=code; int ok=1; for(int i=0;i<K;i++){ int q=c2%(S*S); c2/=S*S; cx[i]=q%S-R; cy[i]=q/S-R; if(cx[i]==0&&cy[i]==0) ok=0; if(i&&(long)(cy[i]*S+cx[i])<=(long)(cy[i-1]*S+cx[i-1])) ok=0; }
      if(!ok) continue; N++; long t=ev(K,cx,cy); if(t>best){best=t; memcpy(bx,cx,sizeof cx); memcpy(by,cy,sizeof cy);} }
    printf("EXHAUSTIF %ld essais ; ",N); IT=-1; }
  if(IT<0) goto fin;
  for(int i=0;i<K;i++){cx[i]=(int)(rnd()%(2*R+1))-R; cy[i]=(int)(rnd()%(2*R+1))-R;} long cur=ev(K,cx,cy);
  for(long it=0;it<IT;it++){ int j=rnd()%K, ox=cx[j],oy=cy[j];
    if(rnd()%2){cx[j]=(int)(rnd()%(2*R+1))-R; cy[j]=(int)(rnd()%(2*R+1))-R;} else {cx[j]+=(int)(rnd()%3)-1; cy[j]+=(int)(rnd()%3)-1; if(abs(cx[j])>R||abs(cy[j])>R){cx[j]=ox;cy[j]=oy;}}
    if(cx[j]==0&&cy[j]==0){cx[j]=ox;cy[j]=oy;}
    long t=ev(K,cx,cy); if(t>=cur){ cur=t; if(t>best){best=t; memcpy(bx,cx,sizeof cx); memcpy(by,cy,sizeof cy);} } else {cx[j]=ox;cy[j]=oy;} }
  fin: printf("K=%d R=%d sortie=%ld (debut autoroute ~%ld) cases ",K,R,best,best-49400); for(int i=0;i<K;i++) printf("%s%d,%d",i?" ; ":"",bx[i],by[i]); printf("\n"); }

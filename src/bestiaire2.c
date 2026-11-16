// bestiaire2.c — analyseur généralisé (grille carrée M=4 ou hexagonale M=6, q couleurs, plusieurs fourmis).
// Carré : directions 0=H(0,-1) 1=D(1,0) 2=B(0,1) 3=G(-1,0), y vers le bas ; lettres R=+1 L=-1 N=0 U=2.
// Hexa (préfixe "H:") : coordonnées axiales, directions 0=E(1,0) 1=SE(0,1) 2=SO(-1,1) 3=O(-1,0) 4=NO(0,-1) 5=NE(1,-1)
//   (sens horaire à l'écran) ; jetons N R1 R2 U L2 L1 (= 0 +1 +2 3 -2 -1).
// Fourmis mises à jour l'une après l'autre ; grille blanche (couleur 0) au départ.
// Usage : ./bestiaire2 REGLE MAXPAS x1 y1 d1 [x2 y2 d2 ...]     ex. ./bestiaire2 RL 3000000 0 0 0
//         ./bestiaire2 H:L2NNL1L2L1 3000000 0 0 0
// Sortie : une ligne JSON (même format que bestiaire.c).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 4096
#define OFF 2048
#define LIM 1900
static unsigned char G[W*W], seen[W*W];
static int touched[W*W/2]; static long nt;
static int M=4, dx[6], dy[6];
static const int sqx[4]={0,1,0,-1}, sqy[4]={-1,0,1,0};
static const int hxx[6]={1,0,-1,-1,0,1}, hxy[6]={0,1,1,0,-1,-1};
static int bx0,bx1,by0,by1;
static int sym(int which,int mode){ // symétries du carré seulement
  long cx=bx0+bx1, cy=by0+by1;
  for(long i=0;i<nt;i++){ long k=touched[i]; int X=k%W-OFF, Y=k/W-OFF;
    if(mode==0 && G[k]==0) continue;
    long u=2*X-cx, v=2*Y-cy, a,b;
    switch(which){case 0:a=-u;b=v;break; case 1:a=u;b=-v;break; case 2:a=v;b=u;break;
      case 3:a=-v;b=-u;break; case 4:a=-u;b=-v;break; default:a=-v;b=u;}
    if((a+cx)%2||(b+cy)%2) return 0;
    long X2=(a+cx)/2, Y2=(b+cy)/2;
    if(X2+OFF<0||Y2+OFF<0||X2+OFF>=W||Y2+OFF>=W) return 0;
    long k2=(Y2+OFF)*W+(X2+OFF);
    if(mode==0 ? G[k2]==0 : !seen[k2]) return 0; }
  return 1;
}
int main(int argc,char**argv){
  const char*rule=argv[1]; int q=0, turn[64];
  if(!strncmp(rule,"H:",2)){ M=6; const char*p=rule+2;
    while(*p){ if(*p=='N'){turn[q++]=0;p++;} else if(*p=='U'){turn[q++]=3;p++;}
      else if(*p=='R'){turn[q++]=p[1]-'0';p+=2;} else if(*p=='L'){turn[q++]=6-(p[1]-'0');p+=2;} else {fprintf(stderr,"regle?\n");return 1;} }
    memcpy(dx,hxx,sizeof hxx); memcpy(dy,hxy,sizeof hxy);
  } else { q=strlen(rule); for(int i=0;i<q;i++) turn[i]=rule[i]=='R'?1:rule[i]=='L'?3:rule[i]=='U'?2:0;
    memcpy(dx,sqx,sizeof sqx); memcpy(dy,sqy,sizeof sqy); }
  long maxs=atol(argv[2]);
  int n=(argc-3)/3, x[16],y[16],d[16],x0[16],y0[16],d0[16];
  for(int i=0;i<n;i++){x0[i]=x[i]=atoi(argv[3+3*i]);y0[i]=y[i]=atoi(argv[4+3*i]);d0[i]=d[i]=atoi(argv[5+3*i]);}
  unsigned char*hist[16]; for(int i=0;i<n;i++) hist[i]=malloc(maxs+1);
  bx0=bx1=x[0]; by0=by1=y[0];
  long nonwhite=0,t,boxlog[64]; int nb=0; long nxt=256; const char*etat="inconnu";
  for(t=1;t<=maxs;t++){
    for(int i=0;i<n;i++){
      long k=(long)(y[i]+OFF)*W+(x[i]+OFF); int c=G[k];
      if(!seen[k]){seen[k]=1;touched[nt++]=k;}
      d[i]=(d[i]+turn[c])%M; int nc=(c+1==q)?0:c+1;
      if(c==0) nonwhite++; if(nc==0) nonwhite--;
      G[k]=nc; x[i]+=dx[d[i]]; y[i]+=dy[d[i]]; hist[i][t]=d[i];
      if(x[i]<bx0)bx0=x[i]; if(x[i]>bx1)bx1=x[i]; if(y[i]<by0)by0=y[i]; if(y[i]>by1)by1=y[i];
    }
    if(t==nxt){boxlog[nb++]=(bx1-bx0>by1-by0?bx1-bx0:by1-by0)+1; nxt*=2;}
    if(nonwhite==0){int ok=1;for(int i=0;i<n;i++) if(x[i]!=x0[i]||y[i]!=y0[i]||d[i]!=d0[i]) ok=0;
      if(ok){etat="cycle";break;}}
    if(bx1-bx0>2*LIM||by1-by0>2*LIM||bx0<-LIM||bx1>LIM||by0<-LIM||by1>LIM){etat="sortie";break;}
  }
  if(t>maxs) t=maxs;
  printf("{\"etat\":\"%s\",\"pas\":%ld,\"cases_visitees\":%ld,\"cases_noires\":%ld,\"boite\":[%d,%d,%d,%d]",etat,t,nt,nonwhite,bx0,bx1,by0,by1);
  printf(",\"taille_boite_2puiss\":["); for(int i=0;i<nb;i++) printf("%s%ld",i?",":"",boxlog[i]); printf("]");
  const char*nom[6]={"miroir_vertical","miroir_horizontal","diagonale","antidiagonale","demi_tour","quart_de_tour"};
  if(M==4){
  printf(",\"symetries_noires\":["); int f=0; for(int s=0;s<6;s++) if(nonwhite&&sym(s,0)){printf("%s\"%s\"",f?",":"",nom[s]);f=1;} printf("]");
  printf(",\"symetries_visitees\":["); f=0; for(int s=0;s<6;s++) if(sym(s,1)){printf("%s\"%s\"",f?",":"",nom[s]);f=1;} printf("]");}
  printf(",\"fourmis\":[");
  for(int i=0;i<n;i++){ long P=0;
    if(strcmp(etat,"cycle")) for(long p=1;p<=20000&&4*p<t;p++){ long j; for(j=t;j>t-3*p;j--) if(hist[i][j]!=hist[i][j-p]) break; if(j==t-3*p){P=p;break;} }
    long debut=-1; int ddx=0,ddy=0;
    if(P){ long j=t; while(j-P>=1 && hist[i][j]==hist[i][j-P]) j--; debut=j-P+1>0?j-P+1:0;
      for(long k=t-P+1;k<=t;k++){ddx+=dx[hist[i][k]];ddy+=dy[hist[i][k]];} }
    printf("%s{\"periode\":%ld,\"deplacement\":[%d,%d],\"debut\":%ld,\"fin\":[%d,%d,%d]}",i?",":"",P,ddx,ddy,debut,x[i],y[i],d[i]);
  }
  printf("]}\n"); return 0;
}

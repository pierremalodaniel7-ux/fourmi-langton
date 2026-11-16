// col.c — collision de 2 autoroutes 104 nées dès le pas 0 (germe de 11 cases, B = A tourné de ROT×90°).
// ./col ROT CX CY L I0 I1 : A en 0,0 ; B posé en (CX,CY)+L·(-u_B)+(i,j), i,j ∈ [I0,I1] (u_B = direction de B par pas de 52)
// Issue = liste des (période, déplacement) des 2 fourmis à la fin (0 = pas d'autoroute : bornée/losange/chaos).
#include "ant.h"
static int TIP[11][2]={{0,1},{1,2},{2,3},{2,2},{2,1},{2,0},{3,0},{3,-1},{2,-2},{1,-2},{-2,-1}};
static const char CAP[]="HDBG";
static void rot(int k,int*x,int*y){ for(int r=0;r<k;r++){ int t=*x; *x=-*y; *y=t; } }
int main(int c,char**v){ int R=atoi(v[1]),CX=atoi(v[2]),CY=atoi(v[3]),L=atoi(v[4]),I0=atoi(v[5]),I1=atoi(v[6]);
  int ux=-1,uy=1; rot(R,&ux,&uy); // direction de B (unité diagonale)
  Grid g; g_init(&g,1<<22);
  for(int i=I0;i<=I1;i++) for(int j=I0;j<=I1;j++){ g_clear(&g); Ant A[2]; memset(A,0,sizeof A);
    for(int k=0;k<11;k++) g_set(&g,TIP[k][0],TIP[k][1],1); A[0].d=2;
    int bx=CX-L*ux+i, by=CY-L*uy+j; for(int k=0;k<11;k++){ int x=TIP[k][0],y=TIP[k][1]; rot(R,&x,&y); g_set(&g,bx+x,by+y,1);} A[1].x=bx; A[1].y=by; A[1].d=(2+R)&3;
    int lp[2]={-1,-1},st=0; long T=0; char res[200];
    for(long t=1;t<=8000000;t++){ a_step(&g,&A[0]); a_step(&g,&A[1]);
      if(t%65536==0&&t>(long)L*104){ int s=0,q[2],dx[2],dy[2]; for(int a=0;a<2;a++){ q[a]=a_period(&A[a],700,20,&dx[a],&dy[a]); }
        sprintf(res,"%d(%d,%d) %d(%d,%d)",q[0],dx[0],dy[0],q[1],dx[1],dy[1]); if(getenv("DBG")) printf("  t=%ld A %d,%d %s | B %d,%d\n",t,A[0].x,A[0].y,res,A[1].x,A[1].y);
        if(q[0]==lp[0]&&q[1]==lp[1]&&q[0]&&q[1]){ if(++st>=4){T=t;break;} } else st=0; lp[0]=q[0]; lp[1]=q[1]; } }
    int cl=((A[0].x+A[0].y+(A[0].d&1?0:1))&1)!=((A[1].x+A[1].y+(A[1].d&1?0:1))&1);
    printf("i=%d j=%d : %s%s classes %s | fourmis \"0,0,B;%d,%d,%c\"\n",i,j,res,T?"":" (non stable)",cl?"diff":"egales",bx,by,CAP[(2+R)&3]); fflush(stdout); }
}

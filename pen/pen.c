#include <assert.h>
#include <complex.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>

int width;
int height;
int size;
unsigned char* image;
double sidelen;
double thickness;
int alias;
#define plotw(x,y,c) plot(swap?(y):(x),swap?(x):(y),c)
#define PHI 1.61803398874989484820
#define RPHI .61803398874989484820
#define ZETA1 (0.30901699437494745+0.9510565162951535*I)
#define ZETA2 (-0.8090169943749473+0.5877852522924732*I)
#define ZETA3 (-0.8090169943749473-0.5877852522924732*I)
#define ZETA4 (0.30901699437494745-0.9510565162951535*I)

complex double zeta(int n) {
  switch (n%5) {
  case 0: return 1;
  case 1: return ZETA1;
  case 2: return ZETA2;
  case 3: return ZETA3;
  case 4: return ZETA4;
  }
}

complex double fourier(complex double z0, complex double z1, complex double z2, complex double z3, complex double z4) {
  return z0+ZETA1*z1+ZETA2*z2+ZETA3*z3+ZETA4*z4;
}

void pgmshow() {
  int i;
  printf("P5 %d %d 255 ",width,height);
  for(i=0;i<size;i++) putc(image[i],stdout);
}

void plot(int x, int y,double value) {
  double u;
  if (alias) value=(value<0.5)?0:1;
  value=sqrt(value);
  if (x<0) return; if (y<0) return;
  if (x>=width) return; if (y>=height) return;
  u=(double)image[width*y+x];
  image[width*y+x]=(unsigned char)(u*value); //value ∈ [0,1], so okay
}

double fpart(double x) {
  return x-(int)(x); 
}
double rfpart(double x) { 
  return 1-fpart(x); 
}

void plotcol(int x, double y, double m,int swap,double colh) {
  double ylow=y-colh; double yhigh=y+colh;
  int ymin; int ymax; int j;
  ymin=round(ylow); ymax=rint(yhigh);
  plotw(x,ymin,fpart(ylow+0.5));
  for(j=ymin+1;j<ymax;j++) {
    plotw(x,j,0.0);
  }
  plotw(x,ymax,rfpart(yhigh+0.5));
}

void xwline(double x1, double y1, double x2, double y2) {
  //antialiased line algorithm; similar to Xiaolin Wu's but with thickness
  //many thanks to X. Wu; also to the pseudo-Python on Wikipedia
  double dx,dy,m,temp,colh; int swap=0;
  dx=x2-x1; dy=y2-y1;
  if (fabs(dy)>fabs(dx)) {
    temp=x1;x1=y1;y1=temp;
    temp=x2;x2=y2;y2=temp;
    temp=dx;dx=dy;dy=temp;
    swap=1;
  }
  if (dx<0) {
    temp=x1;x1=x2;x2=temp;
    temp=y1;y1=y2;y2=temp;
    dx=-dx; dy=-dy;
  } 
  m=dy/dx; colh=thickness*sqrt(1+m*m)/2;
  int xstart,xend; double ystart,yend;

  xstart=rint(x1); ystart=y1+m*(xstart-x1);
  xend=rint(x2); yend=y2+m*(xend-x2);
  
  // the loop
  int x; double y;
  y=ystart;
  for(x=xstart;x<=xend;x++){
    plotcol(x,y,m,swap,colh);
    y+=m;
  }
}

void cline(complex double z1, complex double z2) {
  z1*=sidelen; z2*=sidelen;
  xwline(creal(z1)+(width/2),
	 cimag(z1)+(height/2),
	 creal(z2)+(width/2),
	 cimag(z2)+(height/2));
}

void diamond(complex double m, int a0, int a1, int a2, int a3, int a4) {
  complex double corner00,corner01,corner10,corner11;
  corner00=m*fourier(a0,a1,a2,a3,a4);
  corner01=m*fourier(a0-1,a1,a2,a3,a4);
  corner10=m*fourier(a0,a1-1,a2,a3,a4);
  corner11=m*fourier(a0-1,a1-1,a2,a3,a4);
  cline(corner00,corner01);
  cline(corner01,corner11);
  cline(corner11,corner10);
  cline(corner10,corner00);
}

double k2(double c0, double c1) {
  return RPHI*c1-c0;
}

double k3(double c0, double c1) {
  return -RPHI*(c0+c1);
}

void diamonds(complex double m,complex double xi) {
  double gamma0=creal(xi)*0.4;
  double gamma1=creal(ZETA3*xi)*0.4;
  double gamma2=creal(ZETA1*xi)*0.4;
  double gamma3=creal(ZETA4*xi)*0.4;
  double gamma4=creal(ZETA2*xi)*0.4;
  complex double c0,c1,c2,c3,c4;
  for (int x0=-5;x0<5;x0++) {
    for (int x1=-5;x1<5;x1++) {
      c0=x0-gamma0;
      c1=x1-gamma1;
      complex double z=2*(c0-ZETA4*c1)/(1-ZETA3);
      c2=k2(c0,c1);
      c3=k3(c0,c1);
      c4=k2(c1,c0);
      complex double w=fourier(c0,c2,c4,c1,c3);
      double s=c0+c1+c2+c3+c4;
      //fprintf(stderr,"%f %f %f\n",s,creal(w),cimag(w));
      diamond(m,x0,x1,floor(c2+gamma2),floor(c3+gamma3),floor(c4+gamma4));
    }
  }
}

void diamondc(complex double m, int a0, int a1, int a2, int a3, int a4) {
  complex double corner00,corner01,corner10,corner11;
  corner00=m*fourier(a0,a1,a2,a3,a4);
  corner01=m*fourier(a0-1,a1,a2,a3,a4);
  corner10=m*fourier(a0,a1,a2-1,a3,a4);
  corner11=m*fourier(a0-1,a1,a2-1,a3,a4);
  cline(corner00,corner01);
  cline(corner01,corner11);
  cline(corner11,corner10);
  cline(corner10,corner00);
}

double k3c(double c0, double c2) {
  return -PHI*c0-c2;
}

double k1c(double c0, double c2) {
  return PHI*(c0+c2);
}

void diamondsc(complex double m,complex double xi) {
  double gamma0=creal(xi)*0.4;
  double gamma1=creal(ZETA3*xi)*0.4;
  double gamma2=creal(ZETA1*xi)*0.4;
  double gamma3=creal(ZETA4*xi)*0.4;
  double gamma4=creal(ZETA2*xi)*0.4;
  complex double c0,c1,c2,c3,c4;
  for (int x0=-5;x0<5;x0++) {
    for (int x2=-5;x2<5;x2++) {
      c0=x0-gamma0;
      c2=x2-gamma2;
      c1=k1c(c0,c2);
      c3=k3c(c0,c2);
      c4=k3c(c2,c0);
      complex double w=fourier(c0,c2,c4,c1,c3);
      double s=c0+c1+c2+c3+c4;
      //fprintf(stderr,"%f %f %f\n",s,creal(w),cimag(w));
      diamondc(m,x0,floor(c1+gamma1),x2,floor(c3+gamma3),floor(c4+gamma4));
    }
  }
}

void penrose(complex double xi) {
  diamonds(1,xi);
  diamonds(ZETA1,ZETA3*xi);
  diamonds(ZETA2,ZETA1*xi);
  diamonds(ZETA3,ZETA4*xi);
  diamonds(ZETA4,ZETA2*xi);
  diamondsc(1,xi);
  diamondsc(ZETA1,ZETA3*xi);
  diamondsc(ZETA2,ZETA1*xi);
  diamondsc(ZETA3,ZETA4*xi);
  diamondsc(ZETA4,ZETA2*xi);
}

void argassert(int condition) {
  if (condition) return;
  fprintf(stderr,"Usage: pen [-A] [-t thickness] width height sidelen\n");
  exit(1);
}

void parseargs(int argc, char* argv[]) {
  int c;
  thickness=1.5;
  alias=0;
  while((c=getopt(argc,argv,"t:A"))!=-1)
    switch (c) {
    case 't':
      thickness=atof(optarg);
      break;
    case 'A':
      alias=1;
    }
  argassert(optind<argc); width=atoi(argv[optind++]);
  argassert(optind<argc); height=atoi(argv[optind++]);
  size=height*width;
  argassert(optind<argc); sidelen=PHI*atof(argv[optind++]);
}

int main(int argc, char* argv[]) {
  int x; int y; int i;
  parseargs(argc,argv);
  char imstore[size];
  image=imstore;
  for(i=0;i<size;i++) image[i]=255;
  penrose(1);
  //diamonds(1,0.2);
  /* complex double z0,z1,z2,z3,z4,w; double s; */
  /* z0=2;z1=ZETA1+ZETA4;z2=ZETA2+ZETA3; z3=z2; z4=z1; */
  /* s=z0+z1+z2+z3+z4; w=fourier(z0,z2,z4,z1,z3); */
  /* printf(stderr,"%f %f %f\n",s,creal(w),cimag(w)); */
  pgmshow();
  return 0;
}

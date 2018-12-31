#include <complex.h>
#include <math.h>
#include <stdio.h>

int size=1000;
int length=200;
double span=1.6;

char brightness(int k,complex double z){
  if (k>15) return 255;
  double u; char j;
  u=log2(log2(cabs(z)))-3;
  j=(char)(floor(16*u)); j=15-j; if (j<0) j=0;
  return k*16+j;
}

void julia(complex double c, FILE * f) {
  fprintf(f,"P5 %d %d 255 ",size,size);
  complex double z; double x,y; char t;
  for(int i=0;i<size;i++) {
    y=span*(2*i-size)/size;
    for(int j=0;j<size;j++) {
      x=span*(2*j-size)/size;
      z=x+y*I;
      t=0;
      for(int k=0;k<80;k++) {
	if(cabs(z)>256) {
	  t=brightness(k-3,z);
	  break;
	}
	z=z*z+c;
      }
      fputc(t,f);
    }
  }
}

int main(int argc, char* argv[]) {
  FILE * f; complex double z; char * filename;
  for(int i=0;i<length;i++) {
    sprintf(filename,"julia%03d.pgm",i);
    f=fopen(filename,"w");
    z=0.5*cexp(2*I*M_PI*i/length); z=z*(1-z);
    julia(z,f);
    fclose(f);
  }
}

#include <complex.h>
#include <math.h>
#include <stdio.h>

int size=5000;
double span=2.0;

char brightness(int k,complex double z){
  if (k>15) return 255;
  double u; char j;
  u=log2(log2(cabs(z)))-3;
  j=(char)(floor(16*u)); j=15-j; if (j<0) j=0;
  return k*16+j;
}

void mandel(FILE * f) {
  fprintf(f,"P5 %d %d 255 ",size,size);
  complex double z,c; double x,y; char t;
  for(int i=0;i<size;i++) {
    y=span*(2*i-size)/size;
    for(int j=0;j<size;j++) {
      x=span*(2*j-size)/size;
      c=x+y*I;
      z=0;
      t=0;
      for(int k=0;k<80;k++) {
	if(cabs(z)>256) {
	  t=brightness(k-8,z); //originally k-3
	  break;
	}
	z=z*z+c;
      }
      fputc(t,f);
    }
  }
}

int main(int argc, char* argv[]) {
  FILE * f; complex double z;
  f=fopen("mandel.pgm","w");
  mandel(f);
  fclose(f);
}

/*
program tocalculat vector distances
lab2 ex3
michael cooper
21-10-18
*/

#include <stdio.h>
#include <math.h> // pow function

double VecDist(double x0, double y0, double x1, double y1);

int main(void) {
  // main function
  printf("%.2f\n",VecDist(0,0,4,3));
  printf("%.2f\n",VecDist(21,3,7,9));
  printf("%.2f\n",VecDist(-2,5,17,1));
  printf("%.2f\n",VecDist(-13,-5,9,2));
  printf("%.2f\n",VecDist(-6,-4,-14,19));
  return 0;
}

double VecDist(double x0, double y0, double x1, double y1){
  // Calcualtes the vector distance between two points (x0,y0)
  // and (x1,y1)
  double deltax = x0-x1; // dist between x coords
  double deltay = y0-y1; // sist between y coords
  return pow((deltax*deltax+deltay*deltay),0.5);
}
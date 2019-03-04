#include <stdio.h>

void cylinderV(float h, float r); /* function declaration*/

int main(void) {
  cylinderV(7.0, 4.0);
  cylinderV(20.0, 3.0);
  cylinderV(14.7, 5.2);
}

void cylinderV(float h, float r){
  /*function to calculate the volume of a cylinder*/
  float v = (3.14159265359*r*r)*h;
  printf("The cylinder with height %0.2fcm and radius %0.2fcm has a volume of %0.2fcm^3\n"
  ,h,r,v);
}
#include <stdio.h>

int cmToft(int cm); /* function declaration*/

int main(void) {
  cmToft(101);
  cmToft(3);
  cmToft(15);
  cmToft(92);
  cmToft(24);
}

int cmToft(int cm) {
  /* Converts an int of cm to two ints of feet and inches */
  int inch = (cm*100)/258;
  int feet = inch/12;
  inch = inch%12;
  printf("%d cm is %d feet %d inches to the nearest inch.\n", cm, feet, inch);
  }
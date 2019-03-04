#include <stdio.h>

int main(void) {

  /* Does some stupid arithmetic to always return the rsutl of 5*/
  int x = 7;
  int y = x+3;
  y = y*2;
  y += -4;
  y += -(2*x);
  y += 3;
  
  printf("%d\n",y);

}
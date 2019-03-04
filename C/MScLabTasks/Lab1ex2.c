#include <stdio.h>

void printseq(int x); /*Function Declaration*/

int main(void) {
  printseq(5);
  printseq(10);
  printseq(12);
}

void printseq(int x) {
  /* does some dumb ass counting without using a loop...*/
  printf("%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n"
  ,x,x+1,x+2,x+3,x+4,x+5,x+6,x+7,x+8,x+9,x+10);
}
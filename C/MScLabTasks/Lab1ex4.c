#include <stdio.h>

void fibonacci(int seqlen); /* function declaration*/

int main(void) {
  fibonacci(10);
}

void fibonacci(int seqlen) {
  /*function to print out a specified number within the fibonacci sequence*/
  int x0 = 0;
  int x1 = 1;
  int x2;
  int count = 0;

  while(count<seqlen){
    printf("%d\n",x0);
    x2 = x0+x1;
    x0 = x1;
    x1 = x2;
    count+=1;
  }
}
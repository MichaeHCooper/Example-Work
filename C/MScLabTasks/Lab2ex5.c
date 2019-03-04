/*
program to multiply ints using recursion
lab2 ex5
michael cooper
21-10-18
*/

#include <stdio.h>
#include <stdlib.h> //abs function

int multiply(int x, int y);
int multiplyneg(int x, int y);

int main(void) {
  // main function
  printf("%d\n",multiplyneg(6,3));
  printf("%d\n",multiplyneg(9,9));
  printf("%d\n",multiplyneg(3,0));
  printf("%d\n",multiplyneg(-1,7));
  printf("%d\n",multiplyneg(-29,803));
  return 0;
}

int multiplyneg(int x, int y){
  // seperate function to handle negatives
  if ( ((x<0)&&(y<0))||((x>0)&&(y>0)) ){
    return multiply(abs(x), abs(y));
  }
  if ( ((x<0)&&(y>0))||((x>0)&&(y<0)) ){
    return multiply(-abs(x), abs(y));
  }
  return 0;
}

int multiply(int x, int y){
// multiplys the positive ints x and y together
  if (y==0){
    return 0;
  }
  else {
    return x+multiply(x,y-1);
  }
}
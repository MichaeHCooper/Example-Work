/*
Lab3ex1
Michael Cooper
24.10.18
*/

#include <stdio.h>

int ForFactorial(int x);
int WhileFactorial(int x);
// Function declarations

int NoList[5] = {1,2,4,5,8};
// List of numbers to iterate through.

int main(void) {
  // main function
  // iterates through number list over for factorial
  int i;
  for (i=0; i<=4; i++){
    printf("%d\n", ForFactorial(NoList[i]));
  }
  int j;
  // Iterates throough number list over while factorial
  for (j=0; j<=4; j++){
    printf("%d\n", WhileFactorial(NoList[j]));
  }
  return 0;
}

int ForFactorial(int x){
  // Calculates the factorial of an integer using a for loop.
  int y = 1;
  int i;
  for (i=1; i<=x; i++){
    y *= i;
  }
  return y;
}

int WhileFactorial(int x){
  // Calculates the factorial of an integer using a while loop.
  int y = 1;
  int i = 1;
  while (i <= x){
    y *= i;
    i ++;
  }
  return y;
}
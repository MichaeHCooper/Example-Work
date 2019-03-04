/*
program to write out number facts
lab2 ex4
michael cooper
21-10-18
*/

#include <stdio.h>

void NoFacts(int x);
void isPrime(int x);
void OddEven(int x);

int main(void) {
  // main function
  NoFacts(11);
  NoFacts(74);
  NoFacts(307);
  NoFacts(7402);
  NoFacts(9357);
  return 0;
}

void NoFacts(int x){
  // prints basic facts about integers between 1 and 9999 inclusive
  // specifically if it is odd or even and whether it is prime
  if ((x >= 1)&&(x <= 9999)){
    printf("%d is ", x);
    OddEven(x);
    printf(" and ");
    isPrime(x);
    printf(".\n");
  }
  else {
    printf("number is not between 1 and 9999 inclusive\n");
  }
}

void isPrime(int x){
  // prints prime if prime, prints not prime if not prime
  int notprime = 0;
  for (int i=2; i<x; i++){ // loops from 2 to x-1
    if (x%i == 0){ // checks to see if x is divisible
      notprime = 1; // if it is turns notprime true
    }
  }
  if (notprime == 1){
    printf("not prime");
  }
  if (notprime == 0){
    printf("prime");
  }
}

void OddEven(int x){
  // prints odd if odd and even if even.
  if (x%2 == 0){
    printf("even");
  }
  else {
    printf("odd");
  }
}
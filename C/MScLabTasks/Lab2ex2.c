/*
program to write out numbers in english
lab2 ex2
michael cooper
21-10-18
*/

#include <stdio.h>

void PrintNumber(int x);
void stdFirst(int dig0);
void stdSec(int dig1);
void teens(int dig1);

int main(void) {
  // Main function
  PrintNumber(10);
  PrintNumber(23);
  PrintNumber(100);
  PrintNumber(3);
  PrintNumber(30);
  return 0;
}

void PrintNumber(int x){
  int dig0 = x/10; // first digit
  int dig1 = x%10; // second digit

  if ((x >= 0)&&(x <= 100)){
    if ((dig0 == 0)&&(dig1 != 0)){
      stdSec(dig1); // Catches 1-9
    }
    if ((dig0 == 1)&&(dig1 != 0)){
      teens(dig1); // Catches 11-19
    }
    if ((dig0 >= 2)&&(dig0 <= 9)&&(dig1 != 0)){
      stdFirst(dig0);
      printf(" ");
      stdSec(dig1);
      // Catches 21 - 99 excluding tens
    }
    if ((dig0 >= 0)&&(dig0 <= 10)&&(dig1 == 0)){
      stdFirst(dig0);
      printf("\n"); //Catches multiples of 10
    }
  }
  else {
    printf("No. is not between 0 and 100 inclusive");
  }
}

void stdFirst(int dig0){
  // Prints for standard first digits
  switch(dig0){
    case(0):
      printf("zero");
      break;
    case(1):
      printf("ten");
      break;
    case(2):
      printf("twenty");
      break;
    case(3):
      printf("thirty");
      break;
    case(4):
      printf("forty");
      break;
    case(5):
      printf("fifty");
      break;
    case(6):
      printf("sixty");
      break;
    case(7):
      printf("seventy");
      break;
    case(8):
      printf("eighty");
      break;
    case(9):
      printf("ninety");
      break;
    case(10):
      printf("one hundred");
      break;
  }
}

void stdSec(int dig1){
  // Prints for standard second digits
  switch(dig1){
    case(1):
      printf("one\n");
      break;
    case(2):
      printf("two\n");
      break;
    case(3):
      printf("three\n");
      break;
    case(4):
      printf("four\n");
      break;
    case(5):
      printf("five\n");
      break;
    case(6):
      printf("six\n");
      break;
    case(7):
      printf("seven\n");
      break;
    case(8):
      printf("eight\n");
      break;
    case(9):
      printf("nine\n");
      break;
  }
}

void teens(int dig1){
  // Prints full word if a teen
  switch(dig1){
    case(1):
      printf("eleven\n");
      break;
    case(2):
      printf("twelve\n");
      break;
    case(3):
      printf("thirteen\n");
      break;
    case(4):
      printf("fourteen\n");
      break;
    case(5):
      printf("fifteen\n");
      break;
    case(6):
      printf("sixteen\n");
      break;
    case(7):
      printf("seventeen\n");
      break;
    case(8):
      printf("eighteen\n");
      break;
    case(9):
      printf("nineteen\n");
      break;
  }
}
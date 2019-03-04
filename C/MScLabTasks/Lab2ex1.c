/*
program to create a function to test if even or odd
lab2 ex1
michael cooper
21-10-18
*/

#include <stdio.h>
#include <stdbool.h>
//Libraries

bool isEven(int x);
void isEvenPrint(int x);
// Function Declarations

int main(void) {
  // Main function
  isEvenPrint(10);
  isEvenPrint(21);
  isEvenPrint(33);
  isEvenPrint(8);
  isEvenPrint(200);
  return 0;
}

bool isEven(int x){
  // Function to test if x iseven or odd. returns false
  // if odd otherwise returns true if even.
  if (x%2 == 0){
    return true;
  }
  else {
    return false;
  }
}

void isEvenPrint(int x){
  //prints the output of isEven
  bool out = isEven(x);
  if (out == true){
    printf("True\n");
  }
  else {
    printf("False\n");
  }

}
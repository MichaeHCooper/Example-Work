/*
Lab3ex4
Michael Cooper
24.10.18
*/


#include <stdio.h>
#include <string.h>

int HexToDec(char Hex[]);
int intPow(int x, int n);

int main(void) {
  // Main function
  printf("%d\n",HexToDec("FF"));
  printf("%d\n",HexToDec("10"));
  printf("%d\n",HexToDec("ABC"));
  printf("%d\n",HexToDec("C2"));
  printf("%d\n",HexToDec("-AB"));
  return 0;
}

int HexToDec(char Hex[]){
  // Converts hexadecimal strings to integers
  char LookUpA[16] = "0123456789ABCDEF";
  char LookUpB[16] = "0123456789abcdef";
  char NegSign[1] = "-";
  // Look up tables to see if values match, two one for uppercase and one for lower.
  int y = 0;
  // The output value.
  int neg = 0;
  // Stores if neg. 0 if not negative, 1 if negative
  int valid = 1;
  // 0 if all chars valid 1 if not.

  for (int i=0; i<strlen(Hex); i++){
    if ((Hex[i]==NegSign[0])&&(i==0)){
      neg = 1;
      valid = 0;
    }
    // Scans through each element of the string.
    for (int j=0; j<16; j++){
      // Iterates over the look up tables to check for a match.
      if ((Hex[i]==LookUpA[j])||(Hex[i]==LookUpB[j])){
        y += j*intPow(16,(strlen(Hex)-i-1));
        // Adds j, which is what the symbol converts to as adecimal,multiplied by
        // 16^i, which is how to move up the placeholder.
        valid = 0;
        // If subroutine passes then a mathcing char has been found hence char is valid
      }
    }

    if (valid == 1){
      printf("Please input valid hexadecimal input\n");
      return -1;
    }
    valid = 1;
  }
  // Prints error statement if invalid char found and returns -1.

  if (neg==0){
    return y;
  }
  if (neg==1){
    return y*-1;
  }
  // Sorts out the negative and positive signs.

}

int intPow(int x, int n){
  //Calculates the power of the integer x so long as n is a positive integer or zero.
  if (n>0){
    int y = x;
    for (int i=1; i<n; i++){
      y *= x;
    }
    return y;
  // For all integers greater than 1 inclusive.
  }
  else{
    return 1;
  }
  // For zero
}
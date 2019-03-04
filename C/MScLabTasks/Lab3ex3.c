/*
Lab3ex3
Michael Cooper
24.10.18
*/

#include <stdio.h>
#include <stdlib.h>

void TimesTable(int n);

int main(void) {
  // Main function.
  TimesTable(5);
  printf("\n");
  TimesTable(3);
  printf("\n");
  TimesTable(8);
  return 0;
}

void TimesTable(int n){
  // Creates an array of a square times table and retruns the memory pointer.
  int **Table;
  Table = malloc(sizeof(int*)*n);
  for (int i=0; i<n; i++){
    Table[i] = malloc(sizeof(int)*n);
  }
  // Intialises array and allocates variable memory.
  for (int i=0; i<n; i++){
    for (int j=0; j<n; j++){
      Table[i][j] = (i+1)*(j+1);
    }
  }
  // Fills  out the values in the array.
  for (int i=0; i<n; i++){
    for (int j=0; j<n; j++){
      printf("%d,", Table[i][j]);
    }
    printf("\n");
  }
  // Prints out the array.
}
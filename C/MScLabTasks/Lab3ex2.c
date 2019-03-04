/*
Lab3ex2
Michael Cooper
24.10.18
*/

#include <stdio.h>
#include <string.h> // String Functions
#include <stdlib.h> // Memory Allocation
// Importing Libraries

void TreeLine(int TotalW, int StarW);
void Tree(int Width, int TrunkLength);
// Declaring Functions

int main(void) {
  // Main Function
  Tree(9, 4);
  printf("\n");
  Tree(5, 2);
  printf("\n");
  Tree(11, 6);
  return 0;
}

void Tree(int Width, int TrunkLength){
  if (Width%2 != 0){
    // Prints a tree of specified bush width and trunk length
    int height = (Width+1)/2;
    for (int i=0; i<height; i++){
      TreeLine(Width, (i*2+1));
    }
    // Creates Bush
    for (int i=0; i<TrunkLength; i++){
      TreeLine(Width, 3);
    }
    // Creates Trunk
  }
  else{
    printf("Please use odd width");
  }
}

void TreeLine(int TotalW, int StarW){
  // Prints a line of the tree function, specifically it prints a set number of
  // asterisks centered between a set number of spaces.  Only takes odd integers.
  char *Line;
  Line = (char *) malloc(TotalW);
  // Instansiates a variable amount of memmory to the string line
  int NoSpaces = (TotalW-StarW)/2;
  for (int i=0; i<NoSpaces; i++){
    strcat(Line, " ");
  }
  for (int i=0; i<StarW; i++){
    strcat(Line, "*");
  }
  for (int i=0; i<NoSpaces; i++){
    strcat(Line, " ");
  }
  strcat(Line, "\n");
  // Constructs the string
  printf(Line);
}
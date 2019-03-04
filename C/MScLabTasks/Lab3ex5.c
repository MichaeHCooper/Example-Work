/*
Lab3ex5
Michael Cooper
24.10.18
*/

#include <stdio.h>
#include <string.h>

int reverse(char input[]);

int main(int argc, char *argv[]) {
	// Main program, takes the command line arguments and
	// outputs in the reverse order.
	char output[68];
	// Instantiates the string. 6 words of length 10 chars
	// plus 6 spaces and return line.
	if (argc > 7){
		printf("too many words");
		return 1;
	}
	for (int i=(argc-1); i>0; i--){
		if (strlen(argv[i]) > 11){
			printf("too many chars in word");
			return 1;
		}
		strcat(output, argv[i]);
		strcat(output, " ");
	}
	strcat(output, "\n");
	printf("%s", output);
	
  return 0;
}
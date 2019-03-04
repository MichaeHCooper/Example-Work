/*
Foundations of computation coursework for parser.
Author - Michael Cooper
Date Created - 05.12.2018

The program contains functions to check that words are accepted by a
particular context free grammar given in Chomsky Normal Form.

The Grammar consists of the following rules:
{
    E -> E+T,
    E -> T,
    T -> T∗F,
    T -> F,
    F -> (E),
    F -> x
}

I have converted the Grammar into the following grammar in Chomsky 
Normal Form.
{
    S0->EA, E->EA, A->PT,
    S0->TB, E->TB, T->TB, B->MF,
    S0->LC, E->LC, T->LC, F->LC, C->ER,
    S0->x,  E->x,  T->x,  F->x,
    P->+,   M->*,  L->(,  R->)
}

Also represented by:
{
    S0 -> EA|TB|LC|x
    E  -> EA|TB|LC|x
    T  ->    TB|LC|x
    F  ->       LC|x
    A  -> PT
    B  -> MF
    C  -> ER
    P  -> +
    M  -> *
    L  -> (
    R  -> )
}

S0 internally is represented by S such that there are no two 
charachter strings to read.

Finally the parse trees are represented as a series of successive
words that have one rue applied to them.  Each parse sequence is
unabigous and could be quickly turned into a parse tree by hand.
In short the parse sequences are analagous to the parse trees.

Furthermore the parse tree for the CYK algorithm converts to the
terminals in one step after creating the non-terminals, again this
step is unabiguous.  This has been done for simplicities sake.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// Importing all required libraries.

void parseAlgBasic(char word[]);
// Declaring the parseAlgBasic function.
void parseAlgCYK(char word[]);
// Declaring the parseAlgCYK function.

int main(void)
{
    // CYK parser.
    printf("\n\n########## CYK PARSER ##########\n\n");
    parseAlgCYK("(((x+(x)*x)*x)*x)");
    parseAlgCYK("x*x*x+x*(x)");
    parseAlgCYK("(x*x)*x+x+(x)");
    parseAlgCYK("(x+x))∗((x)∗x");
    return 0;
}

//####################################################################
//####################################################################
//####################################################################

void parseAlgCYK(char word[])
{
    /*
    This function performs the eceptionally effecient CYK
    Algorithm.  The funnction also implements back pointers,
    such that the parse tree can be printed if the word has been
    accepted.

    To assist the marker in understanding correct implementation
    of the program all lines of the psuedo code have been put next
    to their actual lines of code within hats: ^psuedo code^.

    Unlike the niave algroithm which runs at worst case of (2n)!(4^2n)
    complexity, this runs at 11(n^3) complexity which is vastly more
    effecient.
    */

    int n = strlen(word);
    // "word is the input string, with n simply being the length."
    char NT[11] = {'S','E','T','F','A','B','C','P','M','L','R'};
    // NT is the array of all non terminal symbols, such that a
    // symbol's charachter can be called up by index.
    int parseArray[100][100][11];
    // Initialises the array to be operated on.  For a perfect
    // algorithm this should be malloc'd, howver for the purposes of 
    // the coursework it is unlikely that any string longer than 100 
    // is to be encounterd, and at any rate malloc can lead to memory
    // error especially if a very large 3D array is attempted to be
    // initialised. The array is an 3D array of bools with zero being
    // false and one being true.
    int backPoint[100][100][11][6];
    // Creates an array of back pointers to keep track of a parse
    // tree.  Note does not keep track of all parse trees.  The array
    // basically sets 6 numbers to each rule, which point to the
    // location in "parseArray" where the two constituent rules are.

    memset(parseArray, 0, sizeof parseArray);
    memset(backPoint, -1, sizeof backPoint);
    // Clears the memory in the array setting it entirely to zero.
    // this ensures that the array is indeed empty.

    char TRule[8] = {'x','x','x','x','+','*','(',')'};
    // Array of all of the terminal rules.  This is used to both read
    // the rules and to input them into the arrays.
    int Tindex[8] = {0,1,2,3,7,8,9,10};
    // Array that tells the program at what index to put a terminal 
    // rule at.

    int NTindex[12][3] =
    {{0,1,4},{0,2,5},{0,9,6},
     {1,1,4},{1,2,5},{1,9,6},
     {2,2,5},{2,9,6},{3,9,6},
     {4,7,2},{5,8,3},{6,1,10}};
    // Array that tells the program at what index to put a
    // non-terminal rule at, in essenc an integer version of what
    // would be the NTrules.

    for (int i=0; i<n; i++)
    {
        // ^for i = 1 to n do^
        for (int j=0; j<8; j++)
        {
            // ^for each nonterminal A do^
            if (word[i] == TRule[j])
            // ^test whether A → b is a rule, where b = wi;^
            {
                parseArray[i][i][Tindex[j]] = 1;
                // ^if so, place A in table(i, i);^
            }
        }
    }
    // This section of the code reads all of the letters in the word
    // and if they are terminals, places their corresponding non-
    // terminals into the 3D array, showing all possible NT's that can
    // make the respective terminal.

    for (int i=2; i<=n; i++)
    {
        // ^for l = 2 to n do^
        for (int j=1; j<=n-i+1; j++)
        {
            // ^For i = 1 to n − l + 1 do^
            int k = j+i-1;
            // ^let j := i + l − 1;^
            for (int l=j; l<=k-1; l++)
            {
                // ^for k = i to j − 1 do^
                for (int m=1; m<=12; m++)
                {
                    // ^for each rule A → BC do^
                    int B = NTindex[m-1][1];
                    int C = NTindex[m-1][2];
                    int ifB = parseArray[j-1][l-1][B];
                    // ^table(i, k) B^
                    int ifC = parseArray[l+1-1][k-1][C];
                    // ^table(k + 1, j) C^
                    if (ifB==1&&ifC==1)
                    {
                        // ^if table(i, k) contains B and
                        // table(k + 1, j) contains C then put A in
                        // table(i, j);^
                        int A = NTindex[m-1][0];
                        parseArray[j-1][k-1][A] = 1;

                        backPoint[j-1][k-1][A][0] = j-1;
                        backPoint[j-1][k-1][A][1] = l-1;
                        backPoint[j-1][k-1][A][2] = B;
                        backPoint[j-1][k-1][A][3] = l+1-1;
                        backPoint[j-1][k-1][A][4] = k-1;
                        backPoint[j-1][k-1][A][5] = C;
                        // This section then sets the pointers for the
                        // back pointer array.
                    }
                }
            }
        }
    }
    // This section then reads all of the rules working from the
    // bottom up, applying the CYK algorithm.

    int wordAccepted = 0;
    // Initialises wordAccepted, does what it says on the tin.
    if ((parseArray[0][n-1][0] == 1)&&(n>0))
    {
        // ^if S is in table(1, n) then accept^
        wordAccepted = 1;
        printf("Word Accepted\n");
        printf("%s\n", word);
        // Accepting if statement.
    }
    else
    {
        //  else reject;
        wordAccepted = 0;
        printf("Word Rejected\n");
        printf("%s\n\n", word);
        // Rejecting else statement.
    }
    // This section checks to see if there is an S rule in the top
    // right of the table, if so then accepts the word.


    if (wordAccepted == 1)
    {
        // This section of the code is to print out the parse tree
        // if the word has been accepted.

        int treeA[100][3];
        memset(treeA, -1, sizeof treeA);
        treeA[0][0] = 0;
        treeA[0][1] = n-1;
        treeA[0][2] = 0;
        // Initialises the tree that is being read from
        int treeB[100][3];
        memset(treeB, -1, sizeof treeB);
        // Initialises the tree that is being written to.  These trees
        // hold the idex of the rule being read.

        for (int x=0; x<(n); x++)
        {
            // This then loops ofver the lenght of the words, as that
            // is the number of rules applied to make the word.
            for (int y=0; y<100; y++)
            {
                if (treeA[y][0] != -1)
                {
                    int k = treeA[y][2];
                    printf("%c", NT[k]);
                }
            }
            printf(" ->\n");
            // This section prints out in letter form the current
            // tree.

            if (x==n-1)
            {
                for (int y=0; y<100; y++)
                {
                    if (treeA[y][0] != -1)
                    {
                        int k = treeA[y][2];
                        for (int z=0; z<8; z++)
                        {
                            if (Tindex[z] == k)
                            {
                                printf("%c", TRule[z]);
                            }
                        }
                    }
                }
                printf("\n\n");
            }
            // This section the prints out the final word, by looping
            // through each non-terminal and replacing it with the
            // respective terminal rule.

            int locA = 0;
            // locA is the current location in treeA that is being
            // read from.
            int locB = 0;
            // locB is the current location in treeA that is being
            // read from.
            int NTfound = 0;
            // This is a simple boolean of whether a non terminal has
            // been found.

            for (int m=0; m<100; m++)
            {
                int i = treeA[locB][0];
                int j = treeA[locB][1];
                int k = treeA[locB][2];
                // Current letter location in the both the backPoint
                // and parseArray Arrays.
                int left[3] =  {backPoint[i][j][k][0],
                                backPoint[i][j][k][1],
                                backPoint[i][j][k][2]};
                // Left hand rule index.
                int right[3] = {backPoint[i][j][k][3],
                                backPoint[i][j][k][4],
                                backPoint[i][j][k][5]};
                // Right hand rule index.

                if ((left[0] != -1)&&(NTfound == 0))
                {
                    memcpy(treeB[locA], left, sizeof(left));
                    memcpy(treeB[locA+1], right, sizeof(right));
                    locA+=2;
                    locB++;
                    NTfound = 1;
                }
                // If the rule searched is a non-terminal then it
                // places the two rules into treeB.
                else
                {
                    memcpy(treeB[locA], treeA[locB],
                    sizeof(treeA[locB]));
                    locA++;
                    locB++;
                }
                // If the rule is terminal or non existant, then it
                // simply copies what is in treeA.
            }
            memset(treeA, -1, sizeof treeA);
            memcpy(treeA, treeB, sizeof(treeA));
            memset(treeB, -1, sizeof treeA);
            // Finally this sets treeA to treeB and clears the
            // respective memories.
        }
    }
}

//####################################################################
//####################################################################
//####################################################################
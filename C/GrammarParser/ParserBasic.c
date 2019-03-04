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
    // Basic parser.
    printf("\n\n######### BASIC PARSER #########\n\n");
    parseAlgBasic("x+x");
    parseAlgBasic("()");
    parseAlgBasic("xx");
    return 0;
}


//####################################################################
//####################################################################
//####################################################################

void parseAlgBasic(char word[])
{
    /*
    This function performs the basic algorithm to check for an 
    accepted word.  The algorithm is very naive, it simply checks
    every single possible combination of rules along with every
    possible combination of letter which those rules can be applied
    to.  With word length n, the algorithm checks (2n)!(4^2n) words.
    Thus for word lengths:

    | n |        Words Checked       |
    | 0 |                          1 |
    | 1 |                         32 |
    | 2 |                      6 144 |
    | 3 |                  2 949 120 |
    | 4 |              2 642 411 520 |
    | 5 |          3 805 072 588 800 |
    | 6 |      8 036 313 307 545 600 |
    | 7 | 23 401 744 351 572 787 200 |

    Consequently this algorithm is very, very inefficient.  Note that
    whilst the program will work on any word up to length 50 - this is
    the limit hard coded by the array sizes - it will take such a
    preposturously long time for words of length greater than 4, that
    it will appear to not function.

    The algorithm could be made much slightly more effecient by
    terminating derivations that go over wordLength's size in
    letters, however this has not been done.
    */

    char S[4][2] = {{'E','A'},{'T','B'},{'L','C'},{'x','z'}};
    char E[4][2] = {{'E','A'},{'T','B'},{'L','C'},{'x','z'}};
    char T[4][2] = {{'T','B'},{'L','C'},{'x','z'},{'z','z'}};
    char F[4][2] = {{'L','C'},{'x','z'},{'z','z'},{'z','z'}};
    char A[4][2] = {{'P','T'},{'z','z'},{'z','z'},{'z','z'}};
    char B[4][2] = {{'M','F'},{'z','z'},{'z','z'},{'z','z'}};
    char C[4][2] = {{'E','R'},{'z','z'},{'z','z'},{'z','z'}};
    char P[4][2] = {{'+','z'},{'z','z'},{'z','z'},{'z','z'}};
    char M[4][2] = {{'*','z'},{'z','z'},{'z','z'},{'z','z'}};
    char L[4][2] = {{'(','z'},{'z','z'},{'z','z'},{'z','z'}};
    char R[4][2] = {{')','z'},{'z','z'},{'z','z'},{'z','z'}};
    // Hard Coding the parser rules in. 'z' is used to represent null
    // rules, this is so that the program can keep track of where to
    // insert the letters.

    int running = 0;

    int wordLength = strlen(word);
    // Length of the input word.
    if (wordLength == 0)
    {
        running++;
    }
    // This accounts for the special case that the input word is
    // empty, this automatically rejects the word as the grammar
    // cannot generate an empty word.

    for (int i=0; i<wordLength; i++)
    {
        if (!((word[i]=='x')||(word[i]=='+')||(word[i]=='*')||
            (word[i]=='(')||(word[i]==')')))
        {
            running++;
        }
    }
    // This section rejects words made from anything excluding the
    // terminal charachters straight off the bat.

    if (running != 0)
    {
        printf("Word Rejected\n");
        printf("%s\n\n", word);
    }
    // If the word has failed thus far, prints word rejected.

    int ruleCount[100];// = {0,0,3,2,0};
    for (int i=0; i<(2*wordLength); i++)
    {
        ruleCount[i] = 0;
    }
    // Initialises the array which keeps track of which set of rules
    // to try next.

    int letterCount[100];// = {0,1,0,2,1};
    for (int i=0; i<(2*wordLength); i++)
    {
        letterCount[i] = 0;
    }
    // Initialises the array which keeps track of which set letters
    // to try next.
    
    char wordGenA[100];
    // This is the generated word to be read.
    char wordGenB[100];
    // This is the generated word that has the new letters appended to
    // it after reading a rule.
    char wordTest[100];
    // This is the word that is tested against.
    char wordIn[100];
    // This is the input word, formatted such that a strcmp can be
    // used against wordTest.

    int wordFound = 0;
    // A boolean of whether the word has been found or not.

    memset(wordIn, 0, sizeof wordIn);
    for (int i=0; i<wordLength; i++)
    {
        wordIn[i] = word[i];
    }
    // This section formats the word and clears any memory currently
    // in the array.

    while (running<1)
    {
        // This loop searches through every combination of rule
        // through every letter.

        memset(wordGenA, 0, sizeof wordGenA);
        memset(wordGenB, 0, sizeof wordGenB);
        // Clears the memory in each of the arrays.

        wordGenA[0] = 'S';
        // Sets the first word as S.
        for (int i=0; i<(2*wordLength)-1; i++)
        {
            // Iterates through the ruleCount array to generate a
            // single word.
            int n = letterCount[i];
            // This is the position of the letter that a rule is
            // applied to.
            int m = 2;
            int l = 1;
            // These are the positions in the arrays to append the
            // and locate the letters after a rule to.

            char letter = wordGenA[letterCount[i]];
            // The current letter that is read and operated on.

            for (int j=0; j<n-1; j++)
            {
                wordGenB[j]=wordGenA[j];
            }
            // Appends prior letters to word B.

            switch(letter)
            {
                // Massive block of code which applies the rules to a
                // given letter.
                case 'S':
                if ((S[ruleCount[i]][0]=='z')&&(S[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (S[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = S[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = S[ruleCount[i]][0];
                    wordGenB[n+1] = S[ruleCount[i]][1];
                }
                break;

                case 'E':
                if ((E[ruleCount[i]][0]=='z')&&(E[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (E[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = E[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = E[ruleCount[i]][0];
                    wordGenB[n+1] = E[ruleCount[i]][1];
                }
                break;

                case 'T':
                if ((T[ruleCount[i]][0]=='z')&&(T[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (T[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = T[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = T[ruleCount[i]][0];
                    wordGenB[n+1] = T[ruleCount[i]][1];
                }
                break;

                case 'F':
                if ((F[ruleCount[i]][0]=='z')&&(F[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (F[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = F[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = F[ruleCount[i]][0];
                    wordGenB[n+1] = F[ruleCount[i]][1];
                }
                break;

                case 'A':
                if ((A[ruleCount[i]][0]=='z')&&(A[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (A[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = A[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = A[ruleCount[i]][0];
                    wordGenB[n+1] = A[ruleCount[i]][1];
                }
                break;

                case 'B':
                if ((B[ruleCount[i]][0]=='z')&&(B[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (B[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = B[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = B[ruleCount[i]][0];
                    wordGenB[n+1] = B[ruleCount[i]][1];
                }
                break;

                case 'C':
                if ((C[ruleCount[i]][0]=='z')&&(C[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (C[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = C[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = C[ruleCount[i]][0];
                    wordGenB[n+1] = C[ruleCount[i]][1];
                }
                break;

                case 'P':
                if ((P[ruleCount[i]][0]=='z')&&(P[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (P[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = P[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = P[ruleCount[i]][0];
                    wordGenB[n+1] = P[ruleCount[i]][1];
                }
                break;

                case 'M':
                if ((M[ruleCount[i]][0]=='z')&&(M[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (M[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = M[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = M[ruleCount[i]][0];
                    wordGenB[n+1] = M[ruleCount[i]][1];
                }
                break;

                case 'L':
                if ((L[ruleCount[i]][0]=='z')&&(L[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (L[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = L[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = L[ruleCount[i]][0];
                    wordGenB[n+1] = L[ruleCount[i]][1];
                }
                break;

                case 'R':
                if ((R[ruleCount[i]][0]=='z')&&(R[ruleCount[i]][1]=='z'))
                {
                    m -= 2;
                    l -= 1;
                }
                else if (R[ruleCount[i]][1]=='z')
                {
                    wordGenB[n] = R[ruleCount[i]][0];
                    m -= 1;
                }
                else
                {
                    wordGenB[n] = R[ruleCount[i]][0];
                    wordGenB[n+1] = R[ruleCount[i]][1];
                }
                break;
                
                default:
                {
                    m -= 2;
                    l -= 1;
                    // does nothing if a terminal read.
                }
                break;
            }

            for (int j=n; j<2*wordLength; j++)
            {
                wordGenB[j+m]=wordGenA[j+l];
            }
            // This loop appends subsequent letters to the word.
            if (wordFound == 1)
            {
                // This prints the parse sequence if the word has been
                // generated.
                printf("%s ->\n", wordGenA);
            }
            memcpy(wordGenA, wordGenB, sizeof(wordGenA));
            // This then sets the generated word to the read word.
        }
        
        memset(wordTest, 0, sizeof wordTest);
        for (int i=0; i<wordLength; i++)
        {
            wordTest[i] = wordGenB[i];
        }
        // This sets a generated word to the word to be tested aginst.
        // This always produces a word that is of eqaul length to the
        // input word.

        if (strcmp(wordTest, wordIn) == 0)
        {
            if (wordFound == 0)
            {
                printf("Word Accepted\n");
                printf("%s\n", word);
            }
            if (wordFound == 1)
            {
                printf("%s\n\n",wordGenB);
                running++;
            }
            wordFound = 1;
        }
        // This then checks the word against the input word, if they
        // are equal then it terminates the loop and prints "word
        // accepted".  This specific section of code then allows the
        // loop to preceed one more, not changing the rules or
        // letters, so that the parse tree can be printed.

        if (wordFound == 0)
        {
            // If statement prevents the ticker going up if a word has
            // been found.
            ruleCount[2*wordLength-1]++;
            for (int k=1; k<2*wordLength; k++)
            {
            if (ruleCount[2*wordLength-k] == 4)
            {
                ruleCount[2*wordLength-k]=0;
                ruleCount[2*wordLength-k-1]++;
            }
            }
            // Ticks up the rule counter, with every tested word.
            if (ruleCount[0]==4)
            {
                for (int k=0; k<2*wordLength-1; k++)
                {
                    ruleCount[k] = 0;
                }
                // resets the rule counter to all zeros.
                letterCount[2*wordLength-1]++;
                for (int k=1; k<2*wordLength; k++)
                {
                    if (letterCount[2*wordLength-k] ==
                    2*wordLength-k+1)
                    {
                        letterCount[2*wordLength-k]=0;
                        letterCount[2*wordLength-k-1]++;
                    }
                }
            }
            // Ticks up the word counter, after every rule combination is
            // tried.
        }

        if (letterCount[0] == 1)
        {
            printf("Word Rejected\n");
            printf("%s\n\n", word);
            running++;
        }
        // This finally checks to see if every combination has been
        // tried, if so then it prints 
    }
}

//####################################################################
//####################################################################
//####################################################################
/*
Author: Justin Patrick
Class: CS 477
Project: Hwk 3 problem 2a
Date: 2/24/19
*/

#include <stdio.h>
#include <string>

//Name: swapMe
//Purpose: swap the passed integers
//Params:
	//int first: int to be swapped
	//int second: int to be swapped
void swapMe(int *first, int *second)
  {
    int temporary = *first;
    *first = *second;
    *second = temporary;
  }

//Name: printGroup
//Purpose: Print out the contents of the array in it's current order
//Params:
	//int qb[]: the sorted array to be printed
	//int max: the size of the array
void printGroup(int qb[], int max)
{
  int i;
  //for loop looping through passed array to print out its contents
  for (i = 0; i < max; i++)
    {
      printf("%c ", (char)qb[i]);
    }
  //separate print outs for readability
  printf("\n");
}

//Name: bubble_sort
//Purpose: Sort designated array using the bubble sort method
//Params:
	//int qb[]: an array holding the string to be sorted
	//int z: passed integer determined in
void bubble_sort(int qb[], int z)
{
  //variable declaration
  bool beenSwap;
  int a, b;
  int checks = 0;

  //for loop implementing right to left, left to right swap system
  for (a = 0; a < z-1; a++)
    {
      beenSwap = false;
      if(a%2 == 0)
        {
          for (b = 0; b < z-1; b++)
            {
              if(qb[b] > qb[b+1])
                {
                  swapMe(&qb[b], &qb[b+1]);
                  beenSwap = true;
                  checks++;
                }
            }
            printf("Right to left swap: ");
            printGroup(qb,z);
	    printf("\n");
        }
      else
        {
          for (b = z-1; b > 0; b--)
            {
              if(qb[b-1] > qb[b])
                {
                  swapMe(&qb[b],&qb[b-1]);
                  beenSwap = true;
                  checks;
                }
            }
            printf("Left to right swap: ");
            printGroup(qb,z);
	    printf("\n");
        }
      if(beenSwap == false)
        {
          break;
        }
    }
    printf("Comparaisons made: ");
    printf("%d\n", checks);
    printf("\n");
}

//Name: main
//Purpose: run designed bubble sort on "EASYQUESTION"
//Params: none
int main()
{
  //variable declaration
  char definedStr[] = "EASYQUESTION";
  int f = (sizeof(definedStr)/sizeof(*definedStr))-1;
  int* arr = new int [f];
  for(int i=0; i < f; i++)
    {
      arr[i] = (int)definedStr[i];
    }
  //running bubble sort on given array
  printf("Given array: ");
  printGroup(arr, f);
  printf("\n");
  bubble_sort(arr,f);
  printf("Sorted array: ");
  printGroup(arr,f);
  return 0;
}

/*
Author: Justin Patrick
Class: CS 477
Project: Hwk 3 problem 3
Date: 2/24/19
*/

#include <stdlib.h>
#include <stdio.h>

void mergeMe(int group[], int a, int b, int c);

int min(int x, int y) { return (x<y)? x :y; }


//Name: merge_sort
//Purpose: sort passed in array group[]
//Params:
	//int group[]: array holding contents to be swapped
	//int a: indice int
void merge_sort(int group[], int a)
  {
    //size of subarrays being merged
    int sN;
    //starting indice of left subarray being merged
    int iS;
    //for loop operating merge sort
    for(sN = 1;sN <= a-1;sN = 2*sN)
      {
        for(iS = 0;iS < a-1;iS += 2*sN)
          {
            int middle = iS + sN - 1;
            int end = min(iS + 2*sN - 1, a-1);
            mergeMe(group, iS, middle, end);
          }
      }
  }

//Name: mergeMe
//Purpose: merge the two halves found in merge_sort
//Params:
	//int group[]: array holding contents to be merged
	//int a: first sub array start indice
	//int b: first sub array indice end
	//int c: second subarray indice end
void mergeMe(int group[], int a, int b, int c)
    {
      //intial indicies of first, second and merged subarray
      int i, j, k;
      int alpha = b - a + 1;
      int bravo = c - b;

      //temporary arrays left and right
      int Left[alpha], Right[bravo];
      printf("First half...\n");
      for(i = 0; i < alpha; i++)
        {
          Left[i] = group[a + i];
	  printf("[%d] ", Left[i]);
        }
      printf("\n");
      printf("\n");
      printf("Second half...\n");
      for(j = 0; j < bravo; j++)
        {
          Right[j] = group[b + 1 + j];
	         printf("[%d] ", Right[j]);	 
        }
      printf("\n");
      printf("\n");
      i = 0;
      j = 0;
      k = a;
      printf("Merging halves...\n");
      while(i < alpha && j < bravo)
        {
          if(Left[i] <= Right[j])
            {
              group[k] = Left[i];
              i++;
            }
          else
            {
              group[k] = Right[j];
	      j++;
            }
          k++;
	  printf("[%d] ", group[k]);
        }
      printf("\n");
      printf("\n");
      while(i < alpha)
        {
          group[k] = Left[i];
          i++;
          k++;
        }

      while(j < bravo)
        {
          group[k] = Right[j];
          j++;
          k++;
        }
    }

//Name: printGroup
//Purpose: Print out the contents of the array in it's current order
//Params:
	//int group[]: the sorted array to be printed
	//int max: the size of the array
void printGroup(int group[], int max)
  {
    //variable defintions
    int i;
    //for loop looping through array to print contents
    for (i = 0; i < max; i++)
      {
        printf("%C ",(char) group[i]);
      }
    printf("\n");
  }

//Name: main
//Purpose: run designed bubble sort on "ASORTINGEXAMPLE"
//Params: none
int main()
  {
    //variable definitions
    char definedStr[] = "ASORTINGEXAMPLE";
    int n = (sizeof(definedStr)/sizeof(*definedStr))-1;
    int* arr = new int[n];
    for(int i = 0; i < n; i++)
      {
        arr[i] = (int)definedStr[i];
      }

    //running merge sort on the given array
    printf("Given array: ");
    printGroup(arr, n);
    printf("\n");
    merge_sort(arr,n);
    printf("Sorted array is: ");
    printGroup(arr, n);
    return 0;
  }

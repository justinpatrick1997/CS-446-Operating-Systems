/**************************************
Author: Justin Patrick
Class: CS 477
Project: Negative before Positive Sort
Date: 3/7/19
**************************************/

#include <iostream>
#include <algorithm>

using namespace std;

void negPosSort(int pSet[], int pLen);

int main()
{
  int numSet[] = {4, 3, -2, 9, -1, 10, 0, 5, 23, -4};
  //variable for finding size of array
  int setLen = 0;
  //loop var
  int i = 0;
  //finding size of array
  setLen = sizeof(numSet)/sizeof(numSet[0]);
  //sort the set of numbers
  negPosSort(numSet, setLen);
  cout << "[";
  for(i; i < setLen; i++)
    {
      cout << numSet[i];
      if(i < (setLen - 1))
        {
          cout << ", ";
        }
    }
    cout << "]" << endl;
    return 0;
}

void negPosSort(int pSet[], int pLen)
{
  //variable intialize
  int i = 0, j = 0;
  //run loop checking if there exists a negative element after a positive number
  for(i; i < pLen; i++)
    {
      //if the checked number is negative
      if(pSet[i] < 0)
        {
          //swap with the which ever element j is
          swap(pSet[i], pSet[j]);
          j++;
        }
    }

}

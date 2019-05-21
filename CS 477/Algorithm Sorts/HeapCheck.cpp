/**************************************
Author: Justin Patrick
Class: CS 477
Project: Heap Determine
Date: 3/21/19
**************************************/

#include <iostream>
#include <cmath>

using namespace std;

bool heapCheck(int qb[], int indice, int size);

int main()
{
	bool testA, testB;

	int A[] = {16, 14, 10, 8, 7, 9, 3, 2, 4, 1};
	int B[] = {10, 3, 9, 7, 2, 11, 5, 1, 6};
	
	int sizeA = (sizeof(A)/sizeof(A[0]));
	int sizeB = (sizeof(B)/sizeof(B[0]));

	testA = heapCheck(A, 0, sizeA);
	testB = heapCheck(B, 0, sizeB);

	testA ? cout << "YES, A is a heap." << endl : cout << "A is Not a heap." << endl;
  	testB ? cout << "YES, B is a heap." <<endl : cout << "B is Not a heap." <<endl ;
	cout << "In both best and worst case, runtime of this algorithm is O(nlogn)." << endl;

	return 0;
}

bool heapCheck(int qb[], int indice, int size)
{
	//is this node a leaf
	if (indice > ((size-2)/2))
		{
			return true;
		}
	//check left then right, call heapCheck again to determine if heap or not a heap
	if (qb[indice] >= qb[2*indice+1] && qb[indice] >= qb[2*indice+2])
		{
			if(heapCheck(qb, 2*indice+1, size) && heapCheck(qb, 2*indice+2, size))
				{
					return true;
			
				}
		}

	return false;
}


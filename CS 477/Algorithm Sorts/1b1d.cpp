/**************************************
Author: Justin Patrick
Class: CS 477
Project: Dynamic Programming
Date: 4/21/19
**************************************/

#include <iostream>	
#include <vector>		
#include <algorithm>	
using namespace std;

//Function definitions
int maxptB(vector<int> board, vector<int> revenue, int distance, int minimumMilesPerBoard);
void maxptD(vector<int> board, vector<int> revenue, int distance, int minimumMilesPerBoard);

int main()
{
	vector<int> x { 6, 7, 12, 14 };
	vector<int> r { 5, 6, 5, 1 };
	unsigned int d = 20;
	unsigned int minMiPerBoard = 5;
	int maxRev;

	//problem1 partb  print.
	maxRev = maxptB(x, r, d, minMiPerBoard);

	cout << "Maximum revenue: " << maxRev << endl;

	//problem1 partd print.
	maxptD(x, r, d, minMiPerBoard);
	cout << endl;

	return 0;
}

// maxptB computes the optimal value to this problem, showing all subproblems.
int maxptB(vector<int> board, vector<int> revenue, int distance, int minimumMilesPerBoard)
{
	int * opVal = new int[distance + 1];
	int next = 0;
	minimumMilesPerBoard += 1;
	opVal[0] = 0;

	//auxillary table for problem 1 part B.
	cout << "Auxillary Table part B" << endl;
	cout << "----------------------------------" << endl;

	cout << "Subproblems: [";

	//iterate through miles
	for (int i = 1; i <= distance; i++)
	{
		//place an advertisement 
		if (next < board.size())
		{
			//no board at ith-distance, the optimal solution at the i-1th location.
			if (board[next] != i)
			{
				opVal[i] = opVal[i - 1];
			}
			//no board at the ith-distance, place an advertisement.
			else 
			{
				if (minimumMilesPerBoard <= i)
				{
					// recurrence
					opVal[i] = max(opVal[i - minimumMilesPerBoard] + revenue[next], opVal[i - 1]);
				}
				else 
				{
					opVal[i] = revenue[next];
				}

				next++;
			}
		}
		else // Store the current optimal solution if all advertisement locations have been used.
		{
			opVal[i] = opVal[i - 1];
		}

		// Print out the advertisement location where an optimal solution exists.
		cout << opVal[i];

		if (i != 20)
			cout <<" | ";
	}
	// Add a closing brace to the 1-D auxillary table and add some space.
	cout << "]";
	cout << endl;

	// Return the max revenue which is contained where D = 20.
	return opVal[distance];
}

// maxptD computes the optimal value to this problem, showing only the subproblems where an advertisement is placed.
void maxptD(vector<int> board, vector<int> revenue, int distance, int minimumMilesPerBoard)
{
	int * opVal = new int[distance + 1];
	int next = 0, previousMile = 0, currentMile, count;
	bool location = false;
	minimumMilesPerBoard += 1;
	opVal[0] = 0;

	//auxillary table for problem 1 part D.
	cout << "---------------------------------- " << endl;
	cout << endl;
	cout << "Auxillary Table part D" << endl;
	cout << "---------------------------------- " << endl;
	cout << "X: not included" << endl;
	cout << "CM: current mile" << endl;
	cout << "NTR: new total revenue" << endl;
	cout << endl;
	cout << "Subproblems: [";
	//iterate through miles [0, D].
	for (int i = 1; i <= distance; i++)
	{
		if (next < board.size())
		{
			if (board[next] != i)
			{
				opVal[i] = opVal[i - 1];
			}
			else //iff a board exists at the ith-distance, place an advertisement.
			{
				if (minimumMilesPerBoard <= i)
				{
					//recurrence
					opVal[i] = max(opVal[i - minimumMilesPerBoard] + revenue[next], opVal[i - 1]);

					currentMile = opVal[i];

					if (currentMile != previousMile && count >= 6)
					{
						location = true;
						count = 0;
					}

					if (location == true)
					{
						cout << "CM: " << i << " | ";
						cout << "NTR: " << opVal[i];

					}
					previousMile = currentMile;
				}
				else
				{
					opVal[i] = revenue[next];
				}

				next++;
			}
		}
		else
		{
			opVal[i] = opVal[i - 1];
		}

		// If the current location is not used in the optimal solution indicate with X.
		if (location == false)
			cout << "X";

		if (i != 20)
			cout << " | ";

		// Reset the location to be false (indicating that the position is not optimal)
		location = false;
		// Update the accumulator (ensures that optimal solutions maintain the restriction requirement).
		count++;
	}
	// Add a closing brace to the 1-D auxillary table and add some space.
	cout << "]" << endl;
	cout << "---------------------------------- " << endl;
	cout << endl;
}

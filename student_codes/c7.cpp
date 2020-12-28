#include <cstdio>
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;



void FindNarcissisticnumber()
{
	int bit = 0;
	int top = 0;
	int hundred = 0;

	cout << "Result Is: ";
	for (int i = 153; i < 1000; i++)
	{
		int sum = 0;
		int n = i;
		bit = n % 10;
		n = n / 10;
		top = n % 10;
		hundred = n / 10;

		sum = pow(bit, 3) + pow(top, 3) + pow(hundred, 3);
		if (sum == i)
		{
			cout << i << ' ';
		}
	}

	cout << endl;
}



int main(){
	 FindNarcissisticnumber();
}
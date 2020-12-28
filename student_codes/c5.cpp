#include <cstdio>
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;


void FindGCD(unsigned int n1, unsigned int n2)
{


	unsigned int max = n1;
	unsigned int min = n2;
	if (n1 < n2)
	{
		max = n2;
		min = n1;
	}

	vector<int> num;
	for (int i = 1;i <= min; i++)
	{
		if ((n1 % i == 0) && (n2 % i == 0))
		{
			num.push_back(i);
		}
	}
	cout << "The GCD Is: " << num[num.size() - 1] << endl;

	for (int i = min; i > 0; i--)
	{
		if ((n1 % i == 0) && (n2 % i == 0))
		{
			cout << "The GCD Is: " << i << endl;
			break;
		}
	}

}




int main(){
	FindGCD(879, 123);
}
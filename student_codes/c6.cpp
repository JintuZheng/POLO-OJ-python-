#include <cstdio>
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;


void SumofFraction()
{
	double sum = 0.0;
	for (int i = 1; i <= 100; i++)
	{
		sum += pow(-1, i + 1) / i;
	}

	cout << "The Sum of '1/1-1/2+1/3-1/4+1/5 ���� + 1/99 - 1/100' Is: " << sum << endl;
}



int main(){
	 SumofFraction();
}
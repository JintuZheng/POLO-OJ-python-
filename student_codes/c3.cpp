#include <cstdio>
#include <iostream>
#include <cmath>
using namespace std;


void IsLeapYear(int year)
{
	cout << "Please input year:";
	if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0))
	{
		cout << "Is Leap Year!" << endl;
	}
	else
	{
		cout << "Is Not Leap Year!" << endl;
	}
}



int main(){
	IsLeapYear(2020);
}
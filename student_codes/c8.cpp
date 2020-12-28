#include <cstdio>
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;



//9.????
void PrintRhombic()
{
	//????????
	int line = 100;
	cout << "Please input a Odd: ";

	int spacenumber = line / 2;//???
	int starnumber = 1;//???
	for (int i = 0; i < line; i++)
	{
		//????
		if (i <= line / 2)
		{
			for (int j = 0; j < spacenumber; j++)
			{
				cout << ' ';
			}
			for (int j = 0; j < starnumber; j++)
			{
				cout << '*';
			}
			cout << endl;
			if (i == line / 2)
			{
				continue;
			}
			spacenumber--;
			starnumber += 2;
		}
		else//????
		{
			spacenumber++;
			starnumber -= 2;
			for (int j = 0; j < spacenumber; j++)
			{
				cout << ' ';
			}
			for (int j = 0; j < starnumber; j++)
			{
				cout << '*';
			}
			cout << endl;
		}
	}


	int colnmn = line;//?==?
	for (int i = 1; i <= line; i++)
	{
		//????
		if (i <= (line / 2 + 1))
		{
			for (int j = 1; j <= colnmn; j++)
			{
				if (((colnmn + 1) / 2) - (i - 1) <= j && j <= ((colnmn + 1) / 2) + (i - 1))
				{
					cout << '*';
				}
				else
				{
					cout << ' ';
				}
			}
			cout << endl;
		}
		else//????
		{
			for (int j = 1; j <= colnmn; j++)
			{
				if (((colnmn + 1) / 2) - (line - i) <= j && j <= ((colnmn + 1) / 2) + (line - i))
				{
					cout << '*';
				}
				else
				{
					cout << ' ';
				}
			}
			cout << endl;
		}
	}
}



int main(){
	 PrintRhombic();
}
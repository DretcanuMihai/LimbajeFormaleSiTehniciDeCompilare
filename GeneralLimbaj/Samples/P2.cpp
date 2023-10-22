#include <iostream>

using namespace std;

int main() {
	int a;
	int b;
	int r;
	bool flag;

	cout << "a:";
	cin >> a;

	cout << "b:";
	cin >> b;

	flag = b != 0;
	while (flag)
	{
		r = a % b;
		a = b;
		b = r;

		flag = b != 0;
	};
	cout << "cmmdc:";
	cout << a;
	return 0;
}
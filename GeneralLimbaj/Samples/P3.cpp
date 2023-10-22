#include <iostream>

using namespace std;

int main() {

	int nrElemente;
	int index;
	int valoare;
	int suma;
	bool flag;

	cout << "Numar elemente:";
	cin >> nrElemente;

	suma = 0;

	index = 0;
	flag = index < nrElemente;
	while (flag) {
		cout << "Elementul ";
		cout << index;
		cout << ":";
		cin >> valoare;

		suma = suma + valoare;

		index = index + 1;
		flag = index < nrElemente;
	};

	cout << "Suma:";
	cout << suma;
	return 0;
}
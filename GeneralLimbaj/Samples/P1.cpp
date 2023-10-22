#include <iostream>

using namespace std;

struct cerc {
	double raza;
};

int main() {
	struct cerc cerculMeu;
	double pi;
	double perimetru;
	double arie;

	pi = 3.14;

	cout << "Raza:";
	cin >> cerculMeu.raza;

	perimetru = 2 * pi;
	perimetru = perimetru * cerculMeu.raza;

	arie = pi * cerculMeu.raza;
	arie = arie * cerculMeu.raza;

	cout << "Perimetru:";
	cout << perimetru;
	cout << "\n";

	cout << "Arie:";
	cout << arie;
	cout << "\n";

	return 0;
}
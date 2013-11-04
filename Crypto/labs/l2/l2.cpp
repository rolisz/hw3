#include <iostream>
#include "InfInt.h"
#include <vector>
#include <algorithm>  
using namespace std;

vector<InfInt> trial_division_primes(InfInt n) {
    InfInt sqrt_n = n.intSqrt();
    vector<InfInt> divizori;
	InfInt i = 2;
	if (n % i == 0) {
		divizori.push_back(i);
	}
	i = 3;
    while (i <= sqrt_n) {
        if ((n % i) == 0) {
            divizori.push_back(i);
        }
        i+=2;
    }
    return divizori;
}

InfInt prime_factorizations(InfInt a, InfInt b) {
	vector<InfInt> div_a = trial_division_primes(a);
	vector<InfInt> div_b = trial_division_primes(b);
	vector<InfInt>::iterator it;
	int size;
	if (div_a.size() > div_b.size()) {
		size = div_a.size();
	}
	else {
		size = div_b.size();
	}
	vector<InfInt> div_c(size);
	it = set_intersection(div_a.begin(), div_a.end(), div_b.begin(), div_b.end(), div_c.begin());
	div_c.resize(it-div_c.begin()); 
	InfInt div = 1;
	for (it=div_c.begin(); it!=div_c.end(); ++it) {
		div *= *it;
	}
	return div;
}

InfInt euclid(InfInt a, InfInt b) {
    if (a == 0)
        return b;
    if (b == 0)
        return a;
	InfInt temp;
    while (a > 0) {
		temp = a;
        a = b%a;
		b = temp;
	}
    return b;
}

InfInt stein(InfInt num1, InfInt num2)
{
	InfInt pof2, tmp;
	if (num1 == 0) {
		return num2;
	}
	if (num2 == 0) {
		return num2;
	}

	/* cea mai mare putere a lui 2 care divide ambele nr*/
	pof2 = 0;
	while(!(num1 % 2 == 1) && !(num2 % 2 == 1)) {
		num1 /= 2;
		num2 /= 2;
		pof2++;
	}

	do {
		while (!(num1 % 2 == 1)) {
			num1 /= 2;
		}
		while (!(num2 % 2 == 1)) {
			num2 /= 2;
		}
		/* num1 si num2 sunt impare*/
		if (num1 >= num2) {
			num1 = (num1 - num2) / 2;
		}
		else {
			tmp = num1;
			num1 = (num2 - num1) / 2;
			num2 = tmp;
		}
	} while (!(num1 == num2 || num1 == 0));

	while (pof2 > 0) {
		num2 *=2;
		pof2--;
	}
	return num2;
}

int main() {
	//generate_prime_list(65536);
	while (!cin.eof()) {
		InfInt nr1,nr2;
		cin>>nr1;
		cin>>nr2;
		//cout<<"Prime factorization: "<<prime_factorizations(nr1, nr2)<<endl;
		cout<<"Euclid: "<<euclid(nr1, nr2)<<endl;
		cout<<"Stein: "<<stein(nr1, nr2)<<endl;
	}
}

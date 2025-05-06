#include <bitset>
#include <fstream>
#include <random>
#include <iostream>


void get_sequence()
{
	std::random_device rd;
	std::mt19937_64 gen(rd());

	std::bitset<64> first_part(gen());
	std::bitset<64> second_part(gen());

	std::ofstream fout("cpp_sequence.txt");

	if (!fout.is_open()) {
		std::cerr << "File is not be opened" << std::endl;
		return;
	}

	fout << first_part << second_part;
	fout.close();
}


int main()
{
	get_sequence();
	return 0;
}
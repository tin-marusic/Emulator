#ifndef Emulator_h
#define Emulator_h

// C++
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <sstream>
#include <algorithm>
#include <bitset>
#include <random>

// ROOT
//#include "TString.h"


using namespace std;


class Emulator
{

public:
	
	Emulator();
	~Emulator();
   
   pair<int, int> getParametersFromVhFile( const string& );
   vector<vector<int>> vhArchInputToArray( const string& , int, int );
   vector<string> generateInputEnergies( int , int , int , int );
   vector<string> generateInputShifts( int, int );


private:



};
#endif

#include <iostream>


#include "include/Emulator.h"

using namespace std;


int main() {
   
   string input_folder = "inputs/";
   string fileName_CE_E = input_folder + "CE_E_15_new.vh"; // matrica arhitekture za CE_E ulaze
   string fileName_CE_H = input_folder + "CE_H_15_new.vh"; // matrica arhitekture za CE_H ulaze
   
   int nBunch{5};
   bool filesCreatedFlag{"False"};
   
   Emulator *emulate = new Emulator();
   
   auto result_E = emulate->getParametersFromVhFile(fileName_CE_E);
   auto result_H = emulate->getParametersFromVhFile(fileName_CE_H);
   
   cout << "In E num: "  << result_E.first  << endl;
   cout << "Out E num: " << result_E.second << endl;
   cout << "In H num: "  << result_H.first  << endl;
   cout << "Out H num: " << result_H.second << endl;
   
   
   vector<vector<int>> matVariable_CE_E = emulate->vhArchInputToArray( fileName_CE_E, result_E.second, result_E.first );
   vector<vector<int>> matVariable_CE_H = emulate->vhArchInputToArray( fileName_CE_H, result_H.second, result_H.first );



// Test 2D vector
//==========================================
   for( const auto& row : matVariable_CE_E )
   {
      for( int element : row )
      {
         cout << element << " ";
      }
      cout << endl;
   }
   
   cout << endl;
   
   for( const auto& row : matVariable_CE_H )
   {
      for( int element : row )
      {
         cout << element << " ";
      }
      cout << endl;
   }
//==========================================

   
   auto inputArray_CE_E = emulate->generateInputEnergies(result_E.first, 8, 25, 3);
   auto inputArray_CE_H = emulate->generateInputEnergies(result_H.first, 8, 25, 3);


// Test inputArray vector
//==========================================
   for( const auto& str : inputArray_CE_H )
   {
      cout << str << endl;
   }
//==========================================


   auto shiftArray_CE_E = emulate->generateInputShifts(result_E.first, 2);
   
   
// Test shiftArray vector
//==============================
   for( const auto& s : shiftArray_CE_E )
   {
      cout << s << std::endl;
   }
//==============================
  
   
   
   return 0;
}
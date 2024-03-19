// Include classes
#include "Emulator.h"


//=================
Emulator::Emulator()
{

}
//=================



//===========
Emulator::~Emulator()
{
}
//===========



//============================================================================
pair<int, int> Emulator::getParametersFromVhFile( const string& inputFileName )
{
    ifstream f(inputFileName);
    string line;

    getline(f, line); // Read first line
    getline(f, line); // Read second line
    int in_num = 0;
    int out_num = 0;

    bool flag_current_digit = false;
    bool flag_current_alpha = false;
    bool flag_last_digit = false;
    bool flag_last_alpha = false;

    bool flag_start_condition = false;
    bool flag_stop_condition = false;

    bool firstTime = false;

    for (char element : line) {
        if (isdigit(element)) {
            flag_current_digit = true;
            flag_current_alpha = false;
            if (!firstTime) {
                firstTime = true;
            }
        } else {
            flag_current_digit = false;
            flag_current_alpha = true;
        }

        if (flag_current_digit && flag_last_alpha && firstTime) {
            flag_start_condition = true;
        }
        if (flag_current_alpha && flag_last_digit && firstTime) {
            firstTime = false;
            flag_stop_condition = true;
        }

        if (flag_start_condition && !flag_stop_condition) {
            in_num = in_num * 10 + (element - '0');
        }

        flag_last_alpha = flag_current_alpha;
        flag_last_digit = flag_current_digit;
    }


    getline(f, line); // Read third line

    flag_current_digit = false;
    flag_current_alpha = false;
    flag_last_digit = false;
    flag_last_alpha = false;

    flag_start_condition = false;
    flag_stop_condition = false;

    firstTime = false;

    for (char element : line) {
        if (isdigit(element)) {
            flag_current_digit = true;
            flag_current_alpha = false;
            if (!firstTime) {
                firstTime = true;
            }
        } else {
            flag_current_digit = false;
            flag_current_alpha = true;
        }

        if (flag_current_digit && flag_last_alpha && firstTime) {
            flag_start_condition = true;
        }
        if (flag_current_alpha && flag_last_digit && firstTime) {
            firstTime = false;
            flag_stop_condition = true;
        }

        if (flag_start_condition && !flag_stop_condition) {
            out_num = out_num * 10 + (element - '0');
        }

        flag_last_alpha = flag_current_alpha;
        flag_last_digit = flag_current_digit;
    }

    return {in_num, out_num};
}
//============================================================================



//=============================================================================================================
vector<vector<int>> Emulator::vhArchInputToArray( const string& inputFileName, int output_size, int input_size )
{
   vector<vector<int>> output(output_size, vector<int>(input_size, 0));
   ifstream f(inputFileName);
   string line;
   int counter{-1};
   int counter_preamble{5};
   

   // Check 2D vector
//   for( const auto& row : output )
//   {
//      for( int element : row )
//      {
//         cout << element << " ";
//      }
//      cout << endl;
//   }



   if( f.is_open() )
   {
      while( getline(f, line) )
      {         
         counter++;
         cout << line << endl;

         if( counter >= 5 )
         {
            if( line.find("*/") == string::npos ) continue;
              
            auto start_index = line.find("*/") + 7;
//            cout << "start_index = " << start_index << endl;
            auto tempString = line.substr(start_index);
//            cout << "tempString = " << tempString << endl;
            
            stringstream iss(tempString);
            string token;
            
            vector<string> tempString_variable;

            while( getline(iss, token, ',') )
            {
               token.erase(remove(token.begin(), token.end(), ' '), token.end());
               tempString_variable.push_back(token);  
            }
                                   
            tempString_variable.pop_back();
            
//            for( unsigned int i = 0 ; i < tempString_variable.size(); ++i )
//            {
//               cout << "i = " << i << ",   string = " << tempString_variable.at(i) << endl;
//               
//            }
            
//            std::erase_if(tempString_variable, [](auto&& str){return str.find(',', 0) != std::string::npos;});
               
           
            cout << "tempString_variable.size() = " << tempString_variable.size() << endl;

            // Test vector
            //=============================================
            for( const auto& string : tempString_variable )
            {
               cout << "string = " << string << endl;

            }
            //=============================================


            if( tempString_variable.size() > 1 )
            {
               int counter1 = 1;
               
               cout << "stoi(tempString_variable[0]) = " << stoi(tempString_variable[0]) << endl;
             
               for (int i = 0; i < stoi(tempString_variable[0]); i++)
               {
                  output[counter - counter_preamble][stoi(tempString_variable[counter1])] = stoi(tempString_variable[counter1 + 1]);
                  counter1 += 2;
               }
            }// end if
         
         }// end if
      }// end while
      f.close();
   }// end if
    
   return output;

}
//=============================================================================================================



//=============================================================================================================================
vector<string> Emulator::generateInputEnergies( int numberOfItems, int lengthOfItems, int outputLengthNextStep, int manLength )
{
   
   random_device rd;
   mt19937 gen(rd());
   uniform_int_distribution<> dis(0, 255);
   
   vector<string> output;
   string stringForCommand = "0" + to_string(lengthOfItems) + "b"; // "08b"

   for( int i = 0; i < numberOfItems; ++i )
   {
      bitset<8> bits(dis(gen));
      output.push_back(bits.to_string());
      
      string binarySubstring = output.back().substr(output.back().length() - lengthOfItems, lengthOfItems - manLength);
      
      cout << "binarySubstring = " << binarySubstring << endl;


      int validationExp = 0;
      for( int i = 0; i < binarySubstring.length(); ++i )
      {
        validationExp += (binarySubstring[i] - '0') * pow(2, binarySubstring.length() - 1 - i);
      }
      
      
      if( validationExp > outputLengthNextStep - manLength )
      {
         output.back() = "10110" + output.back().substr(output.back().size() - manLength);
      }
   }


    return output;
}
//=============================================================================================================================



//=============================================================================
vector<string> Emulator::generateInputShifts( int numberOfItems, int noOfBits )
{
   
   random_device rd;
   mt19937 gen(rd());
   uniform_int_distribution<> dis(0, (1 << noOfBits) - 1);
    
   vector<string> output;


   for( int i = 0; i < numberOfItems; ++i )
   {
      output.push_back(bitset<2>(dis(gen)).to_string());
   }

   return output;
}
//=============================================================================


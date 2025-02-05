
#include <bits/stdc++.h>
using namespace std;

int main()
{
  int testcases,c,k ;
  string row;
  int i = 0;
  int counter;
  bool could = false;
  char target = '0';
  cin >> testcases;
  while (i < testcases)
  {
    counter = 0;
    could = false;
    cin >> c >> k >> row;
    if(c == row.size())
    {
       for (int j = 0 ; j < row.size() ; j++) // 00000
    {
      if(row[j] == target)
      {
        counter++;

      }
      if(counter == k+1)
      {

        could = true;
        break;
      }

      if(row[j] != target)
      {
        counter = 0;
      }
    }
      if(could == true)
        cout << "yes\n";
      else{
        cout << "no\n";
      }
    }
    else{
      cout << "invalid length of seats";
      continue;
    }
   
  i++;
  }
  return 0;

}

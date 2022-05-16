#include <iostream>
#include <map>
#include <string>

#include "lsystem.cpp"

int main() {
  std::map<std::string, std::string> m = {
      {"a", "1"},
  };
  LSystem lsys(m);
  std::cout << lsys.instructions["a"];
  return 0;
}
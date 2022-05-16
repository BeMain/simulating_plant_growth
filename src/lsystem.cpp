#include <map>
#include <string>

class LSystem {
 public:
  std::map<std::string, std::string>& instructions;

  std::string axiom;
  std::map<std::string, std::string> rules;

  LSystem(const std::map<std::string, std::string>& _instructions) {
    instructions = _instructions;
  }
};
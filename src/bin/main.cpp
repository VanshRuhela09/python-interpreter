#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "../libs/lexer/lexer.hpp"
#include "../libs/parser/parser.hpp"
#include "../libs/ast/ast.hpp"
#include "../libs/interpreter/interpreter.hpp"
#include "../libs/json/json.hpp"

#pragma GCC optimize("Ofast")
#pragma GCC target("avx,avx2,fma")

#ifdef DEBUG
inline void show_tokens(const std::vector<Token>& tokens) {
    for (const auto& token : tokens) {
        std::cout << token << '\n';
    }
    std::cout << std::flush;
}
#endif

int main(int argc, char* argv[]) {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr); std::cout.tie(nullptr);

    if (argc < 2) {
        std::cout << "Usage: ./main [filename].my [--dump-ast]" << std::endl;
        return 1;
    }

    std::string filename = argv[1];
    bool dump_ast = (argc > 2 && std::string(argv[2]) == "--dump-ast");

    std::ifstream inputFile(filename);

    if (!inputFile) {
        std::cerr << "Error: could not open file '" << filename << "'\n";
        return 1;
    }

    std::string source((std::istreambuf_iterator<char>(inputFile)), {});

    try {
        Lexer lexer(source);
        std::vector<Token> tokens = lexer.scanTokens();

        #ifdef DEBUG
            /* To define DEBUG, use `make DEBUG=1` when compiling */
            show_tokens(tokens);
        #endif

        Parser parser(tokens);
        auto root = parser.parse();

        if (dump_ast) {
            // Output AST as JSON
            nlohmann::json ast_json = root->to_json();
            std::cout << ast_json.dump(2) << std::endl;
            return 0;
        }

        Interpreter interpreter;
        interpreter.interpret(root);
        
    } catch (const std::runtime_error& err) {
        std::cerr << err.what() << '\n';
        return EXIT_FAILURE;
    }

    return 0;
}


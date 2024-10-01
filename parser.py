import re

# Token types
TOKEN_IF = 'IF'
TOKEN_ELSE = 'ELSE'
TOKEN_ELSE_IF = 'ELSE_IF'
TOKEN_SWITCH = 'SWITCH'
TOKEN_FOR = 'FOR'
TOKEN_WHILE = 'WHILE'
TOKEN_DO = 'DO'
TOKEN_METHOD = 'METHOD'
TOKEN_LBRACE = 'LBRACE'
TOKEN_RBRACE = 'RBRACE'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'
TOKEN_STATEMENT = 'STATEMENT'

# Simple token structure
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

# Lexical analysis
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_position = 0

    def tokenize(self):
        token_specification = [
            (TOKEN_IF, r'\bif\b'),
            (TOKEN_ELSE_IF, r'\belse\s+if\b'),
            (TOKEN_ELSE, r'\belse\b'),
            (TOKEN_SWITCH, r'\bswitch\b'),
            (TOKEN_FOR, r'\bfor\b'),
            (TOKEN_WHILE, r'\bwhile\b'),
            (TOKEN_DO, r'\bdo\b'),
            (TOKEN_METHOD, r'\b(public|private|protected)?\s*(static\s+)?\s*([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*\{'),
            (TOKEN_LBRACE, r'\{'),
            (TOKEN_RBRACE, r'\}'),
            (TOKEN_LPAREN, r'\('),
            (TOKEN_RPAREN, r'\)'),
            (TOKEN_STATEMENT, r'[^{}();]+'),
        ]

        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        for match in re.finditer(token_regex, self.code):
            token_type = match.lastgroup
            token_value = match.group()
            self.tokens.append(Token(token_type, token_value))
        return self.tokens

# Test code
if __name__ == "__main__":
    java_code = """
    public class Example {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }

        private int add(int a, int b) {
            return a + b;
        }

        protected void displayMessage() {
            System.out.println("This is a message.");
        }

        int subtract(int a, int b) {
            return a - b;
        }

        do {
            // do something
        } while (x < 5);
    }
    """

    lexer = Lexer(java_code)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)

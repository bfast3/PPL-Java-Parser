import re

# Token Types
TOKEN_IF = 'IF'
TOKEN_ELSE_IF = 'ELSE_IF'
TOKEN_ELSE = 'ELSE'
TOKEN_SWITCH = 'SWITCH'
TOKEN_FOR = 'FOR'
TOKEN_WHILE = 'WHILE'
TOKEN_DO = 'DO'
TOKEN_METHOD = 'METHOD'
TOKEN_STATEMENT = 'STATEMENT'
TOKEN_LBRACE = 'LBRACE'  # Left/Opening Curly Brace {
TOKEN_RBRACE = 'RBRACE'  # Right/Closing Curly Brace }

# Token Class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Lexer Class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        # Split the code into lines for easier processing
        lines = self.code.split('\n')

        # Patterns to match
        method_pattern = re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+\w+\s*\(.*\)\s*')
        if_pattern = re.compile(r'\bif\b')
        else_if_pattern = re.compile(r'\belse\s+if\b')
        else_pattern = re.compile(r'\belse\b')
        switch_pattern = re.compile(r'\bswitch\b')
        for_pattern = re.compile(r'\bfor\b')
        while_pattern = re.compile(r'\bwhile\b')
        do_pattern = re.compile(r'\bdo\b')

        for line in lines:
            stripped_line = line.strip()

            # Split lines containing both a statement and curly braces
            self.split_line_and_tokenize(stripped_line)

        return self.tokens

    def split_line_and_tokenize(self, line):
        # Use regex to split statements from curly braces
        # The following regex will match anything before or after `{` or `}`:
        parts = re.split(r'(\{|\})', line)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Check for curly braces and tokenize separately
            if part == '{':
                self.tokens.append(Token(TOKEN_LBRACE, '{'))
            elif part == '}':
                self.tokens.append(Token(TOKEN_RBRACE, '}'))
            else:
                # Check for method declarations
                method_pattern = re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+\w+\s*\(.*\)\s*')
                if method_pattern.match(part):
                    self.tokens.append(Token(TOKEN_METHOD, part))

                # Check for conditional statements
                elif re.search(r'\bif\b', part):
                    self.tokens.append(Token(TOKEN_IF, part))
                elif re.search(r'\belse\s+if\b', part):
                    self.tokens.append(Token(TOKEN_ELSE_IF, part))
                elif re.search(r'\belse\b', part):
                    self.tokens.append(Token(TOKEN_ELSE, part))
                elif re.search(r'\bswitch\b', part):
                    self.tokens.append(Token(TOKEN_SWITCH, part))

                # Check for loop constructs
                elif re.search(r'\bfor\b', part):
                    self.tokens.append(Token(TOKEN_FOR, part))
                elif re.search(r'\bwhile\b', part):
                    self.tokens.append(Token(TOKEN_WHILE, part))
                elif re.search(r'\bdo\b', part):
                    self.tokens.append(Token(TOKEN_DO, part))

                # Otherwise, it's a regular statement
                else:
                    self.tokens.append(Token(TOKEN_STATEMENT, part))

# Example Usage
if __name__ == "__main__":
    java_code = """
    public class Example {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        

        private int add(int a, int b) 
            return a + b;
        

        protected void displayMessage() {
            System.out.println("This is a message.");
        }

        int subtract(int a, int b) {
            return a - b;
        }

        if (x > 0) {
            System.out.println("Positive");
        } else if (x < 0) {
            System.out.println("Negative");
        } else {
            System.out.println("Zero");
        }

        switch (x) {
            case 1:
                System.out.println("One");
                break;
            case 2:
                System.out.println("Two");
                break;
        }

        for (int i = 0; i < 10; i++) {
            System.out.println(i);
            }
        

        while (x < 100) {
            x++;
        }
    }
    """

    code = ''
    fileToRead = input('Please enter a java file to parse: ')
    try:
        with open(fileToRead, 'r') as f:
            for line in f.readlines():
                 code += f'{line}\n'  # Append each line to code with a newline
    except IOError: 
        print("Error: failed to read file")
    
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    with open('input_tokens.txt', 'w') as f:
        for token in tokens:
            f.write(f"{token}\n")
    print('input_tokens.txt successfully created!')

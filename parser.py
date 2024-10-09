import re

# Token Class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Function to parse tokens from the input file
def parse_tokens(input_file):
    tokens = []
    with open(input_file, 'r') as file:
        for line in file:
            # Match the pattern "Token(TYPE, value)"
            match = re.match(r'Token\((\w+), (.*)\)', line.strip())
            if match:
                token_type = match.group(1)
                value = match.group(2)
                tokens.append(Token(token_type, value))
    return tokens

# Pass 1: Identify missing opening curly braces and insert them
def pass_1_insert_opening_braces(tokens):
    output_tokens = []
    
    for i, token in enumerate(tokens):
        # Add current token to the output
        output_tokens.append(token)
        
        # If the token is a construct that should have an opening curly brace
        if token.type in {'METHOD', 'IF', 'ELSE_IF', 'ELSE', 'SWITCH', 'FOR', 'WHILE', 'DO'}:
            # Look ahead to see if the next token is an opening curly brace
            if i + 1 < len(tokens) and tokens[i + 1].type != 'LBRACE':
                # If not, insert an LBRACE token
                output_tokens.append(Token('LBRACE', '{'))
    
    return output_tokens

# Pass 2: Identify missing closing curly braces and insert them before new constructs
# Pass 2: Identify missing closing curly braces and insert them before new constructs
def pass_2_insert_closing_braces(tokens):
    output_tokens = []
    stack = []  # Track constructs that expect closing braces
    skip_class_brace = False  # Flag to skip class LBRACE

    for i, token in enumerate(tokens):
        # Add current token to the output
        output_tokens.append(token)

        # Detect if this token is a class declaration and set the flag to skip its LBRACE
        if token.type == 'STATEMENT' and 'class' in token.value:
            skip_class_brace = True

        # Push opening curly brace onto the stack (unless it's the class LBRACE)
        if token.type == 'LBRACE':
            if not skip_class_brace:
                stack.append(i)
            else:
                skip_class_brace = False  # Reset the flag after skipping the class brace

        # If we encounter a closing curly brace, pop the stack
        elif token.type == 'RBRACE':
            if stack:
                stack.pop()

        # If we encounter a new construct, check if there are unclosed braces in the stack
        elif token.type in {'METHOD', 'IF', 'ELSE_IF', 'ELSE', 'SWITCH', 'FOR', 'WHILE', 'DO'}:
            if stack:
                # Insert a closing brace before the new construct
                output_tokens.insert(len(output_tokens) - 1, Token('RBRACE', '}'))
                stack.pop()  # Pop the stack as we've "closed" the construct

    # At the end of the file, if there are still unclosed braces in the stack, close them
    while stack:
        output_tokens.append(Token('RBRACE', '}'))
        stack.pop()

    return output_tokens


# Main function to process the input file in two passes and generate the output
def process_tokens(input_file, output_file):
    # Parse tokens from the input file
    tokens = parse_tokens(input_file)
    
    # Pass 1: Insert missing opening curly braces
    tokens = pass_1_insert_opening_braces(tokens)
    
    # Pass 2: Insert missing closing curly braces
    tokens = pass_2_insert_closing_braces(tokens)
    
    # Write the updated tokens to the output file
    with open(output_file, 'w') as file:
        for token in tokens:
            file.write(f"{token}\n")

# Example usage
if __name__ == "__main__":
    input_file = 'input_tokens.txt'  # Your input file with tokens
    output_file = 'output_tokens.txt'  # The output file with missing braces identified
    process_tokens(input_file, output_file)
    print('output_tokens.txt successfully created!')
import re

# Token Class
class Token:
    def __init__(self, type, value):
        self.type = type  # Token type (e.g., METHOD, LBRACE)
        self.value = value  # Token value (e.g., 'public static void main(String[] args)')

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
                # Remove enclosing quotes from value if present
                value = value.strip('\'"')
                tokens.append(Token(token_type, value))
    return tokens

def correct_method_declaration(method_declaration):
    # Default visibility modifier and return type
    default_visibility = "public"
    default_return_type = "void"
    reserved_keywords = {'if', 'else', 'switch', 'for', 'while', 'do'}

    # Regex pattern to parse method declarations
    method_pattern = re.compile(r'''
        ^\s*
        (?P<visibility>public|private|protected)?\s*
        (?P<static>static\s+)?               # Optional 'static'
        (?P<return_type>(?!if|else|switch|for|while|do)[\w<>\[\]]+)\s+  # Exclude keywords
        (?P<method_name>\w+)\s*              # Method name
        \((?P<parameters>.*)\)               # Parameters in parentheses
        ''', re.VERBOSE)

    match = method_pattern.match(method_declaration)
    if not match:
        # If the method declaration doesn't match the pattern, return as is
        return method_declaration

    method_name = match.group('method_name')

    # Check if the method name is a reserved keyword
    if method_name in reserved_keywords:
        return method_declaration  # This is not a valid method, skip correction

    # Continue with the existing correction logic
    visibility = match.group('visibility')
    static_part = match.group('static') or ''
    return_type = match.group('return_type')
    parameters = match.group('parameters')

    if not visibility:
        visibility = default_visibility
    if not return_type:
        return_type = default_return_type

    corrected_method = f"{visibility} {static_part}{return_type} {method_name}({parameters})"
    return corrected_method

# Main function to process tokens and correct method declarations
def process_tokens(input_file, output_file):
    tokens = parse_tokens(input_file)
    corrected_tokens = []

    for token in tokens:
        if token.type == 'METHOD':
            corrected_value = correct_method_declaration(token.value)
            corrected_tokens.append(Token(token.type, corrected_value))
        else:
            corrected_tokens.append(token)

    # Write the corrected tokens to the output file
    with open(output_file, 'w') as file:
        for token in corrected_tokens:
            file.write(f"Token({token.type}, {token.value})\n")

# A method to count and return the number of methods
def count_methods(input_file):
    tokens = parse_tokens(input_file)
    count = 0
    for token in tokens:
        if token.type == 'METHOD' and not token.value.startswith("else if"): #the else if was being counted as a method and this change fixed it
            count += 1
    return count

# Method to take all the information and generate the output file need 
def generate_output_file(updated_file, output_file, original_file, count):

    original_tokens = parse_tokens(original_file)
    updated_tokens = parse_tokens(updated_file)
    
    with open(output_file, 'w') as of:
        of.write("Original file (updated)\n") #removed the updated in final build

        # can add some sort of formatting logic here 
        for token in original_tokens:
            of.write(f'{token.value}\n')

        of.write('\n')
        of.write("Corrected file: \n")
        for token in updated_tokens:
            of.write(f'{token.value}\n')
        of.write('\n')
        of.write(f'Method count: {count}')

# Example usage
if __name__ == "__main__":
    input_file = 'output_tokens.txt'   # Input file with tokens
    output_file = 'method_tokens.txt' # Output file with corrected tokens
    process_tokens(input_file, output_file)

    original_file = 'input_tokens.txt'
    output_file = 'output.txt'
    updated_file = 'method_tokens.txt'
    count = count_methods(updated_file)
    generate_output_file(updated_file, output_file, original_file, count)
    print("output.txt successfully created!")
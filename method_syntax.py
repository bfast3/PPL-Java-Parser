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

# Function to correct method declaration errors
def correct_method_declaration(method_declaration):
    # Default visibility modifier and return type
    default_visibility = "public"
    default_return_type = "void"

    # Regex pattern to parse method declarations
    method_pattern = re.compile(r'''
        ^\s*
        (?P<visibility>public|private|protected)?\s*
        (?P<static>static\s+)?               # Optional 'static'
        (?P<return_type>[\w<>\[\]]+)?\s+     # Return type (optional if missing)
        (?P<method_name>\w+)\s*              # Method name
        (\((?P<parameters>.*)\))?            # Parameters in parentheses (optional)
        ''', re.VERBOSE)

    match = method_pattern.match(method_declaration)
    if not match:
        # If the method declaration doesn't match the pattern, return an error
        return method_declaration  # Return as is if it cannot be parsed

    visibility = match.group('visibility')
    static_part = match.group('static') or ''
    return_type = match.group('return_type')
    method_name = match.group('method_name')
    parameters = match.group('parameters')

    # Correct missing visibility modifier
    if not visibility:
        visibility = default_visibility

    # Correct missing return type
    if not return_type:
        return_type = default_return_type

    # Correct invalid visibility modifiers
    valid_visibilities = {'public', 'private', 'protected'}
    if visibility not in valid_visibilities:
        visibility = default_visibility

    # Correct invalid method names
    if not re.match(r'^[a-zA-Z_]\w*$', method_name):
        method_name = 'correctedMethodName'  # Provide a default valid method name

    # Correct missing parentheses
    if parameters is None:
        parameters = ''

    # Reconstruct the corrected method declaration
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

# Example usage
if __name__ == "__main__":
    input_file = 'output_tokens.txt'   # Input file with tokens
    output_file = 'method_tokens.txt' # Output file with corrected tokens
    process_tokens(input_file, output_file)

import re

# Token Class to represent methods
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Function to parse a Java method string and verify its syntax
def verify_method_syntax(method_string):
    # Pattern for a valid method signature
    method_signature_pattern = re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+\w+\s*\(.*\)\s*\{')
    
    # Check if the method signature matches the expected pattern
    if not method_signature_pattern.match(method_string):
        return False, "Invalid method declaration"

    # Ensure the method body starts with an opening curly brace and ends with a closing curly brace
    if method_string.count('{') != method_string.count('}'):
        return False, "Mismatched opening and closing braces"

    # Check for correct parameter list
    parameters_match = re.search(r'\(.*\)', method_string)
    if not parameters_match:
        return False, "Invalid parameter list"

    # Validate the return type and method body
    return_type_match = re.search(r'^\s*(public|private|protected)?\s*(static\s+)?([\w<>\[\]]+)\s+\w+\s*\(', method_string)
    if return_type_match:
        return_type = return_type_match.group(3)
        # Check return statements based on the method's return type
        if return_type != "void":
            if re.search(r'\breturn\b', method_string):
                return True, "Method is syntactically correct"
            else:
                return False, f"Missing return statement for method with return type '{return_type}'"
    
    return True, "Method is syntactically correct"

# Function to test method verification
def test_method_syntax_verification():
    test_cases = [
        # Valid method
        """public int add(int a, int b) {
            return a + b;
        }""",
        
        # Method without return
        """public int subtract(int a, int b) {
            // Missing return statement
        }""",
        
        # Invalid method declaration
        """public invalidMethod(int a, int b {
            return a + b;
        }""",
        
        # Missing curly braces
        """public void displayMessage() 
            System.out.println("Hello");
        """,
        
        # Valid void method
        """public void displayMessage() {
            System.out.println("Hello");
        }"""
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"Test case {i + 1}:")
        result, message = verify_method_syntax(test_case)
        print("Result:", "Valid" if result else "Invalid")
        print("Message:", message)
        print()

# Example usage
if __name__ == "__main__":
    test_method_syntax_verification()

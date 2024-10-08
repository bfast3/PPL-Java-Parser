import re

def process_java_code(java_code):
    # Save the original code
    original_code = java_code.strip()

    # Corrected code will be built as a list of lines
    corrected_lines = []

    # Split the code into lines for easier processing
    lines = java_code.strip().split('\n')

    # Patterns to match methods, decision structures, and loops
    method_pattern = re.compile(r'^\s*(public|private|protected)?\s*(static\s+)?\s*\w+[\s<>\[\]]*\s+\w+\s*\(.*\)\s*{?')
    decision_pattern = re.compile(r'^\s*(if|else if|else|switch)\b.*')
    loop_pattern = re.compile(r'^\s*(for|while|do)\b.*')

    method_count = 0  # To count the number of methods

    i = 0
    brace_stack = []  # To keep track of braces

    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # Check for method declarations
        if method_pattern.match(stripped_line):
            method_count += 1  # Increment method count

            # Ensure method has opening curly brace
            if '{' not in stripped_line:
                # Add opening brace if missing
                corrected_lines.append(line + ' {')
            else:
                corrected_lines.append(line)
            i += 1
            # Ensure method has closing brace
            method_body = []
            open_braces = 1 if '{' not in stripped_line else 0
            while i < len(lines) and open_braces >= 0:
                method_line = lines[i]
                method_body.append(method_line)
                if '{' in method_line:
                    open_braces += method_line.count('{')
                if '}' in method_line:
                    open_braces -= method_line.count('}')
                i += 1
                if open_braces == 0:
                    break
            else:
                # If method doesn't close properly, add closing brace
                method_body.append('}')
            corrected_lines.extend(method_body)
            continue

        # Check for decision structures
        elif decision_pattern.match(stripped_line):
            # Ensure decision structures use curly braces
            corrected_lines.append(line)
            if '{' not in stripped_line:
                # Add opening brace
                corrected_lines.append('{')
                i += 1
                # Copy following lines until we find the end of the block
                while i < len(lines):
                    next_line = lines[i]
                    next_stripped = next_line.strip()
                    corrected_lines.append(next_line)
                    i += 1
                    if ';' in next_line or next_stripped.startswith(('if', 'else', 'switch', 'for', 'while', 'do')):
                        break
                corrected_lines.append('}')
            else:
                i += 1
            continue

        # Check for loops
        elif loop_pattern.match(stripped_line):
            corrected_lines.append(line)
            if '{' not in stripped_line:
                # Add opening brace
                corrected_lines.append('{')
                i += 1
                # Copy following lines until we find the end of the block
                while i < len(lines):
                    next_line = lines[i]
                    corrected_lines.append(next_line)
                    i += 1
                    if ';' in next_line or next_line.strip().startswith(('if', 'else', 'switch', 'for', 'while', 'do')):
                        break
                corrected_lines.append('}')
            else:
                i += 1
            continue

        else:
            corrected_lines.append(line)
            i += 1

    corrected_code = '\n'.join(corrected_lines)

    return original_code, corrected_code, method_count

# Example input Java program
java_code = """
public class Example {
    public static void main(String[] args)
        System.out.println("Hello, World!");

    private int add(int a, int b)
        return a + b;

    protected void displayMessage()
        System.out.println("This is a message.");

    int subtract(int a, int b) {
        return a - b;
    }

    do
        System.out.println("Do something");
    while (x < 5);

    if (x > 0)
        System.out.println("Positive");
    else if (x < 0)
        System.out.println("Negative");
    else
        System.out.println("Zero");

    switch (x)
        case 1:
            System.out.println("One");
            break;
        case 2:
            System.out.println("Two");
            break;

    for (int i = 0; i < 10; i++)
        System.out.println(i);

    while (x < 100)
        x++;
}
"""

# Process the Java code
original_code, corrected_code, method_count = process_java_code(java_code)

# Prepare the output content
output_text = f"""Original Java Code:

{original_code}

Corrected Java Code:
{corrected_code}

Number of methods: {method_count}
"""

# Write the output to a text file
with open('output.txt', 'w') as f:
    f.write(output_text)

# Print the output for verification
print(output_text)

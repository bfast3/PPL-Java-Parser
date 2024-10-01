import re

# Token types
TOKEN_IF = 'IF'
TOKEN_ELSE = 'ELSE'
TOKEN_ELSE_IF = 'ELSE_IF'
TOKEN_SWITCH = 'SWITCH'
TOKEN_FOR = 'FOR'
TOKEN_WHILE = 'WHILE'
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

# Syntax Tree Nodes
class Node:
    def __init__(self, node_type, children=None):
        self.node_type = node_type
        self.children = children or []

    def __repr__(self):
        return f'Node({self.node_type}, {self.children})'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        tree = []
        while self.current_token_index < len(self.tokens):
            tree.append(self.parse_statement())
        return tree

    def parse_statement(self):
        token = self.tokens[self.current_token_index]
        
        if token.type == TOKEN_IF:
            return self.parse_if()
        elif token.type == TOKEN_SWITCH:
            return self.parse_switch()
        elif token.type == TOKEN_FOR:
            return self.parse_for()
        elif token.type == TOKEN_WHILE:
            return self.parse_while()
        else:
            self.current_token_index += 1
            return Node('STATEMENT', token.value)

    def parse_if(self):
        if_node = Node('IF')
        self.current_token_index += 1  # skip 'if'
        if_node.children.append(self.consume_parens())  # condition
        if_node.children.append(self.parse_block())  # if block

        if self.peek().type == TOKEN_ELSE_IF:
            if_node.children.append(self.parse_else_if())
        elif self.peek().type == TOKEN_ELSE:
            if_node.children.append(self.parse_else())

        return if_node

    def parse_else_if(self):
        else_if_node = Node('ELSE_IF')
        self.current_token_index += 1  # skip 'else if'
        else_if_node.children.append(self.consume_parens())  # condition
        else_if_node.children.append(self.parse_block())  # else-if block
        if self.peek().type == TOKEN_ELSE:
            else_if_node.children.append(self.parse_else())
        return else_if_node

    def parse_else(self):
        else_node = Node('ELSE')
        self.current_token_index += 1  # skip 'else'
        else_node.children.append(self.parse_block())  # else block
        return else_node

    def parse_switch(self):
        switch_node = Node('SWITCH')
        self.current_token_index += 1  # skip 'switch'
        switch_node.children.append(self.consume_parens())  # switch condition
        switch_node.children.append(self.parse_block())  # switch block
        return switch_node

    def parse_for(self):
        for_node = Node('FOR')
        self.current_token_index += 1  # skip 'for'
        for_node.children.append(self.consume_parens())  # for condition
        for_node.children.append(self.parse_block())  # for block
        return for_node

    def parse_while(self):
        while_node = Node('WHILE')
        self.current_token_index += 1  # skip 'while'
        while_node.children.append(self.consume_parens())  # while condition
        while_node.children.append(self.parse_block())  # while block
        return while_node

    def parse_block(self):
        if self.peek().type == TOKEN_LBRACE:
            self.current_token_index += 1  # skip '{'
            block_node = Node('BLOCK')
            while self.peek().type != TOKEN_RBRACE:
                block_node.children.append(self.parse_statement())
            self.current_token_index += 1  # skip '}'
            return block_node
        else:
            return self.parse_statement()

    def consume_parens(self):
        # Consume a condition inside parentheses
        if self.peek().type == TOKEN_LPAREN:
            self.current_token_index += 1  # skip '('
            condition_node = Node('CONDITION', [])
            while self.peek().type != TOKEN_RPAREN:
                condition_node.children.append(self.tokens[self.current_token_index])
                self.current_token_index += 1
            self.current_token_index += 1  # skip ')'
            return condition_node
        return None

    def peek(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

# Test code
if __name__ == "__main__":
    java_code = """
    if (x > 0) {
        // do something
    } else if (x < 0) {
        // do something else
    } else {
        // final case
    }

    switch (x) {
        case 1:
            // case 1
            break;
        case 2:
            // case 2
            break;
    }

    for (int i = 0; i < 10; i++) {
        // loop body
    }

    while (x < 100) {
        // while loop
    }
    """

    lexer = Lexer(java_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    syntax_tree = parser.parse()

    for node in syntax_tree:
        print(node)

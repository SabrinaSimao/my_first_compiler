from PrePro import *
from Parser import *
reserved = ['PRINT', 'END', 'WHILE', 'WEND', 'IF', 'OR', 'AND', 'NOT', 'INPUT', 'ELSE', 'THEN', 'SUB', 'MAIN', 'INTEGER', 'BOOLEAN', 'DIM', 'AS', 'TRUE', 'FALSE']

class Token():

    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer():

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        eof = False
        type = None
        value = ""
        string = ""

        if self.position == len(self.origin):
            type = 'EOF'
            value = 0
            eof = True

        if not eof:
            while self.origin[self.position] == ' ':
                self.position += 1
                if self.position == len(self.origin):
                    type = 'EOF'
                    value = 0
                    eof = True
                    self.actual = Token(type, str(value))
                    return self.actual

            if self.origin[self.position].isnumeric():
                while self.position < len(self.origin) and self.origin[self.position].isnumeric():
                    type = 'INT'
                    value += self.origin[self.position]
                    self.position += 1

            elif self.origin[self.position].isalpha():
                while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == "_"):
                    type = 'identifier'
                    string += self.origin[self.position]
                    self.position += 1
                    
                value = string.upper()

                if value in reserved:
                    type = value
                    value = 'reserved'

            elif self.origin[self.position] == '+':
                type = 'PLUS'
                value = '+'
                self.position += 1

            elif self.origin[self.position] == '-':
                type = 'MINUS'
                value = '-'
                self.position += 1

            elif self.origin[self.position] == '*':
                type = 'MULT'
                value = '*'
                self.position += 1

            elif self.origin[self.position] == '/':
                type = 'DIV'
                value = '/'
                self.position += 1
            elif self.origin[self.position] == ')':
                type = ')'
                value = ')'
                self.position +=1
            elif self.origin[self.position] == '(':
                type = '('
                value = '('
                self.position +=1
            elif self.origin[self.position] == '=':
                type = '='
                value = '='
                self.position +=1
            elif self.origin[self.position] == '>':
                type = '>'
                value = '>'
                self.position +=1
            elif self.origin[self.position] == '<':
                type = '<'
                value = '<'
                self.position +=1

            elif ord(self.origin[self.position]) == 10:
                type = 'EOL'
                value = '\n'
                self.position +=1
            else:
                raise SyntaxError("Invalid Sentence")
        
        self.actual = Token(type, str(value))
        return self.actual

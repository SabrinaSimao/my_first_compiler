reserved = ['PRINT', 'BEGIN', 'END']

class PrePro():

    def filter(code):
        i = 0
        to_delete = []
        text = list(code)
        while i < len(text):
            if text[i] == "'":
                j = i
                while text[j] != "\n":
                    j += 1
                    if j == len(text):
                        break
                    
                to_delete.append([i,j])
            i += 1                    
        
        for k in reversed(range(len(to_delete))):
            i = to_delete[k][0]
            j = to_delete[k][1]
            del text[i:j+1]

        string = ''.join(text)
        return string

class SymbolTable():
    def __init__(self):
        self.dic = {}

    def getter(self, index):
        if index in self.dic:
            return self.dic[index]
        else:
            raise ValueError("Variable does not exist", index)

    def setter(self, index, value):
        self.dic[index] = value

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        pass

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        ST.setter(self.children[0].value, self.children[1].Evaluate(ST))


class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        if self.value == '+':
            return self.children[0].Evaluate(ST)
        elif self.value == '-':
            return -self.children[0].Evaluate(ST)
        else:
            print("master blaster error")

class Statements():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, ST):
        for i in self.children:
           i.Evaluate(ST)

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        print(self.children[0].Evaluate(ST))

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        if self.value == '+':
            return (self.children[0].Evaluate(ST) + self.children[1].Evaluate(ST))
        elif self.value == '-':
            return (self.children[0].Evaluate(ST) - self.children[1].Evaluate(ST))
        elif self.value == '*':
            return (self.children[0].Evaluate(ST) * self.children[1].Evaluate(ST))
        elif self.value == '/':
            return (self.children[0].Evaluate(ST) // self.children[1].Evaluate(ST))
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        return int(self.value)

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        return ST.getter(self.value)

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        pass

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
                while self.position < len(self.origin) and self.origin[self.position].isalpha():
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
            elif ord(self.origin[self.position]) == 10:
                type = 'EOL'
                value = '\n'
                self.position +=1
            else:
                raise SyntaxError("Invalid Sentence")
        
        self.actual = Token(type, str(value))
        return self.actual


class Parser():

    def statements():
        statement_children = []

        if Parser.tokens.actual.type == 'BEGIN':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'EOL':
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type != 'END':
                    statement_children.append(Parser.statement())
                    if Parser.tokens.actual.type == 'EOL':
                        Parser.tokens.selectNext()
                    else:
                        raise SyntaxError("Missing End of Line - after code")
                if Parser.tokens.actual.type == 'END':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'EOL':
                        Parser.tokens.selectNext()
                        return Statements('statements', statement_children)
                    else:
                        raise SyntaxError("Missing End of Line - after end")
                else:
                    raise SyntaxError("Missing End")
            else:
                raise SyntaxError("Missing End of Line - after begin")
        else:
            raise SyntaxError("Missing Begin")
    
    def statement():
        if Parser.tokens.actual.type == 'identifier':
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == '=':
                Parser.tokens.selectNext()
                return Assignment('=', [identifier, Parser.parseExpression()])
        elif Parser.tokens.actual.type == 'PRINT':
                Parser.tokens.selectNext()
                return Print('print', [Parser.parseExpression()])
        elif Parser.tokens.actual.type == 'BEGIN':
                return Parser.statements()
        else:
                return NoOp(None, None)


    def parseExpression():
        
       
        left = Parser.termo()

        while Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS':
             # if actual token is +
            if Parser.tokens.actual.type == 'PLUS':

                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = BinOp('+', [left, right])

             # if actual token is -
            elif Parser.tokens.actual.type == 'MINUS':
                
                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = BinOp('-', [left, right])

            else:
                print("ultimate super master error")
            # end of while

        return left

    def termo():

        left = Parser.fator()

        while Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV':
            # if actual token is +
            if Parser.tokens.actual.type == 'MULT':

                Parser.tokens.selectNext()
                
                right = Parser.fator()

                left = BinOp('*', [left, right])

            # if actual token is -
            elif Parser.tokens.actual.type == 'DIV':
                
                Parser.tokens.selectNext()
                
                right = Parser.fator()
                
                left = BinOp('/', [left, right])

            else:
                print("ultimate super master error")
            # end of while

        return left

    def fator():

        new_token = Parser.tokens.actual

        # check if token is unary operator
        if(new_token.type == "PLUS" or new_token.type == "MINUS"):
            if(new_token.type == "PLUS"):
                
                Parser.tokens.selectNext()
                return UnOp('+',[Parser.fator()])
                
            elif(new_token.type == "MINUS"):
                Parser.tokens.selectNext()
                return UnOp('-',[Parser.fator()])
            else:
                raise TypeError("Invalid Token Error: ", new_token.type)

        # check if token is a number
        elif new_token.type == "INT":
            left = IntVal(new_token.value, [])
            Parser.tokens.selectNext()
            return left

        # check if token is a variable
        elif new_token.type == 'identifier':
            left = Identifier(new_token.value, [])
            Parser.tokens.selectNext()
            return left
            
        # check if token is parentesis
        elif new_token.type == "(":
            Parser.tokens.selectNext()
            left = Parser.parseExpression()
            new_token = Parser.tokens.actual
            if new_token.type == ")":
                Parser.tokens.selectNext()
                return left
            else:
                raise TypeError("Invalid Token Error - Expecting Parentesis ')' ")
        else:
            raise SyntaxError("Invalid Token - Sentence should start with number, parentesis or operator (+,-): ", new_token.type)

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result =  Parser.statements()
        if Parser.tokens.actual.type == 'EOF':
            return result
        else:
            raise SyntaxError("Invalid Chain Exception (tip: do not put spaces between numbers)")


if __name__ == '__main__':

    with open('teste.txt', 'r') as file:
        text = file.read()

    replace_inline_comment = text.replace('\\n', '\n')
    code = PrePro.filter(replace_inline_comment)
    res = Parser.run(code)
    ST = SymbolTable()
    res.Evaluate(ST)
import sys

reserved = ['PRINT', 'END', 'WHILE', 'WEND', 'IF', 'OR', 'AND', 'NOT', 'INPUT', 'ELSE', 'THEN', 'SUB', 'MAIN', 'INTEGER', 'BOOLEAN', 'DIM', 'AS']

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
        elif self.value == '~':
            return ~self.children[0].Evaluate(ST)
        else:
            print("master blaster error")

class Statements(Node):
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
        elif self.value == '=':
            return (self.children[0].Evaluate(ST) == self.children[1].Evaluate(ST))
        elif self.value == '>':
            return (self.children[0].Evaluate(ST) > self.children[1].Evaluate(ST))
        elif self.value == '<':
            return (self.children[0].Evaluate(ST) < self.children[1].Evaluate(ST))
        elif self.value == 'OR':
            return (self.children[0].Evaluate(ST) or self.children[1].Evaluate(ST))
        elif self.value == 'AND':
            return (self.children[0].Evaluate(ST) and self.children[1].Evaluate(ST))
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

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        try:
            res = int(input())
        except:
            raise ValueError("input value must be a number")
            
        return res

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        pass

class IF(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        if self.children[0].Evaluate(ST):
            self.children[1].Evaluate(ST)
        elif len(self.children) == 3:
            self.children[2].Evaluate(ST)
        else:
            pass

class WHILE(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        while self.children[0].Evaluate(ST):
            self.children[1].Evaluate(ST)


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


class Parser():

    def program():
        node = Statements('sta', [Parser.statement()])
         if Parser.tokens.actual.type == 'SUB':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'MAIN':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == '(':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == ')':
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == 'EOL':
                            Parser.tokens.selectNext()
                            while Parser.tokens.actual.type != 'END':
                                Parser.tokens.selectNext()
                                node.children.append(Parser.statement())
                                if Parser.tokens.actual.type != 'EOL':
                                    raise SyntaxError("Missing End of Line after statement - program block")
                                else:
                                    Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == 'END':
                                Parser.tokens.selectNext()
                                if Parser.tokens.actual.type == 'SUB': 
                                    Parser.tokens.selectNext()
                                    while Parser.tokens.actual.type == 'EOL':
                                        Parser.tokens.selectNext()
                                else:
                                    raise SyntaxError("Missing last SUB Statement - program block")
                            else:
                                raise SyntaxError("Missing End Statement - program block")
                        else:
                                raise SyntaxError("Missing EOL Statement - program block")
                    else:
                                raise SyntaxError("Missing ) Statement - program block")
                else:
                                raise SyntaxError("Missing ( Statement - program block")
            else:
                                raise SyntaxError("Missing MAIN Statement - program block")
        else:
                                raise SyntaxError("Missing first SUB Statement - program block")
        return node
    
    def statement():

        # identifier
        if Parser.tokens.actual.type == 'identifier':
            identifier = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == '=':
                Parser.tokens.selectNext()
                return Assignment('=', [identifier, Parser.relExpression()])
        
        # print
        elif Parser.tokens.actual.type == 'PRINT':
                Parser.tokens.selectNext()
                return Print('print', [Parser.parseExpression()])

        # dim
        elif Parser.tokens.actual.type == 'DIM':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'identifier':
                value = Parser.tokens.actual.value
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'AS':
                    Parser.tokens.selectNext()
                    return VarDec([Identifier('id', value), Parser.Type()])
                else:
                    raise SyntaxError("Missing AS token - DIM statement")
            else:
                raise SyntaxError("Missing identifier token - DIM statement

        # while
        elif Parser.tokens.actual.type == 'WHILE':
                Parser.tokens.selectNext()
                relExp = Parser.relExpression()
                if Parser.tokens.actual.type == 'EOL':
                    Parser.tokens.selectNext()
                else:
                    raise SyntaxError("Missing EOL token - after relExpression")
                tmp_node_list = []
                while(Parser.tokens.actual.type != 'WEND'):
                    tmp_node_list.append(Parser.statement())
                    if Parser.tokens.actual.type == 'EOL':
                        Parser.tokens.selectNext()
                    else:
                        raise SyntaxError("Missing EOL token - after while statement")
                Parser.tokens.selectNext()
                return WHILE('WHILE', [relExp, Statements('Sta', tmp_node_list)])

        # if
        elif Parser.tokens.actual.type == 'IF':
                Parser.tokens.selectNext()
                if_childrens = [Parser.relExpression()]
                if Parser.tokens.actual.type == 'THEN':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == 'EOL':
                        Parser.tokens.selectNext()
                        tmp_node_if = []
                        while(Parser.tokens.actual.type not in ['END', 'ELSE']):
                            tmp_node_if.append(Parser.statement())
                            if Parser.tokens.actual.type == 'EOL':
                                Parser.tokens.selectNext()
                            else:
                                raise SyntaxError("Missing End of Line after statement - IF statement")

                        if_childrens.append(Statements("Sta", tmp_node_if))

                        if Parser.tokens.actual.type == 'ELSE':
                            tmp_node_else = []
                            Parser.tokens.selectNext()
                            
                            if Parser.tokens.actual.type == 'EOL':
                                Parser.tokens.selectNext()
                            else:
                                raise SyntaxError("Missing End of Line after else - IF statement")                            
                            while(Parser.tokens.actual.type != 'END'):
                                tmp_node_else.append(Parser.statement())
                                if Parser.tokens.actual.type == 'EOL':
                                    Parser.tokens.selectNext()
                                else:
                                    raise SyntaxError("Missing End of Line after else statement - IF statement")

                            if_childrens.append(Statements("Sta", tmp_node_else))
                        
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == 'IF':
                            Parser.tokens.selectNext()
                            return IF("IF", if_childrens)
                        else:
                            raise SyntaxError("Missing IF token - end of IF statement")
                        else:
                            raise SyntaxError("Missing END token - IF statement")
                    else:
                        raise SyntaxError("Missing End of Line after Then - IF statement")
                else:
                    raise SyntaxError("Missing THEN token - IF statement")
        
        # no op
        else:
            return NoOp(None, None)


    def parseExpression():
        
       
        left = Parser.termo()

        while Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == 'OR':
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

            elif Parser.tokens.actual.type == 'OR':
                
                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = BinOp('or', [left, right])

            else:
                print("ultimate super master error")
            # end of while

        return left

    def termo():

        left = Parser.fator()

        while Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV' or Parser.tokens.actual.type == 'AND':

            if Parser.tokens.actual.type == 'MULT':

                Parser.tokens.selectNext()
                
                right = Parser.fator()

                left = BinOp('*', [left, right])

            elif Parser.tokens.actual.type == 'DIV':
                
                Parser.tokens.selectNext()
                
                right = Parser.fator()
                
                left = BinOp('/', [left, right])

            elif Parser.tokens.actual.type == 'AND':
                
                Parser.tokens.selectNext()
                
                right = Parser.fator()
                
                left = BinOp('and', [left, right])

            else:
                print("ultimate super master error")

        return left


    def relExpression():

        left = Parser.parseExpression()

        if Parser.tokens.actual.type == '=':

            Parser.tokens.selectNext()
            
            right = Parser.parseExpression()

            left = BinOp('=', [left, right])

        elif Parser.tokens.actual.type == '>':
            
            Parser.tokens.selectNext()
            
            right = Parser.parseExpression()
            
            left = BinOp('>', [left, right])

        elif Parser.tokens.actual.type == '<':
            
            Parser.tokens.selectNext()
            
            right = Parser.parseExpression()
            
            left = BinOp('<', [left, right])

        else:
            print("ultimate super master error")

        return left


    def fator():

        new_token = Parser.tokens.actual

        # check if token is unary operator
        if(new_token.type == "PLUS" or new_token.type == "MINUS" or new_token.type == "NOT"):
            if(new_token.type == "PLUS"):
                
                Parser.tokens.selectNext()
                return UnOp('+',[Parser.fator()])
                
            elif(new_token.type == "MINUS"):
                Parser.tokens.selectNext()
                return UnOp('-',[Parser.fator()])

            elif(new_token.type == "NOT"):
                Parser.tokens.selectNext()
                return UnOp('~',[Parser.fator()])
                
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

        elif new_token.type == 'INPUT':
            left = Input('input', [])
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

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            text = file.read()

    replace_inline_comment = text.replace('\\n', '\n')
    code = PrePro.filter(replace_inline_comment)
    res = Parser.run(code)
    ST = SymbolTable()
    res.Evaluate(ST)
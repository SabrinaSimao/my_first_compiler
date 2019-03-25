class PrePro():

    def filter(code):
        i = 0
        to_delete = []
        text = list(code)
        while i < len(text):
            if text[i] == "'":
                j = i
                while text[j] != "y":
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


class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self):
        pass

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate()
        elif self.value == '-':
            return -self.children[0].Evaluate()
        else:
            print("master blaster error")

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self):
        if self.value == '+':
            return (self.children[0].Evaluate() + self.children[1].Evaluate())
        elif self.value == '-':
            return (self.children[0].Evaluate() - self.children[1].Evaluate())
        elif self.value == '*':
            return (self.children[0].Evaluate() * self.children[1].Evaluate())
        elif self.value == '/':
            return (self.children[0].Evaluate() // self.children[1].Evaluate())
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self):
        return int(self.value)

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self):
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
        int_token = ""
        int_flag = False
        eof = False
        type = None
        value = None

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


            while self.position < len(self.origin) and self.origin[self.position].isnumeric():
                type = 'INT'
                int_token += self.origin[self.position]
                self.position += 1
                int_flag = True

            if not int_flag:

                if self.origin[self.position] == '+':
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
                else:
                    raise SyntaxError("Invalid Sentence")
        if int_flag:
            self.actual = Token(type, str(int_token))
            return self.actual
        else:
            self.actual = Token(type, str(value))
            return self.actual


class Parser():

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
                raise TypeError("Invalid Token Error (should have gotten INT): ", new_token.type)

        #cheeck if token is a number
        elif new_token.type == "INT":
            left = IntVal(new_token.value, [])
            Parser.tokens.selectNext()
            return left

        #check if token is parentesis
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
        result =  Parser.parseExpression()
        if Parser.tokens.actual.type == 'EOF':
            return result
        else:
            raise SyntaxError("Invalid Chain Exception (tip: do not put spaces between numbers)")


if __name__ == '__main__':
    print("Your input: ")
    text = input()
    code = PrePro.filter(text)
    res = Parser.run(code)
    print(res.Evaluate())
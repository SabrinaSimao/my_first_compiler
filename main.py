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
        
       
        result = int(Parser.termo())

        while Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS':
             # if actual token is +
            if Parser.tokens.actual.type == 'PLUS':

                Parser.tokens.selectNext()
        
                result += int(Parser.termo())

             # if actual token is -
            elif Parser.tokens.actual.type == 'MINUS':
                
                Parser.tokens.selectNext()
            
                result -= int(Parser.termo())
            else:
                print("ultimate super master error")
            # end of while

        return result

    def termo():

        result = int(Parser.fator())

        while Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'DIV':
            # if actual token is +
            if Parser.tokens.actual.type == 'MULT':

                Parser.tokens.selectNext()
        
                result *= int(Parser.fator())

            # if actual token is -
            elif Parser.tokens.actual.type == 'DIV':
                
                Parser.tokens.selectNext()
            
                result /= int(Parser.fator())
            else:
                print("ultimate super master error")
            # end of while

        return result

    def fator():

        new_token = Parser.tokens.actual
        result = 0

        # check if token is unary operator
        if(new_token.type == "PLUS" or new_token.type == "MINUS"):
            if(new_token.type == "PLUS"):
                Parser.tokens.selectNext()
                result += int(Parser.fator())
                return result
            elif(new_token.type == "MINUS"):
                Parser.tokens.selectNext()
                result -= int(Parser.fator())
                return result
            else:
                raise TypeError("Invalid Token Error (should have gotten INT): ", new_token.type)

        #cheeck if token is a number
        elif new_token.type == "INT":
            result = new_token.value
            Parser.tokens.selectNext()
            return result

        #check if token is parentesis
        elif new_token.type == "(":
            Parser.tokens.selectNext()
            result = int(Parser.parseExpression())
            new_token = Parser.tokens.actual
            if new_token.type == ")":
                Parser.tokens.selectNext()
                return result
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
    print(Parser.run(code))

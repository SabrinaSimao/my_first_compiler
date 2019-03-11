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
                else:
                    raise SyntaxError("Invalid Sentence (Sentence must start with number)")
        if int_flag:
            self.actual = Token(type, str(int_token))
            return self.actual
        else:
            self.actual = Token(type, str(value))
            return self.actual


class Parser():

    def parseExpression():
        
       
        result = Parser.termo()

        while Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS':
            # se token atual e +
            if Parser.tokens.actual.type == 'PLUS':

                Parser.tokens.selectNext()
        
                result += Parser.termo()

            # se token atual e -
            elif Parser.tokens.actual.type == 'MINUS':
                
                Parser.tokens.selectNext()
            
                result -= Parser.termo()
            else:
                print("ultimate super master error")
            # fim do while

        
        if Parser.tokens.actual.type == 'EOF':
            return result
        else:
            raise SyntaxError("Invalid Chain Exception (tip: do not put spaces between numbers)")


    def termo():
        # initialize result
        new_token = Parser.tokens.actual

        
        if new_token.type == 'INT':
            result = int(new_token.value)
            new_token = Parser.tokens.selectNext()
            while new_token.type == 'MULT' or new_token.type == 'DIV':
                # se token atual e *
                if new_token.type == 'MULT':
                    new_token = Parser.tokens.selectNext()
                    if new_token.type == 'INT':
                        result *= int(new_token.value)
                    else:
                        raise TypeError("Invalid Token Error: ", new_token.type)
                # se token atual e /
                elif new_token.type == 'DIV':
                    new_token = Parser.tokens.selectNext()
                    if new_token.type == 'INT':
                        result //= int(new_token.value)
                    else:
                        raise TypeError("Invalid Token Error: ", new_token.type)

                new_token = Parser.tokens.selectNext()
            # fim do while
            return result
        else:
            raise TypeError("Invalid Token Error (should have gotten INT): ", new_token.type)

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


if __name__ == '__main__':
    print("Your input: ")
    text = input()
    code = PrePro.filter(text)
    print(Parser.run(code))

import Node as nd
from Tokenizer import *
reserved = ['PRINT', 'END', 'WHILE', 'WEND', 'IF', 'OR', 'AND', 'NOT', 'INPUT', 'ELSE', 'THEN', 'SUB', 'MAIN', 'INTEGER', 'BOOLEAN', 'DIM', 'AS', 'TRUE', 'FALSE']

class Parser():

    def program():
        node = nd.Statements('sta', [Parser.statement()])
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
                            tmp_program_list = []
                            
                            while Parser.tokens.actual.type != 'END':
                                tmp_program_list.append(Parser.statement())
                                if Parser.tokens.actual.type != 'EOL':
                                    raise SyntaxError("Missing End of Line after statement - program block")
                                else:
                                    Parser.tokens.selectNext()
                            
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.type == 'SUB': 
                                Parser.tokens.selectNext()
                                while Parser.tokens.actual.type == 'EOL':
                                    Parser.tokens.selectNext()
                                return nd.Statements('Sta', tmp_program_list)
                            else:
                                raise SyntaxError("Missing last SUB Statement - program block")
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
            identifier = nd.Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == '=':
                Parser.tokens.selectNext()
                return nd.Assignment('=', [identifier, Parser.relExpression()])
        
        # print
        elif Parser.tokens.actual.type == 'PRINT':
                Parser.tokens.selectNext()
                return nd.Print('print', [Parser.parseExpression()])

        # dim
        elif Parser.tokens.actual.type == 'DIM':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'identifier':
                identifier = nd.Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'AS':
                    Parser.tokens.selectNext()
                    return nd.VarDec('VarDec', [identifier, Parser.tipo()])
                else:
                    raise SyntaxError("Missing AS token - DIM statement")
            else:
                raise SyntaxError("Missing identifier token - DIM statement")

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
                return nd.WHILE('WHILE', [relExp, tmp_node_list])

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
                        
                        if_childrens.append(tmp_node_if)
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

                            if_childrens.append(tmp_node_else)
                        
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type == 'IF':
                            Parser.tokens.selectNext()
                            return nd.IF("IF", if_childrens)
                        else:
                            raise SyntaxError("Missing IF token - end of IF statement")
                    else:
                        raise SyntaxError("Missing End of Line after Then - IF statement")
                else:
                    raise SyntaxError("Missing THEN token - IF statement")
        
        # no op
        else:
            return nd.NoOp(None, None)


    def parseExpression():
        
       
        left = Parser.termo()

        while Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == 'OR':
             # if actual token is +
            if Parser.tokens.actual.type == 'PLUS':

                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = nd.BinOp('+', [left, right])

             # if actual token is -
            elif Parser.tokens.actual.type == 'MINUS':
                
                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = nd.BinOp('-', [left, right])

            elif Parser.tokens.actual.type == 'OR':
                
                Parser.tokens.selectNext()
                
                right = Parser.termo()

                left = nd.BinOp('OR', [left, right])

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

                left = nd.BinOp('*', [left, right])

            elif Parser.tokens.actual.type == 'DIV':
                
                Parser.tokens.selectNext()
                
                right = Parser.fator()
                
                left = nd.BinOp('/', [left, right])

            elif Parser.tokens.actual.type == 'AND':
                
                Parser.tokens.selectNext()
                
                right = Parser.fator()
                
                left = nd.BinOp('AND', [left, right])

            else:
                print("ultimate super master error")

        return left


    def relExpression():

        left = Parser.parseExpression()

        if (Parser.tokens.actual.type in ['=', '>', '<']):
            bin_op = Parser.tokens.actual.type
            Parser.tokens.selectNext()

            right = Parser.parseExpression()
            
            return nd.BinOp(bin_op, [left, right])

        else:
            return left
        

    def fator():

        new_token = Parser.tokens.actual

        # check if token is unary operator
        if(new_token.type == "PLUS" or new_token.type == "MINUS" or new_token.type == "NOT"):
            if(new_token.type == "PLUS"):
                
                Parser.tokens.selectNext()
                return nd.UnOp('+',[Parser.fator()])
                
            elif(new_token.type == "MINUS"):
                Parser.tokens.selectNext()
                return nd.UnOp('-',[Parser.fator()])

            elif(new_token.type == "NOT"):
                Parser.tokens.selectNext()
                return nd.UnOp('~',[Parser.fator()])
                
            else:
                raise TypeError("Invalid Token Error: ", new_token.type)

        # check if token is a number
        elif new_token.type == "INT":
            left = nd.IntVal(new_token.value, [])
            Parser.tokens.selectNext()
            return left

        # check if token is a boolean
        elif new_token.type in ['TRUE', 'FALSE']:
            left = nd.BoolVal(new_token.type, [])
            Parser.tokens.selectNext()
            return left

        # check if token is a variable
        elif new_token.type == 'identifier':
            left = nd.Identifier(new_token.value, [])
            Parser.tokens.selectNext()
            return left

        elif new_token.type == 'INPUT':
            left = nd.Input('input', [])
            Parser.tokens.selectNext()
            return left
            
        # check if token is parentesis
        elif new_token.type == "(":
            Parser.tokens.selectNext()
            left = Parser.relExpression()
            new_token = Parser.tokens.actual
            if new_token.type == ")":
                Parser.tokens.selectNext()
                return left
            else:
                raise TypeError("Invalid Token Error - Expecting Parentesis ')' ")
        else:
            raise SyntaxError("Invalid Token - Sentence should start with number, parentesis or operator (+,-): ", new_token.type)

    def tipo():
        if Parser.tokens.actual.type in ['INTEGER', 'BOOLEAN']:
            tipo = Parser.tokens.actual.type
            Parser.tokens.selectNext()
            return nd.Tipo(tipo, [])
        else:
            raise SyntaxError("Variable type unknown: ", tipo)

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        result =  Parser.program()
        if Parser.tokens.actual.type == 'EOF':
            return result
        else:
            raise SyntaxError("Invalid Chain Exception (tip: do not put spaces between numbers)")

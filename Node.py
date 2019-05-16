from main import *
class Assembler():
    commands = []

    def Write(text):
        Assembler.commands.append(text)

    
    def create_assembly():
        #do something with out file

        with open("program.asm", "w+") as fout:
            with open("pre_code.txt") as pre_code:
                for line1 in pre_code:
                    fout.write(line1)

            for line2 in Assembler.commands:
                fout.write(line2 + '\n')
            
            with open("post_code.txt") as post_code:
                for line3 in post_code:
                    fout.write(line3)



class Node():

    i = 0
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
        
    def newID():
        Node.i += 1
        return Node.i
    
    def Evaluate(self, ST):
        pass

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        #this will write "mov ebx, value"
        f1 = self.children[1].Evaluate(ST)
        
        Assembler.Write("MOV [EBP-{}], EBX".format(ST.getter(self.children[0].value)[2]))


class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        if self.value == '+':
            if f0[1] == 'INTEGER':
                Assembler.Write("MOV EAX, 1")
                Assembler.Write("IMUL EBX")
                Assembler.Write("MOV EBX, EAX")
                #return (f0[0], 'INTEGER')
            else:
                raise ValueError("Unary operator + must be followed by an integer")
        elif self.value == '-':
            if f0[1] == 'INTEGER':
                Assembler.Write("MOV EAX, -1")
                Assembler.Write("IMUL EBX")
                Assembler.Write("MOV EBX, EAX")
                #return (-f0[0], 'INTEGER')
            else:
                raise ValueError("Unary operator - must be followed by an integer")
        elif self.value == '~':
            if f0[1] == 'BOOLEAN':
                if f0[0] == 'TRUE':
                    Assembler.Write("MOV EBX, False")
                else:
                    Assembler.Write("MOV EBX, True")
                #return (not f0[0], 'BOOLEAN')
            else:
                raise ValueError("Unary operator ~ must be followed by an boolean")
        else:
            print("master blaster error")

class Statements(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, ST):
        for i in self.children:
           i.Evaluate(ST)

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, ST):
        f = self.children[0].Evaluate(ST)
        #print(f[0])
        Assembler.Write("PUSH EBX")
        Assembler.Write("CALL print")
        Assembler.Write("POP EBX")

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        Assembler.Write("PUSH EBX")
        f1 = self.children[1].Evaluate(ST)
        Assembler.Write("POP EAX")
        if self.value == '+':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("ADD EAX, EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] + f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant sum non integer values")
        elif self.value == '-':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("SUB EAX, EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] - f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant subtract non integer values")
        elif self.value == '*':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("IMUL EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] * f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant muktiply non integer values")
        elif self.value == '/':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("IDIV EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] // f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant divide non integer values")
        elif self.value == '=':
            if (f0[1] == f1[1]):
                Assembler.Write("CMP EAX, EBX")
                Assembler.Write("CALL binop_je")
                #return ([f0[0] == f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare values of diferent types")
        elif self.value == '>':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("CMP EAX, EBX")
                Assembler.Write("CALL binop_jg")
                #return ([f0[0] > f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare (>) non integer values")
        elif self.value == '<':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                Assembler.Write("CMP EAX, EBX")
                Assembler.Write("CALL binop_jl")
                #return ([f0[0] < f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare (<) non integer values")
        elif self.value == 'OR':
            if (f0[1] == f1[1] and f0[1] == 'BOOLEAN'):
                Assembler.Write("OR EAX, EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] or f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant make OR with non boolean values")
        elif self.value == 'AND':
            if (f0[1] == f1[1] and f0[1] == 'BOOLEAN'):
                Assembler.Write("AND EAX, EBX")
                Assembler.Write("MOV EBX, EAX")
                #return ([f0[0] and f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant make AND with non boolean values")
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        Assembler.Write("MOV EBX, {}".format(self.value))
        #return [int(self.value), 'INTEGER']
        

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        Assembler.Write("MOV EBX, {}".format(self.value))
        #return [self.value, 'BOOLEAN']

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        #colocar shift do getter da ST
        Assembler.Write("MOV EBX, [EBP-{}]".format(ST.getter(self.children[0].value)[2]))
        #value = ST.getter(self.value)
        #return value


class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        pass

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        pass

class IF(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        
        condition = self.children[0].Evaluate(ST)
        Assembler.Write("CMP EBX, True")
        Assembler.Write("JE if_{}:".format(self.id))

        if len(self.children) == 3:
        #if there are else condition: evaluate them
            for f2 in self.children[2]:
                f2.Evaluate(ST)

        Assembler.Write("JMP EXIT_{}:".format(self.id))
        Assembler.Write("if_{}:".format(self.id))

        #if(condition[0] == 'TRUE' or condition[0] == True):
        #if condition is always evaluated
        for f in self.children[1]:
            f.Evaluate(ST)
        #else:
        #    pass

        Assembler.Write("EXIT_{}:".format(self.id))

class WHILE(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        Assembler.Write("LOOP_{}:".format(self.id))
        condition = self.children[0].Evaluate(ST)
        
        Assembler.Write("CMP EBX, False")
        Assembler.Write("JE EXIT_{}:".format(self.id))
        #while (self.children[0].Evaluate(ST)[0] == True) or (self.children[0].Evaluate(ST)[0] == 'TRUE'):
        for f in self.children[1]:
            f.Evaluate(ST)
        Assembler.Write("JMP LOOP_{}:".format(self.id))
        Assembler.Write("EXIT_{}:".format(self.id))


class Tipo(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, ST):
        pass

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, ST):
        f0 = self.children[0].value
        f1 = self.children[1].Evaluate(ST)
        ST.creator(f0, None, f1)
        Assembler.Write("PUSH DWORD 0")
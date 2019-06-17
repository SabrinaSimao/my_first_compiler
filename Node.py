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
        f0 = self.children[0].value
        f1 = self.children[1].Evaluate(ST)
        ST.setter(f0, f1)
        Assembler.Write("MOV [EBP-{}], EBX".format(ST.getter(f0)[2]))


class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        if self.value == '+':
                Assembler.Write("MOV EAX, 1")
                Assembler.Write("IMUL EBX")
                Assembler.Write("MOV EBX, EAX")
        elif self.value == '-':
                Assembler.Write("MOV EAX, -1")
                Assembler.Write("IMUL EBX")
                Assembler.Write("MOV EBX, EAX")
        elif self.value == '~':
                if f0 == False or f0 == 'FALSE':
                    Assembler.Write("MOV EBX, TRUE")
                else:
                    Assembler.Write("MOV EBX, FALSE")
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
        if f0 == 'TRUE':
            f0 = True
        if f0 == 'FALSE':
            f0 = False
        if f1 == 'TRUE':
            f1 = True
        if f1 == 'FALSE':
            f1 = False
        if self.value == '+':
            Assembler.Write("ADD EAX, EBX")
            Assembler.Write("MOV EBX, EAX")
        elif self.value == '-':
            Assembler.Write("SUB EAX, EBX")
            Assembler.Write("MOV EBX, EAX")
        elif self.value == '*':
            Assembler.Write("IMUL EBX")
            Assembler.Write("MOV EBX, EAX")
        elif self.value == '/':
            Assembler.Write("IDIV EBX")
            Assembler.Write("MOV EBX, EAX")
        elif self.value == '=':
            Assembler.Write("CMP EAX, EBX")
            Assembler.Write("CALL binop_je")
            return (f0 == f1)
        elif self.value == '>':
            Assembler.Write("CMP EAX, EBX")
            Assembler.Write("CALL binop_jg")
            return (f0 > f1)
        elif self.value == '<':
            Assembler.Write("CMP EAX, EBX")
            Assembler.Write("CALL binop_jl")
            return (f0 < f1)
        elif self.value == 'OR':
            Assembler.Write("OR EAX, EBX")
            Assembler.Write("MOV EBX, EAX")
            return (f0 or f1)
        elif self.value == 'AND':
            Assembler.Write("AND EAX, EBX")
            Assembler.Write("MOV EBX, EAX")
            return (f0 and f1)
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        Assembler.Write("MOV EBX, {}".format(self.value))
        

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        Assembler.Write("MOV EBX, {}".format(self.value))
        return (self.value)

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()
    
    def Evaluate(self, ST):
        
        #colocar shift do getter da ST
        Assembler.Write("MOV EBX, [EBP-{}]".format(ST.getter(self.value)[2]))
        return ST.getter(self.value)[0]

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
        Assembler.Write("JE if_{}".format(self.id))

        if len(self.children) == 3:
        #if there are else condition: evaluate them
            for f2 in self.children[2]:
                f2.Evaluate(ST)

        Assembler.Write("JMP EXIT_{}".format(self.id))
        Assembler.Write("if_{}:".format(self.id))

        #if condition is always evaluated
        for f in self.children[1]:
            f.Evaluate(ST)

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
        Assembler.Write("JE EXIT_{}".format(self.id))
        for f in self.children[1]:
            f.Evaluate(ST)
        Assembler.Write("JMP LOOP_{}".format(self.id))
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
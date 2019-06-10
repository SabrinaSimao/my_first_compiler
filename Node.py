from main import *

class Node():

    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        pass

class FuncDec(Node):
    def __init__(self, value, children):
            self.value = value
            self.children = children

    def Evaluate(self, ST):
        ST.creator(self.value, None, 'FUNCTION')
        ST.setter(self.value, self)

class SubDec(Node):
    def __init__(self, value, children):
            self.value = value
            self.children = children

    def Evaluate(self, ST):
        ST.creator(self.value, None, 'SUB')
        ST.setter(self.value, self)

class FuncCall(Node):
    def __init__(self, value, children):
            self.value = value
            self.children = children

    def Evaluate(self, ST):   
        func = ST.getter(self.value)[0]
        func_type = ST.getter(self.value)[1]
        table = SymbolTable(anc=ST)
        is_func = 0
        if(func_type == 'FUNCTION'):
            table.creator(self.value, None, func.children[0].Evaluate(table))
            is_func = 1
        n = 0
        for i in range(is_func, len(func.children)-1):
            func.children[i].Evaluate(table)
            table.setter(func.children[i].children[0].value, self.children[n].Evaluate(ST)[0])
            n += 1
        func.children[-1].Evaluate(table)
        if is_func:
            return table.dic[self.value]

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        f1 = self.children[1].Evaluate(ST)
        if f1[0] in ['TRUE', 'FALSE']:
            if f1[1] != 'BOOLEAN':
                raise ValueError("Incorrect type assignment: ", f1[1])
        else:
            if f1[0] == 'BOOLEAN':
                raise ValueError("Incorrect type assignment: ", f1[0])

        if isinstance(f1[0], int):
            if f1[1] != 'INTEGER':
                raise ValueError("Incorrect type assignment: ", f1[1])
        else:
            if f1[0] == 'INTEGER':
                raise ValueError("Incorrect type assignment: ", f1[0])

        ST.setter(self.children[0].value, f1[0])

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        if self.value == '+':
            if f0[1] == 'INTEGER':
                return (f0[0], 'INTEGER')
            else:
                raise ValueError("Unary operator + must be followed by an integer")
        elif self.value == '-':
            if f0[1] == 'INTEGER':
                return (-f0[0], 'INTEGER')
            else:
                raise ValueError("Unary operator - must be followed by an integer")
        elif self.value == '~':
            if f0[1] == 'BOOLEAN':
                return (not f0[0], 'BOOLEAN')
            else:
                raise ValueError("Unary operator ~ must be followed by an boolean")
        else:
            print("master blaster error")
        #carrega eax com -1 ou +1
        #se for not, da neg em ebx
        #IMUL EBX
        #mov ebx, eax

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
        f = self.children[0].Evaluate(ST)
        print(f[0])

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        

    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        f1 = self.children[1].Evaluate(ST)
        if self.value == '+':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] + f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant sum non integer values")
        elif self.value == '-':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] - f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant subtract non integer values")
        elif self.value == '*':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] * f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant muktiply non integer values")
        elif self.value == '/':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] // f1[0], 'INTEGER'])
            else:
                raise ValueError("Cant divide non integer values")
        elif self.value == '=':
            if (f0[1] == f1[1]):
                return ([f0[0] == f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare values of diferent types")
        elif self.value == '>':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] > f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare (>) non integer values")
        elif self.value == '<':
            if (f0[1] == f1[1] and f0[1] == 'INTEGER'):
                return ([f0[0] < f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant compare (<) non integer values")
        elif self.value == 'OR':
            if (f0[1] == f1[1] and f0[1] == 'BOOLEAN'):
                return ([f0[0] or f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant make OR with non boolean values")
        elif self.value == 'AND':
            if (f0[1] == f1[1] and f0[1] == 'BOOLEAN'):
                return ([f0[0] and f1[0], 'BOOLEAN'])
            else:
                raise ValueError("Cant make AND with non boolean values")
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):
        return [int(self.value), 'INTEGER']
        

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):
        return [self.value, 'BOOLEAN']

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):
        try:
            value = ST.getter(self.value)
            return value
        except:
            raise ValueError("This identifier was not declared: ", self.value)


class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):
        try:
            res = int(input())
        except:
            raise ValueError("input value must be a number")
            
        return [res, 'INTEGER']

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
        
        condition = self.children[0].Evaluate(ST)
        if(condition[0] == 'TRUE' or condition[0] == True):
            for f in self.children[1]:
                f.Evaluate(ST)
        elif len(self.children) == 3:
            for f2 in self.children[2]:
                f2.Evaluate(ST)
        else:
            pass
        
class WHILE(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    
    def Evaluate(self, ST):
        while (self.children[0].Evaluate(ST)[0] == True) or (self.children[0].Evaluate(ST)[0] == 'TRUE'):
            for f in self.children[1]:
                f.Evaluate(ST)

class Tipo(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        

    def Evaluate(self, ST):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        

    def Evaluate(self, ST):
        f0 = self.children[0].value
        f1 = self.children[1].Evaluate(ST)
        ST.creator(f0, None, f1)
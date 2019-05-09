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
        tipo = ST.getter(self.children[0].value)[1]

        f1 = self.children[1].Evaluate(ST)
        
        if f1 in ['TRUE', 'FALSE']:
            if tipo != 'BOOLEAN':
                raise ValueError("Incorrect type assignment: ", tipo)
        else:
            if tipo == 'BOOLEAN':
                raise ValueError("Incorrect type assignment: ", f1)

        if isinstance(f1, int):
            if tipo != 'INTEGER':
                raise ValueError("Incorrect type assignment: ", tipo)
        else:
            if tipo == 'INTEGER':
                raise ValueError("Incorrect type assignment: ", f1)

        ST.setter(self.children[0].value, f1, tipo)

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
        f = self.children[0].Evaluate(ST)
        if isinstance(f,str):
            value, tipo = ST.getter(f)
            print(value)
        else:
            print(f)

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):

        f0 = self.children[0].Evaluate(ST)
        f1 = self.children[1].Evaluate(ST)

        if isinstance(f0,str):
            f0, t0 = ST.getter(f0)

        if isinstance(f1,str):
            f1, t0 = ST.getter(f1)

        if self.value == '+':
            return (f0 + f1)
        elif self.value == '-':
            return (f0 - f1)
        elif self.value == '*':
            return (f0 * f1)
        elif self.value == '/':
            return (f0 // f1)
        elif self.value == '=':
            return (f0 == f1)
        elif self.value == '>':
            return (f0 > f1)
        elif self.value == '<':
            return (f0 < f1)
        elif self.value == 'OR':
            return (f0 or f1)
        elif self.value == 'AND':
            return (f0 and f1)
        else:
            print("master blaster error")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        return int(self.value)

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        return self.value

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    
    def Evaluate(self, ST):
        return self.value

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
        #if self.children[0].Evaluate in ST:
        #    raise ValueError("VARIABLE WAS ALREADY DECLARED", self.children[0])
            
        #else:
        f0 = self.children[0].Evaluate(ST)
        f1 = self.children[1].Evaluate(ST)
        ST.setter(f0, None, f1)

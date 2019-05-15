import sys
from Parser import *

class SymbolTable():
    def __init__(self):
        self.dic = {}
        self.shift = 0

    def getter(self, index):
        if index in self.dic:
            return self.dic[index]
        else:
            raise ValueError("Variable does not exist", index)

    def setter(self, index, value):
        if index not in self.dic:
            #erro var not declared
            pass
        else:
            self.dic[index][0] = value


    def creator(self, index, value, tipo):
        if index in self.dic:
            #erro var duplicada
            pass
        else:
            self.shift -=4
            self.dic[index] = [None, tipo, self.shift]


if __name__ == '__main__':

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            text = file.read()

    replace_inline_comment = text.replace('\\n', '\n')
    code = PrePro.filter(replace_inline_comment)
    res = Parser.run(code)
    ST = SymbolTable()
    res.Evaluate(ST)
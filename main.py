## VBA COMPILER - Sabrina_Simao@hotmail.com
## Insper - 2019

import sys
from Parser import *
class SymbolTable():
    def __init__(self, anc):
        self.dic = {}
        self.anc = anc

    def getter(self, index):
        
        if index in self.dic and self.dic[index][0] != None:
            return self.dic[index]
        elif (self.anc != None):
            return self.anc.getter(index)
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
            self.dic[index] = [None, tipo]


if __name__ == '__main__':

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            text = file.read()
    #debug
    else:
        with open("teste.vbs", 'r') as file:
            text = file.read()

    replace_inline_comment = text.replace('\\n', '\n')
    code = PrePro.filter(replace_inline_comment)
    res = Parser.run(code)
    ST = SymbolTable(None)
    res.Evaluate(ST)
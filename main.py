import sys
from Parser import *

class SymbolTable():
    def __init__(self):
        self.dic = {}

    def getter(self, index):
        if index in self.dic:
            return self.dic[index]
        else:
            raise ValueError("Variable does not exist", index)

    def setter(self, index, value, tipo):
        self.dic[index] = [value, tipo]


if __name__ == '__main__':

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as file:
            text = file.read()

    replace_inline_comment = text.replace('\\n', '\n')
    code = PrePro.filter(replace_inline_comment)
    res = Parser.run(code)
    ST = SymbolTable()
    res.Evaluate(ST)
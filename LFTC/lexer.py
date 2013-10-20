import re

__author__ = 'Roland'
import sys

keywords = ['float', 'char', 'print', 'input', 'break', 'continue', 'return', 'def', 'if', 'elif',
            'else', 'while', 'or', 'and', 'not']
operators = ['=', '<', '>', '==', '>=', '<=', '!=', '+', '-', '*', '/', '%']

separators = ['[', ']', '(', ')', ',',  ':']

codif = ['var', 'const', '\n', 'indent', 'dedent'] + keywords + operators + separators


def error(line_nr, msg):
    print("Lexical error at line %d: %s" % (line_nr, msg))

class binary_tree(object):

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def add(self, value):
        if self.value is None:
            self.value = value
        elif value < self.value:
            if self.left:
                self.left.add(value)
            else:
                self.left = binary_tree(value)
        else:
            if self.right:
                self.right.add(value)
            else:
                self.right = binary_tree(value)

    def __contains__(self, value):
        if value == self.value:
            return True
        return (self.left and value in self.left) or (self.right and value in self.right)

    def index(self, value):
        # WHAT?
        if self.right and value == self.right.value:
            return self.value, 1
        if self.left and value == self.left.value:
            return self.value, 0
        if self.left and value in self.left:
            return self.left.index(value)
        if self.right and value in self.right:
            return self.right.index(value)

    def __str__(self):
        s = str(self.value)
        if self.left:
            s+= " " + str(self.left)
        else:
            s+= " None "
        if self.right:
            s+= " " + str(self.right)
        else:
            s+= " None "
        return s

def get_poz(atom, ts):
    if atom not in ts:
        ts.add(atom)
    return ts.index(atom)

def lexer(program):
    ts_const = binary_tree(None)
    ts_ident = binary_tree(None)
    fip = []
    indentation = [0]
    for i, line in enumerate(program.splitlines()):
        indent_level = len(line) - len(line.lstrip())
        if indent_level != indentation[-1]:
            if indent_level > indentation[-1]:
                indentation.append(indent_level)
                fip.append((codif.index('indent'), 0))
            else:
                while len(indentation) and indentation[-1] != indent_level:
                    fip.append((codif.index('dedent'), 0))
                    indentation.pop()
                if len(indentation) == 0:
                    error(i, "incorrect indentation")
        print(list(re.split("( |=|<|>|==|>=|<=|!=|\+|-|\*|/|%|\[|\]|\(|\)|,|:)", line)))
        in_string = ""
        for atom in re.split("( |=|<|>|==|>=|<=|!=|\+|-|\*|/|%|\[|\]|\(|\)|,|:)", line):
            if len(atom.strip()) == 0 and not in_string:
                continue

            if '"' in atom:
                if in_string:
                    in_string += atom
                    fip.append((1, get_poz(in_string, ts_const)))
                    in_string = ""
                    continue
                else:
                    in_string = atom
                    continue
            if in_string:
                in_string += atom
                continue

            if atom in keywords or atom in operators or atom in separators:
                fip.append((codif.index(atom), 0))
            else:
                if re.match("^[a-zA-Z][a-zA-Z0-9]*(\[[0-9]+\])?$", atom):
                    fip.append((0, get_poz(atom, ts_ident)))
                elif re.match("[1-9][0-9]*\.[0-9]+", atom):
                    fip.append((1, get_poz(atom, ts_const)))
                else:
                    error(i, " unidentified expression " + atom)
        fip.append((codif.index('\n'), 0))
    return fip, ts_const, ts_ident


if len(sys.argv) == 1:
    print("You must give file to analyze as argument")

#file = sys.argv[1]
file = "p1.mpy"
f = open(file, "rb")
fip, ts_const, ts_ident = lexer(f.read())
print(fip)
print(ts_const)
print(ts_ident)
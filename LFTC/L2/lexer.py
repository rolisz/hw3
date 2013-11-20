#!/usr/bin/python
from fsm import parse_automaton, accept

import re

__author__ = 'Roland'
import sys

keywords = ['float', 'char', 'print', 'input', 'break', 'continue', 'return', 'def', 'if', 'elif',
            'else', 'while', 'or', 'and', 'not']
operators = ['=', '<', '>', '==', '>=', '<=', '!=', '+', '-', '*', '/', '%']

separators = ['[', ']', '(', ')', ',', ':']

codif = ['var', 'const', '\n', 'indent', 'dedent'] + keywords + operators + separators


def error(line_nr, msg):
    """
        Show an error message `msg` found at line number `line_nr`
    """
    print("Lexical error at line %d: %s" % (line_nr, msg))


def value_or_none(tree):
    """
        Helper function to return string, even if given a tree, string or None
    """
    if tree is None:
        return 'None'
    else:
        if type(tree) == str:
            return tree
        return str(tree.value)


class binary_tree(object):
    """
        Binary search tree. It remembers the order in which elements were added.
    """

    def __init__(self, value):
        """
            Constructor
        """
        self.value = value
        if self.value:
            self.elements = [value]
        else:
            self.elements = []
        self.left = None
        self.right = None

    def add(self, value):
        """
            Add `value` to the tree to the correct place
        """
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
        """
            Search for `value` in the tree.
        """
        if value == self.value:
            return True
        return (self.left and value in self.left) or (self.right and value in self.right)

    def index(self, value):
        """
            Return the parent and sibling node of `value`. Return None if it is not found,
            and (None, None) for root node.
        """
        if self.value == value:
            return (None, None)
        if self.right and value == self.right.value:
            return self.value, self.left
        if self.left and value == self.left.value:
            return self.value, self.right
        if self.left and value in self.left:
            return self.left.index(value)
        if self.right and value in self.right:
            return self.right.index(value)

    def __str__(self):
        """
        String representation of the tree, using a table with parent and sibling relations.
        """
        s = ""
        for i, element in enumerate(self.elements):
            parent, sibling = self.index(element)
            s += (str(i) + " | " + str(element) + " | " + value_or_none(parent) + " | " + value_or_none(sibling) + "\n")
        return s


def get_poz(atom, ts):
    """
        Get the position of `atom` in the tree `ts`, and insert it if it's not in the tree.
    """
    if atom not in ts:
        ts.add(atom)
        ts.elements.append(atom)
    parent, sibling = ts.index(atom)
    return ts.elements.index(atom)


var_lang = ["i a-z s B",
            "i A-Z s B",
            "s a-z s F",
            "s A-z s F",
            "s 0-9 s F",
            "s [ t",
            "t 0-9 f",
            "f 0-9 f",
            "f ] l F"]
var_aut = parse_automaton(var_lang)
num_lang = ["i 0 s B",
            "i 1-9 t B",
            "s . n",
            "t 0-9 f", "t . n", "f 0-9 f", "f . n", "n 0-9 n F"]
num_aut = parse_automaton(num_lang)
def lexer(program):
    """
        Function to do the actual lexing.
    """
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
        in_string = ""
        for atom in re.split("( |=|<|>|==|>=|<=|!=|\+|-|\*|/|%|\[|\]|\(|\)|,|:)", line):
            if len(atom.strip()) == 0 and not in_string:
                continue

            if '"' in atom:
                if in_string:
                    in_string += atom
                    if re.search('[^ "a-zA-Z0-9]', in_string):
                        error(i, " invalid character in string constant")
                        continue
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
                if accept(*var_aut, string=atom) == True:
                    fip.append((0, get_poz(atom, ts_ident)))
                elif accept(*num_aut, string=atom) == True:
                    fip.append((1, get_poz(atom, ts_const)))
                else:
                    error(i, " unidentified expression " + atom)
        if in_string:
            error(i, " unterminated string constant ")
        fip.append((codif.index('\n'), 0))
    return fip, ts_const, ts_ident


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You must give file to analyze as argument")

    file = sys.argv[1]
    f = open(file, "rb")
    fip, ts_const, ts_ident = lexer(f.read())
    print(fip)
    print(ts_const)
    print(ts_ident)

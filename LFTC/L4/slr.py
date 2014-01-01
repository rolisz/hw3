#!/usr/bin/python
import sys
from collections import namedtuple

if len(sys.argv) < 2:
    print("You must give a grammar file and an input file!")
    exit(1)

Grammar = namedtuple('Grammar', ['terminals', 'nonterminals', 'rules', 'start'])

def parse_grammar(lines):
    terminals = set()
    nonterminals = set()
    rules = set()
    start = ''
    for line in lines:
        line = line.strip()
        parts = line.split("=")
        lh = parts[0].strip()
        if start == '':
            start = lh
        nonterminals.add(lh)
        rh = map(lambda x: x.strip().split(), "=".join(parts[1:]).split("|"))
        for right in rh:
            for part in right:
                if part[0] == "'" and part[-1] == "'" and len(part) > 1:
                    terminals.add(part)
            rules.add((lh, tuple(right)))
    nonterminals.add(start+"'")
    rules.add((start+"'", (start,)))
    return Grammar(terminals, nonterminals, rules, start)


def expand_item_set(s, grammar):
    new_s = list(s)
    while len(new_s) > 0:
        item = new_s.pop(0)
        dot_index = item[1].index('..')
        if dot_index < len(item[1]) - 1:
            nxt = item[1][dot_index+1]
            if nxt in grammar.nonterminals:
                for rule in grammar.rules:
                    if rule[0] == nxt:
                        s.add((rule[0], ('..', ) + rule[1]))
                        new_s.append((rule[0], ('..',) + rule[1]))
    return s


def move_dot(item):
    dot_index = item[1].index('..')
    if dot_index < len(item[1]) - 1:
        rh = list(item[1])
        rh[dot_index], rh[dot_index+1] = rh[dot_index + 1], rh[dot_index]
        return rh[dot_index], (item[0], tuple(rh))
    return None, None


def analyze_grammar(grammar):
    item_sets = [expand_item_set({(grammar.start+"'",
                                 ('..', grammar.start))}, grammar)]

    new_items = item_sets[:]
    print(new_items)
    while len(new_items) > 0:
        it_s = new_items.pop(0)
        print(it_s)
        print("=======")
        for it in it_s:
            mv, n_s = move_dot(it)
            print(n_s)
            print(expand_item_set({n_s},grammar))

    return item_sets



gr_file = open(sys.argv[1], "rb")
import pprint
parsed_grammar = parse_grammar(gr_file.readlines())

print(parsed_grammar)
analyzed_grammar = analyze_grammar(parsed_grammar)

pprint.pprint(analyzed_grammar)

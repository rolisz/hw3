#!/usr/bin/python
import pprint
import sys
from collections import namedtuple

if len(sys.argv) < 2:
    print("You must give a grammar file and an input file!")
    exit(1)

Grammar = namedtuple('Grammar', ['terminals', 'nonterminals', 'rules', 'start'])

def parse_grammar(lines):
    terminals = set()
    nonterminals = set()
    rules = []
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
            if lh == 'atom':
                print(right)
            if len(right) == 0:    # epsilon
                rules.append((lh, tuple([''])))
            else:
                rules.append((lh, tuple(right)))
    nonterminals.add(start+"'")
    rules.insert(0, (start+"'", (start,)))
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
                        exp = (rule[0], ('..', ) + rule[1])
                        if exp not in s:
                            s.add(exp)
                            new_s.append(exp)
    return s


def move_dot(item):
    dot_index = item[1].index('..')
    if dot_index < len(item[1]) - 1:
        rh = list(item[1])
        rh[dot_index], rh[dot_index+1] = rh[dot_index + 1], rh[dot_index]
        return rh[dot_index], (item[0], tuple(rh))
    return None, None


def add_transition(transitions, ind, mv, nxt):
    if (ind, mv) in transitions:
        raise "Conflict"
    transitions[(ind, mv)] = nxt


def cross_first(first, *terms):
    if '' not in first[terms[0]]:
        return first[terms[0]]
    tmp = first[terms[0]] - {''}
    if len(terms) > 1:
        tmp.update(cross_first(first, *terms[1:]))
    if all('' in first[x] for x in terms):
        tmp.add('')
    return tmp


def make_first_set(grammar):
    first = {}
    for term in grammar.terminals:
        first[term] = {term}
    for lh, rh in grammar.rules:
        if lh not in first:
            first[lh] = set()
        if rh[0] in grammar.terminals or rh[0] == '':
            first[lh].add(rh[0])
    changed = True
    while changed:
        changed = False
        for lh, rh in grammar.rules:
            if rh == ('',):
                continue
            old = first[lh].copy()
            first[lh].update(cross_first(first, *rh))
            if old != first[lh]:
                changed = True
    return first


def make_follow_set(grammar):
    follow = {x:set() for x in grammar.nonterminals}
    follow[grammar.start+"'"] = '$'

    first = make_first_set(grammar)

    changed = True
    while changed:
        changed = False
        for lh, rh in grammar.rules:
            if lh == 'E':
                import pdb
                # pdb.set_trace()
            if rh[-1] in grammar.nonterminals:
                old = follow[rh[-1]].copy()
                follow[rh[-1]].update(follow[lh])
                if old != follow[rh[-1]]:
                    changed = True
            if len(rh) > 1:
                i = -2
                print(rh)
                while rh[i] not in grammar.nonterminals and i >= - len(rh):
                    i-=1
                if i >= - len(rh):
                    old = follow[rh[i]].copy()
                    fb = cross_first(first, *rh[i+1:])
                    follow[rh[i]].update(fb.difference({''}))
                    if '' in fb:
                        follow[rh[i]].update(follow[lh])
                    if old != follow[rh[i]]:
                        changed = True

    return follow

def analyze_grammar(grammar):
    item_sets = [expand_item_set({(grammar.start+"'",
                                 ('..', grammar.start))}, grammar)]

    follow_set = make_follow_set(grammar)
    print(follow_set)
    transitions = {}
    new_items = item_sets[:]
    while len(new_items) > 0:
        it_s = new_items.pop(0)
        moves = {}
        for it in it_s:
            mv, n_s = move_dot(it)
            if mv != None:
                if mv not in moves:
                    moves[mv] = set()
                moves[mv].update(expand_item_set({n_s}, grammar))
        for mv in moves:
            if moves[mv] not in item_sets:
                new_items.append(moves[mv])
                item_sets.append(moves[mv])
            add_transition(transitions, item_sets.index(it_s), mv, item_sets.index(moves[mv]))

    for i, item in enumerate(item_sets):
        if (grammar.start+"'", (grammar.start, '..')) in item:
            add_transition(transitions, i, '$', 'acc')
    pprint.pprint(transitions)

    return item_sets



gr_file = open(sys.argv[1], "rb")
parsed_grammar = parse_grammar(gr_file.readlines())

print(parsed_grammar)
pprint.pprint(make_first_set(parsed_grammar))
pprint.pprint(make_follow_set(parsed_grammar))
# analyzed_grammar = analyze_grammar(parsed_grammar)

# pprint.pprint(analyzed_grammar)

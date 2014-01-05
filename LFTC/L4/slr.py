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
        raise "Conflict shift/reduce"
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
    follow = {x:set() for x in grammar.nonterminals.union(grammar.terminals)}
    follow[grammar.start+"'"] = '$'

    first = make_first_set(grammar)

    changed = True
    while changed:
        changed = False
        for lh, rh in grammar.rules:
            if lh == 'E':
                import pdb
                # pdb.set_trace()
            for i in range(len(rh) -1):
                    old = follow[rh[i]].copy()
                    fb = cross_first(first, *rh[i+1:])
                    follow[rh[i]].update(fb.difference({''}))
                    if '' in fb:
                        follow[rh[i]].update(follow[lh])
                    if old != follow[rh[i]]:
                        changed = True
            if rh[-1] in grammar.nonterminals:
                old = follow[rh[-1]].copy()
                follow[rh[-1]].update(follow[lh])
                if old != follow[rh[-1]]:
                    changed = True

    return follow


def has_end(item, grammar):
    res = []
    for it in item:
        if it[1][-1] == '..':
            rule = (it[0], it[1][:-1])
            res.append(grammar.rules.index(rule))
    if len(res) > 1:
        pprint.pprint(item)
        print(res)
        for r in res:
            print(grammar.rules[r])
        print("Conflict reduce/reduce!")
        exit()
    return res[0] if len(res) else None

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

    for i, it in enumerate(item_sets):
        print(i)
        pprint.pprint(it, depth=4)

    for i, item in enumerate(item_sets):
        if (grammar.start+"'", (grammar.start, '..')) in item:
            add_transition(transitions, i, '$', 'acc')
        rule = has_end(item, grammar)
        if rule:
            for act in follow_set[grammar.rules[rule][0]]:
                add_transition(transitions, i, act, 'r'+str(rule))

    return transitions


def analyze_input(grammar, transitions, inp):
    stack = [0]
    try:
        inp = inp + ['$']
    except:
        inp = inp + '$'
    out_st = []
    import pdb
    # pdb.set_trace()
    while len(inp) and len(stack):
        current_state = stack[-1]
        char = "'" + inp[0] + "'" if inp[0] != '$'  else inp[0]
        if (current_state, char) not in transitions and (current_state, '') in transitions:
            char = ''
        # print(char)
        if (current_state, char) in transitions:
            nxt = transitions[(current_state, char)]
            if type(nxt) == int:
                stack.append(char)
                stack.append(nxt)
                if char != '':
                    inp = inp[1:]
            elif nxt[0] == 'r':
                rule = grammar.rules[int(nxt[1:])]
                for i in range(len(rule[1])):
                    stack.pop()
                    stack.pop()
                stack.append(rule[0])
                stack.append(transitions[(stack[-2], stack[-1])])
                out_st.append(rule)
            elif nxt == 'acc':
                if inp[0] == '$':
                    return out_st
        else:
            print("Invalid character/state combo")
            print(char, current_state)
            break
    print(stack)
    print(inp)
    print(out_st)
    print("Input not accepted!")

if __name__ == "__main__":
    gr_file = open(sys.argv[1], "rb")
    parsed_grammar = parse_grammar(gr_file.readlines())

    print(parsed_grammar)
    pprint.pprint(make_first_set(parsed_grammar))
    pprint.pprint(make_follow_set(parsed_grammar))
    transitions = analyze_grammar(parsed_grammar)

    pprint.pprint(transitions)

    if len(sys.argv) > 2:
        import lexer

        codif = lexer.codif

        f = open(sys.argv[2], "rb")
        fip, _, _ = lexer.lexer(f.read())

        print(fip)

        parsed_fip = map(lambda x: codif[x[0]], fip)
        print(parsed_fip)

        print(analyze_input(parsed_grammar, transitions, parsed_fip))

    else:
        while True:
            x = raw_input("Dati o secventa: ")
            if not x:
                break
            print(analyze_input(parsed_grammar, transitions, x))


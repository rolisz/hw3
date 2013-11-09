from pprint import pprint

__author__ = 'Roland'
import sys

def parse_automaton(descr):
    states = set()
    transitions = {}
    alphabet = set()
    finals = set()
    begin_state = ""
    for line in descr:
        line = line.strip().split()
        states.add(line[0])
        states.add(line[2])
        if len(line[1]) == 3 and line[1][1] == '-':
            begin = ord(line[1][0])
            end = ord(line[1][2])
            alphabet.update(chr(x) for x in range(begin, end + 1))
            for x in range(begin, end + 1):
                transitions[(line[0], chr(x))] = line[2]
        else:
            alphabet.add(line[1])
            transitions[(line[0], line[1])] = line[2]
        if len(line) == 4:
            if line[3] == "B":
                begin_state = line[0]
            elif line[3] == "F":
                finals.add(line[2])

    return begin_state, states, alphabet, transitions, finals

def accept(begin_state, states, alphabet, transitions, finals, string):
    current_state = begin_state
    full_string = string
    prefix = ""
    temp_match = ""
    while string:
        current_char = string[0]
        string = string[1:]
        try:
            next_state = transitions[(current_state, current_char)]
        except KeyError:
            return 0, prefix
        temp_match += current_char
        if next_state in finals:
            prefix += temp_match
            temp_match = ""

        current_state = next_state
    if current_state in finals:
        return True
    else:
        return 1, prefix


def interpret(automat, string):
    rez = accept(*automat, string=string)
    if rez == True:
        return "Secventa %s este acceptata" % string
    elif rez[0] == 0:
        return "Secventa %s nu este acceptata de acest automat finit, nu s-a putut consuma tot sirul! Prefixul " \
               "maximal consumat este: %s" % (string, rez[1])
    else:
        return "Secventa %s nu este acceptata, nu s-a ajuns intr-o stare terminala! Prefixul " \
               "maximal consumat este: %s" % (string, rez[1])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "rb")
        descr = f.readlines()
        f.close()
    else:
        descr = []
        text = raw_input("Dati automatul finit. Pentru oprire lasati linia goala: ")
        while len(text):
            descr.append(text)
            text = raw_input()

    #print(descr)
    automaton = parse_automaton(descr)
    #print(begin_state)
    #print(states)
    #print(alphabet)
    #print(finals)
    #pprint(transitions)
    #check_string = raw_input("Dati secventa de verificat: ")
    check_string = "0xA23F"
    print(interpret(automaton, string=check_string))
    print(interpret(automaton, string="123"))
    print(interpret(automaton, string="xyx"))
    print(interpret(automaton, string="01234"))
    print(interpret(automaton, string="123ll"))
    print(interpret(automaton, string="123l"))
    print(interpret(automaton, string="0x123l"))
    print(interpret(automaton, string="0x123u"))
    print(interpret(automaton, string="0x123LL"))
    print(interpret(automaton, string="0x123xL"))
    print(interpret(automaton, string="0x"))
    print(interpret(automaton, string="0"))
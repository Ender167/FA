
import re
from termcolor import colored
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None

    def __str__(self):
        return str(self.key)


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        self.rehashed = False

    def _hash(self, key):
        return hash(key) % self.capacity

    def get_key_position(self, key):
        return self._hash(key)

    def add(self, key):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key)
            #self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    return
                current = current.next
            new_node = Node(key)
            new_node.next = self.table[index]
            self.table[index] = new_node
            #self.size += 1

        self.size += 1

        loadFactor = self.computeLoadFactor()
        #print("Load factor is:" + str(loadFactor))

        if loadFactor > 0.75:
            #print("Calling rehash function, load factor=" + str(loadFactor) + ", element " + str(key))
            self.rehash()

    def lookup(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return True
            current = current.next

        return False

    def rehash(self):
        #rehashes the hash table by doubling the capacity and
        #calling the hash function again for each element

        self.rehashed = True
        self.capacity = self.capacity * 2

        copyNodes = []

        for el in self.table:
            current = el
            while current:
                copyNodes.append(current.key)
                current = current.next

        self.table.clear()
        self.table = [None] * self.capacity

        for el in copyNodes:
            self.add(el)


    def computeLoadFactor(self):
        #returns the current load factor of the hash table
        if self.size > 0:
            return self.size / self.capacity
        return 0

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.lookup(key)
            return True
        except KeyError:
            return False

class FiniteAutomata:
    def __init__(self, st= None, alph=None, init_st = None, fin_st = None):
        if alph is None:
            alph = []
        if st is None:
            st = {}
        self.states = st
        self.alphabet = alph
        self.initialState = init_st
        self.finalState = fin_st

    def addState(self, state):
        if state not in self.states:
            self.states[state] = []

    def addStateList(self, states):
        for el in states:
            self.addState(el)

    def addTransition(self, state, transition):
        if state in self.states:
            self.states[state].append(transition)


def rebuildPif(ht, pif1, number_pif1):

    new_pif = []
    new_numbered_pif = []
    if ht.rehashed:
        for i in range(0, len(pif1)):
            a1, b1 = pif1[i]
            a2, b2 = number_pif1[i]

            new_a = a1
            new_b = b1

            new_a2 = a2

            if b1 != -1:
                new_b = ht.get_key_position(a1)
            new_pif.append((new_a, new_b))
            new_numbered_pif.append((new_a2, new_b))

        ht.rehashed = False
    return new_pif, new_numbered_pif

def runScanner(fa):
    ht = HashTable(100)
    program = open("p1err.kami.txt")
    tokens_raw = open("token.in.txt")
    pif_file = open("PIF.out.txt", "w")
    st_file = open("ST.out.txt", "w")

    token_list = []

    token_lines = tokens_raw.readlines()
    for i in token_lines:
        i = i.replace('\n', '')
        token_list.append(i)

    separators = token_list[0:6]
    operators = token_list[6:19]
    types = token_list[19:23]
    tokens = token_list[23: 33]
    bool_values = token_list[33:len(token_list)]

    program_lines = program.readlines()

    declared_variables_list = []
    line_number = 0
    lexical_errors_list = []
    pif = []
    number_pif = []

    for i in program_lines:
        token = ""
        beginning_reserved_word = ""
        line_number += 1
        if len(i) > 1:
            for c in range(len(i)):
                if i[c] in separators or (i[c] in operators and c+1 < len(i) and i[c+1] not in operators)\
                         or i[c] == '\n' or (i[c] == ' ' and len(token) >= 1 and token[0] != '"') or\
                        (c+1 < len(i) and i[c+1] == ' ' and len(token) >= 1 and token[0] != '"'):

                    if i[c] != ' ' and i[c] not in separators and i[c] != '\n' and i[c] not in operators\
                                and len(token) >= 0 and token[0] != '"':
                        token += i[c]

                    if len(token) <= 1 and i[c] in operators:
                        token += i[c]

                    if len(token) >= 1 and token[0] != '"':
                        token = token.replace('\n', '')

                    if i[c] == ' ' and len(token) >= 1 and token[0] == '"':
                        token += i[c]

                    if token != ' ' and token != '\n' and token != '':
                        if token in types:
                            #print('Correct type: ' + token)
                            numeric_token = token_list.index(token)
                            #print(numeric_token)
                            pif.append((token, -1))
                            number_pif.append((numeric_token, -1))

                        elif token in operators:
                            #print('Correct operator: ' + token)
                            numeric_token = token_list.index(token)
                            #print(numeric_token)
                            pif.append((token, -1))
                            number_pif.append((numeric_token, -1))

                        elif token in tokens:
                            numeric_token = token_list.index(token)
                            #print(numeric_token)
                            #print('Correct reserved word: ' + token)
                            pif.append((token, -1))
                            number_pif.append((numeric_token, -1))

                        elif validateFA(fa, beginning_reserved_word + " " + token):
                            print("Found token + identifier by FA: " + beginning_reserved_word + " " + token)
                            numeric_token = -2
                            #print(numeric_token)
                            if token not in declared_variables_list:
                                declared_variables_list.append(token)
                            if not ht.lookup(token):
                                ht.add(token)
                            if ht.lookup(token):
                                number_pif.append((numeric_token, ht.get_key_position(token)))
                                pif.append((token, ht.get_key_position(token)))

                        #case if identifier has no token
                        elif (token in declared_variables_list) and not token.isnumeric():
                            #print('Correct identifier: ' + token)
                            numeric_token = -2
                            #print(numeric_token)
                            if token not in declared_variables_list:
                                declared_variables_list.append(token)
                            if not ht.lookup(token):
                                ht.add(token)
                            if ht.lookup(token):
                                number_pif.append((numeric_token, ht.get_key_position(token)))
                                pif.append((token, ht.get_key_position(token)))

                        elif validateFA(fa, token):
                            #print("Found integer constant by FA: " + token)
                            numeric_token = -3
                            if not ht.lookup(token):
                                ht.add(token)
                            if ht.lookup(token):
                                number_pif.append((numeric_token, ht.get_key_position(token)))
                                pif.append((token, ht.get_key_position(token)))

                        elif (token[0] == '"' and token[len(token) - 1] == '"') or token in bool_values: #For other constants
                            #print('Correct constant: ' + token)
                            numeric_token = -3
                            if not ht.lookup(token):
                                ht.add(token)
                            if ht.lookup(token):
                                number_pif.append((numeric_token, ht.get_key_position(token)))
                                pif.append((token, ht.get_key_position(token)))
                        else:
                            lexical_errors_list.append("Incorrect: " + token + " at line " + str(line_number))

                    if len(token) >= 0:
                        if i[c] in operators:
                            numeric_token = token_list.index(i[c])
                            #print('Correct operator: ' + i[c])
                            pif.append((i[c], -1))
                            number_pif.append((numeric_token, -1))
                        if i[c] in separators:
                            numeric_token = token_list.index(i[c])
                            #print('Correct separator: ' + i[c])
                            pif.append((i[c], -1))
                            number_pif.append((numeric_token, -1))

                    if beginning_reserved_word == "":
                        beginning_reserved_word = token

                    token = ""
                else:
                    if i[c] != ' ':
                        token += i[c]
                    if i[c] == ' ' and len(token) >= 1 and token[0] == '"':
                        token += i[c]



        ''' 
        declaration_singleVariables = re.findall("(^[ ]*(?:int|bool|string)+ (?:[a-zA-Z]+[0-9]*[,]*[ ]*)+;)", i)
        declaration_arrays = ["".join(x) for x in re.findall("(^[ ]*int\[[0-9]+\] [a-zA-Z]+[0-9]*;)|(^[ ]*bool\[[0-9]+\] [a-zA-Z]+[0-9]*;)", i)]
        stmt_if = re.findall("(^[ ]*cond[ ]*\([ ]*[a-zA-Z]+[0-9]*[ ]*[+\-%]*[ ]*[a-zA-Z]+[0-9]*[ ]*(<|>|==|<=|>=)[ ]*[a-zA-Z]*[0-9]*[ ]*\)[ ]*do[ ]*)", i)

        #declaration_singleVariables = re.search("(^[ ]*((int)|(bool)|(string))+ ([a-zA-Z]+[0-9]*[,]*[ ]*)+;)", i)
        #|(^[ ]*string [a-zA-Z]+[0-9]*;)|(^[ ]*bool [a-zA-Z]+[0-9]*;)|(^[ ]*char [a-zA-Z]+[0-9]*;)

        if len(declaration_arrays) > 0:
            print(declaration_arrays)

        if len(declaration_singleVariables) > 0:
            print(declaration_singleVariables)

        if len(stmt_if) > 0:
            print(stmt_if)
        '''

    print()

    print("Lexical errors")
    if len(lexical_errors_list) > 0:
        for elem in lexical_errors_list:
            print(elem)
    else:
        print("lexically correct")

    print()

    if ht.rehashed:
        print("Rebuilding pif")
        pif, number_pif = rebuildPif(ht, pif, number_pif)

    print("PIF")
    for a, b in number_pif:
        pif_txt = str(a) + " " + str(b) + '\n'
        pif_file.write(pif_txt)
        print(pif_txt)

    print()

    print("Symbol table")
    st_file.write("Hash Table capacity " + str(ht.capacity) + " size " + str(ht.size) + '\n')
    for el in ht.table:
        current = el
        while current:
            st_txt = str(ht.get_key_position(current.key)) + " " + str(current) + '\n'
            st_file.write(st_txt)
            print(st_txt)
            current = current.next


def readFa():
    fa = open("FA.in")
    fa_lines = fa.readlines()
    states = []
    alphabet = []
    initial = []
    final = []
    transitions = []
    for i in fa_lines:
        newRow = i.split()
        if len(newRow) > 0:
            if newRow[0] == "states":
                for e in range(1, len(newRow)):
                    states.append(newRow[e])

            if newRow[0] == "alphabet":
                for e in range(1, len(newRow)):
                    alphabet.append(newRow[e])

            if newRow[0] == "initial":
                for e in range(1, len(newRow)):
                    initial.append(newRow[e])

            if newRow[0] == "final":
                for e in range(1, len(newRow)):
                    final.append(newRow[e])

            if newRow[0] in states:
                transitions.append(newRow)

    fa = FiniteAutomata()
    for el in states:
        fa.addState(el)
    for el in transitions:
        if el[1] == '@':
            el[1] = ' '
        fa.addTransition(el[0], [el[1], el[2]])
    fa.alphabet = alphabet
    fa.initialState = initial
    fa.finalState = final

    return fa

def validateFA(fa, validate):
    current_state = fa.initialState[0]
    path = []
    found = False
    path.append(current_state)
    for c in validate:
        found = False
        current_transitions = fa.states[current_state]
        for transition in current_transitions:
            if transition[0] == c:
                current_state = transition[1]
                found = True
                break
        if found:
            path.append(current_state)
        if not found:
            break
    print(path)
    return found

def main():
    fa = readFa()

    print("States")
    print(fa.states)
    print("Alphabet")
    print(fa.alphabet)
    print("Initial")
    print(fa.initialState)
    print("Final")
    print(fa.finalState)
    print("Transitions")

    for e in fa.states:
        print(e)
        for el in fa.states[e]:
            print(el)

    runScanner(fa)



if __name__ == '__main__':
    main()














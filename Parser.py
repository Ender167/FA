class Parser:
    def __init__(self, s,i,w_st,in_st,gr,w):
        self.state=s
        self.position=i             #position of current symbol in input sequence
        self.working_stack=w_st
        self.input_stack= in_st
        self.grammar=gr
        self.sequence=w

    def advance(self):
        self.position += 1
        terminal = self.input_stack.pop()
        self.working_stack.append(terminal)

    def momentary_insuccess(self):
        self.state = 'b'

    def expand(self):
        prod = self.input_stack.pop()

        non_terminal = ""
        prod_nr = -1
        found = False
        for el in self.grammar.productions:
            i = 1
            for e in self.grammar.productions[el]:
                if e == prod:
                    non_terminal = el
                    prod_nr = i
                    found = True
                    break
                i = i + 1
            if found:
                break

        self.working_stack.append((non_terminal, prod_nr))
        for i in range(len(self.grammar.productions[non_terminal]) - 1):
            self.input_stack.pop()

        self.input_stack.append(self.grammar.productions[non_terminal][0][::-1])



    def back(self):
        self.position -= 1
        terminal = self.working_stack.pop()
        self.input_stack.append(terminal)

    def another_try(self):
        pair = self.working_stack.pop()
        non_terminal = pair[0]
        prod_nr = pair[1]
        index = prod_nr-1                                            #indexu in lista incepe de la 0 deci prod_nr-1
        if prod_nr < len(self.grammar.productions[non_terminal]):    #exista productie deci o folosim pe aia
            self.state = 'q'
            self.working_stack.append((non_terminal,prod_nr+1))
            for i in range(len(self.grammar.productions[non_terminal][index])):                     #scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i]==self.input_stack[len(self.input_stack)-1]:  #ifu nu ii necesar e just in case
                    self.input_stack.pop()
            for i in range(len(self.grammar.productions[non_terminal][index+1])-1, -1, -1):           #si o punem pe aia noua in ordine inversa
                self.input_stack.append(self.grammar.productions[non_terminal][index+1][i])
        elif self.position==1 and self.grammar.starting_point==non_terminal:
            for i in range(
                    len(self.grammar.productions[non_terminal][index])):                            # scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i] == self.input_stack[len(self.input_stack) - 1]:  #ifu nu ii necesar e just in case
                    self.input_stack.pop()
            self.state = 'e'
        else:
            for i in range(len(self.grammar.productions[non_terminal][index])):                     #scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i]==self.input_stack[len(self.input_stack)-1]:
                    self.input_stack.pop()
            self.input_stack.append(non_terminal)                                                   #si adaugam non terminalu

    def succes(self):
        self.state = 'f'

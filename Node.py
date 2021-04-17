from re import split, search

class Token:
    word = ""
    id = None
    # ongoing list of keyword and characters needed to be recognized from java
    # typeSpecs = ["int", "float", "double", "boolean", "String", "char"]
    # operators = ['+', '-', '*', '/', '%']
    # comparison = ['==', '<=', '>=', '!=', '!']
    # tryStatements = ["try", "catch", "finally"]
    # logic = ["true", "false"]
    # modifiers = ["public", "static", "private", "protected", "final", "abstract", "native"]

    def __init__(self, word, id=None):
        self.word = word
        self.id = id


class Node:
    def __init__(self, line = ""):
        # token placeholder
        self.line = line
        self.tokens = []
        self.indent = False
        self.tokenizeLine(line)
        # self.identifier = identifier

    splitters = ["--","++","+=","-=","*=","/=","%=",">>=",">>>","<<",">>","<=",">=","==","!=","&=","&&","||=","|=","^="]

    def tokenizeLine(self, inLine):
        # self.nextBlock = None
        # if 'System.out.print' in self.line:
        #     self.print_split(self.line)
        # elif '\"' in self.line:
        #     self.string_split(self.line)
        # else:
        #     tklist = self.line.split()
        #     for x in tklist:
        #         # if tklist[0] == "//":
        #         #     temptk = Token(" ".join(tklist[1:len(tklist)]), "comment")
        #         #     self.tokens.append(temptk)
        #         #     break
        #         # else:
        #         temptk = Token(x)
        #         self.tokens.append(temptk)
        if "System.out.print" in inLine:
            self.print_split(inLine)
        elif "\"" in inLine:
            self.string_split(inLine)
        elif "\'" in inLine:
            self.char_split(inLine)
        elif any(c.isdigit() for c in inLine):
            self.num_split(inLine)
        elif any(splitter in inLine for splitter in self.splitters):
            self.splitter_split(inLine)
        else:
            self.line_split(inLine)

    def print_split(self, strn):
        start = 0
        index = strn.find('System.out.println', start)
        length = len('System.out.println')
        line1 = strn
        line2 = ""
        if index == -1:
            index = strn.find('System.out.print', start)
            length = len('System.out.print')
        if index != -1:
            start = index
            line1 = strn[0:start]
            line2 = strn[index+length:]

        if len(line1) > 0:
            self.tokenizeLine(line1)

        temptk = Token("print", "print")
        self.tokens.append(temptk)

        if len(line2) > 0:
            self.tokenizeLine(line2)

    def string_split(self, strn):
        start = 0
        index = strn.find('\"')
        line1 = strn
        line2 = ""
        if index != -1:
            start = index+1
            index = strn.find('\"', start)
            # if index == -1:
            #     print("ERROR")
            #     exit

            line1 = strn[0:start-1]
            line2 = strn[index+1:]

        if len(line1) > 0:
            self.tokenizeLine(line1)

        temptk = Token(strn[start:index], "string")
        self.tokens.append(temptk)

        if len(line2) > 0:
            self.tokenizeLine(line2)

    def char_split(self, strn):
        start = 0
        index = strn.find('\'')
        line1 = strn
        line2 = ""
        if index != -1:
            start = index+1
            index = strn.find('\'', start)
            # if index == -1 or index - start != 2:
            #     print("ERROR")
            #     exit

            line1 = strn[0:start-1]
            line2 = strn[index+1:]

        if len(line1) > 0:
            self.tokenizeLine(line1)

        temptk = Token(strn[start:index], "char")
        self.tokens.append(temptk)

        if len(line2) > 0:
            self.tokenizeLine(line2)

    def num_split(self, strn):
        start = 0
        num = search('\d*\.?\d+', strn)
        index = num.span()[0]
        line1 = strn
        line2 = ""
        print(line1, line2)
        if index != -1:
            start = index
            index = index + len(num.group())

            line1 = strn[0:start]
            line2 = strn[index:]

        print(line1, line2)

        print()
        if len(line1) > 0:
            self.tokenizeLine(line1)

        temptk = Token(strn[start:index], "num")
        self.tokens.append(temptk)

        if len(line2) > 0:
            self.tokenizeLine(line2)

    def splitter_split(self, strn):
        for splitter in self.splitters:
            index = strn.find(splitter)
            if index != -1:
                line1 = strn[:index]
                line2 = strn[index + 2:]

                if len(line1) > 0:
                    self.tokenizeLine(line1)

                temptk = Token(strn[index:index + 2])
                self.tokens.append(temptk)

                if len(line2) > 0:
                    self.tokenizeLine(line2)

    def line_split(self, strn):
        tokArr = split('(\W)', strn)
        for s in tokArr:
            if not s.isspace() and len(s) > 0:
                self.tokens.append(Token(s))

    def toString(self):
        ret = ""
        for token in self.tokens:
            ret+=token.word
            ret+="\n"
        return ret

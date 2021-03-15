class Token:
    word = ""
    id = None
    # ongoing list of keyword and characters needed to be recognized from java
    typeSpecs = ["int", "float", "double", "boolean", "String", "char"]
    operators = ['+', '-', '*', '/', '%']
    comparison = ['==', '<=', '>=', '!=', '!']
    tryStatements = ["try", "catch", "finally"]
    logic = ["true", "false"]
    modifiers = ["public", "static", "private", "protected", "final", "abstract", "native"]

    def __init__(self, word, id=None):
        self.word = word
        self.id = id
        if id is None:
            self.identify()

    def identify(self):
        if self.word == 'import':
            self.id = "import_statement"
        if self.word == '{':
            self.id = "start_indent"
        elif self.word == "/*":
            self.id = "start_comment"
        elif self.word == "*/":
            self.id == "end_comment"
        elif self.word == '}':
            self.id = "end_indent"
        elif self.word == "class":
            self.id = "class_declaration"
        elif self.word == "void":
            self.id = "void"
        elif self.word in self.typeSpecs:
            self.id = "type_specifier"
        elif self.word in self.modifiers:
            self.id = "modifier"
        elif self.word in self.tryStatements:
            self.id = "try_statement"
        elif self.word in self.logic:
            self.id = "logical_expression"
        elif self.word in self.operators:
            self.id = "operator"
        elif self.word in self.comparison:
            self.id = "comparison_operator"

        # list of if statements? make list of arrays to compare to


class Node:
    def __init__(self, line):
        # token placeholder
        self.line = line
        self.tokens = []
        self.indent = False
        self.tokenizeLine()
        # self.identifier = identifier

    def tokenizeLine(self):
        # self.nextBlock = None
        if '\"' in self.line:
            self.string_split(self.line)
        else:
            tklist = self.line.split()
            for x in tklist:
                # if tklist[0] == "//":
                #     temptk = Token(" ".join(tklist[1:len(tklist)]), "comment")
                #     self.tokens.append(temptk)
                #     break
                # else:
                temptk = Token(x)
                self.tokens.append(temptk)

    def string_split(self, strn):
        start = 0
        index = strn.find('\"', start)
        strToken = []
        line1 = strn
        line2 = ""
        if index != -1:
            start = index+1
            index = strn.find('\"', start)
            if index == -1:
                print("ERROR")
                exit

            line1 = strn[0:start-1]
            line2 = strn[index+1:]

        line1 = line1.split()
        line2 = line2.split()

        for t in line1:
            temptk = Token(t)
            self.tokens.append(temptk)

        temptk = Token(strn[start:index], "string")
        self.tokens.append(temptk)

        for t in line2:
            temptk = Token(t)
            self.tokens.append(temptk)

    def toString(self):
        ret = ""
        for token in self.tokens:
            ret+=token.word
            ret+="\n"
        return ret

from Node import *

class Scanner:
    # could turn java file into txt file and remove indents
    infile = None
    lineCount = 0
    bracketCount = 0
    progNodes = []
    current = None

    # prepares java file for parser by creating tokens
    def prepFile(self, f):
        self.infile = open(f, "r+")
        self.lineCount = len(self.infile.readlines())
        self.infile.seek(0)
        self.scanLines()
        # print(inputFile.readLine())

    # used by prep file to scan lines from file
    def scanLines(self):
        pos = 0
        while (pos < self.lineCount):
            # might remove
            tempLine = self.infile.readline()
            if tempLine.find("//") != -1:
                self.addComment(tempLine)
            elif tempLine.find("/*") != -1:
                while tempLine.find("*/") != -1 and pos < self.lineCount:
                    self.addComment(tempLine)
                    tempLine = self.infile.readline()
                    pos += 1
            else:
                self.addLine(tempLine)
            pos += 1

            """
            if self.progNodes.len() != 0:

            if tempLine.find("{") != -1 and tempLine.find('"') == -1:
                self.addLine(tempLine.find("//"), "comment")
            #checks if there is a comment present, but only if the "//" is found outside of quotes
            if tempLine.find("//") != -1 and (tempLine.index("//") == 0 or tempLine[tempLine.index("//") - 1] != '"'):
                self.addLine(tempLine.find("//"), "comment")
            elif tempLine.find('class') != -1:
                #passes just the word following class
                self.addLine(tempLine[tempLine.find('class') + 6:tempLine.find('{')], 'class')
            elif tempLine.find("if(") or tempLine.find("if (") or tempLine.find("while(") or tempLine.find("while (") != -1:
                self.addLine(tempLine, "conditional")

            else:
                self.addLine(tempLine, "statement")
            """

    # used by prepfile
    def addLine(self, line):
        tempN = Node(line)
        if len(tempN.tokens) != 0:
            self.progNodes.append(tempN)

    def addComment(self, line):
        index = line.find("//")
        comLine = ""
        if index != -1:
            comLine = line[:index] + line[index+2:]
        index = line.find("/*")
        if index != -1:
            comLine = line[:index] + line[index+2:]
        index = line.find("*/")
        if index != -1:
            comLine = line[:index] + line[index+2:]

        node = Node()
        node.tokens = [Token(comLine, "comment")]

        self.progNodes.append(node)

    def showLine(self, num):
        print(len(self.progNodes))
        temp = self.progNodes[num]
        for x in temp.tokens:
            print(str(x.word) + ", " + str(x.id))
    # def scanBlock(self):


# tem = test.progNodes[0].tokens
# print(str(tem[0].word))
# print(len(test.progNodes))
# test.showLine(0)
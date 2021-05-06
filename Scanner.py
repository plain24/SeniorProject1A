from Node import *


class Scanner:
    def __init__(self):
        self.infile = None
        self.lineCount = 0
        self.bracketCount = 0
        self.progNodes = []
        self.current = None

    # prepares java file for parser by creating tokens
    def prepFile(self, f):
        self.infile = open(f, "r+")
        self.lineCount = len(self.infile.readlines())
        self.infile.seek(0)
        self.scanLines()
        self.infile.close()
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


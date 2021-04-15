from Parser import *
from pprint import pprint
'''class Node:
    data = ''
    def __init__(self,data):
        self.children = None
        self.data = data'''
class Translator:
    # get tree from main function of parser, it returns the tree
    def __init__(self, tree):
        self.jTree = tree
        self.pFile = open("output_file.txt", "w")
        self.pFile.write("Translator")

    # text file to output python code to
    def readTree(self):
        # reads the tree and figures out what each line is
        # sets current node to 'compilation_unit'
        # rootNode = self.jTree
        # outer for loop runs based on the length of children from compilation, inner loop iterates through the children of each node
        # could use recursive or non-recursive method to iterate through children outside of this method in analyeNode
        self.analyzeNode(self.jTree, 0)
        self.pFile.close()

    def handleStatement(self,currentNode, indent):
        cond = None
        space = '   ' * indent
        if(currentNode.children is not None):
            for n in currentNode.children:
                if n.data == 'expression':
                    self.handleExpression(n, indent)
                if n.data == 'statement':
                    for a in n.children:
                        self.handleStatement(a, indent)
                if n.data == 'statement_block':
                    if n.children[0] == 'statement':
                        self.handleStatement(n.children[0], indent)
                if n.data == 'comment' and n.children is not None:
                    '''self.pFile.write(space + '#')
                    for b in n.children:
                        self.pFile.write(' ' + b.data)
                    self.pFile.write('\n')'''
                    print("Line 43", n.data)
                    self.analyzeNode(n, indent)
                elif n.data == 'if_statement':
                    cond = 'if'
                    self.pFile.write(space + 'if ')
                    for x in n.children:
                        if x.data == 'expression':
                            self.handleExpression(x, indent)
                            self.pFile.write(':\n')
                        else:
                            self.handleStatement(x, indent)
                elif n.data == 'while_statement' :
                    cond = 'while'
                    self.pFile.write('while ')
                   # self.handleStatement(indent, 'while')
                elif n.data == 'for_statement':
                    cond = 'for'
                    self.pFile.write('for ')
                    #self.handleStatement(indent, 'for')
                elif currentNode.data == 'try_statement':
                    cond = 'try'
                    self.pFile.write('try: \n')
                elif currentNode.data == 'catch':
                    cond = 'catch'
                    self.pFile.write('except: \n')
               # self.handleStatement(indent, 'catch')
                if n.data == 'variable_declaration':
                    for a in n.children:
                        x = a
                        '''if a.data == 'type':
                            while x.children is not None:
                                x = a.children[0]
                            store = x.data
                            self.pFile.write(x.data + ' ')'''
                        if a.data == 'variable_declarators':
                            #set to variable_declarator
                            x = a.children[0]
                            if x.children[0].data == 'identifier':
                                x = x.children[0]
                                self.pFile.write(x.children[0].data)

                            x = a.children[0]
                            if x.children[2].data == 'variable_initalizer' and x.children[2].children is not None:
                                self.handleExpression(x.children[2].children[0], indent)
                if n.data == 'expression':
                    self.handleExpression(n, indent)
                elif n.data == 'statement':
                    self.handleStatement(n, indent)

               #if elseFlag
               #indent = indent - 1'''


    def handleExpression(self, currentNode, indent):
        r = currentNode
        space = '   ' * indent
        if currentNode != None:
            if currentNode.data == 'expression' and len(currentNode.children) > 0:
                    self.handleExpression(currentNode.children[0], indent)

            if currentNode.data == 'logical_expression' and currentNode.children is not None:
                for n in currentNode.children:
                    if n.data == 'true':
                        self.pFile.write('True')
                    elif n.data == 'false':
                        self.pFile.write('False')
                    elif n.data == '&&':
                        self.pFile.write(' and ')
                    elif n.data in ('||', '| |'):
                        self.pFile.write(' or ')
                    elif n.data in (  '|=', '==', '>' ,'<',  '>=', '<=' ):
                        self.pFile.write(n.data)
                    elif n.data == 'expression':
                        self.handleExpression(n, indent)

            if currentNode.data == 'identifier_expression' and currentNode.children is not None:
                # while r.children is not None and r is not None:
                #     print(r.data)

                r = r.children[0].children[0]

                if r.data in ('System.out.println', 'System.out.print'):
                    self.pFile.write(space + 'print')
                else:
                    self.pFile.write(r.data)
            if currentNode.data == 'method_expression' and currentNode.children is not None:
                self.handleExpression(currentNode.children[0], indent)
                temp = currentNode.children[1]
                if temp.data == 'arglist' and temp.children is not None:
                    self.pFile.write('(')
                    for n in temp.children:
                        self.handleExpression(n, indent)
                    self.pFile.write(')\n')

            #in progress
            if currentNode.data == 'dot_expression' and currentNode.children is not None:
                    self.pFile.write(space)
                    for n in currentNode.children:
                        if n.data == '.':
                            self.pFile.write('.')
                        elif n.data == 'expression':
                            self.handleExpression(n,indent)
                        #while temp.children is not None:

            if currentNode.data == 'literal_expression' and currentNode.children is not None:
                quotes = False
                r = r.children[0]
                if r.data in ('string', 'character') and r.children[0] is not None:
                    self.pFile.write('\'' + r.children[0].data + '\'')
                else:
                    self.pFile.write(r.children[0].data)
            if currentNode.data == 'numeric_expression' and currentNode.children is not None:
                #self.pFile.write('(')
                for n in r.children:
                    if n.data in (  "+", "+=", "-", "-=",  "*",  "*=", "/", "/=", "%", "%=", "++", "--" ):
                        self.pFile.write(n.data)
                    else:
                        self.handleExpression(n, indent)
                #self.pFile.write(')')

            if currentNode.data == 'creating_expression' and currentNode.children is not None:
                n = currentNode
                arglist = None

                if n[1].children is not None:
                    arglist = n[1].children
                # get class name from last node
                while n.children is not None:
                    n = n.children[0]


                self.pFile.write(n.data + ' ')
    def analyzeNode(self, currentNode, indent):
        space = '   ' * indent
        # uses if statements to analye data from each node. Uses the analyeNode recursively for data that is known to have multiple children
        # goal is to eliminate repetiveness that will come with trying to identify everything
        if currentNode is not None:

            # print(currentNode.data)
            if currentNode.data == 'package_statement' and currentNode.children[0] is not None:
                self.pFile.write('#package: ' + currentNode.children[0].data + '\n')
            elif currentNode.data == 'expression':
                self.handleExpression(currentNode, indent)
            elif currentNode.data == 'import_statement' and currentNode.children is not None:
                for n in currentNode.children:
                    if n is not None:
                        self.pFile.write('import ' + n.data + '\n')

            elif currentNode.data == 'method_declaration' and currentNode.children is not None:

                for n in currentNode.children:
                    temp = n
                    if n.data == 'type':
                        c = n.children[0]
                        self.pFile.write(space + '#type: ' + c.children[0].data + '\n')
                    if n.data == 'identifier':
                            self.pFile.write(space + 'def ' + n.children[0].data  + '(self')

                    if n.data == 'parameter_list' and n.children is not None:
                        #equals 'parameters' expecting child list of params
                        temp = temp.children[0]
                        param_list = []

                        for i in temp.children:
                            temp2 = i.children[1]

                            if temp2.data == 'identifier' and temp2.children is not None:
                                param_list.append(temp2.children[0].data)
                        if len(param_list) == 0:
                            self.pFile.write('):\n')
                        else:
                            self.pFile.write(', '+ ', '.join(param_list)+'):\n')
                    if n.data == 'parameter':
                        if n.children[0] is None:
                            self.pFile.write('):\n')

                    if n.data == 'statement_block':
                        for a in n.children:
                            print("Line 221", a)
                            self.analyzeNode(a, indent + 1)
                self.pFile.write('\n')
            elif currentNode.data == 'comment' and len(currentNode.children) > 0:

                self.pFile.write(space + '#')
                for n in currentNode.children:
                     self.pFile.write(' ' + n.data)
                self.pFile.write('\n')
            elif currentNode.data == 'statement' and currentNode.children is not None:
                self.handleStatement(currentNode, indent)
            elif currentNode.data in ('type_declaration', 'field_declaration', 'declaration',
                                    'compilation_unit') and currentNode.children is not None:
                for n in currentNode.children:
                    print("Line 235", n)
                    self.analyzeNode(n, indent)
            elif currentNode.data == 'class_declaration' and currentNode.children is not None:
                for n in currentNode.children:
                    if n.data == 'identifier':
                        self.pFile.write('class ' + n.children[0].data + ': \n')
                    if n.data == 'contents':
                        for a in n.children:
                            print("Line 243", n)
                            self.analyzeNode(a, indent + 1)
        else:
            self.pFile.write("none")

#mini tests; eventually would need to test shaws entire tree output but testing little by little to make sure everything works first
'''tree = Node('compilation_unit')
#recursion working as intended for compilation_unit, can replace this with any other from the relevant if statement in analyenode
node1 = Node('expression')
node2 = Node('identifier_expression')
node3 = Node('identifier')
node4 = Node('System.out.println')
node3.children = [node4]
node2.children = [node3]
node1.children = [node2]
tree.children = [node1]'''

#t = Scanner()
#t.prepFile("java.txt")
# p = getNode()
# #p.children[2].children = None
# print(p.toString())
# test = Translator(p)
# test.readTree()
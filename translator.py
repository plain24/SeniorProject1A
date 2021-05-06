from Parser import *

class Translator:
    # get tree from main function of parser, it returns the tree

    def __init__(self, tree):
        self.jTree = tree
        self.elseif = False
        self.pFile = None
        # CHANGED
        self.currentClass = ""
        self.mainClass = ""
        self.dot = False
        self.needStr = False
    # text file to output python code to


    def readTree(self):
        # reads the tree and figures out what each line is
        # sets current node to 'compilation_unit'
        self.pFile = open("output_file.txt", "w")
        rootNode = self.jTree
        # outer for loop runs based on the length of children from compilation, inner loop iterates through the children of each node
        # could use recursive or non-recursive method to iterate through children outside of this method in analyeNode
        self.analyzeNode(rootNode, 0)
        # CHANGED
        if self.mainClass != "":
            self.pFile.write("m = " + self.mainClass + '()\n')
            self.pFile.write(self.mainClass + ".main(m, None)")
        self.pFile.close()
    def handleSwitch(self, var, currentNode, indent):
        space = '      ' * indent

        if currentNode.data == 'cases':
            for i in currentNode.children:
                x = i.children[0]
                while len(x.children) > 0:
                    x = x.children[0]
                if isinstance(var, str):
                    if i is currentNode.children[0]:
                        self.pFile.write(space + "if "+ var + ' == ' + x.data + ':\n')
                    else:
                        self.pFile.write(space + "elif " + var + ' == ' + x.data + ':\n')
                else:
                    if i is currentNode.children[0]:
                        self.pFile.write(space + "if ")
                        self.handleExpression(var, indent)
                        self.pFile.write(' == ' + x.data + ':\n')
                    else:
                        self.pFile.write(space + "elif ")
                        self.handleExpression(var, indent)
                        self.pFile.write(' == ' + x.data + ':\n')
                x = i.children[1]
                for a in x.children:
                   self.handleStatement(a, indent + 1)

    def handleStatement(self,currentNode, indent):
        space = '      ' * indent
        if len(currentNode.children) > 0:
            for n in currentNode.children:
                if n.data == 'expression':
                    self.handleExpression(n, indent)
                if n.data == 'statement':
                    for a in n.children:
                        self.handleStatement(a, indent)
                if n.data == 'switch_statement':
                    x = n.children[0]
                    if x.data == 'expression':
                        self.handleSwitch(x , n.children[1], indent)
                    else:
                        while len(x.children) > 0:
                            x = x.children[0]
                        self.handleSwitch(x.data, n.children[1], indent)
                if n.data == 'statement_block':
                    for x in n.children:
                        if x is not None and x.data == 'statement':
                            #cond = True
                            self.handleStatement(x, indent)
                if n.data == 'return':
                    self.pFile.write(space + 'return ')
                if n.data == 'comment' and len(n.children) > 0:
                    self.analyzeNode(n, indent)
                elif n.data == 'if_statement':
                    if not self.elseif:
                        self.pFile.write(space + 'if ')
                    self.elseif = False
                    for x in n.children:
                        if x.data == 'expression':
                            # old - self.handleExpression(x, indent)
                            self.handleExpression(x, 0)
                            self.pFile.write(':\n')
                        elif x.data == 'statement':
                            if x == n.children[len(n.children) - 1] and len(x.children) > 0:
                                if x.children[1].data != 'if_statement':
                                    self.pFile.write('\n' + space + 'else:\n')
                                    self.handleStatement(x, indent + 1)
                                else:
                                    self.pFile.write(space + 'elif ')
                                    self.elseif = True
                                    self.handleStatement(x, indent)
                            else:
                                self.handleStatement(x, indent + 1)


                elif n.data == 'while_statement' :
                    self.pFile.write(space + 'while ')
                    for x in n.children:
                        if x.data == 'expression':
                            # old - self.handleExpression(x , indent)
                            self.handleExpression(x, 0)
                            self.pFile.write(':\n')
                        elif x.data == 'statement':
                            self.handleStatement(x, indent + 1)
                   # self.handleStatement(indent, 'while')
                elif n.data == 'for_statement':
                    x = n.children[0].children[2].children[0]
                    #set to variable_declarator

                    for i in x.children:
                        if i.data == 'identifier':
                            self.pFile.write(space +'for ' + i.children[0].data + ' in range(')
                        if i.data =='variable_initializer':
                            self.handleExpression(i.children[0], indent)
                    self.pFile.write(',')
                    x = n.children[1].children[0]

                    if x.data == 'testing_expression':
                        x = x.children[2]
                        self.handleExpression(x, indent)

                    x = n.children[2].children[0]
                    if x.data == 'numeric_expression':
                        x = x.children[1]
                        if x.data == '++':
                            self.pFile.write(',1): \n')
                        elif x.data == '--':
                            self.pFile.write(',-1): \n')

                    x = n.children[3]
                    self.handleStatement(x, indent + 1)

                    #self.handleStatement(indent, 'for')
                elif n.data == 'try_statement':
                    self.pFile.write(space + 'try:\n ')
                    for x in n.children:
                        if x.data == 'catch':
                            self.handleExpression(x, indent)
                            self.pFile.write('catch(')
                        elif x.data == 'statement':
                            self.handleStatement(x, indent + 1)
                elif n.data == 'catch':
                    self.pFile.write('except: \n')
               # self.handleStatement(indent, 'catch')
                if n.data == 'variable_declaration':
                    returnFlag = False
                    for a in n.children:
                        x = a
                        if a.data == 'type':
                            while len(x.children) > 0:
                                x = x.children[0]
                            store = x.data
                            if x.data == 'return':
                                self.pFile.write(space + x.data + ' ')
                                returnFlag = True
                        if a.data == 'variable_declarators':
                            #self.pFile.write(space)
                            #set to variable_declarator
                            for x in a.children:
                                if x.children[0].data == 'identifier':
                                    x = x.children[0]
                                    if x.children[0].data in ('true', 'false'):
                                        self.pFile.write(x.children[0].data.capitalize())
                                    else:
                                    # old - self.pFile.write(space + x.children[0].data)
                                        if returnFlag:
                                            self.pFile.write(x.children[0].data)
                                        else:
                                            self.pFile.write(space + x.children[0].data)

                                x = a.children[0]
                                if x.children[2].data == 'variable_initializer' and len(x.children[2].children) > 0:
                                    self.pFile.write(' = ')
                                    b = x.children[2].children[0]
                                    if b.children[0].data == 'dot_expression':
                                        # old - self.handleExpression(x.children[2].children[0], indent - 2)
                                        self.handleExpression(x.children[2].children[0], 0)
                                    else:
                                        # old - self.handleExpression(x.children[2].children[0], indent)
                                        self.handleExpression(x.children[2].children[0], 0)
                                else:
                                # old - self.pFile.write(' = None')
                                    if returnFlag:
                                        pass
                                    else:
                                        self.pFile.write(' = None')
                            returnFlag = False
                            self.pFile.write('\n')


    def handleExpression(self, currentNode, indent):
        r = currentNode
        space = '      ' * indent
        if currentNode != None and len(currentNode.children) > 0:
            if currentNode.data == 'expression':
                    self.handleExpression(currentNode.children[0], indent)
            elif currentNode.data == 'comma_expression':
                for n in currentNode.children:
                    self.handleExpression(n, indent)
                    if n.data != ',' and len(currentNode.children) > 1 and n is not currentNode.children[len(currentNode.children) - 1]:
                        self.pFile.write(", ")
            elif currentNode.data == 'logical_expression':
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
            elif currentNode.data == 'print':
                self.pFile.write(space + 'print(')
                for n in currentNode.children:
                    self.needStr = True
                    self.handleExpression(n, indent)
                    if len(currentNode.children) > 1 and n is not currentNode.children[len(currentNode.children) - 1]:
                        self.pFile.write(' + ')
                self.pFile.write(')\n')
                self.needStr = False

            elif currentNode.data == 'identifier_expression':
                if len(r.children[0].children) > 0:
                    r = r.children[0].children[0]

                if r.data in ('System.out.println', 'System.out.print'):
                    self.pFile.write(space + 'print')
                else:
                    if self.needStr:
                        self.pFile.write('str(' + r.data + ')')
                    else:
                        self.pFile.write(r.data)
            elif currentNode.data == 'method_expression':
                self.handleExpression(currentNode.children[0], indent)
                temp = currentNode.children[1]
                if temp.data == 'arglist' and temp.children is not None:
                    self.pFile.write('(')
                    for n in temp.children:
                        if n is not temp.children[0]:
                            self.pFile.write(', ')
                        self.handleExpression(n, indent)
                    self.pFile.write(')\n')

            elif currentNode.data == 'dot_expression':
                self.pFile.write(space)
                self.dot = True
                for n in currentNode.children:
                    if n.data == '.':
                        self.pFile.write('.')
                    elif n.data == 'expression':
                        # old - self.handleExpression(n, indent)
                        self.handleExpression(n, 0)
                self.dot = False

                    #while temp.children is not None:

            elif currentNode.data == 'literal_expression':
                quotes = False
                r = r.children[0]
                if r.data in ('string', 'character') and r.children[0] is not None:
                    tempString = None
                    if "'" in r.children[0].data:
                        tempString = r.children[0].data.replace("'", "\\'")
                        self.pFile.write('\'' + tempString + '\'')
                    else:
                        self.pFile.write('\'' + r.children[0].data + '\'')
                else:
                    self.pFile.write(r.children[0].data)
            elif currentNode.data == 'numeric_expression':
                #self.pFile.write('(')
                for n in r.children:
                    if n.data in (  "+", "+=", "-", "-=",  "*",  "*=", "/", "/=", "%", "%=", "++", "--" ):
                        self.pFile.write(n.data)
                    else:
                        self.handleExpression(n, 0)
                #self.pFile.write(')')
            elif currentNode.data == 'creating_expression':
                n = currentNode
                c = n.children[0]
                #self.pFile.write(" = ")
                if c.data == "class_name":
                    self.pFile.write(self.handleClass_name(c))
                    self.pFile.write("(")
                    arglen = len(n.children[1].children)
                    if arglen > 0:
                        i = 0
                        for arg in n.children[1].children:
                            self.handleExpression(arg, indent)
                            i += 1
                            if i < arglen:
                                self.pFile.write(", ")
                    self.pFile.write(")")
                elif c.data == "type_specifier":
                    self.pFile.write("[")
                    if n.children[1].children[0] is not None:
                        self.handleExpression(n.children[1].children[0])
                    self.pFile.write("]")
                else:
                    pass
            elif currentNode.data == 'testing_expression':
                for n in currentNode.children:
                    if n.data in ('>',  '<',  '>=',  '<=',  '==',  '!='):
                        self.pFile.write(' ' + n.data + ' ')
                    elif n.data == 'expression':
                        self.handleExpression(n, indent)
            elif currentNode.data == 'keyword_expression':
                if currentNode.children[0].data == 'null':
                    self.pFile.write('None')
                if currentNode.children[0].data == 'this':
                    self.pFile.write('self')
            elif currentNode.data == 'assignment_expression':
                if self.dot:
                    self.pFile.write(space)
                for x in currentNode.children:
                    if x is currentNode.children[0]:
                        self.pFile.write(space)
                    # old - self.handleExpression(x, indent)
                    self.handleExpression(x, 0)
                    if x is currentNode.children[0]:
                        self.pFile.write(' = ')
                self.pFile.write('\n')
    def handleClass_name(self, node):
        out = ""
        if node.children[0].children[0] is not None:
            for pack in node.children[0].children:
                if len(pack.children) > 0:
                    out += pack.children[0].data
                else:
                    out += pack.data
        return out
    def analyzeNode(self, currentNode, indent):
        space = '      ' * indent
        # uses if statements to analye data from each node. Uses the analyeNode recursively for data that is known to have multiple children
        # goal is to eliminate repetiveness that will come with trying to identify everything
        if currentNode is not None:
            if currentNode.data == 'package_statement' and currentNode.children[0] is not None:
                self.pFile.write('#package: ' + currentNode.children[0].data + '\n')
            elif currentNode.data == 'expression' and currentNode:
                self.handleExpression(currentNode, indent)
            elif currentNode.data == 'import_statement' and len(currentNode.children) > 0:
                for n in currentNode.children:
                    if n is None:
                        return
                    self.pFile.write('import ' + n.data + '\n')

            elif currentNode.data == 'method_declaration' and len(currentNode.children) > 0:
                # CHANGED
                mname = ""
                margs = []
                for n in currentNode.children:
                    temp = n
                    if n.data == 'type':
                        c = n
                        while len(c.children)> 0:
                            c = c.children[0]
                        if c.data == self.currentClass:
                            self.pFile.write(space + 'def __init__' + '(self')
                        else:
                            # old - self.pFile.write(space + '#type: ' + c.data + '\n')
                            self.pFile.write(space + '# type: ' + c.data + '\n')
                    if n.data == 'identifier':
                        # CHANGED
                        mname = n.children[0].data
                        self.pFile.write(space + 'def ' + n.children[0].data + '(self')

                    if n.data == 'parameter_list' and len(currentNode.children) > 0:
                        #equals 'parameters' expecting child list of params
                        temp = temp.children[0]
                        param_list = []

                        for i in temp.children:
                            temp2 = i.children[1]

                            if temp2.data == 'identifier' and len(temp2.children) > 0:
                                param_list.append(temp2.children[0].data)
                        # CHANGED
                        margs = param_list
                        if len(param_list) == 0:
                            self.pFile.write('):\n')
                        else:
                            self.pFile.write(', '+ ', '.join(param_list)+'):\n')
                    if n.data == 'parameter':
                        if n.children[0] is None:
                            self.pFile.write('):\n')
                    # CHANGED
                    if mname == "main" and margs == ["args"]:
                        self.mainClass = self.currentClass

                    if n.data == 'statement_block':
                        for a in n.children:
                            self.analyzeNode(a, indent + 1)
                self.pFile.write('\n')
            elif currentNode.data == 'comment' and currentNode.children[0] is not None:
                self.pFile.write(space + '#')
                for n in currentNode.children:
                    if n is not None:
                     # old - self.pFile.write(' ' + n.data)
                     self.pFile.write(' ' + n.data.lstrip())
                #self.pFile.write('\n')
            elif currentNode.data == 'statement' and len(currentNode.children) > 0:
                self.handleStatement(currentNode, indent)
            elif currentNode.data in ('type_declaration', 'field_declaration', 'declaration',
                                    'compilation_unit') and len(currentNode.children) > 0:
                for n in currentNode.children:
                    self.analyzeNode(n, indent)
            elif currentNode.data == 'variable_declaration':
                for a in currentNode.children:
                    x = a
                    if a.data == 'type':
                        while len(x.children) > 0:
                            x = x.children[0]
                        store = x.data
                        if x.data == 'return':
                            self.pFile.write(space + x.data + ' ')
                    if a.data == 'variable_declarators':
                        # self.pFile.write(space)
                        # set to variable_declarator
                        for x in a.children:
                            if x.children[0].data == 'identifier':
                                x = x.children[0]
                                if x.children[0].data in ('true', 'false'):
                                    self.pFile.write(x.children[0].data.capitalize())
                                else:
                                    self.pFile.write(space + x.children[0].data)

                            x = a.children[0]
                            if x.children[2].data == 'variable_initializer' and len(x.children[2].children) > 0:
                                self.pFile.write(' = ')
                                b = x.children[2].children[0]
                                if b.children[0].data == 'dot_expression':
                                    # old - self.handleExpression(x.children[2].children[0], indent - 2)
                                    self.handleExpression(x.children[2].children[0], 0)
                                else:
                                    # old - self.handleExpression(x.children[2].children[0], indent - 2)
                                    self.handleExpression(x.children[2].children[0], 0)
                            else:
                                self.pFile.write(' = None')
                        self.pFile.write('\n')
            elif currentNode.data == 'class_declaration' and len(currentNode.children) > 0:
                for n in currentNode.children:
                    if n.data == 'identifier':
                        # CHANGED
                        self.currentClass = n.children[0].data
                        self.pFile.write('class ' + n.children[0].data + ': \n')
                    if n.data == 'contents':
                        for a in n.children:
                            self.analyzeNode(a, indent + 1)

from Node import *

from Scanner import *

class Item:
    def __init__(self, children, data):
        self.children = []
        self.data = data

    # toString used for outputting tree
    def toString(self, level = 0):
        # print node data indented based on level in tree
        ret = "\t"*level+"└-"+repr(self.data)+"\n"
        if self.children is not None:
            for child in self.children:
                if child is not None:
                    # call toString in children in next level
                    ret += child.toString((level+1))
        return ret


currentLine = 0
currentToken = 0

maxLoopDepth = 10
loopCount = 0

progLines = []

def init():
    global currentLine
    global currentToken
    global maxLoopDepth
    global loopCount
    global progLines

    currentLine = 0
    currentToken = 0

    maxLoopDepth = 10
    loopCount = 0

    progLines = []

def main(input):
    init()
    global progLines
    progLines = input
    tree = compilation_unit()
    return tree


def setCurrentLine(v):
    global currentLine
    currentLine = v


def setCurrentToken(v):
    global currentToken
    currentToken = v
    #print("TOKEN = ", v)


def nextLine():
    setCurrentLine(currentLine + 1)
    if currentLine < len(progLines):
        return progLines[currentLine]
    else:
        return None


def nextToken():
    setCurrentToken(currentToken + 1)
    if currentToken < len(peekLine().tokens):
        return peekToken()
    else:
        return None


def nextTokenAnyLine():
    if nextToken() is not None:
        return peekToken()
    else:
        if nextLine() is not None:
            setCurrentToken(0)
            return peekToken()
        else:
            setCurrentLine(-1)
            return None


def peekLine():
    return progLines[currentLine]


def peekToken():
    try:
        return progLines[currentLine].tokens[currentToken]
    except:
        return None


def oneOrZero(fun):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    temp = fun()
    if temp is None:
        setCurrentToken(saveToken)
        setCurrentLine(saveLine)
        item.children.append(None)
    else:
        item.children.append(temp)
        # nextTokenAnyLine()

    return item


def oneOrMany(fun):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    temp = fun()
    if temp is None:
        setCurrentToken(saveToken)
        setCurrentLine(saveLine)
        return None
    while temp is not None:
        saveToken = currentToken
        saveLine = currentLine
        item.children.append(temp)
        # if literal(",") is not None:
        #     nextTokenAnyLine()
        literal(",")
        temp = fun()
    setCurrentToken(saveToken)
    setCurrentLine(saveLine)
    return item


def onlyOne(fun):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    temp = fun()
    if temp is None:
        setCurrentToken(saveToken)
        setCurrentLine(saveLine)
        return None
    item.children.append(temp)
    # nextTokenAnyLine()
    return item


def anyNumberComma(fun):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    temp = fun()
    if temp is None:
        item.children.append(None)
        setCurrentToken(saveToken)
        setCurrentLine(saveLine)
        return item
    while temp is not None:
        item.children.append(temp)
        # if literal(",") is not None:
        #     nextTokenAnyLine()
        literal(",")
        temp = fun()
    return item

def anyNumberPlus(fun):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    temp = fun()
    if temp is None:
        item.children.append(None)
        setCurrentToken(saveToken)
        setCurrentLine(saveLine)
        return item
    while temp is not None:
        item.children.append(temp)
        literal("+")
        temp = fun()
    return item


def oneOf(funs):
    item = Item([], "")

    saveToken = currentToken
    saveLine = currentLine
    for fun in funs:
        temp = fun()
        if temp is not None:
            item.children.append(temp)
            # nextTokenAnyLine()
            return item
        else:
            setCurrentToken(saveToken)
            setCurrentLine(saveLine)
    return None


def literal(t):
    item = Item([], t)

    saveToken = currentToken
    saveLine = currentLine
    if peekToken() is None:
        return None

    if peekToken().word == t:
        nextTokenAnyLine()
        return item

    setCurrentToken(saveToken)
    setCurrentLine(saveLine)
    return None


def parseLine(tokens):
    return


def compilation_unit():
    item = Item([], "compilation_unit")

    packstate = oneOrZero(package_statement)
    packstate.data = "package_statement"
    item.children.append(packstate)

    impstate = anyNumberComma(import_statement)
    impstate.data = "import_statement"
    item.children.append(impstate)

    typedec = anyNumberComma(type_declaration)
    typedec.data = "type_declaration"
    item.children.append(typedec)

    return item


def package_statement():
    item = Item([], "package_statement")

    if literal("package") is None:
        return None

    name = onlyOne(package_name)
    if name is None:
        return None
    name = name.children[0]
    # name.data = "package_name"
    item.children.append(name)

    if literal(";") is None:
        return None

    return item


def import_statement():
    item = Item([], "import_statement")

    if literal("import") is None:
        return None

    name = oneOf({package_name, class_name, interface_name})
    if name is None:
        return None
    name = name.children[0]
    if name.data == "package_name":
        if literal(".") is None:
            return None
        if literal("*") is None:
            return None
    # elif name.children[0].data == "class_name":
    #     name.data = "class_name"
    # else:
    #     name.data = "interface_name"
    item.children.append(name)

    if literal(";") is None:
        return None

    return item


def type_declaration():
    item = Item([], "type_declaration")

    comm = oneOrZero(doc_comment)
    comm.data = "comment"
    if comm.children[0] is not None:
        comm = comm.children[0]
    item.children.append(comm)

    decl = oneOf({class_declaration, interface_declaration})
    if decl is None:
        return None
    decl = decl.children[0]
    # if decl.children[0].data == "interface_declaration":
    #     decl.data = "interface_declaration"
    # else:
    #     decl.data = "class_declaration"
    item.children.append(decl)

    if literal(";") is None:
        return None

    return item


def doc_comment():
    item = Item([], "comment")

    # if literal("//") is not None:
    #     setCurrentToken(currentToken - 1)
    #     while nextToken() is not None:
    #         item.children.append(Item([], peekToken().word))
    #     setCurrentLine(currentLine + 1)
    #     setCurrentToken(0)
    #     return item
    #
    # if literal("/*") is not None:
    #     setCurrentToken(currentToken - 1)
    #     while literal("*/") is None:
    #         if nextToken is not None:
    #             item.children.append(Item([], peekToken().word))
    #         else:
    #             if nextLine() is not None:
    #                 item.children.append(Item([], "\n"))
    #                 setCurrentLine(currentLine+1)
    #                 setCurrentToken(0)
    #             else:
    #                 return None

    while peekToken() is not None and peekToken().id == "comment":
        item.children.append(Item([], peekToken().word))
        nextTokenAnyLine()

    if len(item.children) == 0:
        return None

    return item


def class_declaration():
    item = Item([], "class_declaration")

    modif = anyNumberComma(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    if literal("class") is None:
        return None

    ident = onlyOne(identifier)
    if ident is None:
        return None
    ident = ident.children[0]
    item.children.append(ident)

    ext = oneOrZero(extends)
    ext.data = "extends"
    item.children.append(ext)

    impl = oneOrZero(implements)
    impl.data = "implements"
    item.children.append(impl)

    if literal("{") is None:
        return None

    contents = anyNumberComma(field_declaration)
    contents.data = "contents"
    item.children.append(contents)

    if literal("}") is None:
        return None

    return item


def interface_declaration():
    item = Item([], "interface_declaration")

    modif = anyNumberComma(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    if literal("interface") is None:
        return None

    ident = onlyOne(identifier)
    if ident is None:
        return None
    ident.data = "identifier"
    item.children.append(ident)

    ext = oneOrZero(extends)
    ext.data = "extends"
    item.children.append(ext)

    impl = oneOrZero(implements)
    impl.data = "implements"
    item.children.append(impl)

    if literal("{") is None:
        return None

    contents = anyNumberComma(field_declaration)
    contents.data = "contents"
    item.children.append(contents)

    if literal("}") is None:
        return None

    return item


def extends():
    item = Item([], "extends")

    if literal("extends") is None:
        return None

    clnm = onlyOne(class_name)
    if clnm is None:
        return None
    clnm = clnm.children[0]
    item.children.append(clnm)

    return item


def implements():
    item = Item([], "implements")

    if literal("implements") is None:
        return None

    innm = oneOrMany(interface_name)
    if innm is None:
        return None
    innm.data = "interface_name"
    item.children.append(innm)

    return item


def field_declaration():
    item = Item([], "field_declaration")

    comm = oneOrZero(doc_comment)
    comm.data = "comment"
    if comm.children[0] is not None:
        comm = comm.children[0]
    item.children.append(comm)

    fd = oneOf({declare, static_initializer})
    if fd is None:
        if literal(";") is None:
            return None
        return item
    fd = fd.children[0]
    item.children.append(fd)

    return item


def declare():
    item = Item([], "declaration")

    decl = oneOf({method_declaration, constructor_declaration, variable_declaration})
    if decl is None:
        return None
    decl = decl.children[0]
    item.children.append(decl)

    return item


def method_declaration():
    item = Item([], "method_declaration")

    modif = anyNumberComma(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    typ = onlyOne(type)
    if typ is None:
        return None
    typ = typ.children[0]
    item.children.append(typ)

    iden = oneOrZero(identifier)
    if iden is None:
        return None
    if iden.children[0] is not None:
        iden = iden.children[0]
    item.children.append(iden)

    if literal("(") is None:
        return None

    plist = oneOrZero(parameter_list)
    plist.data = "parameter"
    if plist.children[0] is not None:
        plist = plist.children[0]
    item.children.append(plist)

    if literal(")") is None:
        return None

    arry = anyNumberComma(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    sblock = onlyOne(statement_block)
    if sblock is None:
        sblock = literal(";")
    if sblock is None:
        return None
    sblock = sblock.children[0]
    item.children.append(sblock)

    return item


def constructor_declaration():
    item = Item([], "constructor_declaration")

    modif = anyNumberComma(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    if literal("(") is None:
        return None

    plist = oneOrZero(parameter_list)
    plist.data = "parameter"
    if plist.children[0] is not None:
        plist = plist.children[0]
    item.children.append(plist)

    if literal(")") is None:
        return None

    sblock = onlyOne(statement_block)
    if sblock is None:
        return None
    sblock = sblock.children[0]
    item.children.append(sblock)

    return item


def statement_block():
    item = Item([], "statement_block")

    if literal("{") is None:
        return None

    statements = anyNumberComma(statement)
    statements.data = "statement_block"
    item = statements

    if literal("}") is None:
        return None

    return item


def variable_declaration():
    item = Item([], "variable_declaration")

    modif = anyNumberComma(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    typ = onlyOne(type)
    if typ is None:
        return None
    typ = typ.children[0]
    item.children.append(typ)

    vardec = oneOrMany(variable_declarator)
    if vardec is None:
        return None
    vardec.data = "variable_declarators"
    item.children.append(vardec)

    if literal(";") is None:
        return None

    return item


def variable_declarator():
    item = Item([], "variable_declarator")

    idn = onlyOne(identifier)
    if idn is None:
        return None
    idn = idn.children[0]
    item.children.append(idn)

    arry = anyNumberComma(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    if literal("=") is not None:
        init = onlyOne(variable_initializer)
        if init is None:
            return None
        init = init.children[0]
        item.children.append(init)
    else:
        init = Item([], "variable_initializer")
        item.children.append(init)

    return item


def array_braces():
    item = Item([], "array_braces")

    if literal("[") is None:
        return None
    if literal("]") is None:
        return None
    item = Item([], "[]")

    return item


def variable_initializer():
    item = Item([], "variable_initializer")

    expr = onlyOne(expression)
    if expr is not None:
        expr = expr.children[0]
        item.children.append(expr)
        return item

    if literal("{") is None:
        return None

    vinit = anyNumberComma(variable_initializer)
    vinit.data = "array"
    item.children.append(vinit)

    if literal("}") is None:
        return None

    return item


def static_initializer():
    item = Item([], "static_initializer")

    l = literal("static")
    if l is None:
        return None
    item.children.append(l)

    sblock = onlyOne(statement_block)
    if sblock is None:
        return None
    sblock = sblock.children[0]
    item.children.append(sblock)

    return item


def parameter_list():
    item = Item([], "parameter_list")

    param = oneOrMany(parameter)
    if param is None:
        return None
    param.data = "parameters"
    item.children.append(param)

    return item


def parameter():
    item = Item([], "parameter")

    typ = onlyOne(type)
    if typ is None:
        return None
    typ = typ.children[0]
    item.children.append(typ)

    iden = onlyOne(identifier)
    if iden is None:
        return None
    iden = iden.children[0]
    item.children.append(iden)

    arry = anyNumberComma(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    return item


def statement():
    item = Item([], "statement")

    comm = oneOrZero(doc_comment)
    comm.data = "comment"
    if comm.children[0] is not None:
        comm = comm.children[0]
    item.children.append(comm)

    vardec = onlyOne(variable_declaration)
    if vardec is not None:
        vardec = vardec.children[0]
        item.children.append(vardec)
        return item

    sblock = onlyOne(statement_block)
    if sblock is not None:
        sblock = sblock.children[0]
        item.children.append(sblock)
        return item

    ifst = onlyOne(if_statement)
    if ifst is not None:
        ifst = ifst.children[0]
        item.children.append(ifst)
        return item

    dost = onlyOne(do_statement)
    if dost is not None:
        dost = dost.children[0]
        item.children.append(dost)
        return item

    whilest = onlyOne(while_statement)
    if whilest is not None:
        whilest = whilest.children[0]
        item.children.append(whilest)
        return item

    forst = onlyOne(for_statement)
    if forst is not None:
        forst = forst.children[0]
        item.children.append(forst)
        return item

    tryst = onlyOne(try_statement)
    if tryst is not None:
        tryst = tryst.children[0]
        item.children.append(tryst)
        return item

    swtst = onlyOne(switch_statement)
    if swtst is not None:
        swtst = swtst.children[0]
        item.children.append(swtst)
        return item

    rtrn = literal("return")
    if rtrn is not None:
        item.children.append(rtrn)
        expr = oneOrZero(expression)
        if expr.children[0] is not None:
            expr = expr.children[0]
        item.children.append(expr)
        if literal(";") is None:
            return None
        # item.children.append(rtrn)
        return item

    thrw = literal("throw")
    if thrw is not None:
        item.children.append(thrw)
        expr = onlyOne(expression)
        if expr is None:
            return None
        expr = expr.children[0]
        item.children.append(expr)
        if literal(";") is None:
            return None
        # item.children.append(thrw)
        return item

    brk = literal("break")
    if brk is not None:
        item.children.append(brk)
        iden = oneOrZero(identifier)
        if iden.children[0] is not None:
            iden = iden.children[0]
        item.children.append(iden)
        if literal(";") is None:
            return None
        # item.children.append(brk)
        return item

    cnt = literal("continue")
    if cnt is not None:
        item.children.append(cnt)
        iden = oneOrZero(identifier)
        if iden.children[0] is not None:
            iden = iden.children[0]
        item.children.append(iden)
        if literal(";") is None:
            return None
        # item.children.append(cnt)
        return item

    if literal(";") is not None:
        return item

    saveToken = currentToken
    saveLine = currentLine
    idencol = check_iden_colon()
    if idencol is not None:
        item = idencol
        return item

    setCurrentToken(saveToken)
    setCurrentLine(saveLine)
    expr = onlyOne(expression)
    if expr is not None:
        expr = expr.children[0]
        item.children.append(expr)
        if literal(";") is None:
            return None
        return item

    return None

def check_iden_colon():
    item = Item([], "statement")
    iden = onlyOne(identifier)
    if iden is not None:
        iden = iden.children[0]
        item.children.append(iden)
        if literal(":") is None:
            return None
        st = onlyOne(statement)
        if st is None:
            return None
        st = st.children[0]
        item.children.append(st)
        return item


def if_statement():
    item = Item([], "if_statement")

    if literal("if") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp = exp.children[0]
    item.children.append(exp)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    if literal("else") is None:
        item.children.append(Item([None], "statement"))
        return item

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    return item


def do_statement():
    item = Item([], "do_statement")

    if literal("do") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    if literal("while") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp = exp.children[0]
    item.children.append(exp)

    if literal(")") is None:
        return None
    if literal(";") is None:
        return None

    return item


def while_statement():
    item = Item([], "while_statement")

    if literal("while") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp = exp.children[0]
    item.children.append(exp)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    return item


def for_statement():
    item = Item([], "for_statement")

    if literal("for") is None:
        return None
    if literal("(") is None:
        return None

    vardec = onlyOne(variable_declaration)
    if vardec is not None:
        vardec = vardec.children[0]
        item.children.append(vardec)
    else:
        exp = oneOrZero(expression)
        exp.data = "expression"
        if exp.children[0] is not None:
            exp = exp.children[0]
        item.children.append(exp)
        if literal(";") is None:
            return None

    exp = oneOrZero(expression)
    exp.data = "expression"
    if exp.children[0] is not None:
        exp = exp.children[0]
    item.children.append(exp)
    if literal(";") is None:
        return None

    exp = oneOrZero(expression)
    exp.data = "expression"
    if exp.children[0] is not None:
        exp = exp.children[0]
    item.children.append(exp)

    if literal(")") is None:
        return None


    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    return item


def try_statement():
    item = Item([], "try_statement")

    if literal("try") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    ct = anyNumberComma(catch)
    ct.data = "catch"
    item.children.append(ct)

    if literal("finally") is None:
        item.children.append(Item([None], "statement"))
        return item

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    return item


def catch():
    item = Item([], "catch")

    if literal("catch") is None:
        return None
    if literal("(") is None:
        return None

    para = onlyOne(parameter)
    if para is None:
        return None
    para = para.children[0]
    item.children.append(para)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st = st.children[0]
    item.children.append(st)

    return item


def switch_statement():
    item = Item([], "switch_statement")

    if literal("switch") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp = exp.children[0]
    item.children.append(exp)

    if literal(")") is None:
        return None
    if literal("{") is None:
        return None

    cases = anyNumberComma(switch_case)
    cases.data = "cases"
    item.children.append(cases)

    if literal("}") is None:
        return None

    return item


def switch_case():
    item = Item([], "switch_case")

    if literal("case") is not None:
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
    elif literal("default") is not None:
        item.children.append(Item([], "default"))
    else:
        return None

    if literal(":") is None:
        return None

    st = oneOrMany(statement)
    if st is None:
        return None
    st.data = "statements"
    item.children.append(st)

    return item


def expression():
    item2 = Item([], "expression")
    item = Item([], "")

    item2.children.append(item)

    if peekToken().id == "print":
        tempToken = currentToken
        item.data = "print"
        nextToken()
        l = literal("(")
        if l is None:
            setCurrentToken(tempToken)
            return None
        exp = anyNumberPlus(expressionPrint)
        item.children = exp.children
        l = literal(")")
        if l is None:
            setCurrentToken(tempToken)
            return None
        return item2
                

    # next = nextToken()
    # setCurrentToken(currentToken - 1)
    #
    # numex = onlyOne(numeric_expression)
    # if numex is not None:
    #     numex.data = "numeric_expression"
    #     item.children.append(numex)
    #     return item
    symbols = {"-", "++", "--"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "numeric_expression"
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp = exp.children[0]
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp
    #
    # testex = onlyOne(testing_expression)
    # if testex is not None:
    #     testex.data = "testing_expression"
    #     item.children.append(testex)
    #     if literal(";") is None:
    #         return None
    #     return item
    #
    # logex = onlyOne(logical_expression)
    # if logex is not None:
    #     logex.data = "logical_expression"
    #     item.children.append(logex)
    #     return item
    l = literal("!")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp

    l = literal("true")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp

    l = literal("false")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # strex = onlyOne(string_expression)
    # if strex is not None:
    #     strex.data = "string_expression"
    #     item.children.append(strex)
    #     return item
    #
    # bitex = onlyOne(bit_expression)
    # if bitex is not None:
    #     bitex.data = "bit_expression"
    #     item.children.append(bitex)
    #     return item
    l = literal("~")
    if l is not None:
        item.data = "bit_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # castex = onlyOne(casting_expression)
    # if castex is not None:
    #     castex.data = "casting_expression"
    #     item.children.append(castex)
    #     return item

    l = literal("(")
    if l is not None:
        item.data = "casting_expression"
        typ = onlyOne(type)
        if typ is None:
            return None
        typ = typ.children[0]
        item.children.append(typ)

        if literal(")") is None:
            return None

        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)

        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # createex = onlyOne(creating_expression)
    # if createex is not None:
    #     createex.data = "creating_expression"
    #     item.children.append(createex)
    #     return item
    crex = onlyOne(creating_expression)
    if crex is not None:
        item.data = crex.children[0].data
        item.children = crex.children[0].children
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # litex = onlyOne(literal_expression)
    # if litex is not None:
    #     litex.data = "literal_expression"
    #     item.children.append(litex)
    #     return item
    litex = onlyOne(literal_expression)
    if litex is not None:
        item2.children[0] = item = litex.children[0]
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # null = literal("null")
    # if null is not None:
    #     item.children.append(null)
    #     return item
    l = literal("null")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # spr = literal("super")
    # if spr is not None:
    #     item.children.append(spr)
    #     return item
    l = literal("super")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # ths = literal("this")
    # if ths is not None:
    #     item.children.append(ths)
    #     return item
    l = literal("this")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    # iden = onlyOne(identifier)
    # if iden is not None:
    #     iden.data = "identifier"
    #     item.children.append(iden)
    #     return item
    iden = onlyOne(identifier)
    if iden is not None:
        item.data = "identifier_expression"
        iden = iden.children[0]
        item.children.append(iden)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    l = literal("(")
    if l is not None:
        item.data = "parenthesis_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        l = literal(")")
        if l is None:
            return None
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    #
    #
    # exp = onlyOne(expression)
    # if exp is not None:
    #     item.children.append(exp)
    #     if literal("(") is not None:
    #         alist = oneOrZero(arglist)
    #         alist.data = "arglist"
    #         item.children.append(alist)
    #         if literal(")") is None:
    #             return None
    #         return item
    #     elif literal("[") is not None:
    #         item.children.append(Item([], "[]"))
    #         exptwo = onlyOne(expression)
    #         if exptwo is None:
    #             return None
    #         exptwo.data = "expression"
    #         item.children.append(exptwo)
    #         if literal("]") is None:
    #             return None
    #         return item
    #     elif literal(".") is not None:
    #         item.children.append(Item([], "."))
    #         exptwo = onlyOne(expression)
    #         if exptwo is None:
    #             return None
    #         exptwo.data = "expression"
    #         item.children.append(exptwo)
    #         return item
    #     elif literal(",") is not None:
    #         item.children.append(Item([], ","))
    #         exptwo = onlyOne(expression)
    #         if exptwo is None:
    #             return None
    #         exptwo.data = "expression"
    #         item.children.append(exptwo)
    #         return item
    #     elif literal("instanceof") is not None:
    #         item.children.append(Item([], "isntanceof"))
    #         name = oneOf({class_name, interface_name})
    #         if name is None:
    #             return None
    #         name.data = "name"
    #         item.children.append(name)
    #         return item

    return None


def expression_prime():
    item2 = Item([], "expression")
    item = Item([], "")

    item2.children.append(item)

    symbols = {"++", "--"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "numeric_expression"
            item.children.append(l)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp

    symbols = {"+", "+=", "-", "-=", "*", "*=", "/", "/=", "%", "%="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "numeric_expression"
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp = exp.children[0]
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp


    symbols = {">", "<", ">=", "<=", "==", "!="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "testing_expression"
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp = exp.children[0]
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp


    symbols = {"&", "&=", "|", "|=", "^", "^=", "&&", "||=", "%", "%="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "logical_expression"
            item.children.append(l)
            exptwo = onlyOne(expression)
            if exptwo is None:
                return None
            exptwo = exptwo.children[0]
            item.children.append(exptwo)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp

    l = literal("?")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo = exptwo.children[0]
        item.children.append(exptwo)
        ltwo = literal(":")
        if ltwo is not None:
            item.children.append(ltwo)
            expthree = onlyOne(expression)
            if expthree is None:
                return None
            expthree = expthree.children[0]
            item.children.append(expthree)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp

    # symbols = {"+", "+="}
    # for symbol in symbols:
    #     l = literal(symbol)
    #     if l is not None:
    #         item.data = "string_expression"
    #         item.children.append(l)
    #         exptwo = onlyOne(expression)
    #         if exptwo is None:
    #             return None
    #         exptwo = exptwo.children[0]
    #         item.children.append(exptwo)
    #         expp = onlyOne(expression_prime)
    #         if expp is None:
    #             return item
    #         expp = expp.children[0]
    #         item.children.extend(expp.children)
    #         return item


    symbols = {">>=", "<<", ">>", ">>>"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "bit_expression"
            item.children.append(l)
            exptwo = onlyOne(expression)
            if exptwo is None:
                return None
            exptwo = exptwo.children[0]
            item.children.append(exptwo)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item2
            expp = expp.children[0]
            expp.children[0].children.insert(0, item2)
            return expp

    l = literal("=")
    if l is not None:
        item.data = "assignment_expression"
        item.children.append(l)
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo = exptwo.children[0]
        item.children.append(exptwo)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp

    if literal("(") is not None:
        item.data = "method_expression"
        alist = oneOrZero(arglist)
        alist.data = "arglist"
        if alist.children[0] is not None:
            alist = alist.children[0]
        item.children.append(alist)
        if literal(")") is None:
            return None
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    elif literal("[") is not None:
        item.data = "brackets_expression"
        item.children.append(Item([], "["))
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo = exptwo.children[0]
        item.children.append(exptwo)
        if literal("]") is None:
            return None
        item.children.append(Item([], "]"))
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    elif literal(".") is not None:
        item.data = "dot_expression"
        item.children.append(Item([], "."))
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo = exptwo.children[0]
        item.children.append(exptwo)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp
    # elif literal(",") is not None:
    #     item.data = "comma_expression"
    #     item.children.append(Item([], ","))
    #     exptwo = onlyOne(expression)
    #     if exptwo is None:
    #         return None
    #     exptwo = exptwo.children[0]
    #     item.children.append(exptwo)
    #     expp = onlyOne(expression_prime)
    #     if expp is None:
    #         return item2
    #     expp = expp.children[0]
    #     expp.children[0].children.insert(0, item2)
    #     return expp
    elif literal("instanceof") is not None:
        item.data = "instance_expression"
        item.children.append(Item([], "isntanceof"))
        name = oneOf({class_name, interface_name})
        if name is None:
            return None
        name = name.children[0]
        item.children.append(name)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item2
        expp = expp.children[0]
        expp.children[0].children.insert(0, item2)
        return expp

    return None


# def numeric_expression():
#     item = Item([], "numeric_expression")
#
#     exp = onlyOne(expression)
#     if exp is None:
#         return None
#     exp.data = "expression"
#     item.children.append(exp)
#
#     symbols = {"++", "--"}
#     for symbol in symbols:
#         l = literal(symbol)
#         if l is not None:
#             item.children.append(l)
#             return item
#
#     symbols = {"+", "+=", "-", "-=", "*", "*=", "/", "/=", "%", "%="}
#     for symbol in symbols:
#         l = literal(symbol)
#         if l is not None:
#             item.children.append(l)
#             exp = onlyOne(expression)
#             if exp is None:
#                 return None
#             exp.data = "expression"
#             item.children.append(exp)
#             return item
#
#     return None
#
#
# def testing_expression():
#     item = Item([], "testing_expression")
#
#     exp = onlyOne(expression)
#     if exp is None:
#         return None
#     exp.data = "expression"
#     item.children.append(exp)
#
#     symbols = {">", "<", ">=", "<=", "==", "!="}
#     for symbol in symbols:
#         l = literal(symbol)
#         if l is not None:
#             item.children.append(l)
#             exp = onlyOne(expression)
#             if exp is None:
#                 return None
#             exp.data = "expression"
#             item.children.append(exp)
#             return item
#
#     return None
#
#
# def logical_expression():
#     item = Item([], "logical_expression")
#
#     exp = onlyOne(expression)
#     if exp is not None:
#         exp.data = "expression"
#         item.children.append(exp)
#         symbols = {"&","&=","|","|=","^","^=","&&","||=","%","%="}
#         for symbol in symbols:
#             l = literal(symbol)
#             if l is not None:
#                 item.children.append(l)
#                 exptwo = onlyOne(expression)
#                 if exptwo is None:
#                     return None
#                 exptwo.data = "expression"
#                 item.children.append(exptwo)
#                 return item
#
#         l = literal("?")
#         if l is not None:
#             item.children.append(l)
#             exptwo = onlyOne(expression)
#             if exptwo is None:
#                 return None
#             exptwo.data = "expression"
#             item.children.append(exptwo)
#             ltwo = literal(":")
#             if ltwo is not None:
#                 item.children.append(ltwo)
#                 expthree = onlyOne(expression)
#                 if expthree is None:
#                     return None
#                 expthree.data = "expression"
#                 item.children.append(expthree)
#                 return item
#
#     return None
#
#
# def string_expression():
#     item = Item([], "string_expression")
#
#     exp = onlyOne(expression)
#     if exp is None:
#         return None
#     exp.data = "expression"
#     item.children.append(exp)
#
#     symbols = {"+", "+="}
#     for symbol in symbols:
#         l = literal(symbol)
#         if l is not None:
#             item.children.append(l)
#             exptwo = onlyOne(expression)
#             if exptwo is None:
#                 return None
#             exptwo.data = "expression"
#             item.children.append(exptwo)
#             return item
#
#     return None
#
#
# def bit_expression():
#     item = Item([], "bit_expression")
#
#     exp = onlyOne(expression)
#     if exp is None:
#         return None
#     exp.data = "expression"
#     item.children.append(exp)
#
#     symbols = {">>=", "<<", ">>", ">>>"}
#     for symbol in symbols:
#         l = literal(symbol)
#         if l is not None:
#             item.children.append(l)
#             exptwo = onlyOne(expression)
#             if exptwo is None:
#                 return None
#             exptwo.data = "expression"
#             item.children.append(exptwo)
#             return item
#
#     return None
#
#
# def casting_expression():
#     item = Item([], "bit_expression")
#
#     return item
#

def creating_expression():
    item = Item([], "creating_expression")

    if literal("new") is None:
        return None

    name = onlyOne(class_name)
    if name is not None:
        name = name.children[0]
        item.children.append(name)
        if literal("(") is None:
            return None
        alist = oneOrZero(arglist)
        alist.data = "arglist"
        if alist.children[0] is not None:
            alist = alist.children[0]
        item.children.append(alist)
        if literal(")") is None:
            return None
        return item

    typ = onlyOne(type_specifier)
    if typ is not None:
        typ = typ.children[0]
        item.children.append(typ)
        if literal("[") is not None:
            exp = oneOrZero(expression)
            if exp.children[0] is not None:
                exp = exp.children[0]
                item.children.append(exp)
            else:
                item.children.append(Item([], "expression"))
                setCurrentToken(currentToken - 1)
                arry = oneOrMany(array_braces)
                if arry is None:
                    return None

                arry.data = "array_braces"
                item.children.append(arry)
                return item
            if literal("]") is None:
                return None
            return item

    if literal("(") is not None:
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp.data = "parenthesis_expression"
        item.children.append(exp)
        if literal(")") is None:
            return None
        return item

    return None


def literal_expression():
    item = Item([], "literal_expression")

    ltrl = oneOf({number, character, string})
    if ltrl is None:
        return None
    ltrl = ltrl.children[0]
    item.children.append(ltrl)

    return item


def expressionPrint():
    item2 = Item([], "expression")
    item = Item([], "")

    item2.children.append(item)

    if peekToken().id == "print":
        tempToken = currentToken
        item.data = "print"
        nextToken()
        l = literal("(")
        if l is None:
            setCurrentToken(tempToken)
            return None
        exp = anyNumberPlus(expressionPrint)
        item.children = exp.children
        l = literal(")")
        if l is None:
            setCurrentToken(tempToken)
            return None
        return item2

    symbols = {"-", "++", "--"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.data = "numeric_expression"
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp = exp.children[0]
            item.children.append(exp)
            return item2

    l = literal("!")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        return item2

    l = literal("true")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        return item2

    l = literal("false")
    if l is not None:
        item.data = "logical_expression"
        item.children.append(l)
        return item2

    l = literal("~")
    if l is not None:
        item.data = "bit_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        return item2

    l = literal("(")
    if l is not None:
        item.data = "casting_expression"
        typ = onlyOne(type)
        if typ is None:
            return None
        typ = typ.children[0]
        item.children.append(typ)

        if literal(")") is None:
            return None

        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)

        return item2

    crex = onlyOne(creating_expression)
    if crex is not None:
        item = crex.children[0]
        return item2

    litex = onlyOne(literal_expression)
    if litex is not None:
        item2.children[0] = item = litex.children[0]
        return item2

    l = literal("null")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        return item2

    l = literal("super")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        return item2

    l = literal("this")
    if l is not None:
        item.data = "keyword_expression"
        item.children.append(l)
        return item2

    iden = onlyOne(identifier)
    if iden is not None:
        item.data = "identifier_expression"
        iden = iden.children[0]
        item.children.append(iden)
        return item2

    l = literal("(")
    if l is not None:
        item.data = "parenthesis_expression"
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp = exp.children[0]
        item.children.append(exp)
        l = literal(")")
        if l is None:
            return None
        item.children.append(l)
        return item2
    return None

def arglist():
    item = Item([], "arglist")

    alist = oneOrMany(expression)
    if alist is None:
        return None
    alist.data = "arglist"
    item = alist

    return item


def type():
    item = Item([], "type")

    typsp = onlyOne(type_specifier)
    if typsp is None:
        return None
    typsp = typsp.children[0]
    item.children.append(typsp)

    arry = anyNumberComma(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    return item


def type_specifier():
    item = Item([], "type_specifier")

    symbols = {"boolean", "byte", "char", "short", "int", "float", "long", "double", "void"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            return item

    clnm = onlyOne(class_name)
    if clnm is not None:
        clnm = clnm.children[0]
        item.children.append(clnm)
        return item

    innm = onlyOne(interface_name)
    if innm is not None:
        innm = innm.children[0]
        item.children.append(innm)
        return item

    return None


def modifier():
    item = Item([], "modifier")

    symbols = { "public", "private", "protected", "static", "final", "native", "synchronized", "abstract", "threadsafe", "transient"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            return item

    return None


def package_name():
    item = Item([], "package_name")

    iden = onlyOne(identifier)
    if iden is None:
        return None
    iden = iden.children[0]
    item.children.append(iden)

    l = literal(".")
    if l is not None:
        item.children.append(l)
        pname = onlyOne(package_name)
        if pname is not None:
            item.children.extend(pname.children)
        else:
            iden = onlyOne(identifier)
            if iden is None:
                return None
            iden = iden.children[0]
            item.children.append(iden)

    return item
    # pname = onlyOne(package_name)
    # if pname is not None:
    #     item.children.append(pname)
    #     iden = onlyOne(identifier)
    #     if iden is not None:
    #         item.children.append(iden)
    #         return item

    return None


def class_name():
    item = Item([], "class_name")

    iden = onlyOne(package_name)
    if iden is not None:
        iden = iden.children[0]
        item.children.append(iden)
        return item

    # pname = oneOrZero(package_name)
    # if pname.children[0] is not None:
    #     pname = pname.children[0]
    #
    # item.children.append(pname)
    # iden = onlyOne(identifier)
    # if iden is not None:
    #     iden = iden.children[0]
    #     item.children.append(iden)
    #     return item

    return None


def interface_name():
    item = Item([], "interface_name")

    iden = onlyOne(identifier)
    if iden is not None:
        iden = iden.children[0]
        item.children.append(iden)
        return item

    pname = onlyOne(package_name)
    if pname is not None:
        pname = pname.children[0]
        item.children.append(pname)
        iden = onlyOne(identifier)
        if iden is not None:
            iden = iden.children[0]
            item.children.append(iden)
            return item

    return None


def number():
    item = Item([], "number")

    if peekToken().id != "num":
        return None

    n = peekToken().word
    item.children.append(Item([], n))
    nextTokenAnyLine()
    return item


def character():
    item = Item([], "character")

    if peekToken().id != "char":
        return None
    n = peekToken().word
    item.children.append(Item([], n))
    nextTokenAnyLine()
    return item


def string():
    item = Item([], "string")

    if peekToken().id != "string":
        return None
    n = peekToken().word
    item.children.append(Item([], n))
    nextTokenAnyLine()
    return item


def identifier():
    item = Item([], "identifier")

    n = peekToken().word
    if not (n[0].isalpha() or n[0] == '_' or n[0] == '$'):
        return None
    for c in n[1:]:
        if not (n[0].isalnum() or n[0] == '_' or n[0] == '$'):
            return None
    item.children.append(Item([], n))
    nextTokenAnyLine()
    return item


# create a scanner object then use prepfile on required file
def getNode(data):
    test = Scanner()
    test.prepFile(data)
    return main(test.progNodes)
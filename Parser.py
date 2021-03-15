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


def main(input):
    global progLines
    progLines = input
    tree = compilation_unit()
    # print(tree.toString())
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
        item.children.append(temp)
        if literal(",") is not None:
            nextTokenAnyLine()
        temp = fun()
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


def anyNumber(fun):
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
        if literal(",") is not None:
            nextTokenAnyLine()
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

    impstate = anyNumber(import_statement)
    impstate.data = "import_statement"
    item.children.append(impstate)

    typedec = anyNumber(type_declaration)
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
    name.data = "package_name"
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
    if name.children[0].data == "package_name":
        name.data = "package_name"
        if literal(".") is None:
            return None
        if literal("*") is None:
            return None
    elif name.children[0].data == "class_name":
        name.data = "class_name"
    else:
        name.data = "interface_name"
    item.children.append(name)

    if literal(";") is None:
        return None

    return item


def type_declaration():
    item = Item([], "type_declaration")

    comm = oneOrZero(doc_comment)
    comm.data = "doc_comment"
    item.children.append(comm)

    decl = oneOf({class_declaration, interface_declaration})
    if decl is None:
        return None
    if decl.children[0].data == "interface_declaration":
        decl.data = "interface_declaration"
    else:
        decl.data = "class_declaration"
    item.children.append(decl)

    if literal(";") is None:
        return None

    return item


def doc_comment():
    item = Item([], "comment")

    if literal("//") is not None:
        setCurrentToken(currentToken - 1)
        while nextToken() is not None:
            item.children.append(Item([], peekToken().word))
        setCurrentLine(currentLine + 1)
        setCurrentToken(0)
        return item

    if literal("/*") is not None:
        setCurrentToken(currentToken - 1)
        while literal("*/") is None:
            if nextToken is not None:
                item.children.append(Item([], peekToken().word))
            else:
                if nextLine() is not None:
                    item.children.append(Item([], "\n"))
                    setCurrentLine(currentLine+1)
                    setCurrentToken(0)
                else:
                    return None

    return item


def class_declaration():
    item = Item([], "class_declaration")

    modif = anyNumber(modifier)
    modif.data = "modifiers"
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

    contents = anyNumber(field_declaration)
    contents.data = "contents"
    item.children.append(contents)

    if literal("}") is None:
        return None

    return item


def interface_declaration():
    item = Item([], "interface_declaration")

    modif = anyNumber(modifier)
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

    contents = anyNumber(field_declaration)
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
    clnm.data = "class_name"
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

    comm = oneOrZero(doc_comment)
    item.children.append(comm)

    decl = oneOf({method_declaration, constructor_declaration, variable_declaration})
    if decl is None:
        return None
    decl.data = "declare"
    item.children.append(decl)

    return item


def method_declaration():
    item = Item([], "method_declaration")

    modif = anyNumber(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    typ = onlyOne(type)
    if typ is None:
        return None
    typ.data = "type"
    item.children.append(typ)

    iden = oneOrZero(identifier)
    if iden is None:
        return None
    iden.data = "identifier"
    item.children.append(iden)

    if literal("(") is None:
        return None

    plist = oneOrZero(parameter_list)
    plist.data = "parameter_list"
    item.children.append(plist)

    if literal(")") is None:
        return None

    arry = anyNumber(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    sblock = onlyOne(statement_block)
    if sblock is None:
        sblock = literal(";")
    if sblock is None:
        return None
    item.children.append(sblock)

    return item


def constructor_declaration():
    item = Item([], "constructor_declaration")

    modif = anyNumber(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    if literal("(") is None:
        return None

    plist = oneOrZero(parameter_list)
    plist.data = "parameter_list"
    item.children.append(plist)

    if literal(")") is None:
        return None

    sblock = onlyOne(statement_block)
    if sblock is None:
        return None
    item.children.append(sblock)

    return item


def statement_block():
    item = Item([], "statement_block")

    if literal("{") is None:
        return None

    statements = anyNumber(statement)
    statements.data = "statements"
    item.children.append(statements)

    if literal("}") is None:
        return None

    return item


def variable_declaration():
    item = Item([], "variable_declaration")

    modif = anyNumber(modifier)
    modif.data = "modifier"
    item.children.append(modif)

    typ = onlyOne(type)
    if typ is None:
        return None
    typ.data = "type"
    item.children.append(typ)

    vardec = oneOrMany(variable_declarator)
    if vardec is None:
        return None
    vardec.data = "variable_declarator"

    if literal(";") is None:
        return None

    return item


def variable_declarator():
    item = Item([], "variable_declarator")

    idn = onlyOne(identifier)
    if idn is None:
        return None
    idn.data = "identifier"
    item.children.append(idn)

    arry = anyNumber(array_braces)
    arry.data = "array_braces"
    item.children.append(arry)

    if literal("=") is None:
        return item

    init = onlyOne(variable_initializer)
    if init is None:
        return None
    init.data = "variable_initializer"
    item.children.append(init)

    return item


def array_braces():
    item = Item([], "array_braces")

    if literal("[") is None:
        return None
    if literal("]") is None:
        return None
    item.children.append(Item([], "[]"))

    return item


def variable_initializer():
    item = Item([], "variable_initializer")

    expr = onlyOne(expression)
    if expr is not None:
        expr.data = "expression"
        item.children.append(expr)
        return item

    if literal("{") is None:
        return None

    vinit = anyNumber(variable_initializer)
    vinit.data = "variable_initializer"
    item.children.append(vinit)

    if literal("}") is None:
        return None

    return item


def static_initializer():
    item = Item([], "static_initializer")

    if literal("static") is None:
        return None

    sblock = onlyOne(statement_block)
    if sblock is None:
        return None
    sblock.data = "statement_block"
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
    typ.data = "type"
    item.children.append(typ)

    iden = onlyOne(identifier)
    if iden is None:
        return None
    iden.data = "identifier"
    item.children.append(iden)

    arry = anyNumber(array_braces)
    item.children.append(arry)

    return item


def statement():
    item = Item([], "statement")

    comm = oneOrZero(doc_comment)
    comm.data = "doc_comment"
    item.children.append(comm)

    vardec = onlyOne(variable_declaration)
    if vardec is not None:
        vardec.data = "variable_declaration"
        item.children.append(vardec)
        return item

    expr = onlyOne(expression)
    if expr is not None:
        expr.data = "expression"
        item.children.append(expr)
        if literal(";") is None:
            return None
        return item

    sblock = onlyOne(statement_block)
    if sblock is not None:
        sblock.data = "statement_block"
        item.children.append(sblock)
        return item

    ifst = onlyOne(if_statement)
    if ifst is not None:
        ifst.data = "if_statement"
        item.children.append(ifst)
        return item

    dost = onlyOne(do_statement)
    if dost is not None:
        dost.data = "do_statement"
        item.children.append(dost)
        return item

    whilest = onlyOne(while_statement)
    if whilest is not None:
        whilest.data = "while_statement"
        item.children.append(whilest)
        return item

    forst = onlyOne(for_statement)
    if forst is not None:
        forst.data = "for_statement"
        item.children.append(forst)
        return item

    tryst = onlyOne(try_statement)
    if tryst is not None:
        tryst.data = "try_statement"
        item.children.append(tryst)
        return item

    swtst = onlyOne(switch_statement)
    if swtst is not None:
        swtst.data = "switch_statement"
        item.children.append(swtst)
        return item

    rtrn = literal("return")
    if rtrn is not None:
        expr = oneOrZero(expression)
        rtrn.children.append(expr)
        if literal(";") is None:
            return None
        item.children.append(rtrn)
        return item

    thrw = literal("throw")
    if thrw is not None:
        expr = onlyOne(expression)
        if expr is None:
            return None
        thrw.children.append(expr)
        if literal(";") is None:
            return None
        item.children.append(thrw)
        return item

    iden = onlyOne(identifier)
    if iden is not None:
        iden.data = "identifier"
        item.children.append(whilest)
        if literal(":") is None:
            return None
        st = onlyOne(statement)
        if st is None:
            return None
        st.data = "statement"
        item.children.append(st)
        return item

    brk = literal("break")
    if brk is not None:
        iden = oneOrZero(identifier)
        brk.children.append(iden)
        if literal(";") is None:
            return None
        item.children.append(brk)
        return item

    cnt = literal("continue")
    if cnt is not None:
        iden = oneOrZero(identifier)
        cnt.children.append(iden)
        if literal(";") is None:
            return None
        item.children.append(cnt)
        return item

    if literal(";") is not None:
        return item

    return None


def if_statement():
    item = Item([], "if_statement")

    if literal("if") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp.data = "expression"
    item.children.append(exp)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
    item.children.append(st)

    if literal("else") is None:
        item.children.append(Item([], "statement"))
        return item

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
    item.children.append(st)

    return item


def do_statement():
    item = Item([], "do_statement")

    if literal("do") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
    item.children.append(st)

    if literal("while") is None:
        return None
    if literal("(") is None:
        return None

    exp = onlyOne(expression)
    if exp is None:
        return None
    exp.data = "expression"
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
    exp.data = "expression"
    item.children.append(exp)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
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
        vardec.data = "variable_declaration"
        item.children.append(vardec)
    else:
        exp = oneOrZero(expression)
        exp.data = "expression"
        item.children.append(exp)
        if literal(";") is None:
            return None

    exp = oneOrZero(expression)
    exp.data = "expression"
    item.children.append(exp)
    if literal(";") is None:
        return None

    exp = oneOrZero(expression)
    exp.data = "expression"
    item.children.append(exp)
    if literal(";") is None:
        return None

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
    item.children.append(st)

    return item


def try_statement():
    item = Item([], "try_statement")

    if literal("try") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
    item.children.append(st)

    ct = anyNumber(catch)
    ct.data = "catch"
    item.children.append(ct)

    if literal("finally") is None:
        item.children.append(Item([], "statement"))
        return item

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
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
    para.data = "parameter"
    item.children.append(para)

    if literal(")") is None:
        return None

    st = onlyOne(statement)
    if st is None:
        return None
    st.data = "statement"
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
    exp.data = "expression"
    item.children.append(exp)

    if literal(")") is None:
        return None
    if literal("{") is None:
        return None

    cases = anyNumber(switch_case)
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
        exp.data = "expression"
        item.children.append(exp)
    else:
        item.children.append(Item([], "default"))

    st = anyNumber(statement)
    st.data = "statement"
    item.children.append(st)

    return item


def expression():
    item = Item([], "expression")

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
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp.data = "expression"
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item
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
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp.data = "expression"
        item.children.append(exp)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item

    l = literal("true")
    if l is not None:
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item

    l = literal("false")
    if l is not None:
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
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
        item.children.append(l)
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp.data = "expression"
        item.children.append(exp)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # castex = onlyOne(casting_expression)
    # if castex is not None:
    #     castex.data = "casting_expression"
    #     item.children.append(castex)
    #     return item

    l = literal("(")
    if l is not None:
        typ = onlyOne(type)
        if typ is None:
            return None
        typ.data = "type"
        item.children.append(typ)

        if literal(")") is None:
            return None

        exp = onlyOne(expression)
        if exp is None:
            return None
        exp.data = "expression"
        item.children.append(exp)

        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # createex = onlyOne(creating_expression)
    # if createex is not None:
    #     createex.data = "creating_expression"
    #     item.children.append(createex)
    #     return item
    crex = onlyOne(creating_expression)
    if crex is not None:
        item.children.append(crex)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # litex = onlyOne(literal_expression)
    # if litex is not None:
    #     litex.data = "literal_expression"
    #     item.children.append(litex)
    #     return item
    litex = onlyOne(literal_expression)
    if litex is not None:
        item.children.append(litex)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # null = literal("null")
    # if null is not None:
    #     item.children.append(null)
    #     return item
    l = literal("null")
    if l is not None:
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # spr = literal("super")
    # if spr is not None:
    #     item.children.append(spr)
    #     return item
    l = literal("super")
    if l is not None:
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # ths = literal("this")
    # if ths is not None:
    #     item.children.append(ths)
    #     return item
    l = literal("this")
    if l is not None:
        item.children.append(l)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    # iden = onlyOne(identifier)
    # if iden is not None:
    #     iden.data = "identifier"
    #     item.children.append(iden)
    #     return item
    iden = onlyOne(identifier)
    if iden is not None:
        iden.data = "identifier"
        item.children.append(iden)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    #
    if literal("(") is not None:
        exp = onlyOne(expression)
        if exp is None:
            return None
        exp.data = "expression"
        item.children.append(exp)
        if literal(")") is None:
            return None
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
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
    item = Item([], "expression")

    symbols = {"++", "--"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item

    symbols = {"+", "+=", "-", "-=", "*", "*=", "/", "/=", "%", "%="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp.data = "expression"
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item


    symbols = {">", "<", ">=", "<=", "==", "!="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            exp = onlyOne(expression)
            if exp is None:
                return None
            exp.data = "expression"
            item.children.append(exp)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item


    symbols = {"&", "&=", "|", "|=", "^", "^=", "&&", "||=", "%", "%="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            exptwo = onlyOne(expression)
            if exptwo is None:
                return None
            exptwo.data = "expression"
            item.children.append(exptwo)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item

    l = literal("?")
    if l is not None:
        item.children.append(l)
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo.data = "expression"
        item.children.append(exptwo)
        ltwo = literal(":")
        if ltwo is not None:
            item.children.append(ltwo)
            expthree = onlyOne(expression)
            if expthree is None:
                return None
            expthree.data = "expression"
            item.children.append(expthree)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item

    symbols = {"+", "+="}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            exptwo = onlyOne(expression)
            if exptwo is None:
                return None
            exptwo.data = "expression"
            item.children.append(exptwo)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item


    symbols = {">>=", "<<", ">>", ">>>"}
    for symbol in symbols:
        l = literal(symbol)
        if l is not None:
            item.children.append(l)
            exptwo = onlyOne(expression)
            if exptwo is None:
                return None
            exptwo.data = "expression"
            item.children.append(exptwo)
            expp = onlyOne(expression_prime)
            if expp is None:
                return item
            expp.data = "expression_p"
            item.children.append(expp)
            return item


    if literal("(") is not None:
        alist = oneOrZero(arglist)
        alist.data = "arglist"
        item.children.append(alist)
        if literal(")") is None:
            return None
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    elif literal("[") is not None:
        item.children.append(Item([], "[]"))
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo.data = "expression"
        item.children.append(exptwo)
        if literal("]") is None:
            return None
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    elif literal(".") is not None:
        item.children.append(Item([], "."))
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo.data = "expression"
        item.children.append(exptwo)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    elif literal(",") is not None:
        item.children.append(Item([], ","))
        exptwo = onlyOne(expression)
        if exptwo is None:
            return None
        exptwo.data = "expression"
        item.children.append(exptwo)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item
    elif literal("instanceof") is not None:
        item.children.append(Item([], "isntanceof"))
        name = oneOf({class_name, interface_name})
        if name is None:
            return None
        name.data = "name"
        item.children.append(name)
        expp = onlyOne(expression_prime)
        if expp is None:
            return item
        expp.data = "expression_p"
        item.children.append(expp)
        return item

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
        name.data = "class_name"
        item.children.append(name)
        if literal("(") is None:
            return None
        alist = oneOrZero(arglist)
        alist.data = "arglist"
        item.children.append(alist)
        if literal(")") is None:
            return None
        return item

    typ = onlyOne(type_specifier)
    if typ is not None:
        typ.data = "type_specifier"
        item.children.append(typ)
        if literal("[") is not None:
            exp = oneOrZero(expression)
            exp.data = "expression"
            item.children.append(exp)
            if exp.children[0] is None:
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
        exp.data = "expression"
        item.children.append(exp)
        if literal(")") is None:
            return None
        return item

    return None


def literal_expression():
    item = Item([], "literal_expression")

    ltrl = oneOf({integer_literal, float_literal, character, string})
    if ltrl is None:
        return None
    ltrl = ltrl.children[0]
    item.children.append(ltrl)

    return item


def arglist():
    item = Item([], "arglist")

    alist = oneOrMany(expression)
    if alist is None:
        return None
    alist.data = "arglist"
    item.children.append(alist)

    return item


def type():
    item = Item([], "type")

    typsp = onlyOne(type_specifier)
    if typsp is None:
        return None
    typsp.data = "type_specifier"
    item.children.append(typsp)

    arry = anyNumber(array_braces)
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
        clnm.data = "class_name"
        item.children.append(clnm)
        return item

    innm = onlyOne(interface_name)
    if innm is not None:
        innm.data = "interface_name"
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
    iden.data = "identifier"
    item.children.append(iden)

    l = literal(".")
    if l is not None:
        item.children.append(l)
        pname = onlyOne(package_name())
        if pname is not None:
            item.children.extend(pname.children)
        else:
            iden = onlyOne(identifier)
            if iden is None:
                return None
            iden.data = "identifier"
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

    iden = onlyOne(identifier)
    if iden is not None:
        item.children.append(iden)
        return item

    pname = onlyOne(package_name)
    if pname is not None:
        item.children.append(pname)
        iden = onlyOne(identifier)
        if iden is not None:
            item.children.append(iden)
            return item

    return None


def interface_name():
    item = Item([], "interface_name")

    iden = onlyOne(identifier)
    if iden is not None:
        item.children.append(iden)
        return item

    pname = onlyOne(package_name)
    if pname is not None:
        item.children.append(pname)
        iden = onlyOne(identifier)
        if iden is not None:
            item.children.append(iden)
            return item

    return None


def integer_literal():
    item = Item([], "integer_literal")

    if peekToken().id != "int":
        return None

    n = peekToken().word
    try:
        value = int(n)
        item.children.append([], value)
        nextTokenAnyLine()
        return item
    except ValueError:
        return None


def float_literal():
    item = Item([], "float_literal")

    if peekToken().id != "float":
        return None

    n = peekToken().word
    try:
        value = float(n)
        item.children.append([], value)
        nextTokenAnyLine()
        return item
    except ValueError:
        return None

#
# def decimal_digits():
#     return

#
# def exponent_part():
#     return
#
#
# def float_type_suffix():
#     return


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
#          test = Scanner()

#          test.prepFile("java.txt")
# for n in test.progNodes:
#     print(n.toString())
#          main(test.progNodes)
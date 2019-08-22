from tokenizer import tokenizer,transfer_XML
import pdb

OPS = ['+','-','*','/','&amp;','|','&lt;','&gt;','=']    
UNARYOPS = ['-','~']
KEYWORDCONSTANTS = ['true','false','null','this']
STATEMENTS = ['let','if','while','do','return']

class Node:
    def __init__(self, tag='class', level=0, value='', category=None):
        self.tag = tag
        self.level = level
        self.value = value
        self.children = []
        self.isTerminate = True if value else False

    def __repr__(self):
        return self.tag+':'+str(self.level)+':'+self.value+':'+str(self.isTerminate)

class CompilationEngine:

    def __init__(self, inputPath):
        with open(inputPath,'r') as f:
            content = f.read()
        self.tokens = tokenizer(content)
        self.curIdx = 0
        self.tree = Node()
        self.compileClass()

    def writeXML(self,target_path = './out.xml'):
        with open(target_path, 'w') as f:
            f.write(self.XML)
        
    def treeToXml(self, targetPath = './test.xml'):
        tree = self.tree
        arr = []
        self.treeToXmlHelper(tree, arr)
        ret = ''.join(arr)
        with open(targetPath,'w') as f:
            f.write(ret)

    def treeToXmlHelper(self, tree, arr):
        if tree.isTerminate:
            arr += [transfer_XML(tree.value, tree.tag)]
        else:
            tag = tree.tag
            openTag = '<'+tag+'>\n'
            closeTag = '</'+tag+'>\n'
            arr+= [openTag]
            for child in tree.children:
                self.treeToXmlHelper(child, arr)
            arr+=[closeTag]


    '''
    'class' className '{' classVarDec* subroutineDec* '}'
    '''
    def compileClass(self):
        tokens = self.tokens
        tree = self.tree

        self.consume('class', 'keyword', tree)

        self.consume(e_type = 'identifier', tree = tree)

        self.consume('{', 'symbol', tree = tree)

        while tokens[self.curIdx][0] == 'field' or tokens[self.curIdx][0] == 'static':
            self.compileClassVarDec(tree)            

        while tokens[self.curIdx][0] in ['constructor', 'function', 'method']:
            self.compileSubroutineDec(tree)

        self.consume('}', 'symbol', tree = tree)


    '''    
    ('static'|'field')type varName(','varName)*';'
    '''
    def compileClassVarDec(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='classVarDec',level=parentTree.level+1)
        parentTree.children += [tree]
        
        self.consume(['static','field'],'keyword',tree = tree)

        self.consume(e_type = ['keyword','identifier'], tree= tree)

        self.consume(e_type = 'identifier', tree = tree)
        
        while tokens[self.curIdx][0] != ';':
            self.consume(',','symbol', tree = tree)
            self.consume(e_type = 'identifier', tree = tree)

        self.consume(';','symbol', tree = tree)


    '''
    ('constructor'|'function'|'method')('void'|type) subroutineName '(' parameterList ')' subroutineBody
    constructor Square new(int Ax, int Ay, int Asize) 
    '''
    def compileSubroutineDec(self, parentTree):

        tree = Node(tag='subroutineDec',level=parentTree.level+1)
        parentTree.children += [tree]
    
        self.consume(['constructor', 'function', 'method'], 'keyword', tree = tree)
        
        self.consume(e_type = ['identifier', 'keyword'], tree = tree)

        self.consume(e_type = 'identifier', tree = tree)

        self.consume('(','symbol', tree = tree)
        
        self.compileParameterList(tree)

        self.consume(')','symbol', tree = tree)

        self.compileSubroutineBody(tree)



    '''
    ((type varName)(','type varName)*)?
    '''
    def compileParameterList(self, parentTree):
        tokens = self.tokens
        
        tree = Node(tag='parameterList',level=parentTree.level+1)
        parentTree.children += [tree]

        while tokens[self.curIdx][0] != ')':
            self.consume(e_type = ['keyword','identifier'], tree=tree)
            self.consume(e_type = ['identifier'], tree = tree)
            if tokens[self.curIdx][0] == ',': self.consume(',','symbol', tree=tree)

    '''
    '{' varDec* statements '}'
    '''
    def compileSubroutineBody(self, parentTree):
        tokens = self.tokens
        
        tree = Node(tag='subroutineBody',level=parentTree.level+1)
        parentTree.children += [tree]

        self.consume('{', 'symbol', tree=tree)

        while tokens[self.curIdx][0] == 'var': self.compileVarDec(tree)
        
        self.compileStatements(tree)

        self.consume('}', 'symbol', tree=tree)


    '''
    'var' type varName(','varName)*';'
    '''
    def compileVarDec(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='varDec',level=parentTree.level+1)
        parentTree.children += [tree]
        
        self.consume('var', 'keyword', tree=tree)

        self.consume(e_type = ['identifier','keyword'], tree=tree)

        self.consume(e_type = 'identifier', tree=tree)

        while tokens[self.curIdx][0] != ';':
            self.consume(',','symbol', tree=tree)
            self.consume(e_type = 'identifier', tree=tree)

        self.consume(';','symbol', tree=tree)


    '''
    statement*
    statement: letStatement| ifStatement| whileStatement| doStatement| returnStatement
    '''
    def compileStatements(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='statements',level=parentTree.level+1)
        parentTree.children += [tree]
            
        while tokens[self.curIdx][0] in STATEMENTS:
            st = tokens[self.curIdx][0]
            if st == 'let': self.compileLet(tree)
            elif st == 'if': self.compileIf(tree)
            elif st == 'while': self.compileWhile(tree)
            elif st == 'do': self.compileDo(tree)
            elif st == 'return': self.compileReturn(tree)

    '''
    let varName('[' expression ']')?'='expression';'
    '''
    def compileLet(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='letStatement',level=parentTree.level+1)
        parentTree.children += [tree]
        
        self.consume('let', 'keyword', tree=tree)

        self.consume(e_type = 'identifier', tree=tree)

        if tokens[self.curIdx][0] == '[':
            self.consume('[','symbol', tree=tree)
            self.compileExpression(tree)
            self.consume(']','symbol', tree=tree)

        self.consume('=', 'symbol', tree=tree)
        self.compileExpression(tree)
        self.consume(';', 'symbol', tree=tree)


    '''
    'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    '''    
    def compileIf(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='ifStatement',level=parentTree.level+1)
        parentTree.children += [tree]
        
        self.consume('if', 'keyword', tree=tree)
        self.consume('(', 'symbol', tree=tree)
        self.compileExpression(tree)   
        self.consume(')', 'symbol', tree=tree)

        self.consume('{', 'symbol', tree=tree)
        self.compileStatements(tree)
        self.consume('}', 'symbol', tree=tree)

        if tokens[self.curIdx][0] == 'else':
            self.consume('else','keyword', tree=tree)
            self.consume('{', 'symbol', tree=tree)
            self.compileStatements(tree)
            self.consume('}','symbol', tree=tree)


    '''
    'while' '(' expression ')' '{' statements '}'
    '''
    def compileWhile(self, parentTree):
        
        tree = Node(tag='whileStatement',level=parentTree.level+1)
        parentTree.children += [tree]

        self.consume('while','keyword', tree=tree)
        self.consume('(','symbol', tree=tree)
        self.compileExpression(tree)
        self.consume(')','symbol', tree=tree)

        self.consume('{','symbol', tree=tree)
        self.compileStatements(tree)
        self.consume('}','symbol', tree=tree)


    '''
    'do' subroutineCall ';'
    '''
    def compileDo(self, parentTree):
        
        tree = Node(tag='doStatement',level=parentTree.level+1)
        parentTree.children += [tree]

        self.consume('do','keyword', tree=tree)
        self.compileSubroutineCall(tree)
        self.consume(';','symbol', tree=tree)


    '''
    'return' expression?';'
    '''
    def compileReturn(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='returnStatement',level=parentTree.level+1)
        parentTree.children += [tree]

        self.consume('return','keyword', tree=tree)
        if tokens[self.curIdx][0] != ';':
            self.compileExpression(tree)
        self.consume(';','symbol', tree=tree)


    '''
    term (op term)*
    '''
    def compileExpression(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='expression',level=parentTree.level+1)
        parentTree.children += [tree]

        self.compileTerm(tree)
        
        while tokens[self.curIdx][0] in OPS:
            op = tokens[self.curIdx][0]
            self.consume(op, 'symbol', tree=tree) 
            self.compileTerm(tree)


    '''
    integerConstant|stringConstant|keywordConstant|varName|varName'['expression']'|subroutineCall|'('expression')'|unaryOp term
    '''
    def compileTerm(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='term',level=parentTree.level+1)
        parentTree.children += [tree]

        cur_token,cur_type = tokens[self.curIdx][0],tokens[self.curIdx][1]
        next_token = tokens[self.curIdx+1][0]

        if next_token == '[':
            self.consume(e_type = 'identifier',tree=tree)
            self.consume('[','symbol',tree=tree)
            self.compileExpression(tree)
            self.consume(']','symbol',tree=tree)
        elif cur_token == '(':
            self.consume('(','symbol',tree=tree)
            self.compileExpression(tree)
            self.consume(')','symbol',tree=tree)
        elif cur_token in UNARYOPS:
            self.consume(cur_token, 'symbol',tree=tree)
            self.compileTerm(tree)
        elif cur_type == 'identifier' and next_token in ['(','.']:
            self.compileSubroutineCall(tree)
        else:
            self.consume(tree=tree)


    '''
    expression(','expression)*)?
    '''
    def compileExpressionList(self, parentTree):
        tokens = self.tokens

        tree = Node(tag='expressionList',level=parentTree.level+1)
        parentTree.children += [tree]

        if tokens[self.curIdx][0] != ')':
            self.compileExpression(tree)
            while tokens[self.curIdx][0] != ')':
                self.consume(',','symbol',tree=tree) 
                self.compileExpression(tree)


    '''
    subroutineCall: subroutineName'('expressionList')'|(className|varName)'.'subroutineName'('expressionList')'
    '''
    def compileSubroutineCall(self, parentTree):
        tokens = self.tokens
        tree = parentTree
        self.consume(e_type = 'identifier', tree=tree)
        if tokens[self.curIdx][0] == '.':
            self.consume('.','symbol', tree=tree)
            self.consume(e_type = 'identifier', tree=tree)
        self.consume('(','symbol', tree=tree)
        self.compileExpressionList(tree)
        self.consume(')','symbol', tree=tree)

    def getAndVerify(self, idx, e_token = None, e_type = None, tree = None):
        tokens = self.tokens
        token,_type = tokens[idx][0], tokens[idx][1]
        if e_token: 
            if type(e_token) is str: assert token == e_token
            elif type(e_token) is list:
                if not token in e_token: 
                    raise Exception(f"token {token} not in {e_token}")
        if e_type:
            if type(e_type) is str: assert _type == e_type
            elif type(e_type) is list:
                if not _type in e_type: raise Exception(f"_type {_type} not in {e_type}")
        if tree:
            tree.children += [Node(tag = _type, value = token, level = tree.level+1)]
        return token,_type
    
    def consume(self, e_token=None, e_type=None, tree = None):
        token,_type = self.getAndVerify(self.curIdx, e_token, e_type, tree)
        self.curIdx +=1

        
def batch_test():
    for jack_path,target_path in [  ['../test/ArrayTest/Main.jack', '../test/engine_test/array_main_actual.xml'],
                                    ['../test/Square/Main.jack', '../test/engine_test/square_main_actual.xml'],
                                    ['../test/Square/Square.jack', '../test/engine_test/square_actual.xml'],
                                    ['../test/Square/SquareGame.jack', '../test/engine_test/square_game_actual.xml'],
                                    ['../test/ExpressionLessSquare/Main.jack', '../test/engine_test/exp_main_actual.xml'],
                                    ['../test/ExpressionLessSquare/Square.jack', '../test/engine_test/exp_actual.xml'],
                                    ['../test/ExpressionLessSquare/SquareGame.jack', '../test/engine_test/exp_game_actual.xml']
                                ]:
        print(jack_path)
        print(target_path)
        CompilationEngine(jack_path).treeToXml(target_path)
        

if __name__ == '__main__':
    #inputPath = '../test/Square/Square.jack'
    #targetPaht = '../test/engine_test/square_actual.xml'

    #ce = CompilationEngine(inputPath)
    #ce.treeToXml(targetPaht)
    

    batch_test()

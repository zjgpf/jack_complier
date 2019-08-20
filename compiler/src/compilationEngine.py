from tokenizer import tokenizer,transfer_XML,KEYWORDS,SYMBOLS
import pdb

OPS = ['+','-','*','/','&','|','<','>','=']    
UNARYOPS = ['-','~']
KEYWORDCONSTANTS = ['true','false','null','this']

class CompilationEngine:

    def __init__(self, inputPath):
        with open(inputPath,'r') as f:
            content = f.read()
        self.tokens = tokenizer(content)
        self.curIdx = 0
        self.XMLArr = []
        self.compileClass()


    '''
    'class' className '{' classVarDec* subroutineDec* '}'
    '''
    def compileClass(self):
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<class>\n']
        
        #verify token is 'class' and type is keyword
        self.consume('class', 'keyword')

        self.consume(e_type = 'identifier')

        self.consume('{', 'symbol')

        while tokens[self.curIdx][0] == 'field' or tokens[self.curIdx][0] == 'static':
            self.compileClassVarDec()            

        while tokens[self.curIdx][0] in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()

        XMLArr += ['</class>\n']
    
        self.printXML()
        


    '''    
    ('static'|'field')type varName(','varName)*';'
    '''
    def compileClassVarDec(self):
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<classVarDec>\n']
        
        self.consume(['static','field'],'keyword')

        self.consume(e_type = ['keyword','identifier'])

        self.consume(e_type = 'identifier')
        
        while tokens[self.curIdx][0] != ';':
            self.consume(',','symbol')
            self.consume(e_type = 'identifier')

        self.consume(';','symbol')
        XMLArr += ['</classVarDec>\n']


    '''
    ('constructor'|'function'|'method')('void'|type) subroutineName '(' parameterList ')' subroutineBody
    constructor Square new(int Ax, int Ay, int Asize) 
    '''
    def compileSubroutineDec(self):
        #tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<subroutineDec>\n']
    
        self.consume(['constructor', 'function', 'method'], 'keyword')
        
        self.consume(e_type = ['identifier', 'keyword'])

        self.consume(e_type = 'identifier')

        self.consume('(','symbol')
        
        self.compileParameterList()

        self.consume(')','symbol')

        self.compileSubroutineBody()

        XMLArr += ['</subroutineDec>\n']


    '''
    ((type varName)(','type varName)*)?
    '''
    def compileParameterList(self):
        tokens = self.tokens
        XMLArr = self.XMLArr
        
        XMLArr += ['<parameterList>\n']

        while tokens[self.curIdx][0] != ')':
            self.consume(e_type = ['keyword','identifier'])
            self.consume(e_type = ['identifier'])
            if tokens[self.curIdx][0] == ',': self.consume(',','symbol')

        XMLArr += ['</parameterList>\n']
        

    '''
    '{' varDec* statements '}'
    '''
    def compileSubroutineBody(self):
        XMLArr = self.XMLArr
        tokens = self.tokens
        
        XMLArr += ['<subroutineBody>\n']

        self.consume('{', 'symbol')

        while tokens[self.curIdx][0] == 'var': self.compileVarDec()
        
        self.compileStatements()

        #self.consume('}', 'symbol')
        
        XMLArr += ['</subroutineBody>\n']


    '''
    'var' type varName(','varName)*';'
    '''
    def compileVarDec(self):
        XMLArr = self.XMLArr
        tokens = self.tokens

        XMLArr += ['<varDec>\n']
        
        self.consume('var', 'keyword')

        self.consume(e_type = ['identifier','keyword'])

        self.consume(e_type = 'identifier')

        while tokens[self.curIdx][0] != ';':
            self.consume(',','symbol')
            self.consume(e_type = 'identifier')

        self.consume(';','symbol')

        XMLArr += ['</varDec>\n']

    '''
    statement*
    statement: letStatement| ifStatement| whileStatement| doStatement| returnStatement
    '''
    def compileStatements(self):
        XMLArr = self.XMLArr
        tokens = self.tokens

        XMLArr += ['<statements>\n']
            
        st = tokens[self.curIdx][0]
        if st == 'let': self.compileLet()
        elif st == 'if': self.compileIf()
        elif st == 'while': self.compileWhile()
        elif st == 'do': self.compileDo()
        elif st == 'return': self.compileReturn()
        else: raise Exception(f'Invalid statement {st}')

        XMLArr += ['</statements>\n']
        

    '''
    let varName('[' expression ']')?'='expression';'
    '''
    def compileLet(self):
        XMLArr = self.XMLArr
        tokens = self.tokens

        XMLArr += ['<letStatement>\n']
        
        self.consume('let', 'keyword')

        self.consume(e_type = 'identifier')

        if tokens[self.curIdx][0] == '[':
            self.consume('[','symbol')
            self.compileExpression()
            self.consume(']','symbol')

        self.consume('=', 'symbol')
        self.compileExpression()
        self.consume(';', 'symbol')

        XMLArr += ['</letStatement>\n']

    '''
    'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    '''    
    def compileIf(self):
        XMLArr = self.XMLArr
        tokens = self.tokens

        XMLArr += ['<ifStatement>\n']
        
        self.consume('if', 'keyword')
        self.consume('(', 'symbol')
        self.compileExpression()   
        self.consume(')', 'symbol')

        self.consume('{', 'symbol')
        self.compileStatements()
        self.consume('}', 'symbol')

        if tokens[self.curIdx][0] == 'else':
            self.consume('else','keyword')
            self.consume('{', 'symbol')
            self.compileStatements
            self.consume('}','symbol')

        XMLArr += ['</ifStatement>\n']

    '''
    'while' '(' expression ')' '{' statements '}'
    '''
    def compileWhile(self):
        XMLArr = self.XMLArr
        
        XMLArr += ['<whileStatement>\n']

        self.consume('while','keyword')
        self.consume('(','symbol')
        self.compileExpression()
        self.consume(')','symbol')

        self.consume('{','symbol')
        self.compileStatements()
        self.consume('}','symbol')

        XMLArr += ['/<whileStatement>\n']

    '''
    'do' subroutineCall ';'
    '''
    def compileDo(self):
        XMLArr = self.XMLArr
        
        XMLArr += ['<doStatement>\n']

        self.consume('do','keyword')
        self.compileSubroutineCall()
        self.consume(';','symbol')

        XMLArr += ['</doStatement>\n']


    '''
    'return' expression?';'
    '''
    def compileReturn(self):
        XMLArr = self.XMLArr
        tokens = self.tokens

        self.consume('return','keyword')
        if tokens[self.curIdx][0] != ';':
            self.compileExpression()
        self.consume(';','symbol')

    '''
    term (op term)*
    '''
    def compileExpression(self):
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<expression>\n']

        self.compileTerm()
        
        while tokens[self.curIdx][0] in OPS:
            op = tokens[self.curIdx][0]
            self.consume(op, 'symbol') 
            self.compileTerm()

        XMLArr += ['</expression>\n']

    '''
    integerConstant|stringConstant|keywordConstant|varName|varName'['expression']'|subroutineCall|'('expression')'|unaryOp term
    '''
    def compileTerm(self):
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<term>\n']

        cur_token,cur_type = tokens[self.curIdx][0],tokens[self.curIdx][1]
        next_token = tokens[self.curIdx+1][0]

        if next_token == '[':
            self.consume(e_type = 'identifier')
            self.consume('[','symbol')
            self.compileExpression()
            self.consume(']','symbol')
        elif cur_token == '(':
            self.consume('(','symbol')
            self.compileExpression()
            self.consume(')','symbol')
        elif cur_token in UNARYOPS:
            self.consume(cur_token, 'symbol')
            self.compileTerm()
        elif cur_type == 'identifier' and next_token in ['(','.']:
            self.compileSubroutineCall()
        else:
            self.consume()

        XMLArr += ['</term>\n']

    '''
    expression(','expression)*)?
    '''
    def compileExpressionList(self):
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<expressionList>\n']

        if tokens[self.curIdx][0] != ')':
            self.compileExpression()
            while tokens[self.curIdx][0] != ')':
                self.consume(',','symbol') 
                self.compileExpression()

        XMLArr += ['</expressionList>\n']

    '''
    subroutineCall: subroutineName'('expressionList')'|(className|varName)'.'subroutineName'('expressionList')'
    '''
    def compileSubroutineCall(self):
        tokens = self.tokens
        self.consume(e_type = 'identifier')
        if tokens[self.curIdx][0] == '.':
            self.consume('.','symbol')
            self.consume(e_type = 'identifier')
        self.consume('(','symbol')
        self.compileExpressionList()
        self.consume(')','symbol')

    def getAndVerify(self, idx, e_token = None, e_type = None):
        tokens = self.tokens
        token,_type = tokens[idx][0], tokens[idx][1]
        if e_token: 
            if type(e_token) is str: assert token == e_token
            elif type(e_token) is list:
                if not token in e_token: raise Exception(f"token {token} not in {e_token}")
        if e_type:
            if type(e_type) is str: assert _type == e_type
            elif type(e_type) is list:
                if not _type in e_type: raise Exception(f"_type {_type} not in {e_type}")
        return token,_type
    
    def consume(self, e_token=None, e_type=None):
        token,_type = self.getAndVerify(self.curIdx, e_token, e_type)
        self.XMLArr += [transfer_XML(token, _type)]
        self.curIdx +=1

    def printXML(self):
        for tag in self.XMLArr:
            print(tag, end="")
        

if __name__ == '__main__':
    inputPath = '../test/Square/Square.jack'
    inputPath = '../test/Square/Main.jack'
    ce = CompilationEngine(inputPath)

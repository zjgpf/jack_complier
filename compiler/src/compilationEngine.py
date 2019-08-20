from tokenizer import tokenizer,transfer_XML,KEYWORDS,SYMBOLS
import pdb

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
        
        self.consume(e_type = 'identifier')

        self.consume(e_type = 'identifier')

        self.consume('(','symbol')
        
        self.compileParameterList()

        self.consume(')','symbol')

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
        

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        pass

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

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
    ce = CompilationEngine(inputPath)

from tokenizer import tokenizer,transfer_XML
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
        curIdx = self.curIdx
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<class>\n']
        
        #verify token is 'class' and type is keyword
        token,_type = self.getAndVerify(curIdx,e_token = 'class', e_type = 'keyword')
        XMLArr += [transfer_XML(token, _type)]
        
        curIdx += 1

        #verify type is identifier
        token,_type = self.getAndVerify(curIdx, e_type = 'identifier')
        XMLArr += [transfer_XML(token, _type)]

        curIdx += 1

        #verify token is '{' and type is symbol
        token,_type = self.getAndVerify(curIdx,'{', 'symbol')
        XMLArr += [transfer_XML(token, _type)]

        curIdx += 1
        self.curIdx = curIdx

        #while tokens[self.curIdx][0] == 'field' or tokens[self.curIdx][0] == 'static':
            #self.compileClassVarDec()            



        XMLArr += ['</class>\n']
    
        print(XMLArr)
        
        pass

    def compileClassVarDec(self):
        curIdx = self.curIdx
        tokens = self.tokens
        XMLArr = self.XMLArr

        XMLArr += ['<classVarDec>\n']

        XMLArr += ['</classVarDec>\n']

    def compileSubroutineDec(self):
        pass

    def compileParameterList(self):
        pass

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
        if e_token: assert token == e_token
        if e_type: assert _type == e_type
        return token,_type
        

if __name__ == '__main__':
    inputPath = '../test/Square/Square.jack'
    ce = CompilationEngine(inputPath)

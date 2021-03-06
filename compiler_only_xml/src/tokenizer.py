import os
import pdb
import re

INTEGER_PATTERN = '^[0-9]+$'
IDENTIFIER_PATTERN = '^[a-zA-Z_][a-zA-Z_0-9]*$'


STRING = 'string'
SYMBOL = 'symbol'
KEYWORD = 'keyword'
IDENTIFIER = 'identifier'
INTEGER = 'integer'

TOKEN_OPEN = r'<tokens>'
TOKEN_CLOSE= r'</tokens>'

KEYWORD_START = r'<keyword>'
KEYWORD_CLOSE = r'</keyword>'

IDENTIFIER_START = r'<identifier>'
IDENTIFIER_CLOSE = r'</identifier>'

SYMBOL_START = r'<symbol>'
SYMBOL_CLOSE = r'</symbol>'

STRING_START = r'<stringConstant>'
STRING_CLOSE = r'</stringConstant>'

INTEGER_START = r'<integerConstant>'
INTEGER_CLOSE = r'</integerConstant>'

NEXT_LINE = '\n'

KEYWORDS = ['class' , 'constructor' , 'function' , 'method' ,
'field' , 'static' , 'var' , 'int' , 'char' , 'boolean' ,
'void' , 'true' , 'false' , 'null' , 'this' , 'let' , 'do' ,
'if' , 'else' , 'while' , 'return']

SYMBOLS = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' , '*' ,
'/' , '&' , '|' , '<' , '>' , '=' , '~']

def tokenizer(content):
    tokens_all = []
    content_lines = content.split(NEXT_LINE)
    skip = False
    for line in content_lines:
        line = line.strip()
        if line.startswith('//') or line == '': continue 
        if line.startswith('/**'): skip = True
        if line.endswith('*/'): 
            skip = False
            continue
        if skip: continue
        tokens_line = tokenize_line(line)
        tokens_all += tokens_line
    return tokens_all
    
def generate_token_XML(jack_path, target_path = 'jack.xml'):
    ret = '<tokens>'+NEXT_LINE
    with open(jack_path, 'r') as f:
        content = f.read()
    tokens_all = tokenizer(content)
    for t in tokens_all:
        token,_type = t[0],t[1]
        ret += transfer_XML(token, _type)
    ret += '</tokens>'
    with open(target_path, 'w') as f:
        f.write(ret)

def transfer_XML(token,_type):
    ret = ''
    if _type == STRING:
        ret = STRING_START + ' ' + token + ' ' + STRING_CLOSE + NEXT_LINE
    elif _type == INTEGER:
        ret = INTEGER_START+ ' ' + token + ' ' + INTEGER_CLOSE + NEXT_LINE
    elif _type == KEYWORD:
        ret = KEYWORD_START+ ' ' + token + ' ' + KEYWORD_CLOSE + NEXT_LINE
    elif _type == SYMBOL:
        ret = SYMBOL_START+ ' ' + token + ' ' + SYMBOL_CLOSE + NEXT_LINE
    elif _type == IDENTIFIER:
        ret = IDENTIFIER_START+ ' ' + token + ' ' + IDENTIFIER_CLOSE + NEXT_LINE
    return ret
        
        

def tokenize_line(line):
    line = line.strip()
    tokens = []
    p_start = 0
    p_cur = 0
    length = len(line)

    while p_cur < length: 
        if line[p_cur] in SYMBOLS:
            if p_cur > p_start:
                token = line[p_start:p_cur]
                if token in KEYWORDS:
                    tokens += [[token,KEYWORD]]
                elif len(re.findall(IDENTIFIER_PATTERN,token)) == 1:
                    tokens += [[token,IDENTIFIER]]
                elif len(re.findall(INTEGER_PATTERN,token)) == 1:
                    tokens += [[token,INTEGER]]
                else:
                    raise Exception(f'Unknown identifier {token}')
            token = line[p_cur]
            if token == '>': token = '&gt;'
            elif token == '<': token = '&lt;'
            elif token == '"': token = '&quot;'
            elif token == '&': token = '&amp;'
            elif token == '/' and line[p_cur+1] == '/': break
            tokens += [[token, SYMBOL]]
            p_cur+=1
            p_start = p_cur
        elif line[p_cur] == '"':
            p_cur += 1
            p_start = p_cur
            if p_cur == '"':
                tokens += [["", STRING]]
                p_cur += 1
                p_start = p_cur
                continue
            while p_cur < length and line[p_cur] != '"':
                p_cur += 1
            if p_cur == length:
                raise Exception('Missing " for string')
            tokens += [[line[p_start:p_cur], STRING]]
            p_cur += 1
            p_start = p_cur
            
        elif line[p_cur] == ' ':
            if p_cur > p_start:
                token = line[p_start:p_cur]
                if token in KEYWORDS:
                    tokens += [[token,KEYWORD]]
                elif len(re.findall(INTEGER_PATTERN,token)) == 1:
                    tokens += [[token,INTEGER]]
                elif len(re.findall(IDENTIFIER_PATTERN,token)) == 1:
                    tokens += [[token,IDENTIFIER]]
                else:
                    raise Exception(f'Unknown token {token}')
            p_cur+=1
            p_start = p_cur
        else:
            p_cur+=1

    return tokens

def batch_test():
    for jack_path,target_path in [  ['../test/ArrayTest/Main.jack', '../test/token_test/array_main_actual.xml'],
                                    ['../test/Square/Main.jack', '../test/token_test/square_main_actual.xml'],
                                    ['../test/Square/Square.jack', '../test/token_test/square_actual.xml'],
                                    ['../test/Square/SquareGame.jack', '../test/token_test/square_game_actual.xml'],
                                    ['../test/ExpressionLessSquare/Main.jack', '../test/token_test/exp_main_actual.xml'],
                                    ['../test/ExpressionLessSquare/Square.jack', '../test/token_test/exp_actual.xml'],
                                    ['../test/ExpressionLessSquare/SquareGame.jack', '../test/token_test/exp_game_actual.xml']
                                ]:
        print(jack_path)
        print(target_path)
        generate_token_XML(jack_path, target_path)
        
    
if __name__ == '__main__':
    #JACKPATH='../test/ArrayTest/Main.jack'
    #TARGETPATH = '../test/array_main_actual.xml'

    #JACKPATH='../test/Square/Main.jack'
    #TARGETPATH = '../test/square_main_actual.xml'

    #JACKPATH='../test/Square/Square.jack'
    #TARGETPATH = '../test/square_actual.xml'

    #JACKPATH='../test/Square/SquareGame.jack'
    #TARGETPATH = '../test/square_game_actual.xml'

    #JACKPATH='../test/ExpressionLessSquare/Main.jack'
    #TARGETPATH = '../test/exp_main_actual.xml'

    #JACKPATH='../test/ExpressionLessSquare/Square.jack'
    #TARGETPATH = '../test/exp_actual.xml'

    #JACKPATH='../test/ExpressionLessSquare/SquareGame.jack'
    #TARGETPATH = '../test/exp_game_actual.xml'

    batch_test()

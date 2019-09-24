import sys
import os
import pdb
from tokenizer import tokenizer
from compilationEngine import CompilationEngine

DEFAULTPATH = "/Users/pengfeigao/git/jack_complier/compilerII/test/Seven/Main.jack"

class Compiler:
    def __init__(self, inputPath):
        isDir = True
        if inputPath[-5:] == '.jack': isDir = False
        self.isDir = isDir

        if not isDir:
            with open(inputPath, 'r') as f:
                self.content = f.read()
            fileName = inputPath.split('/')[-1][:-5]
            self.className = fileName
            outputName = fileName+'.vm'
            self.outputPath = inputPath.replace(fileName+'.jack', outputName)

        else:
            contents = {}
            self.fileName = inputPath.split('/')[-1] + '.vm'
            self.outputPath = os.path.join(inputPath,self.fileName)
            files = os.listdir(inputPath)   
            for file in files:
                if not file[-3:] == '.jack': continue
                with open(os.path.join(inputPath,file), 'r') as f:
                    contents[file[:-3]] = f.read()
            
            self.contents = contents

        self.vmCmds = []
    
    def run(self):
        if not self.isDir: self.runSingleFile()
        else: self.runDir()

    def runDir(self):
        pass
       
        #with open(self.outputPath, 'w') as f:
        #    f.write(''.join(asmCmds))
        
        

    def runSingleFile(self, isWrite=True):
        tokens =  tokenizer(self.content)
        engine = CompilationEngine(tokens)
        pdb.set_trace()
        if isWrite:
            with open(self.outputPath, 'w') as f:
                f.write(''.join(asmCmds))
         
        

if __name__ == '__main__':
    args = sys.argv
    if  len(args) < 2: inputPath = DEFAULTPATH
    else: inputPath = sys.argv[1]
    compiler = Compiler(inputPath)
    compiler.run()


from tokenizer import tokenizer
from compilationEngine import CompilationEngine

class Analyzer:

    def __init__(self, inputPath):
        with open(inputPath, 'r') as f:
            content = f.read()
        tokens = tokenizer(content)
        self.engine = CompilationEngine(tokens)


if __name__ == '__main__':
    inputPath = '../test/Square/Square.jack'
    analyzer = Analyzer(inputPath)

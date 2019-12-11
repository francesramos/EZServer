from EZServerLexPar import EZ_Lexer, EZ_Parser
print('Bienvenido a EZServer ver 0.1')

lexer = EZ_Lexer()
parser = EZ_Parser()

while True:
    try:
        command = input('EZServer> ')
    except EOFError:
        break

    #parse code
    tokens = lexer.tokenize(command)
    result = parser.parse(tokens)
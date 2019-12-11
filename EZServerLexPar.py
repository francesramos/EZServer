from sly import Lexer
from sly import Parser
import IntermediateCode as builtin
import operator
class EZ_Lexer(Lexer):
    # Set of Tokens
    tokens = {'SERVERACTIONS', 'ID', 'NUMBER', 'STRING', 'ASSIGN'}

    # Set of tokens to be interpreted as literals
    literals = {'{', '}', ':', '(', ')', ',', '.'}

    # String containing ignored characters
    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'%.*'

    # Regular expressions for tokens.
    STRING = r'\"(.*?)"'
    NUMBER = r'\d+'
    ASSIGN = r':='

    # Special cases
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        identifiers = {
            'crear': 'SERVERACTIONS',
            'conn': 'SERVERACTIONS',
            'reciv': 'SERVERACTIONS',
            'env': 'SERVERACTIONS',
            'cerrar': 'SERVERACTIONS',
            'print': 'SERVERACTIONS',
            'exit': 'SERVERACTIONS'
        }

        if t.value in identifiers:
            t.type = identifiers.get(t.value)

        else:
            t.type = 'ID'

        return t


class EZ_Parser(Parser):
    tokens = EZ_Lexer.tokens

    def __init__(self):
        self.names = {}

    #Syntax

    @_('statementList')
    def declaration(self, p):
        return p.statementList

    @_('function "," statementList')
    def statementList(self, p):
        return p.function, p.statementList

    @_('assignment "," statementList')
    def statementList(self, p):
        return p.assignment, p.statementList

    @_('statement')
    def statementList(self, p):
        return p.statement

    @_('function')
    def statement(self, p):
        return p.function

    @_('assignment')
    def statement(self, p):
        return p.assignment

    @_('ID ASSIGN STRING')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.STRING

    @_('ID ASSIGN NUMBER')
    def assignment(self, p):
        if p.ID in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            self.names[p.ID] = p.NUMBER

    @_('ID ASSIGN ID')
    def assignment(self, p):
        if p.ID0 in self.names.keys():
            raise Exception("Variables are immutable.")
        else:
            if p.ID1 not in self.names.keys():
                raise Exception("Variable " + p.ID1 + " does not exist.")
            else:
                self.names[p.ID0] = self.names[p.ID1]

    @_('ID ASSIGN function')
    def assignment(self, p):
        if p.ID in self.names:
            raise Exception("Variables are immutable.")

        else:
            self.names[p.ID] = p.function

    @_('SERVERACTIONS "{" argumentList "}"')
    def function(self, p):
        try:
            arguments = p.argumentList.split(':')
        except:
            pass

        if p.SERVERACTIONS == 'crear':
            if arguments[0] in self.names:
                raise Exception("Server ya existe.")
            else:
                self.names[arguments[0]] = builtin.crearServer(arguments[1])

        elif p.SERVERACTIONS == 'conn':
            if arguments[0] not in self.names:
                raise Exception("Server no existe.")

            elif arguments[1] in self.names:
                raise Exception("Nombre de conneción ya existe.")

            else:
                self.names[arguments[1]] = builtin.connect(self.names[arguments[0]])

        elif p.SERVERACTIONS == 'reciv':
            if arguments[0] not in self.names:
                raise Exception("Connection does not exist.")

            else:
                return builtin.receiveMsg(self.names[arguments[0]])

        elif p.SERVERACTIONS == 'env':
            if arguments[0] not in self.names:
                raise Exception("Connección no existe.")

            elif arguments[1] in self.names:
                builtin.envMsg(self.names[arguments[0]], self.names[arguments[1]])

            else:
                builtin.envMsg(self.names[arguments[0]], arguments[1])

        elif p.SERVERACTIONS == 'cerrar':
            if arguments[0] not in self.names:
                raise Exception("Connección no existe.")

            else:
                builtin.cerrar(self.names[arguments[0]])
                del self.names[arguments[0]]

        elif p.SERVERACTIONS == 'print':
            if arguments[0] in self.names:
                builtin.display(self.names[arguments[0]])

            else:
                builtin.display(arguments[0])

        elif p.SERVERACTIONS == 'exit':
            builtin.exit()

    @_('argument ":" argumentList')
    def argumentList(self, p):
        return p.argument + ":" + p.argumentList

    @_('argument')
    def argumentList(self, p):
        return p.argument

    @_('ID')
    def argument(self, p):
        return p.ID

    @_('NUMBER')
    def argument(self, p):
        return p.NUMBER

    @_('STRING')
    def argument(self, p):
        return p.STRING

    @_('function')
    def argument(self, p):
        return p.function

    @_('filename')
    def argument(self, p):
        return p.filename

    @_('ID "." ID')
    def filename(self, p):
        if p.ID1 != "ez":
            raise Exception('File must be in EZ format.')
        else:
            return p.ID0 + "." + p.ID1

    @_('empty')
    def argument(self, p):
        return p.empty

    @_('')
    def empty(self, p):
        pass

parser = EZ_Parser()
lexer = EZ_Lexer()



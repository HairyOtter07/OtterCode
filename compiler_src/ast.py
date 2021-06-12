class AST(object):
    pass

class Program(AST):
    def __init__(self, statement_list):
        self.statement_list = statement_list

class Statement(AST):
    def __init__(self, expr):
        self.expr = expr

class FunCall(AST):
    def __init__(self, func, expr_list):
        self.func = func
        self.expr_list = expr_list

class ArithOp(AST):
    def __init__(self, op_token):
        self.token = op_token
        self.op = self.token.value

class Var(AST):
    def __init__(self, id_token):
        self.token = id_token
        self.id = self.token.value

class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

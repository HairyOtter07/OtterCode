from .ast import *
from .errors import ErrorCode, ParserError
from .tokens import TokenType
from .lexer import Lexer

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = self.lexer.get_tokens()
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value}: {token}'
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.token_index += 1
            if self.token_index > len(self.tokens) - 1:
                self.current_token = None
            else:
                self.current_token = self.tokens[self.token_index]
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def peek_next_token(self):
        if self.token_index + 1 > len(self.tokens) - 1:
            return None
        else:
            return self.tokens[self.token_index + 1]

    def program(self):
        """program : statement_list"""
        return Program(self.statement_list())

    def statement_list(self):
        """statement_list : (expr SEMI)*"""
        result = []
        result.append(Statement(self.expr()))
        while self.current_token.type == TokenType.SEMI and self.peek_next_token().type != TokenType.EOF:
            self.eat(TokenType.SEMI)
            result.append(Statement(self.expr()))
        self.eat(TokenType.SEMI)
        return result

    def expr(self):
        """expr : operator COLON LPAREN (expr (COMMA expr)*)? RPAREN | NUMBER"""
        if self.current_token.type == TokenType.NUMBER:
            node = Number(self.current_token)
            self.eat(TokenType.NUMBER)
            return node
        else:
            op = self.operator()
            self.eat(TokenType.COLON)
            self.eat(TokenType.LPAREN)
            expr_list = []
            if self.current_token.type != TokenType.RPAREN:
                expr_list.append(self.expr())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    expr_list.append(self.expr())
            self.eat(TokenType.RPAREN)
            return FunCall(op, expr_list)

    def operator(self):
        """operator : arith_op"""
        if self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            return self.arith_op()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def arith_op(self):
        op = self.current_token
        self.eat(self.current_token.type)
        return ArithOp(op)

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(ErrorCode.INVALID_EOF, self.current_token)
        return node

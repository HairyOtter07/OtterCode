from enum import Enum

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected Token"

class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class SemanticError(Error):
    pass


from typing import Tuple

from .lib.parser import *
from .lib.lexer import *
   
#############################################
# RUN
#############################################

def run(file_name, text) -> Tuple[BinaryOperatorNode, Error]:
    # Generate Tokens:
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    
    # Generate Abstract Syntax Tree:
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None
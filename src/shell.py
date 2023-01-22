from typing import Tuple

from .lib.parser import *
from .lib.lexer import *
from .lib.interpreter import *
from .lib.context import *
   
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
    if ast.error: return None, ast.error

    # Run program (INTERPRETER):
    interpreter = Interpreter()
    context = Context('<9gram>')
    res = interpreter.visit(ast.node, context)

    return res.value, res.error
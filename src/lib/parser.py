from .tokens import *
from .nodes import *
from .constants import *

#############################################
# PARSER
#############################################

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()
        
    def advance(self) -> Token:
        self.token_index += 1;
        if self.token_index < len(self.tokens):
           self.current_token = self.tokens[self.token_index]
        return self.current_token
    
    def parse(self) -> BinaryOperatorNode:
        res = self.expr()

        return res
    
    # Grammar rules:
    def factor(self) -> NumberNode:
        token = self.current_token
        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self) -> BinaryOperatorNode:
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expr(self) -> BinaryOperatorNode:
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))
    
    def binary_operation(self, func, operations) -> BinaryOperatorNode:
        left = func()

        while self.current_token.type in operations:
            operator_token = self.current_token
            self.advance()
            right = func()
            left = BinaryOperatorNode(left, operator_token, right)
            
        return left
     
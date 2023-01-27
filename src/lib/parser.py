from .tokens import *
from .nodes import *
from .constants import *
from .errors import *

#############################################
# PARSE RESULT
#############################################
class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        
        return res
    
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

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
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    "Expected '+', '-', '*' or '/'", self.current_token.loc_start, self.current_token.loc_end
                )
            )
        
        return res
    
    # Grammar rules:
    def atom(self) -> NumberNode:
        res = ParseResult()
        token = self.current_token
        
        if token.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(token))
        
        elif token.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                print("----------------------------")
                print(type(token))
                return res.failure(InvalidSyntaxError(
                    "Expected ')'", self.current_token.loc_start, self.current_token.loc_end
                ))
                
        return res.failure(
                InvalidSyntaxError(
                    "Expected '+', '-', '*' or '/'", token.loc_start, token.loc_end
                )
            )
        
    def power(self) -> BinaryOperatorNode:
        return self.binary_operation(self.atom, (TT_POW, ), self.factor)
    
    def factor(self) -> BinaryOperatorNode:
        res = ParseResult()
        token = self.current_token
        
        if token.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(
                UnaryOperatorNode(token, factor)
            )
        
        return self.power()

    def term(self) -> BinaryOperatorNode:
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expr(self) -> BinaryOperatorNode:
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))
    
    def binary_operation(self, func_a, operations, func_b=None) -> BinaryOperatorNode:
        if not func_b:
            func_b = func_a
        
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_token.type in operations:
            operator_token = self.current_token
            res.register(self.advance())
            right = res.register(func_b())
            if res.error: return res
            left = BinaryOperatorNode(left, operator_token, right)
            
        return res.success(left)
     
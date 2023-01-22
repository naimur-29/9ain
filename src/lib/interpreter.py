from .tokens import *
from .parser import *

#############################################
# RUNTIME RESULT
#############################################

class RuntimeResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res

    def success(self, value):
        self.value = value
        return value

    def failure(self, error):
        self.error = error
        return self

#############################################
# VALUES
#############################################

class Number:
    def __init__(self, value=None) -> None:
        self.value = value 
        self.error = None
        self.set_loc()
        self.set_context()
       
    def set_loc(self, loc_start=None, loc_end=None):
        self.loc_start = loc_start
        self.loc_end = loc_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    # math operators basic operations:
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    "Division by zero not allowed! :)", other.loc_start, other.loc_end, self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        
    def __repr__(self) -> str:
        return str(self.value)

#############################################
# INTERPRETER
#############################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined!')
    
    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_loc(node.loc_start, node.loc_end)
        )

    def visit_BinaryOperatorNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res
        
        if node.operator_token.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.operator_token.type == TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.operator_token.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.operator_token.type == TT_DIV:
            result, error = left.divided_by(right)
            
        if error:
            return res.failure(error)
        return res.success(result.set_loc(node.loc_start, node.loc_end))
        
    def visit_UnaryOperatorNode(self, node, context):
        res = RuntimeResult()
        result = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None        
        if node.operator_token.type == TT_MINUS:
            result, error = result.multiplied_by(Number(-1))
        
        if error:
            return res.failure(error)
        return res.success(result.set_loc(node.loc_start, node.loc_end))
#############################################
# NODES
#############################################        
class NumberNode:
    def __init__(self, token) -> None:
       self.token = token
       
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOperatorNode:
    def __init__(self, left_node, operator_token, right_node) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        
    def __repr__(self) -> str:
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'
    
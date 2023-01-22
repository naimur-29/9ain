#############################################
# NODES
#############################################        
class NumberNode:
    def __init__(self, token) -> None:
       self.token = token
       self.loc_start = self.token.loc_start
       self.loc_end = self.token.loc_end
       
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOperatorNode:
    def __init__(self, left_node, operator_token, right_node) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        
        self.loc_start = self.left_node.loc_start
        self.loc_end = self.right_node.loc_end
        
    def __repr__(self) -> str:
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'
    
class UnaryOperatorNode:
    def __init__(self, operator_token, node) -> None:
        self.operator_token = operator_token 
        self.node = node
        
        self.loc_start = self.operator_token.loc_start
        self.loc_end = self.node.loc_end

    def __repr__(self) -> str:
        return f'({self.operator_token}, {self.node})'
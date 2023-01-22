#############################################
# TOKENS
#############################################

TT_INT      = 'TT_INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF      = 'EOF'

class Token:
    def __init__(self, type_, value=None, loc_start=None, loc_end=None) -> None:
        self.type = type_
        self.value = value
        
        if loc_start:
            self.loc_start = loc_start.copy()
            self.loc_end = loc_start.copy()
            self.loc_end.advance()

        if loc_end:
            self.loc_end = loc_end
    
    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'
    
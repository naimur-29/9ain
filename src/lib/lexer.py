from typing import Tuple, List

from .errors import *
from .tokens import *
from .location import *
from .constants import *

#############################################
# LEXER
#############################################

class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.loc = Location(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()
        
    def advance(self) -> None:
        self.loc.advance(self.current_char)
        self.current_char = self.text[self.loc.index] if self.loc.index < len(self.text) else None
        
    def make_tokens(self) -> Tuple[List[Token], Error]:
        tokens = []
        
        while self.current_char:
            # Handling spaces:
            if self.current_char in ' \t':
                self.advance()
                
            # Handling digits:
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                
            # Handling operators:
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, loc_start=self.loc))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, loc_start=self.loc))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, loc_start=self.loc))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, loc_start=self.loc))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, loc_start=self.loc))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, loc_start=self.loc))
                self.advance()
            else:
                loc_start = self.loc.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f"'{char}'", loc_start, self.loc)
        
        tokens.append(Token(TT_EOF))
        return tokens, None
                
    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0
        loc_start = self.loc.copy()
        
        while self.current_char and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
                
        if dot_count:
            return Token(TT_FLOAT, float(num_str), loc_start, self.loc)
        else:
            return Token(TT_INT, int(num_str), loc_start, self.loc)
        
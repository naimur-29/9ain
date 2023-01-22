#############################################
# ERRORS
#############################################

from .string_with_arrows import *

class Error:
    def __init__(self, error_name, details,  loc_start, loc_end) -> None:
        self.error_name = error_name
        self.details = details
        self.loc_start = loc_start
        self.loc_end = loc_end
    
    def as_string(self) -> str:
        res = f'{self.error_name}: {self.details}\n'
        res += f'File {self.loc_start.file_name}, Line: {self.loc_start.line + 1}'
        res += '\n\n' + string_with_arrows(self.loc_start.file_content, self.loc_start, self.loc_end)
        
        return res
        
class IllegalCharError(Error):
    def __init__(self, details, loc_start, loc_end) -> None:
        super().__init__('Illegal Character', details, loc_start, loc_end)
        
class InvalidSyntaxError(Error):
    def __init__(self, details, loc_start, loc_end) -> None:
        super().__init__('Invalid Syntax', details, loc_start, loc_end)
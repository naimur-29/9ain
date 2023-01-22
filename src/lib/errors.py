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
        res = f'===> {self.error_name}: {self.details} <===\n'
        res += f'File {self.loc_start.file_name}, Line: {self.loc_start.line + 1}'
        res += '\n\n' + string_with_arrows(self.loc_start.file_content, self.loc_start, self.loc_end)
        
        return res
        
class IllegalCharError(Error):
    def __init__(self, details, loc_start, loc_end) -> None:
        super().__init__('Illegal Character', details, loc_start, loc_end)
        
class InvalidSyntaxError(Error):
    def __init__(self, details, loc_start, loc_end) -> None:
        super().__init__('Invalid Syntax', details, loc_start, loc_end)        

class RuntimeError(Error):
    def __init__(self, details, loc_start, loc_end, context=None) -> None:
        super().__init__('Runtime Error', details, loc_start, loc_end)
        self.context = context
        
    def as_string(self) -> str:
        res = self.generate_traceback()
        res += f'===> {self.error_name}: {self.details} <===\n'
        res += '\n\n' + string_with_arrows(self.loc_start.file_content, self.loc_start, self.loc_end)
        
        return res

    def generate_traceback(self):
        result = ''
        loc = self.loc_start
        context = self.context
        print(context, "---------------------")

        while context:
            result += f'  File {loc.file_name}, Line: {str(loc.line + 1)}, in {context.display_name}\n'
            loc = context.parent_entry_loc
            context = context.parent
            
        return 'Traceback (most recent call last):\n' + result
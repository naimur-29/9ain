#############################################
# LOCATION
#############################################
 
class Location:
    def __init__(self, index, line, column, file_name, file_content) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_content = file_content
        
    def advance(self, current_char=None):
        self.index += 1
        self.column += 1
        
        if current_char == '\n':
            self.line += 1
            self.column = 0
            
        return self
    
    def copy(self):
        return Location(self.index, self.line, self.column, self.file_name, self.file_content)
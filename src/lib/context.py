#############################################
# CONTEXTS
#############################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_loc=None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_loc = parent_entry_loc
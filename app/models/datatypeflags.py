from app.models.flags import Flag

class DatatypeFlag(Flag):
    
    DEFAULT_FLAGS = {
        # "canDoMathOperation": bool,
        # "canDoLogicalOperation": bool,
        # "isIterable": bool
    }
    
    
    def __init__(self, flags_map: dict | int):
        super().__init__(self.DEFAULT_FLAGS, flags_map)



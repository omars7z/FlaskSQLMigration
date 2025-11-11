from ..extensions import db

# mixin class
class BaseDBModel(db.Model):
    __abstract__ = True  # dont create a table 
    
    def get_flag(self) -> int:
        return getattr(self, "flag", 0) or 0
    
    def to_int_flags(self, flags: dict) -> int:
        val = 0
        for i, key in enumerate(self.flags.keys()):
            if flags.get(key, self.flags[key]):
                val |= (1 << i)
        return val

    def to_dict_flags(self) -> dict:
        val = getattr(self, "flag", 0) or 0
        res = {}
        for i, key in enumerate(self.flags.keys()): #return bool if flag is set or no
            checked =  bool(val & (1 << i))
            res[key] = checked
        return res 

    def set_flags(self, flags: dict):
        val = getattr(self, "flag", 0) or 0
        for i, key in enumerate(self.flags.keys()):
            if key in flags:
                if flags[key]:
                    val |= (1 << i)
                else:
                    val &= ~(1 << i)
        setattr(self, "flag", val)
        return val

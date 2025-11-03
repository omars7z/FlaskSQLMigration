from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# mixin class
class BaseModel2(db.Model):
    __abstract__ = True  # dont create a table for this class
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        # <algorithm>:<hash function>:<iterations>$<salt>$<derived_key>
        # pbkdf2:sha256:260000$uGbprVjZ6EbgmFlD$41e5d5fda0f6b28ef0a3cbe56e...
        
    def check_password(self, password):
        self.password = check_password_hash(self.password, password)
    

    def get_flag(self) -> int:
        return getattr(self, "flag", 0) or 0
    
    def to_int_flags(self, flags: dict) -> int:
        if not hasattr(self, "flags_map"):
            raise AttributeError(f"{self.__class__.__name__} doesn'tt have flags_map")
        val = 0
        for i, key in enumerate(self.flags_map.keys()):
            if flags.get(key, self.flags_map[key]):
                val |= (1 << i)
        return val

    def to_dict_flags(self) -> dict:
        if not hasattr(self, "flags_map"):
            raise AttributeError(f"{self.__class__.__name__} doesn'tt have flags_map")
        val = getattr(self, "flag", 0) or 0
        return {key: bool(val & (1 << i)) for i, key in enumerate(self.flags_map.keys())} #return bool if flag is set or no

    def set_flags(self, flags: dict):
        if not hasattr(self, "flags_map"):
            raise AttributeError(f"{self.__class__.__name__} doesn'tt have flags_map")
        val = getattr(self, "flag", 0) or 0
        for i, key in enumerate(self.flags_map.keys()):
            if key in flags:
                if flags[key]:
                    val |= (1 << i)
                else:
                    val &= ~(1 << i)
        setattr(self, "flag", val)
        return val

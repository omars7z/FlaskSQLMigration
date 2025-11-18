from ..extensions import db
from sqlalchemy import inspect
from sqlalchemy import String, func
 
# mixin class
class BaseDBModel(db.Model):
    __abstract__ = True  # dont create a table 

    def cast_value(self, column, value):
        try:
            python_type = column.type.python_type
            if python_type is bool:
                return str(value).lower() in ["1", "true", "yes"]
            return python_type(value)
        except Exception:
            return value

    @classmethod
    def apply_filters(cls, query, filters: dict):
        if not filters:
            return query

        mapper = inspect(cls)

        for key, val in filters.items():

            if key in getattr(cls, "flags", {}):
                bit_val = 1 << list(cls.flags.keys()).index(key)
                val_bool = str(val).lower() in ["1", "true", "yes"]
                query = query.filter((cls.flag.op("&")(bit_val)) == (bit_val if val_bool else 0))
                continue

            col = mapper.columns[key]

            if isinstance(col.type, String):
                query = query.filter(func.lower(col) == str(val).lower())
            else:
                casted_val = cls().cast_value(col, val)
                query = query.filter(col == casted_val)

        return query

    
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
        db.session.commit()
        return val

    def get_permissions(self):
        pass
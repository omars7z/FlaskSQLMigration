
from app.Models.datatype import Datatype
from app.extensions import db
from app.Repositries.base_repositry import BaseRepositry
from sqlalchemy import func

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        dt = Datatype.query.filter_by(id=id).first()
        if dt and dt.to_dict_flags().get("isDeleted"):
            return None
        return dt
        
        
    def get(self, filters: dict = None):
        filters = filters or {}
        flags_keys = list(Datatype.flags_map.keys())
        query = Datatype.query.filter(Datatype.flag.op('&')(16) == 0)  # skip deleted

        for key, val in filters.items():
            if hasattr(Datatype, key):
                col = getattr(Datatype, key)

                if key == "name":
                    query = query.filter(func.lower(col) == val.lower())
                else:
                    query = query.filter(col == val)

            elif key in Datatype.flags_map:
                bit_val = 1 << flags_keys.index(key)
                if val:
                    query = query.filter((Datatype.flag.op('&')(bit_val)) == bit_val)
                else:
                    query = query.filter((Datatype.flag.op('&')(bit_val)) == 0)

        return query.all()            


    def create(self, data: dict):
        # take flags from input or use defaults
        flag_fields = {k: data.pop(k, Datatype.flags_map[k]) for k in Datatype.flags_map.keys()}
        
        dt = Datatype(**data)  # destructure abd set name, example, ...
        dt.set_flags(flag_fields)
        db.session.add(dt)
        db.session.commit()
        return dt

    def update(self, id, data: dict):
        dt = self.get_by_id(id)
        if not dt:
            return None

        flag_fields = {k: data.pop(k) for k in list(data.keys()) if k in Datatype.flags_map}
        if flag_fields:
            dt.set_flags(flag_fields)

        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt


    def delete(self, obj):
        obj.set_flags({"isDeleted":True})
        print("DELETEDD this")
        # db.session.delete(obj)
        db.session.commit()
        return obj
        

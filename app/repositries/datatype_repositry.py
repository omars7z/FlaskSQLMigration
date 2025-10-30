
from app.models.datatype import Datatype
from app.extensions import db
from app.repositries.base_repositry import BaseRepositry
# from sqlalchemy import func

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        dt = Datatype.query.filter_by(id=id).first()
        if dt and dt.flags_dict.get("isDeleted"):
            return None
        return dt
        
        
    def get(self, filters: dict = None):
        # case_sens = query_params.pop("case_sens", "true").lower() == "true"
            # return query.filter(func.lower(Datatype.name)==name.lower()).all()

        query = Datatype.query.filter(Datatype.flag.op('&')(16) == 0) 
        flags_keys = list(Datatype.flags_map.keys())

        for key, val in filters.items():
            if hasattr(Datatype, key):
                col = getattr(Datatype, key)
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
        # db.session.delete(obj)
        obj.set_flags({"isDeleted":True})
        db.session.commit()
        return obj
        

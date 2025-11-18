
from sqlalchemy import func
from app.extensions import db
from app.Models.datatype import Datatype
from app.Repositries.base_repositry import BaseRepositry

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        return Datatype.query.get(id)
        
    def get(self, filters: dict = None):
        query = Datatype.query.filter(Datatype.flag.op('&')(16) == 0)  # skip deleted
        query = Datatype.apply_filters(query, filters)
        return query.all()            


    def create(self, data: dict):
        # take flags from input or use defaults
        flag_fields = {k: data.pop(k, Datatype.flags[k]) for k in Datatype.flags.keys()}
        
        dt = Datatype(**data)
        dt.set_flags(flag_fields)
        db.session.add(dt)
        db.session.commit()
        return dt

    def update(self, dt, data: dict):
        flag_fields = {k: data[k] for k in Datatype.flags if k in data}
        if flag_fields:
            dt.set_flags(flag_fields)

        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt


    def delete(self, obj):
        obj.set_flags({"isDeleted":True})
        # db.session.delete(obj)
        db.session.commit()
        return obj
        

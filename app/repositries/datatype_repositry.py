
from app.models.datatype import Datatype
from app.extensions import db
from app.repositries.base_repositry import BaseRepositry
from sqlalchemy import func
from datetime import datetime

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        return Datatype.query.filter_by(id=id, is_deleted=False).first()

    def get_by_name(self, name: str, case_sens: bool):
        query = Datatype.query.filter_by(is_deleted=False)
        if case_sens:
            return query.filter(Datatype.name==name).first()
        else:
            return query.filter(func.lower(Datatype.name)==name.lower()).first()
        

    def get_all(self):
        return Datatype.query.filter_by(is_deleted=False).all() 

    def create(self, data: dict):
        # extract flags from input or use defaults
        flags_data = {k: data.pop(k, Datatype.flags_map[k]) for k in Datatype.flags_map.keys()}
        
        dt = Datatype(**data)  # destructure abd set name, example, etc.
        dt.set_flags(flags_data)

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
        obj.is_deleted = True
        obj.deleted_at = datetime.now()
        # db.session.delete(obj)
        db.session.commit()
        

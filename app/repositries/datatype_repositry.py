
from app.models.datatype import Datatype
from app.models.flags import Flag
from app.extensions import db
from app.repositries.base_repositry import BaseRepositry
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        return Datatype.query.filter_by(id=id, is_deleted=False).first()

    def get_by_name(self, name: str, case_sens: bool):
        query = Datatype.query.filter_by(is_deleted=False)
        if case_sens:
            query = query.filter(Datatype.name==name)
        else:
            query = query.filter(func.lower(Datatype.name)==name.lower())
        return query.first()

    def get_all(self):
        return Datatype.query.filter_by(is_deleted=False).all() 

    def create(self, data: dict):
        flags_data = {k: data.pop(k) for k in Datatype.schema.keys() if k in data}
        data['flags'] = flags_data
        dt = Datatype(data)
        # dt.set_flags(flags_data)
        db.session.add(dt)
        db.session.commit()
        return dt

    def update(self, id, data):
        dt = self.get_by_id(id)
        if not dt:
            return None
        
        flag_fields = {k: data[k] for k in data if k in Datatype.schema}
        print(flag_fields)
        if flag_fields:
            flag_obj = Flag(flag_fields, schema=Datatype.schema)
            data["flag"] = flag_obj.get_flag()
            #take flag fields from data
            for k in flag_fields.keys():
                data.pop(k)
        
        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt

    def delete(self, obj):
        obj.is_deleted = True
        obj.deleted_at = datetime.now()
        # db.session.delete(obj)
        db.session.commit()
        


from app.models.datatype import Datatype
from app.extensions import db
from app.repositries.base_repositry import BaseRepositry
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

class DatatypeRepositry(BaseRepositry):
    
    def get_by_id(self, id):
        return Datatype.query.get(id)

    def get_by_name(self, name: str):
        return Datatype.query.filter(func.lower(Datatype.name) == name.lower()).first()

    
    def get_all(self):
        return Datatype.query.all()

    def create(self, data: dict):
        flags_data = {k: data.pop(k) for k in Datatype.schema.keys() if k in data}

        dt = Datatype(**data)
        dt.set_flags(flags_data)
        db.session.add(dt)
        db.session.commit()
        return dt

    def update(self, id, data):
        dt = self.get_by_id(id)
        if not dt:
            return None
        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt

    def delete(self, obj):
        db.session.delete(obj)

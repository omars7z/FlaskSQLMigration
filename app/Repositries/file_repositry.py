from app.Models.file import File
from sqlalchemy import desc
from app.extensions import db

class FileRepositry:
    
    def get_by_id(self, id):
        return File.query.get(id)
    
    def get_by_name(self, name):
        return File.query.filter_by(filename=name).first()
        
    def get(self, filters):
        query = File.query
        query = File.apply_filters(query, filters)
        return query.all()
    
    def create(self, data):
        file = File(**data)
        db.session.add(file)
        db.session.commit()
        return file
    
    def delete(self, id):
        db.session.delete(id)
        db.session.commit()
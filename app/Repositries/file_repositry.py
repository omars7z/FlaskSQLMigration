from app.Models.file import File
from sqlalchemy import desc
from app.extensions import db

class FileRepositry:
    
    def get_by_id(self, id):
        return File.query.filter_by(id=id).first()
    
    def get_by_name(self, name):
        return File.query.filter_by(filename=name).first()
        
    def get(self, filters):
        filters = filters or {} 
        query = File.query
        
        for key, val in filters.items():
            if hasattr(File, key):
                col = getattr(File, key)
                query.filter(col == val)
                
        # query = query.order_by(desc(File))
        return query.all()
    
    def create(self, data):
        file = File(**data)
        db.session.add(file)
        db.session.commit()
        return file
        
    def update(self, id, data):
        file = self.get_by_id(id)
        if not file:
            return None
        
        protected_file = ['filename', 'file_size'] #dont edit by
        for f in protected_file:
            if f in data:
                data.pop(f)
                
        for key, val in data.items():
            setattr(file, key, val)
        
        db.session.comit()
        return file
    
    def delete(self, id):
        db.session.delete(id)
        db.session.commit()
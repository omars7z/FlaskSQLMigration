from app.Models.permission import Permission
from app.extensions import db

class PermissionRepositry:
    
    def get_by_id(self, id):
        return Permission.query.filter_by(id=id).first() #first_or_404
    
    def get(self, filters:dict = None):       
        filters = filters or {}
        query = Permission.query

        for key, val in filters.items():
            if hasattr(Permission, key):
                col = getattr(Permission, key)
                query = query.filter(col == val)
                
        return query.all()
        
    def create_permission(self, **kwargs):
        permission = Permission(**kwargs)
        db.session.add(permission)
        db.session.commit()
        return permission
    
    def update_permission(self, id, data):
        perm = self.get_by_id(id)
        for key, value in data.items():
            setattr(perm, key, value)
        db.session.commit()
        return perm
    
    def delete_permission(self, id):
        permission = Permission.query.filter_by(id=id).first()
        db.session.delete(permission)
        db.session.commit()
        return permission
    
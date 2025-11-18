from app.Models.permission import Permission
from app.extensions import db

class PermissionRepositry:
    
    def get_by_id(self, id):
        return Permission.query.get(id)
    
    def get(self, filters:dict = None):    
        query = Permission.query
        query = Permission.apply_filters(query, filters)
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
        permission = Permission.query.get(id)
        db.session.delete(permission)
        db.session.commit()
        return permission
    
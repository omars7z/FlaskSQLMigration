from app.Models.permission import Permission
from app.Models.role import Role
from app.extensions import db

class PermissionRepositry:
    
    def get_by_id(self, id):
        return Permission.query.filter_by(id=id).first_or_404()
    
    
    def get(self, filters:dict = None):
        
        filters = filters or {}
        query = Permission.query

        for key, val in filters.items():
            if hasattr(Permission, key):
                col = getattr(key, val)
                query = query.filter(col == val)
                
        return query.all()
        
    
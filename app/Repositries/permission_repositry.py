from app.Models.permission import Permission
from app.Models.role import Role
from app.extensions import db

class PermissionRepositry:
    
    def get_by_id(self, id):
        return Permission.query.filter_by(id=id).first() #first_or_404
    
    def get(self, filters:dict = None):       
        filters = filters or {}
        query = Permission.query

        for key, val in filters.items():
            if hasattr(Permission, key):
                v = getattr(Permission, key)
                query = query.filter(v == val)
                
        return query.all()
        
    def create_permission(self, **kwargs):
        permission = Permission(**kwargs)
        db.session.add(permission)
        db.session.commit()
        return permission
    
    def update_permission(self, id, data):
        dt = self.get_by_id(id)
        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt
    
    def delete_permission(self, id):
        permission = Permission.query.filter_by(id=id).first()
        db.session.delete(permission)
        db.session.commit()
        return permission
    
    def assign_permission(self, role_id, perm_id):
        role = Role.query.filter_by(id=role_id).first()
        permission = self.get_by_id(perm_id)
        
        if role not in permission.roles:
            permission.roles.append(role)
            db.session.commit()
        return role
    
    def remove_permission(self, role_id, perm_id):
        role = Role.query.filter_by(id=role_id).first()
        permission = self.get_by_id(perm_id)
        
        if permission in role.permissions:
            role.permissions.remove(permission) 
            db.session.commit()
        
        return permission
    
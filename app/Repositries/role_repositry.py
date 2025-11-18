from app.Models.role import Role
from app.Models.permission import Permission
from sqlalchemy.orm import joinedload
from app.extensions import db

class RoleRepositry:
    
    def get_by_id(self, id:int):
        return Role.query.get(id)
    
    def get(self, filters:dict = None):
        query = Role.query
        query = Role.apply_filters(query, filters)
        query = query.options(joinedload(Role.permissions))
        return query.all()
    
    def create_role(self, **kwargs):
        role = Role(**kwargs)
        db.session.add(role)
        db.session.commit()
        return role
    
    def update_role(self, id, data):
        role = self.get_by_id(id)
        for key, value in data.items():
            setattr(role, key, value)
        db.session.commit()
        return role
    
    def delete_role(self, id):
        role = Role.query.get(id)
        db.session.delete(role)
        db.session.commit()
        return role
            
    def assign_permission(self, role_id, perm_id):
        permission = Permission.query.get(perm_id)
        role = self.get_by_id(role_id)
        
        permission.set_flags({"isActive":True})
        if permission not in role.permissions:
            role.permissions.append(permission) 
            
        db.session.commit()
        return role
    
    def remove_permission(self, role_id, perm_id):
        permission = Permission.query.get(perm_id)
        role = self.get_by_id(role_id)
        
        if permission in role.permissions:
            role.permissions.remove(permission) 
            db.session.commit()
        
        return role
    
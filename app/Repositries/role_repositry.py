from app.Models.role import Role
from app.Models.permission import Permission
from app.extensions import db
from app.Mappers.role_mapper import RoleMapper

class RoleRepositry():
    
    def get_by_id(self, id:int):
        return Role.query.filter_by(id=id).first()
    
    def get(self, filters:dict = None):
        filters = {} or filters
        query = Role.query
        
        for key, val in filters.items():
            if hasattr(Role, key):
                col = getattr(Role, key)
                query = query.filter(col == val)
            
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
        role = Role.query.filter_by(id=id).first()
        db.session.delete(role)
        db.session.commit()
        return role
            
    def assign_permission(self, role_id, perm_id):
        permission = Permission.query.filter_by(id=perm_id).first()
        role = self.get_by_id(role_id)
        
        permission.set_flags({"isActive":True})
        if permission not in role.permissions:
            role.permissions.append(permission) 
            
        db.session.commit()
        return RoleMapper.to_dict(role)
    
    def remove_permission(self, role_id, perm_id):
        permission = Permission.query.filter_by(id=perm_id).first()
        role = self.get_by_id(role_id)
        
        if permission in role.permissions:
            role.permissions.remove(permission) 
            db.session.commit()
        
        return role
    
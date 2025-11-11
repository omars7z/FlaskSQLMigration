from app.Models.role import Role
from app.Models.user import User
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
        dt = self.get_by_id(id)
        if not dt:
            return None

        for key, value in data.items():
            setattr(dt, key, value)
        db.session.commit()
        return dt
    
    def delete_role(self, id):
        role = Role.query.filter_by(id=id).first()
        if role is None:
            return None
        db.session.delete(role)
        db.session.commit()
        return role
            
    def assign_permission(self, role_id, perm_id):
        role = Role.query.filter_by(id=role_id).first()
        permission = self.get_by_id(perm_id)
        
        if role not in permission.roles:
            permission.roles.append(role)
            db.session.commit()
        return RoleMapper.to_dict()
    
    def remove_permission(self, role_id, perm_id):
        role = Role.query.filter_by(id=role_id).first()
        permission = self.get_by_id(perm_id)
        
        if permission in role.permissions:
            role.permissions.remove(permission) 
            db.session.commit()
        
        return role
    
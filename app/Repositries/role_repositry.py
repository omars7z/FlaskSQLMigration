from app.Models.role import Role
from app.Models.user import User
from app.extensions import db

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
    
    def assign_role(self, user_id, role_id):
        user = User.query.filter_by(id=user_id).first()
        role = self.get_by_id(role_id)
        
        if not user or not role:
            raise ValueError() 
        if user not in role.users:
            role.users.append(user)
            db.session.commit()
            
        return user
    
    def remove_role(self, user_id, role_id):
        user = User.query.filter_by(id=user_id).first()
        role = self.get_by_id(role_id)
        if not user or not role:
            return None
        if user in role.users:
            role.users.remove(user) 
            db.session.commit()
        else:
            None
        return user
        
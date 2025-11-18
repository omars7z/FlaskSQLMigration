from app.extensions import db
import secrets
from sqlalchemy.orm import selectinload
from app.Models.user import User
from app.Models.role import Role

class UserRepositry:
    
    def get_by_id(self, id: int):
        return User.query.get(id)
    
    def get_by_email(self, email):
        return User.query.filter(User.email == email).first()
     
    def get(self, filters: dict = None):
        query = User.query.options(
            selectinload(User.roles).selectinload(Role.permissions),
            selectinload(User.files)
            )
        query = User.apply_filters(query, filters)
        return query.all()      
    
    def create_user(self, name, email):
        token = secrets.token_urlsafe(32)
        user = User(
            name=name,
            email=email,
            token=token,
        )
        db.session.add(user)
        db.session.commit()
        return user
        
    def delete_user(self, id):
        user = self.get_by_id(id)
        db.session.delete(user)
        db.session.commit()
        return user
    
    def set_password(self, token, password):
        user = User.query.filter_by(token=token).first()
        if not user:    #wrong http
            return None
        user.set_password(password) 
        user.set_flags({"isActive":True})
        user.token = None
        db.session.commit()
        return user 
    
    def assign_role(self, user_id, role_id):
        role = Role.query.get(role_id)
        user = self.get_by_id(user_id)  

        role.set_flags({"isActive": True})
        if role not in user.roles:
            user.roles.append(role)

        db.session.commit()
        return user

    
    def remove_role(self, user_id, role_id):
        role = Role.query.get(role_id)
        user = self.get_by_id(user_id)
        if role in user.roles:
            user.roles.remove(role) 
        db.session.commit()
        return user
        
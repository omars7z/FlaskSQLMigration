from app.extensions import db
import secrets
from sqlalchemy import func
from app.Models.user import User
from app.Models.role import Role
from app.Mappers.user_mapper import UserMapper

class UserRepositry:
    
    def get_by_id(self, id: int):
        return User.query.filter_by(id=id).first()
    
    def get_by_email(self, email):
        return User.query.filter(User.email == email).first()
     
    def get(self, filters: dict = None):
        filters = filters or {}
        flags_keys = list(User.flags.keys())
        query = User.query.filter()  # skip deleted

        for key, val in filters.items():
            if hasattr(User, key):
                col = getattr(User, key)

                if key == "name":
                    query = query.filter(func.lower(col) == val.lower())
                else:
                    query = query.filter(col == val)

            elif key in User.flags:
                bit_val = 1 << flags_keys.index(key)
                if val:
                    query = query.filter((User.flag.op('&')(bit_val)) == bit_val)
                else:
                    query = query.filter((User.flag.op('&')(bit_val)) == 0)

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
        role = Role.query.filter_by(id=role_id).first()
        user = self.get_by_id(user_id)  

        role.set_flags({"isActive": True})
        if role not in user.roles:
            user.roles.append(role)

        db.session.commit()
        return user

    
    def remove_role(self, user_id, role_id):
        role = Role.query.filter_by(id=role_id).first()
        user = self.get_by_id(user_id)
        if role in user.roles:
            user.roles.remove(role) 
        db.session.commit()
        return user
        
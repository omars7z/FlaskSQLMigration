from app.Models.user import User
from app.extensions import db
import secrets
from sqlalchemy import func

class UserRepositry:
    
    def get_by_id(self, id: int):
        print(User.query.all())
        return User.query.filter_by(id=id).first()
    
    def get_by_email(self, email):
        return User.query.filter(func.lower(User.email) == email.lower()).first()
    
    
    def get(self, filters: dict = None):
        filters = filters or {}
        flags_keys = list(User.flags_map.keys())
        query = User.query.filter()  # skip deleted

        for key, val in filters.items():
            if hasattr(User, key):
                col = getattr(User, key)

                if key == "name":
                    query = query.filter(func.lower(col) == val.lower())
                else:
                    query = query.filter(col == val)

            elif key in User.flags_map:
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
        user = User.query.filter_by(id=id).first()
        user.set_flags({"isDeleted": True})
        # db.session.delete(id)
        db.session.commit()
        return user
    
    def set_password(self, token, password):
        user = User.query.filter_by(token=token).first()
        if not user:
            return None
        user.set_password(password) #model to base_model
        user.set_flags({"isActive":True})
        user.token = None
        db.session.commit()
        return user 
    
    def assign_role(self, id, role):
        user = self.service.get_by_id(id)
        role = User.query.filter_by(name=role).first()
        if not role:
            raise ValueError("role doesn't exist")
        user.roles.append(role)
        db.session.commit()
        return user
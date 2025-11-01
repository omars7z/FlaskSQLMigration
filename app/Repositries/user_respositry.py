from app.Models.user import User
from app.extensions import db
import secrets

class UserRepositry:
    
    def get_by_id(self, id:int):
        return User.query.filter(id=id).first()
    
    def get_by_email(self, email:str):
        return User.query.filter(email=email).first()
    
    def create_user(self, name, email, super_admin=False):
        token = secrets.token_urlsafe(32)
        user = User(
            name=name,
            email=email,
            token=token,
            flag=2 if super_admin else 0
        )
        db.session.add(user)
        db.session.commit()
        
    def set_password(self, token, password):
        user = User.query.filter(token=token).first()
        if not user:
            return None
        user.set_password(password)
        user.flags_map({"isActive":True})
        user.token = True
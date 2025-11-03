from app.Helpers.registry import register
from app.Util.jwt_token import create_access_token

@register("User")
class UserServices:
    
    def __init__(self, repositry):
        self.repo = repositry
        
    def get_by_id(self, id:int):
        return self.repo.get_by_id(id)
    
    def get(self, filters):
        return self.repo.get(filters)
        
    def create_user(self, name, email, current_user):
        if current_user and not current_user.to_dict_flags().get("isSuperAdmin"):
            raise PermissionError("can't create user unless Super Admin")
        return self.repo.create_user(name, email)
    
    def set_password(self, token, password):
        return self.repo.set_password(token, password)
    
    def login(self, email, password):
        user = self.repo.get_by_email(email)
        password = user.check_password(password)
        if not user or not password:
            return None
        if not user.to_dict_flags().get("isActive"):
            return None
        return create_access_token(user.id)
    
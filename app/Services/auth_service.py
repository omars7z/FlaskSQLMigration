
from app.Util.jwt_token import create_access_token
from app.Helpers.registry import register

@register("Auth", repo="User")
class AuthService:
    
    def __init__(self, repository):
        self.repo = repository
        
    def login(self, email, password):
        user = self.repo.get_by_email(email)
        if not user:
            return None
        validated_password = user.check_password(password)
        if not validated_password:
            return None 
        if not user.to_dict_flags().get("isActive"):
            return None
        return create_access_token(user.id)

from app.Helpers.registry import register

@register("Auth", repo="User")
class AuthService:
    
    def __init__(self, repository):
        self.repo = repository.get("User")
        
    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        if not user.check_password(password):
            raise ValueError("Incorrect password")
        if not user.to_dict_flags().get("isActive"):
            raise ValueError("User account is inactive")
        return user
    
    def set_password(self, token, password):
        user = self.repo.set_password(token, password)
        if not user:
            raise ValueError("Wrong credinitials")
        return user

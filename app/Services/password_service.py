
from app.Helpers.registry import register

@register("Password", repo="User")
class PasswordService:
    def __init__(self, repositry):
        self.repo = repositry

    def set_password(self, token, password):
        return self.repo.set_password(token, password)

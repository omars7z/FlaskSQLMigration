
from app.Helpers.registry import register

@register("Password")
class PasswordService:
    def __init__(self, user_repo):
        self.repo = user_repo

    def set_password(self, token, password):
        return self.repo.set_password(token, password)

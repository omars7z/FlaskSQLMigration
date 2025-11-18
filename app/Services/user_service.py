from app.Helpers.registry import register

@register("User", repo=("User", "Role"))
class UserService:

    def __init__(self, repository):
        self.user_repo = repository.get("User")
        self.role_repo = repository.get("Role")

    def get_by_id(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return user

    def get(self, filters=None):
        user = self.user_repo.get(filters)
        if not user:
            return None
        return user

    def create_user(self, name: str, email: str):
        if not name or not email:
            raise ValueError("Name and email are required")
        return self.user_repo.create_user(name, email)

    def delete_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id={user_id} not found")
        return self.user_repo.delete_user(user_id)

    def assign_role(self, user_id: int, role_id: int):
        user = self.user_repo.get_by_id(user_id)
        role = self.role_repo.get_by_id(role_id)
        if not user or not role:
            raise ValueError("User or role not found")
        return self.user_repo.assign_role(user_id, role_id)

    def remove_role(self, user_id: int, role_id: int):
        user = self.user_repo.get_by_id(user_id)
        role = self.role_repo.get_by_id(role_id)
        if not user or not role:
            raise ValueError("User or role not found")
        if len(user.roles) <= 1:
            raise ValueError("Cannot remove role: User must have at least one role")
        return self.user_repo.remove_role(user_id, role_id)
